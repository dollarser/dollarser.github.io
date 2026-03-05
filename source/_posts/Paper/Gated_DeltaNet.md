---
title: Gated DeltaNet详解
date: 2026-03-05 13:51:00
toc: true
tags:
 - LLM
categories:
 - paper
typora-root-url: ..\..
typora-copy-images-to: ..\..\img\paper 
---



- 作者博客：https://sustcsonglin.github.io/blog/
- 官方仓库：https://github.com/NVlabs/GatedDeltaNet
- **Flash Linear Attention (FLA)** 库：https://github.com/fla-org/flash-linear-attention
- 参考pdf：https://sustcsonglin.github.io/assets/pdf/talk_linear_transformer.pdf
- 应用场景：Qwen3.5，Kimi Linear



## 核心思想

Gated DeltaNet 是 **DeltaNet** 的升级版，核心洞察是：**门控机制（Gating）** 与 **Delta 规则（Delta Rule）** 在记忆管理中是互补的：

- **门控机制**：实现快速的全局记忆衰减（遗忘）
- **Delta 规则**：实现精确的局部记忆更新（纠错）

两者的结合解决了纯 DeltaNet "缺乏快速清除过时信息能力" 的问题。

------

## 数学原理

### 1. 基础：Linear Attention 的 RNN 形式

标准 Linear Attention 可表示为矩阵值状态的 RNN：
$$
\mathbf{S}_t = \mathbf{S}_{t-1} + \mathbf{v}_t\mathbf{k}_t^\top,  \mathbf{o} = \mathbf{S}_t\mathbf{q}_t
$$
其中 $\mathbf{S}_t \in \mathbf{R}^{d\times d}$ 是状态矩阵，累积 Key-Value 外积。

### 2. DeltaNet：引入纠错机制

DeltaNet 的核心是 **Delta Rule（纠错学习规则）**：
$$
\mathbf{S}_t = \mathbf{S}_{t-1} - \beta_t(\mathbf{S}_{t-1}\mathbf{k}_t - \mathbf{v}_t) \mathbf{k}_t^\top
$$
等价于：
$$
\mathbf{S}_t = \mathbf{I}_{t-1} (\mathbf{I} - \beta_t \mathbf{k}_t \mathbf{k}_t^\top) + \beta_t \mathbf{v}_t \mathbf{k}_t^\top
$$
**直观理解**：

1. $\mathbf{S}_{t-1}\mathbf{k}_t$ ：从记忆中检索与当前 key 关联的"旧 value"
2. $\mathbf{S}_{t-1}\mathbf{k}_t - \mathbf{v}_t$ ：计算预测误差（Delta）
3. 按误差方向更新状态，实现"先删除旧关联，再写入新关联" 

### 3. Gated DeltaNet：引入遗忘门

在 DeltaNet 基础上增加门控系数 $\alpha_t \in (0,1)$ ：
$$
\mathbf{S}_t = \mathbf{S}_{t-1} (\underbrace{ \alpha_t (\mathbf{I} - \beta_t \mathbf{k}_t \mathbf{k}_t^\top) }_{ \text{门控+Delta} }) + \beta_t \mathbf{v}_t \mathbf{k}_t^\top\
$$
**关键特性**：

- **当 $\alpha_t→ 0$ **：立即清空记忆（快速遗忘）
- **当 $\alpha_t→ 1$  ** ：退化为纯 Delta Rule（精确更新）
- **当 $\alpha_t \in (0,1)$ **：根据输入动态调整 ，自适应平衡全局遗忘与局部更新

------



## 架构设计

### Token Mixer 结构

```plain
输入 x
  ↓
┌──────────────────────────────────────────┐
│  Linear Projection + Short Conv + SiLU   │
│  生成 q, k, v（带 L2 Normalization）       │
└──────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│  Linear Projection 生成 α, β             │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│  Gated Delta Rule 计算:                  │
│  S_t = S_{t-1}(α(I - βkk^T)) + βvk^T    │
│  o_t = S_t q_t                          │
└─────────────────────────────────────────┘
  ↓
Layer Norm + Gating + Output Projection
```

