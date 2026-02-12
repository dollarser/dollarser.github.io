---
title: Multi-Head Latent Attention (MLA)详解
date: 2025-8-5 12:00:00
toc: true
tags:
 - AI
 - Multi-Head Latent Attention
 - paper
typora-root-url: ../..
typora-copy-images-to: ../../img/llm
mathjax: true
---

# Multi-Head Latent Attention (MLA)详解

- 论文 [DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model](https://arxiv.org/abs/2405.04434)

- github: [DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model](https://github.com/deepseek-ai/DeepSeek-V2)

参考博客：

- https://www.bilibili.com/video/BV1wjQvY6Enm
- https://bruceyuan.com/post/hands-on-deepseek-mla-projection-absorption.html

- https://kexue.fm/archives/10091
- https://github.com/madsys-dev/deepseekv2-profile/blob/main/workspace/blog/optimizing-mla.md

```text
洞见：
1.位置编码目前是添加到Q和K中，不再是直接添加到embedding中
2.RoPE虽然叫位置编码，但是自变量除了位置之外还有embeding维度。所以如果嵌入维度变了，位置编码也会变。
	所以可以只在固定维度添加位置编码？保证维度变了，位置编码不变？
```

![image-20250811164641624](/img/llm/image-20250811164641624.png)

## 1. Multi-Head Attention (MHA) 回顾

标准的多头注意力：$d$ 表示嵌入维度，$n_h$ 表示注意力头的数量，$d_h$ 表示每个头的维度，$h_t \in R^d$ 表示在注意力层中第t个token的注意力输入。

标准**MHA**机制通过三个矩阵$W^Q、W^K、W^V \in \mathbb{R}^{d_h n_h \times d}$分别生成输入$h_t$的查询向量$q_t\in \mathbb{R}^{𝑑_ℎ}$、键向量$k_t\in \mathbb{R}^{𝑑_ℎ}$和值向量$v_t\in \mathbb{R}^{𝑑_ℎ}$。公式如下：
$$
q_t = W^Q h_t \tag{1}
$$

$$
k_t = W^K h_t \tag 2
$$

$$
v_t = W^V h_t \tag 3
$$

接下来，$q_t$，$k_t$，$v_t$将被切分成$n_h$个头，用于多头注意力计算:

$$
[q_{t,1}; q_{t,2}; \ldots; q_{t,n_h}] = q_t \quad \tag 4
$$

$$
[𝑘_{𝑡,1}; 𝑘_{𝑡,2}; \ldots; 𝑘_{𝑡,𝑛_ℎ}] = 𝑘_𝑡 \quad \tag 5
$$

$$
[𝑣_{𝑡,1}; 𝑣_{𝑡,2}; \ldots; 𝑣_{𝑡,𝑛_ℎ}] = 𝑣_𝑡  \quad \tag 6
$$

其中：
- $q_{t,i}, k_{t,i}, v_{t,i} \in \mathbb{R}^{d_h}$ 是第 $t$ 个 token 的第i个头的 query、key、value 向量。
- $n_h$ 是注意力头数，QKV分头前的特征维度为$d$，分头后每个头的维度是 $d_h$。

公式含义：将原始的 $q_t, k_t, v_t$ 按列切分成 $n_h$ 个头的子向量。

每个头的注意力计算公式为:

$$
\text{attention\_weight}_{t,i} = \text{Softmax}_{j=1}^{t}\left( \frac{q_{t,i}^\top k_{j,i}}{\sqrt {d_h}} \right) \tag {7.1}
$$


$$
o_{t,i} = \sum_{j=1}^{t} \text{Softmax}\left(\frac{q_{t,i}^\top k_{j,i}}{\sqrt{d_h}}\right) v_{j,i} \tag {7.2}
$$

最后拼接所有头的输出，再做输出投影:

$$
𝑢_𝑡 = 𝑊^𝑂 [𝑜_{𝑡,1}; 𝑜_{𝑡,2}; \ldots; 𝑜_{𝑡,𝑛_ℎ}] \tag 8
$$

其中 $𝑊^𝑂 \in \mathbb{R}^{𝑑 \times 𝑑_ℎ 𝑛_ℎ}$ 是输出映射矩阵。

**推理时问题**：  
- 所有 key 和 value 需要缓存，KV cache大小为 $2𝑛_ℎ 𝑑_ℎ 𝑙$（$𝑙$ 为序列长度），当 batch size 和 $𝑙$ 很大时会占用大量显存。

---

## 2. Low-Rank Key-Value Joint Compression（低秩 KV 联合压缩）

MLA 核心是通过低秩联合压缩减少 KV cache大小。

1. **压缩输入**:

   将输入 $ h_t $ 压缩到KV低维共享表示 $ c_t^{KV} $：
   $$
   𝑐_{𝑡}^{𝐾𝑉} = 𝑊^{𝐷𝐾𝑉} ℎ_𝑡 \tag 9
   $$
   - $𝑐_{𝑡}^{𝐾𝑉} \in \mathbb{R}^{𝑑_𝑐}$：压缩后的 latent 表示，$𝑑_𝑐 \ll 𝑑_ℎ 𝑛_ℎ$。
   - $𝑊^{𝐷𝐾𝑉} \in \mathbb{R}^{𝑑_𝑐 \times 𝑑}$：降维矩阵，D的含义是降维down_sample。
   
2. **解码 key 和 value**:
   
   从 $𝑐_{𝑡}^{𝐾𝑉}$ 解码出 key 和 value：
   $$
   𝑘_{𝑡}^{𝐶} = 𝑊^{𝑈𝐾} 𝑐_{𝑡}^{𝐾𝑉} \tag {10}
   $$

   $$
   𝑣_{𝑡}^{𝐶} = 𝑊^{𝑈𝑉} 𝑐_{𝑡}^{𝐾𝑉} \tag {11}
   $$
   - $𝑊^{𝑈𝐾}, 𝑊^{𝑈𝑉} \in \mathbb{R}^{𝑑_ℎ 𝑛_ℎ \times 𝑑_𝑐}$：升维矩阵，U的含义是升维up_sample。

3. **低秩压缩后的注意力权重计算方式**：

$$
𝑞_{𝑡}^\top 𝑘_{j}^{𝐶} = (W^Q h_t)^\top  𝑊^{𝑈𝐾} 𝑐_{𝑡}^{𝐾𝑉} =  h_t^\top (W^Q)^\top  𝑊^{𝑈𝐾} 𝑐_{𝑡}^{𝐾𝑉} = \\ h_t (𝑊^{𝑈𝐾})^\top W^Q 𝑐_{𝑡}^{𝐾𝑉}
$$

4. **最后的输出**: 

多头注意力相当于把 **注意力权重**$attention\_weight$从一维向量变为了二维向量，shape: (seq_len,) -> (seq_len, head_num)，但本质上还是一个张量，只是得到这个张量的方式注意力机制计算比较复杂。
$$
[𝑜_{𝑡,1}; 𝑜_{𝑡,2}; \ldots; 𝑜_{𝑡,𝑛_ℎ}] = v_t @ attention\_weight =  \\
𝑊^{𝑈𝑉} 𝑐_{𝑡}^{𝐾𝑉} @ attention\_weight
$$

$$
𝑢_𝑡 = 𝑊^𝑂 [𝑜_{𝑡,1}; 𝑜_{𝑡,2}; \ldots; 𝑜_{𝑡,𝑛_ℎ}] \\
𝑢_𝑡 = 𝑊^𝑂 𝑊^{𝑈𝑉} (𝑐_{𝑡}^{𝐾𝑉} @ attention\_weight)
$$



**优势**：  

- 推理时仅需缓存 $𝑐_{𝑡}^{𝐾𝑉}$（每 token 只需 $𝑑_𝑐$ 维），KV 缓存大小从 $2𝑑_ℎ 𝑛_ℎ 𝑙$ 缩减到 $𝑑_𝑐 𝑙$。  
- 可将 $𝑊^{𝑈𝐾} \in \mathbb{R}^{𝑑_ℎ 𝑛_ℎ \times 𝑑_𝑐}$ 与 $𝑊^𝑄 \in \mathbb{R}^{d_h n_h \times d}$合并，将$𝑊^{𝑈𝑉} \in \mathbb{R}^{𝑑_ℎ 𝑛_ℎ \times 𝑑_𝑐}$ 与 $𝑊^𝑂 \in \mathbb{R}^{𝑑 \times 𝑑_ℎ 𝑛_ℎ}$合并，无需显式生成或存储 key/value。

### 矩阵合并分析：

上面公式看似需要使用$𝑐_{𝑡}^{𝐾𝑉}$重新生成历史的KV，但是通过权重吸收(合并)可以将重新生成的步骤合并其他向量的投影中，从而无需真正重新生成。

 $𝑊^{𝑈𝐾} \in \mathbb{R}^{𝑑_ℎ 𝑛_ℎ \times 𝑑_𝑐}$ 与 $𝑊^𝑄 \in \mathbb{R}^{d_h n_h \times d}$的合并，维度变换是 $d -> d_hn_h -> d_c$，吸收后是 $d -> d_c$，如果是原始的MHA不进行维度压缩$d -> d_hn_h$，可以看出来吸收后相比MHA计算量减少，不吸收则增大计算量。

$𝑊^{𝑈𝑉} \in \mathbb{R}^{𝑑_ℎ 𝑛_ℎ \times 𝑑_𝑐}$ 与 $𝑊^𝑂 \in \mathbb{R}^{𝑑 \times 𝑑_ℎ 𝑛_ℎ}$合并，维度变换是 $d_c -> d_hn_h -> d$, 吸收后是$d_c -> d$，同样吸收后相比MHA计算量减少，不吸收则增大计算量。

---



## 3. Low-Rank Query Compression（低秩 Query 压缩）

虽然压缩 Query 不能减少 KV 缓存，但是也能节省计算。

1. **压缩 Query**：  
   $$
   𝑐_{𝑡}^{𝑄} = 𝑊^{𝐷𝑄} ℎ_𝑡 \quad \tag {12}
   $$
   $$
   𝑞_{𝑡}^{𝐶} = 𝑊^{𝑈𝑄} 𝑐_{𝑡}^{𝑄} \quad \tag {13}
   $$
   - $𝑐_{𝑡}^{𝑄} \in \mathbb{R}^{𝑑_𝑐'}$：压缩后的 query 表示，$𝑑_𝑐' \ll 𝑑_ℎ 𝑛_ℎ$。
   - $𝑊^{𝐷𝑄} \in \mathbb{R}^{𝑑_𝑐' \times 𝑑}$，$𝑊^{𝑈𝑄} \in \mathbb{R}^{𝑑_ℎ 𝑛_ℎ \times 𝑑_𝑐'}$：降维和升维矩阵。

**作用**：  

- 降维后再升维，减少全连接计算量，尤其适用于输入维度 $𝑑$ 较大的场景。



## 4. Decoupled Rotary Position Embedding（解耦 RoPE）

### 背景

前面的推理没有考虑位置编码，如果考虑RoPE位置编码，会发现权重吸收和位置编码不兼容：
$$
𝑞_{𝑡}^\top 𝑘_{j}^{𝐶} => RoPE(𝑞_{𝑡}^\top)RoPE(𝑘_{j}^{𝐶}) \tag {-1}
$$

$$
\begin{array}{c}
RoPE(𝑞_{𝑡}^\top)RoPE(𝑘_{j}^{𝐶}) = (R_t𝑞_{𝑡})^\top R_j 𝑘_{j}^{𝐶} = \\
𝑞_{𝑡}^\top R_t^\top R_j 𝑘_{j}^{𝐶} = 𝑞_{𝑡}^\top R_{j-t} 𝑘_{j}^{𝐶} = h_t^\top (W^Q)^\top R_{j-t} 𝑊^{𝑈𝐾} 𝑐_{𝑡}^{𝐾𝑉} \tag {-2}
\end{array}
$$

前面 $𝑊^{𝑈𝐾}$ 与 $𝑊^𝑄$ 可以合并，是因为$(W^Q)^\top  𝑊^{𝑈𝐾}$ 是常量，但是$(W^Q)^\top R_{j-t} 𝑊^{𝑈𝐾}$是与query向量的位置$t$相关的变量$R_{j-t}$，即随推理过程中query的位置变化而变化，导致旧的缓存不能直接使用，所以无法直接合并。

为什么GQA的低秩投影没有受RoPE影响，因为GQA只减少了头数，计算时又恢复了头数，但是隐式恢复头数直接通过广播实现，不涉及特征维度改变序列长度改变；而MLA减小的是每个头的特征维度，计算时为了避免增加计算量，只能隐式恢复特征维度，即需要借助权重吸收，而两个权重之间又夹着RoPE，没办法权重吸收。

> RoPE（Rotary Position Embedding）对 key 和 query 都是位置敏感的。
>
> *若直接将 RoPE 应用于压缩后的 key，升维矩阵 $𝑊^{𝑈𝐾}$ 无法与 $𝑊^𝑄$ 合并，影响推理效率？*
>
> *一个简单的逻辑应该是把位置编码都应用到压缩后的特征上。*

### 原因

- RoPE 是依赖位置的旋转矩阵，矩阵乘法不满足交换律。
- 若在升维后的 key 上应用 RoPE，需重新计算所有历史 key 的位置编码，无法仅用缓存恢复。

### 解决方案  
将 query 和 key 分为两部分，一部分就用MLA不使用RoPE 位置编码，另一部分用MQA使用位置编码：

1. **对 query 和 key 分别应用 RoPE**：  
   
   将输入的查询内容向量 $c^Q_t$通过矩阵 $W^{QR}$投影到 RoPE 编码后的空间，得到分离后的旋转位置编码查询向量 $q^R_t$，并按多头$n_h$分块。
   $$
   [𝑞_{𝑡,1}^𝑅; 𝑞_{𝑡,2}^𝑅; \ldots; 𝑞_{𝑡,𝑛_ℎ}^𝑅] = \text{RoPE}(𝑊^{𝑄𝑅} 𝑐_{𝑡}^{𝑄}) \quad \text{(14)}
   $$
   将隐藏状态 $ h_t $ 通过矩阵 $W^{KR}$投影，并应用 RoPE 得到分离后的旋转位置编码键向量$ k^R_t $。
   $$
   𝑘_{𝑡}^𝑅 = \text{RoPE}(𝑊^{𝐾𝑅} ℎ_𝑡) \quad \text{(15)}
   $$
   
2. **拼接压缩部分和 RoPE 部分**：  
   
   将内容查询向量与旋转位置编码查询向量进行拼接，得到最终的第 $i$个头的查询向量。
   $$
   𝑞_{𝑡,𝑖} = [𝑞_{𝑡,𝑖}^𝐶, 𝑞_{𝑡,𝑖}^𝑅] \quad \text{(16)}
   $$
   将内容键向量与旋转位置编码键向量拼接，得到最终的第$i$个头的键向量。
   $$
   𝑘_{𝑡,𝑖} = [𝑘_{𝑡,𝑖}^𝐶, 𝑘_{𝑡,𝑖}^𝑅] \quad \text{(17)}
   $$
   
3. **注意力计算**：  
   
   通过点积计算第 $i$ 个头在时间步 $t$的查询向量与历史键向量的相关性，除以 $\sqrt{d_h + d^R_h}$进行缩放，然后使用 Softmax 得到注意力权重，对对应的值向量 $v^C_{j,i}$进行加权求和。
   $$
   𝑜_{𝑡,𝑖} = \sum_{𝑗=1}^{𝑡} \text{Softmax}\left(\frac{𝑞_{𝑡,𝑖}^\top 𝑘_{𝑗,𝑖}}{\sqrt{𝑑_ℎ + 𝑑_ℎ^𝑅}}\right) 𝑣_{𝑗,𝑖}^𝐶 \quad \text{(18)}
   $$
   
4. **最终输出**：  
   
   将所有头的输出 $o_{t,i}$ 拼接起来，并通过输出权重矩阵 $W^O$得到最终的输出向量 $u_t$。
   $$
   𝑢_𝑡 = 𝑊^𝑂 [𝑜_{𝑡,1}; 𝑜_{𝑡,2}; \ldots; 𝑜_{𝑡,𝑛_ℎ}] \quad \text{(19)}
   $$

其中 $W^{QR} \in \mathbb{R}^{d^R_h n_h \times d'_c}$ 和 $W^{KR} \in \mathbb{R}^{d^R_h \times d}$ 是分别用于生成分离查询向量和分离键向量的矩阵；$RoPE(·)$表示应用旋转位置编码的操作；符号$[\cdot ;\cdot]$表示拼接操作。在推理阶段，分离的键向量也需要被缓存。因此，MLA需要一个包含 $(d_c + d^R_h)l$元素的 KV 缓存。

**参数说明**：  

- $d_h^R$: RoPE 部分的维度。
- 推理时只需缓存 $c_{t}^{KV}$（大小约为 $𝑑_𝑐 + 𝑑_ℎ^𝑅$）。

---

## 5. 总结 MLA 思路

MLA 的核心目标是降低推理时的显存占用和计算延迟，同时保持注意力效果。具体方法包括：  
1. **低秩联合压缩 KV**：通过共享压缩表示 $𝑐_{𝑡}^{𝐾𝑉}$ 减少 KV 缓存大小。  
2. **低秩 Query 压缩**：减少 Query 的计算量。  
3. **解耦 RoPE**：在保留位置编码效果的同时，使压缩策略兼容 RoPE，避免破坏缓存复用。  

**最终效果**：  
- 显存占用从 $2𝑑_ℎ 𝑛_ℎ 𝑙$ 降至 $𝑑_𝑐 𝑙$。  
- 计算效率提升，适用于大规模模型部署。



