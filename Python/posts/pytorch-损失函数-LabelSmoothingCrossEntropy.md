---
title: 损失函数-Label Smoothing Cross Entropy
date: 2025-04-16 16:00:00
tags:
 - PyTorch
 - 深度学习
 - CTCLoss
typora-root-url: ..
typora-copy-images-to: ../img/pytorch
---



### 什么是 Label Smoothing Cross Entropy？

Label Smoothing 是一种正则化技术，用于改进分类任务中的交叉熵损失函数。传统的交叉熵损失函数假设目标标签是硬性（hard）的，即每个样本只有一个正确的类别标签，并且该类别的概率为 1，其他类别的概率为 0。然而，这种硬性标签可能会导致模型过拟合训练数据，尤其是在训练数据有限或标签可能存在噪声的情况下。

Label Smoothing 的基本思想是对目标标签进行“平滑”处理，将原本硬性的标签分布替换为一个更柔和的分布。这样可以减少模型对单一类别的过度自信，从而提高模型的泛化能力。

------

<!--more-->

### Label Smoothing 的工作原理

#### 1. **传统交叉熵损失**

在分类问题中，交叉熵损失函数定义如下：
$$
Cross\ Entropy\ Loss = -\sum_{i=1}^{C} y_i log(p_i)
$$
其中：

- *C* 是类别总数。
- $y_i $是目标标签的 one-hot 编码（硬性标签），即正确类别的值为 1，其他类别的值为 0。
- $p_i$ 是模型预测的第 *i* 类的概率。

在硬性标签的情况下，模型会努力最大化正确类别的概率 $p_i$，而完全忽略其他类别的概率。

#### 2. **Label Smoothing 的引入**

Label Smoothing 将目标标签从硬性分布转换为软性分布，具体公式如下：
$$
y_i′ =\left\{
\begin{aligned}
1−ϵ, & if\ i =true\ class\\
\frac ϵ{C-1}, & otherwise
\end{aligned}
\right.
$$
其中：

- *ϵ* 是平滑参数，通常取值在 [0, 1] 范围内（例如 0.1）。
- $y_i'$ 是平滑后的目标标签分布。
- 正确类别的概率被降低为 1−*ϵ*，而其他类别的概率被提升为$\frac ϵ {C−1}$。

#### 3. **平滑后的交叉熵损失**

使用平滑后的标签分布$y_i'$，交叉熵损失变为：
$$
Smoothed\ Cross\ Entropy Loss = -\sum_{i=1}^{C} y'_i log(p_i)
$$


展开后可以写为：
$$
Smoothed\ Cross\ Entropy\ Loss =-(1-ϵ) log(p_{true}) -\sum_{i \neq true} \frac ϵ {C-1} log(p_i)
$$
其中：

- $p_{true}$ 是模型对正确类别的预测概率。
- $\sum_{i \neq true} \frac ϵ {C-1} log(p_i)$是对其他类别的惩罚项。

通过这种方式，模型不仅需要最大化正确类别的概率，还需要关注其他类别的预测结果，从而避免对单一类别的过度自信。

------

### Label Smoothing 的优点

1. **减少过拟合**
   Label Smoothing 防止模型对训练数据中的硬性标签过于依赖，从而提高了模型的泛化能力。
2. **改善模型的校准**
   使用 Label Smoothing 后，模型的预测概率通常更加接近真实分布，而不是过度集中在某个类别上。
3. **缓解标签噪声的影响**
   如果训练数据中的标签存在噪声，Label Smoothing 可以通过平滑标签分布来降低噪声对模型的影响。
4. **增强模型的鲁棒性**
   在对抗攻击等场景下，Label Smoothing 可以使模型对输入扰动更加鲁棒。

### Label Smoothing 的实现

以下是一个基于 PyTorch 的 Label Smoothing 实现示例：

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class LabelSmoothingCrossEntropy(nn.Module):
    def __init__(self, label_smoothing=0.1, class_weights=None, reduction='mean'):
        super(LabelSmoothingCrossEntropy, self).__init__()
        self.label_smoothing = label_smoothing
        self.reduction = reduction
        # 类别权重,此处可忽略
        self.class_weights = class_weights

    def forward(self, preds, targets):
        # targets是每个样本的类别标签, 此处类别使用的是数字编号不是one-hot
        n_classes = preds.size(-1)
        # 计算预测值的对数概率
        log_preds = F.log_softmax(preds, dim=-1)

        # 平滑后的目标分布, 创建一个初始值为ϵ/(C−1)的张量
        smooth_labels = torch.full_like(preds, self.label_smoothing / (n_classes - 1))
        # 将正确类别的值设置为 1−ϵ
        # scatter_(dim, index, src): 根据给定的索引，将指定的值写入目标张量的对应位置。
        smooth_labels.scatter_(1, targets.unsqueeze(1), 1 - self.label_smoothing)

        # 最后计算加权对数概率的和作为损失
        if self.class_weights is not None:
            loss = -(smooth_labels * log_preds * self.class_weights.unsqueeze(0)).sum(dim=-1)
        else:
            loss = -(smooth_labels * log_preds).sum(dim=-1)

        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        else:
            return loss

# 示例用法
preds = torch.tensor([[2.0, 1.0, 0.1], [1.5, 2.5, 0.3]])  # 模型预测的 logits
targets = torch.tensor([0, 1])  # 目标标签

criterion = LabelSmoothingCrossEntropy(label_smoothing=0.1, class_weights= torch.as_tensor([1, 2, 1]))
loss = criterion(preds, targets)
print("Label Smoothing Cross Entropy Loss:", loss.item())
```



+ PyTorch 1.10之后CrossEntropyLoss 已经原生支持标签平滑功能

```python
import torch
from torch.nn import CrossEntropyLoss

# 示例用法
preds = torch.tensor([[2.0, 1.0, 0.1], [1.5, 2.5, 0.3]])  # 模型预测的 logits
targets = torch.tensor([0, 1])  # 目标标签

criterion = CrossEntropyLoss(weight=None, label_smoothing=0.1)

loss = criterion(preds, targets)
print("Label Smoothing Cross Entropy Loss:", loss.item())

```



### Label Smoothing 的注意事项

1. 选择合适的平滑参数 *ϵ* 的值通常在 0.1 左右。如果 *ϵ* 过大，可能会导致模型对正确类别的学习不足；如果 *ϵ* 过小，则效果可能不明显。
2. **适用于大规模分类任务**
   Label Smoothing 在类别数量较多的任务中效果更显著，因为平滑后的分布能够更好地反映类别间的关联性。
3. **与知识蒸馏结合**
   Label Smoothing 常与知识蒸馏（Knowledge Distillation）结合使用。通过使用教师模型生成软标签，学生模型可以学习到更加丰富的类别间关系。