**关键组件**：

- **Short Convolution**：深度可分离卷积（kernel=4），提供局部归纳偏置，增强 in-context learning 能力 
- **qk L2 Normalization**：确保训练稳定性，使特征值有界 
- **SwiGLU MLP**：与 Llama 架构保持一致 

------

## 与相关架构的对比

| 架构               | 状态更新公式                                                 | 核心特点             | 局限性                   |
| ------------------ | ------------------------------------------------------------ | -------------------- | ------------------------ |
| **Mamba2**         | $\mathbf{S}_t = \mathbf{S}_{t-1} \odot \mathbf{G}_t + \mathbf{v}_t \mathbf{k}_t^\top$ | 元素级门控，硬件高效 | 无法精确更新特定 key     |
| **DeltaNet**       | $\mathbf{S}_t = \mathbf{S}_{t-1}(\mathbf{I} - \beta_t \mathbf{k}_t \mathbf{k}_t^\top) + \beta_t \mathbf{v}_t \mathbf{k}_t^\top$ | 按 key 方向精确擦写  | 缺乏快速全局遗忘         |
| **Gated DeltaNet** | $\mathbf{S}_t = \mathbf{S}_{t-1}\alpha_t(\mathbf{I} - \beta_t \mathbf{k}_t \mathbf{k}_t^\top) + \beta_t \mathbf{v}_t \mathbf{k}_t^\top$ | **两者结合**         | 固定状态维度限制检索上限 |



## 代码实现

