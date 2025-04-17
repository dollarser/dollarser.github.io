---
title: 损失函数-CTCLoss
date: 2025-04-16 14:00:00
tags:
 - PyTorch
 - 深度学习
 - CTCLoss
typora-root-url: ..
typora-copy-images-to: ../img/pytorch
---

### 什么是CTCLoss？

CTC (Connectionist Temporal Classification) 是一种用于序列到序列学习的损失函数，特别适用于输入和输出长度不固定的场景。它在语音识别、手写体识别等任务中应用广泛。CTC 的核心思想是通过引入一个“空白”符号（blank token），允许模型对不定长的输入序列生成不定长的输出序列，同时避免了对输入和输出进行显式的对齐操作。

传统的序列标注方法通常需要将输入和输出进行严格的对齐（例如，逐帧标注），而 CTC 允许模型自动学习输入和输出之间的对齐关系，从而大大简化了训练过程。

------
<!--more-->

### CTCLoss 的工作原理

#### 1. **输入与输出的关系**

- 输入是一个不定长的序列，比如语音信号或手写笔迹的时间序列。
- 输出是一个较短的目标序列，比如文本转录结果。
- 输入和输出的长度可能不同，且没有明确的对齐关系。

#### 2. **引入空白符号**

CTC 引入了一个特殊的“空白”符号（通常记作 `-` 或 `blank`），表示某个时间步没有对应的输出。空白符号在最终的输出中会被移除。

#### 3. **路径的概念**

CTC 将输入序列到输出序列的所有可能对齐方式称为“路径”。例如：

- 输入序列长度为 *T*，目标序列长度为 *L*。
- 每个时间步可以选择输出字符或空白符号。
- 所有可能的路径构成了所有可能的输入到输出的对齐方式。

#### 4. **路径的约束**

为了保证输出的有效性，CTC 对路径施加了一些约束：

- 相邻的重复字符会被合并。例如，路径 `a--a-b` 会被解码为 `ab`。
- 空白符号会被忽略。例如，路径 `a-b---c` 会被解码为 `abc`。

#### 5. **概率计算**

对于每个可能的路径，CTC 计算其概率，并将所有可能路径的概率相加，得到目标序列的总概率。

#### 6. **损失函数**

CTC Loss 的目标是最大化目标序列的总概率（即最小化负对数似然）。公式如下：
$$
CTC Loss=−log{\sum_{π\in Paths(y)} P(π∣X)}
$$


其中：

- Paths(*y*) 表示所有能生成目标序列 *y* 的路径集合。
- *P*(*π*∣*X*) 表示给定输入 *X* 时路径 *π* 的概率。

------

### CTCLoss 的计算过程演示

假设我们有以下输入和目标序列：

#### 输入序列

- 输入序列为一个长度为 *T*=6 的特征序列。
- 模型的输出是一个 *T*×*V* 的矩阵，其中 *V* 是词汇表大小（包括空白符号）。
- 假设词汇表为 `{a, b, c, blank}`，则 *V*=4。

#### 目标序列

- 目标序列为 `abc`。

#### 步骤 1：生成所有可能路径

CTC 需要找到所有可以生成目标序列 `abc` 的路径。例如：

- 路径 `a-b-c`。
- 路径 `a-b-c-blank`。
- 路径 `a-blank-b-c`。
- 路径 `a-blank-blank-b-c`。
- 等等。

注意：相邻的重复字符会被合并，因此路径 `a-a-b-c` 也会被解码为 `abc`。

#### 步骤 2：计算每条路径的概率

对于每条路径，计算其概率。假设模型输出的 *T*×*V* 矩阵如下：

| 时间步 | a    | b    | c    | blank |
| ------ | ---- | ---- | ---- | ----- |
| 1      | 0.4  | 0.1  | 0.1  | 0.4   |
| 2      | 0.3  | 0.4  | 0.1  | 0.2   |
| 3      | 0.1  | 0.3  | 0.4  | 0.2   |
| 4      | 0.2  | 0.3  | 0.2  | 0.3   |
| 5      | 0.1  | 0.2  | 0.5  | 0.2   |
| 6      | 0.1  | 0.1  | 0.6  | 0.2   |

例如，路径 `a-b-c` 的概率为：
$$
P(a−b-c)=P(a|t=1)⋅P(b∣t=2)⋅P(c∣t=3) = 0.4 ⋅ 0.4 ⋅ 0.4 = 0.064
$$
例如，路径 `a-b-blank-c` 的概率为：
$$
P(a−b-c)=P(a|t=1) ⋅ P(b∣t=2) ⋅ P(blank∣t=3) ⋅ P(c∣t=4) = 0.4 ⋅ 0.4 ⋅ 0.2 ⋅ 0.4 = 0.0128
$$

#### 步骤 3：合并路径概率

根据 CTC 的规则，将所有能生成目标序列 `abc` 的路径概率相加，得到目标序列的总概率。

#### 步骤 4：计算损失

最终，CTC Loss 为：
$$
CTC Loss=−log{\sum_{π\in Paths(y)} P(π∣X)}
$$

### PyTorch实现

```python
import torch
import torch.nn as nn
# 参数定义
T = 6               # 时间步长（如音频帧数）
N = 1               # 批次大小
C = 4               # 类别数（含空白符）
target_length = 3   # 每个样本的标签长度

# 定义输入输出
log_probs = torch.tensor([
    [[0.4, 0.1, 0.1, 0.4],  # t=1
     [0.3, 0.4, 0.1, 0.2],  # t=2
     [0.1, 0.3, 0.4, 0.2],  # t=3
     [0.2, 0.3, 0.2, 0.3],  # t=4
     [0.1, 0.2, 0.5, 0.2],  # t=5
     [0.1, 0.1, 0.6, 0.2]]  # t=6
], dtype=torch.float32).log_softmax(dim=2)  # 取对数概率
log_probs = log_probs.permute(1, 0, 2)  # shape: time_step, batch_size, dimension
targets = torch.tensor([[0, 1, 2]])  # 目标序列索引，对应 'a', 'b', 'c'

# 定义输入序列的实际长度
input_lengths = torch.tensor([T]*N)  # 输入序列长度
input_lengths = torch.full(size=(N,), fill_value=T, dtype=torch.long)

# 标签实际长度（假设每个样本的标签长度为 target_length）
target_lengths = torch.tensor([len(target) for target in targets])  # 目标序列长度

print(target_lengths)

# 定义 CTCLoss
ctc_loss = nn.CTCLoss(blank=3)  # 空白符号索引为 3
loss = ctc_loss(log_probs, targets, input_lengths, target_lengths)

print("CTC Loss:", loss.item())
```