```python
"""
Gated DeltaNet 和 DeltaNet 的 PyTorch 实现
基于论文: "Gated Delta Networks: Improving Mamba2 with Delta Rule" (ICLR 2025)
作者: Songlin Yang, Jan Kautz, Ali Hatamizadeh (NVIDIA)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple
import math


class DeltaNetLayer(nn.Module):
    """
    基础 DeltaNet 层
    核心: 使用 Delta Rule (纠错学习规则) 更新线性注意力状态
    
    状态更新公式:
    S_t = S_{t-1} * (I - beta_t * k_t * k_t^T) + beta_t * v_t * k_t^T
    """
    def __init__(
        self,
        d_model: int,
        n_heads: int = 8,
        qk_dim: Optional[int] = None,
        v_dim: Optional[int] = None,
        use_short_conv: bool = True,
        conv_size: int = 4,
        eps: float = 1e-6
    ):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.eps = eps
        
        # 维度设置
        self.qk_dim = qk_dim or d_model // n_heads
        self.v_dim = v_dim or d_model // n_heads
        self.head_dim = self.v_dim  # 每个头的维度
        
        # 投影层: 生成 q, k, v
        self.q_proj = nn.Linear(d_model, n_heads * self.qk_dim, bias=False)
        self.k_proj = nn.Linear(d_model, n_heads * self.qk_dim, bias=False)
        self.v_proj = nn.Linear(d_model, n_heads * self.v_dim, bias=False)
        
        # Beta 投影: 生成 Delta Rule 的学习率 beta (0 < beta <= 1)
        self.beta_proj = nn.Linear(d_model, n_heads, bias=True)
        
        # 可选的短卷积 (Short Convolution) 提供局部归纳偏置
        self.use_short_conv = use_short_conv
        if use_short_conv:
            # 深度可分离卷积: 每个通道独立卷积
            self.conv = nn.Conv1d(
                n_heads * self.qk_dim,  # 输入通道
                n_heads * self.qk_dim,  # 输出通道
                kernel_size=conv_size,
                padding=conv_size - 1,  # 因果填充
                groups=n_heads * self.qk_dim,  # 深度可分离
                bias=True
            )
            self.conv_act = nn.SiLU()
        
        # 输出投影
        self.o_proj = nn.Linear(n_heads * self.v_dim, d_model, bias=False)
        
        # Layer Norm
        self.norm = nn.LayerNorm(d_model)
        
        self.reset_parameters()
    
    def reset_parameters(self):
        nn.init.xavier_uniform_(self.q_proj.weight)
        nn.init.xavier_uniform_(self.k_proj.weight)
        nn.init.xavier_uniform_(self.v_proj.weight)
        nn.init.xavier_uniform_(self.o_proj.weight)
        # Beta 初始化为较小值，确保稳定
        nn.init.zeros_(self.beta_proj.bias)
        nn.init.normal_(self.beta_proj.weight, std=0.02)
    
    def forward(
        self,
        x: torch.Tensor,
        state: Optional[torch.Tensor] = None,
        use_chunkwise: bool = True,
        chunk_size: int = 64
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            x: 输入张量 [batch, seq_len, d_model]
            state: 初始状态 [batch, n_heads, head_dim, qk_dim] 或 None
            use_chunkwise: 是否使用分块并行算法加速训练
            chunk_size: 分块大小
        
        Returns:
            output: 输出张量 [batch, seq_len, d_model]
            new_state: 最终状态 [batch, n_heads, head_dim, qk_dim]
        """
        batch_size, seq_len, _ = x.shape
        
        # 投影生成 q, k, v
        q = self.q_proj(x)  # [B, L, n_heads * qk_dim]
        k = self.k_proj(x)
        v = self.v_proj(x)  # [B, L, n_heads * v_dim]
        
        # 应用短卷积 (因果卷积)
        if self.use_short_conv:
            # 转置为 [B, C, L] 适应 Conv1d
            k_conv = k.transpose(1, 2)  # [B, n_heads*qk_dim, L]
            k_conv = self.conv(k_conv)[..., :seq_len]  # 因果: 截断多余填充
            k_conv = k_conv.transpose(1, 2)  # [B, L, n_heads*qk_dim]
            k = k * self.conv_act(k_conv)  # 门控融合
        
        # 重塑为多头形式
        q = q.view(batch_size, seq_len, self.n_heads, self.qk_dim).transpose(1, 2)  # [B, H, L, qk_dim]
        k = k.view(batch_size, seq_len, self.n_heads, self.qk_dim).transpose(1, 2)
        v = v.view(batch_size, seq_len, self.n_heads, self.v_dim).transpose(1, 2)   # [B, H, L, v_dim]
        
        # L2 归一化 (关键稳定性技巧)
        q = F.normalize(q, p=2, dim=-1, eps=self.eps)
        k = F.normalize(k, p=2, dim=-1, eps=self.eps)
        
        # 生成 beta (Delta Rule 学习率), 范围 (0, 1]
        beta = torch.sigmoid(self.beta_proj(x))  # [B, L, n_heads]
        beta = beta.transpose(1, 2).unsqueeze(-1)  # [B, H, L, 1]
        beta = beta.clamp(min=0.01, max=1.0)  # 防止过小或过大
        
        if use_chunkwise and self.training:
            # 训练时使用分块并行算法 (Chunkwise Parallel)
            output, new_state = self.chunkwise_parallel(q, k, v, beta, chunk_size)
        else:
            # 推理时使用递归形式 (Recurrent)
            output, new_state = self.recurrent_forward(q, k, v, beta, state)
        
        # 合并多头并输出投影
        output = output.transpose(1, 2).contiguous().view(batch_size, seq_len, -1)
        output = self.o_proj(output)
        
        # 残差连接 + Layer Norm
        output = self.norm(output + x)
        
        return output, new_state
    
    def recurrent_forward(
        self,
        q: torch.Tensor,
        k: torch.Tensor,
        v: torch.Tensor,
        beta: torch.Tensor,
        state: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        递归前向传播 (适合推理)
        状态: S_t [B, H, v_dim, qk_dim]
        """
        batch_size, n_heads, seq_len, qk_dim = k.shape
        v_dim = v.shape[-1]
        
        # 初始化状态
        if state is None:
            state = torch.zeros(
                batch_size, n_heads, v_dim, qk_dim,
                device=k.device, dtype=k.dtype
            )
        
        outputs = []
        
        for t in range(seq_len):
            q_t = q[:, :, t, :]      # [B, H, qk_dim]
            k_t = k[:, :, t, :]      # [B, H, qk_dim]
            v_t = v[:, :, t, :]      # [B, H, v_dim]
            beta_t = beta[:, :, t, :]  # [B, H, 1]
            
            # Delta Rule 状态更新:
            # S_t = S_{t-1} * (I - beta_t * k_t * k_t^T) + beta_t * v_t * k_t^T
            
            # 步骤 1: 计算 S_{t-1} * k_t (从记忆中检索)
            S_k = torch.matmul(state, k_t.unsqueeze(-1)).squeeze(-1)  # [B, H, v_dim]
            
            # 步骤 2: 计算误差 (Delta) = S_{t-1}*k_t - v_t
            delta = S_k - v_t  # [B, H, v_dim]
            
            # 步骤 3: 状态更新
            # 外积: delta ⊗ k_t = [B, H, v_dim, 1] @ [B, H, 1, qk_dim] = [B, H, v_dim, qk_dim]
            state = state - beta_t.unsqueeze(-1) * torch.matmul(
                delta.unsqueeze(-1), k_t.unsqueeze(-2)
            )
            
            # 步骤 4: 输出 o_t = S_t * q_t
            o_t = torch.matmul(state, q_t.unsqueeze(-1)).squeeze(-1)  # [B, H, v_dim]
            outputs.append(o_t)
        
        output = torch.stack(outputs, dim=2)  # [B, H, L, v_dim]
        return output, state
    
    def chunkwise_parallel(
        self,
        q: torch.Tensor,
        k: torch.Tensor,
        v: torch.Tensor,
        beta: torch.Tensor,
        chunk_size: int = 64
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        分块并行算法 (适合训练)
        参考: Flash Linear Attention 库的实现
        """
        batch_size, n_heads, seq_len, qk_dim = k.shape
        v_dim = v.shape[-1]
        
        # 填充到 chunk_size 的倍数
        pad_len = (chunk_size - seq_len % chunk_size) % chunk_size
        if pad_len > 0:
            q = F.pad(q, (0, 0, 0, pad_len))
            k = F.pad(k, (0, 0, 0, pad_len))
            v = F.pad(v, (0, 0, 0, pad_len))
            beta = F.pad(beta, (0, 0, 0, pad_len))
        
        num_chunks = (seq_len + pad_len) // chunk_size
        new_seq_len = seq_len + pad_len
        
        # 重塑为块
        q_chunks = q.view(batch_size, n_heads, num_chunks, chunk_size, qk_dim)
        k_chunks = k.view(batch_size, n_heads, num_chunks, chunk_size, qk_dim)
        v_chunks = v.view(batch_size, n_heads, num_chunks, chunk_size, v_dim)
        beta_chunks = beta.view(batch_size, n_heads, num_chunks, chunk_size, 1)
        
        outputs = []
        state = torch.zeros(batch_size, n_heads, v_dim, qk_dim, device=q.device, dtype=q.dtype)
        
        for i in range(num_chunks):
            q_i = q_chunks[:, :, i]      # [B, H, chunk, qk_dim]
            k_i = k_chunks[:, :, i]      # [B, H, chunk, qk_dim]
            v_i = v_chunks[:, :, i]      # [B, H, chunk, v_dim]
            beta_i = beta_chunks[:, :, i]  # [B, H, chunk, 1]
            
            # 块内并行计算
            # 1. 计算局部注意力
            # k_i: [B, H, chunk, qk_dim] -> [B, H, qk_dim, chunk]
            k_i_T = k_i.transpose(-2, -1)
            
            # 2. 计算块内 Delta 更新 (简化版，实际需更复杂的并行算法)
            for j in range(chunk_size):
                q_ij = q_i[:, :, j, :]
                k_ij = k_i[:, :, j, :]
                v_ij = v_i[:, :, j, :]
                beta_ij = beta_i[:, :, j, :]
                
                # 递归更新状态
                S_k = torch.matmul(state, k_ij.unsqueeze(-1)).squeeze(-1)
                delta = S_k - v_ij
                state = state - beta_ij.unsqueeze(-1) * torch.matmul(
                    delta.unsqueeze(-1), k_ij.unsqueeze(-2)
                )
                
                o_ij = torch.matmul(state, q_ij.unsqueeze(-1)).squeeze(-1)
                outputs.append(o_ij)
        
        output = torch.stack(outputs, dim=2)[:, :, :seq_len, :]  # 截断填充
        return output, state


class GatedDeltaNetLayer(nn.Module):
    """
    Gated DeltaNet 层
    在 DeltaNet 基础上增加门控遗忘机制 alpha_t ∈ (0,1)
    
    状态更新公式:
    S_t = S_{t-1} * alpha_t * (I - beta_t * k_t * k_t^T) + beta_t * v_t * k_t^T
    
    其中:
    - alpha_t: 门控遗忘系数 (接近0时快速清空记忆, 接近1时保留记忆)
    - beta_t: Delta Rule 学习率
    """
    def __init__(
        self,
        d_model: int,
        n_heads: int = 8,
        qk_dim: Optional[int] = None,
        v_dim: Optional[int] = None,
        use_short_conv: bool = True,
        conv_size: int = 4,
        gate_activation: str = "sigmoid",
        eps: float = 1e-6
    ):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.eps = eps
        
        self.qk_dim = qk_dim or d_model // n_heads
        self.v_dim = v_dim or d_model // n_heads
        self.head_dim = self.v_dim
        
        # 投影层
        self.q_proj = nn.Linear(d_model, n_heads * self.qk_dim, bias=False)
        self.k_proj = nn.Linear(d_model, n_heads * self.qk_dim, bias=False)
        self.v_proj = nn.Linear(d_model, n_heads * self.v_dim, bias=False)
        
        # 门控投影: 生成 alpha (遗忘门)
        self.gate_proj = nn.Linear(d_model, n_heads, bias=True)
        
        # Beta 投影: 生成 beta (Delta Rule 学习率)
        self.beta_proj = nn.Linear(d_model, n_heads, bias=True)
        
        # 短卷积
        self.use_short_conv = use_short_conv
        if use_short_conv:
            self.conv = nn.Conv1d(
                n_heads * self.qk_dim,
                n_heads * self.qk_dim,
                kernel_size=conv_size,
                padding=conv_size - 1,
                groups=n_heads * self.qk_dim,
                bias=True
            )
            self.conv_act = nn.SiLU()
        
        # 输出投影
        self.o_proj = nn.Linear(n_heads * self.v_dim, d_model, bias=False)
        self.norm = nn.LayerNorm(d_model)
        
        self.reset_parameters()
    
    def reset_parameters(self):
        nn.init.xavier_uniform_(self.q_proj.weight)
        nn.init.xavier_uniform_(self.k_proj.weight)
        nn.init.xavier_uniform_(self.v_proj.weight)
        nn.init.xavier_uniform_(self.o_proj.weight)
        
        # Gate 初始化: 偏置设为较小值，初始遗忘率适中
        nn.init.zeros_(self.gate_proj.bias)
        nn.init.normal_(self.gate_proj.weight, std=0.02)
        
        nn.init.zeros_(self.beta_proj.bias)
        nn.init.normal_(self.beta_proj.weight, std=0.02)
    
    def forward(
        self,
        x: torch.Tensor,
        state: Optional[torch.Tensor] = None,
        use_chunkwise: bool = True,
        chunk_size: int = 64
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        batch_size, seq_len, _ = x.shape
        
        # 投影
        q = self.q_proj(x)
        k = self.k_proj(x)
        v = self.v_proj(x)
        
        # 短卷积
        if self.use_short_conv:
            k_conv = k.transpose(1, 2)
            k_conv = self.conv(k_conv)[..., :seq_len]
            k_conv = k_conv.transpose(1, 2)
            k = k * self.conv_act(k_conv)
        
        # 重塑多头
        q = q.view(batch_size, seq_len, self.n_heads, self.qk_dim).transpose(1, 2)
        k = k.view(batch_size, seq_len, self.n_heads, self.qk_dim).transpose(1, 2)
        v = v.view(batch_size, seq_len, self.n_heads, self.v_dim).transpose(1, 2)
        
        # L2 归一化
        q = F.normalize(q, p=2, dim=-1, eps=self.eps)
        k = F.normalize(k, p=2, dim=-1, eps=self.eps)
        
        # 生成门控 alpha (遗忘系数) 和 beta (学习率)
        # alpha ∈ (0, 1): 控制全局记忆保留程度
        alpha = torch.sigmoid(self.gate_proj(x))  # [B, L, n_heads]
        alpha = alpha.transpose(1, 2).unsqueeze(-1)  # [B, H, L, 1]
        
        # beta ∈ (0, 1]: 控制 Delta Rule 更新强度
        beta = torch.sigmoid(self.beta_proj(x))
        beta = beta.transpose(1, 2).unsqueeze(-1)
        beta = beta.clamp(min=0.01, max=1.0)
        
        if use_chunkwise and self.training:
            output, new_state = self.chunkwise_parallel(q, k, v, alpha, beta, chunk_size)
        else:
            output, new_state = self.recurrent_forward(q, k, v, alpha, beta, state)
        
        # 输出投影
        output = output.transpose(1, 2).contiguous().view(batch_size, seq_len, -1)
        output = self.o_proj(output)
        output = self.norm(output + x)
        
        return output, new_state
    
    def recurrent_forward(
        self,
        q: torch.Tensor,
        k: torch.Tensor,
        v: torch.Tensor,
        alpha: torch.Tensor,
        beta: torch.Tensor,
        state: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Gated DeltaNet 递归前向
        
        关键区别: 状态更新包含 alpha_t 门控遗忘
        S_t = S_{t-1} * alpha_t * (I - beta_t * k_t * k_t^T) + beta_t * v_t * k_t^T
        
        当 alpha_t -> 0: 快速清空记忆 (遗忘)
        当 alpha_t -> 1: 保留记忆并按 Delta Rule 更新
        """
        batch_size, n_heads, seq_len, qk_dim = k.shape
        v_dim = v.shape[-1]
        
        if state is None:
            state = torch.zeros(batch_size, n_heads, v_dim, qk_dim, device=k.device, dtype=k.dtype)
        
        outputs = []
        
        for t in range(seq_len):
            q_t = q[:, :, t, :]
            k_t = k[:, :, t, :]
            v_t = v[:, :, t, :]
            alpha_t = alpha[:, :, t, :]  # 门控遗忘系数
            beta_t = beta[:, :, t, :]    # Delta Rule 学习率
            
            # 步骤 1: 门控遗忘 + Delta Rule
            # 先应用门控: S' = alpha_t * S_{t-1}
            gated_state = alpha_t.unsqueeze(-1) * state  # [B, H, v_dim, qk_dim]
            
            # 步骤 2: Delta Rule 更新
            S_k = torch.matmul(gated_state, k_t.unsqueeze(-1)).squeeze(-1)  # [B, H, v_dim]
            delta = S_k - v_t
            
            # 状态更新: S_t = gated_state - beta_t * delta ⊗ k_t
            state = gated_state - beta_t.unsqueeze(-1) * torch.matmul(
                delta.unsqueeze(-1), k_t.unsqueeze(-2)
            )
            
            # 步骤 3: 输出
            o_t = torch.matmul(state, q_t.unsqueeze(-1)).squeeze(-1)
            outputs.append(o_t)
        
        output = torch.stack(outputs, dim=2)
        return output, state
    
    def chunkwise_parallel(
        self,
        q: torch.Tensor,
        k: torch.Tensor,
        v: torch.Tensor,
        alpha: torch.Tensor,
        beta: torch.Tensor,
        chunk_size: int = 64
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Gated DeltaNet 分块并行 (简化实现)
        实际生产环境应使用 CUDA 优化的 Flash Linear Attention 库
        """
        # 简化版: 使用递归形式但分块处理
        # 完整实现需要复杂的块间状态传递逻辑
        return self.recurrent_forward(q, k, v, alpha, beta, None)


```

