---
title: pytorch-优化器算法
date: 2024-05-14 14:24:00
toc: true
tags:
 - PyTorch
 - 深度学习
typora-root-url: ..
typora-copy-images-to: ../img/pytorch
---

# 优化器算法



[TOC]

## 0. 基础

### 1. 导入

```python
import torch.optim as optim
```

### 2. 常用的优化器

+ SGD/Momentum SGD
+ Adam/AdamW
+ AdaGrad
+ RMS prop

<!--more-->



### 3. 使用框架

+ 生成优化器

```python
import torch.optim as optim

optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
optimizer = optim.Adam([var1, var2], lr=0.0001)
```

+ 同一个模型定义不同的优化器

```python
import torch
import torch.optim as optim

# params可以用字典传参，给不同的参数赋值不同的学习率
optim.SGD([{'params': model.base.parameters(), 'lr': 1e-2},
            {'params': model.classifier.parameters()}
        ], lr=1e-3, momentum=0.9)

# 给不同的参数设置不同的权重衰减系数，bias权重衰减设为0
bias_params = [p for name, p in model.named_parameters() if 'bias' in name]
others = [p for name, p in model.named_parameters() if 'bias' not in name]
optim.SGD([{'params': others},
           {'params': bias_params, 'weight_decay': 0}
           ], weight_decay=1e-2, lr=1e-2)
```



+ 使用优化器

```python
for input, target in dataset:
    # 梯度清零
    optimizer.zero_grad()
    output = model(input)
    # 计算损失
    loss = loss_fn(output, target)
    # 损失反向传播（计算每个参数的梯度）
    loss.backward()
    # 根据梯度更新权重参数
    optimizer.step()
```



## 1. SGD/Momentum SGD

SGD：随机梯度优化，最简单常用的优化器，卷积神经网络时代比较好用，transformer时代被AdamW取代。

### 1.1 SGD原理

**1. 计算梯度**:  $f_t$是模型函数，$θ_{t-1}$是上一步的参数，$\nabla_θ$是向量梯度计算，$\lambda$是权重衰减系数

$$g_t=\nabla_θ f_t (θ_{t-1})$$

$$g_t=g_t + \lambda θ_{t-1} $$

**2. 梯度更新**：$\lambda$是权重衰减系数，$\gamma$是学习率


$$\theta_t = \theta_{t-1} -\gamma g_t $$

### 1.2 Momentum SGD原理

**1. 计算梯度**: 和SGD一样计算权重衰减后的梯度

$$g_t=\nabla_θ f_t (θ_{t-1})$$

$$g_t=g_t + \lambda θ_{t-1} $$

**2. 计算动量**：$m_t$是当前动量，$m_{t-1}$上一步的动量，$\beta$是动量系数

$$m_0 = g_0$$

$$m_t = \beta m_{t-1} + (1-\beta)g_t $$

目前新的版本使用$1- \tau$ 代替$1- \beta$，$\tau$作为动量抑制系数

$$m_t = \beta m_{t-1} + (1-\tau)g_t $$

**3. 梯度更新**：$\gamma$是学习率

$$g_t = b_t$$

$$\theta_t = \theta_{t-1} -\gamma g_t $$



### 1.3 代码

```python
class SGD(Optimizer):
    def __init__(self, params, 
                 lr=1e-3, 
                 momentum=0, 
                 dampening=0,
                 weight_decay=0, 
                 nesterov=False, *, 
                 maximize: bool = False, 
                 foreach: Optional[bool] = None,
                 differentiable: bool = False, 
                 fused: Optional[bool] = None):
```

参数：

* **params**：待优化的模型参数，通过**model.parameters()**获得
* **lr**：学习率$\gamma$
* **momentum**：梯度动量系数$\mu$
* **dampening**：动量抑制$\tau$
* **eps**：分母的添加项，增加数值稳定性1e-8
* **weight_decay**：权重衰减系数，正则化系数$\lambda$

## 2. Adam/AdamW

### 2.1 Adam

**1. 计算梯度**:  $f_t$是模型函数，$θ_{t-1}$是上一步的参数，$\nabla_θ$是向量梯度计算，$\lambda$是权重衰减系数

$$g_t=\nabla_θ f_t (θ_{t-1})$$

$$g_t=g_t + \lambda θ_{t-1}$$

**2. 计算动量**：$m_t$是当前动量，$m_{t-1}$上一步的动量，$\beta_1$是动量系数

$$m_t = \beta_1 m_{t-1} + (1-\beta_1)g_t $$

**3. 计算二阶动量**：$b_t$是当前动量，$b_{t-1}$上一步的动量，$\mu$是动量系数

$$v_t = \beta_2 v_{t-1} + (1-\beta_2)g^2_t $$

**4. 快速启动**：由于初始时$m_0=0, v_0=0,\beta \approx1 $，m和v更新很慢，需要很多步才能到正常值，需要进行偏差修正

$$\hat{m_t}=m_t/(1-\beta^t_1)$$

$$\hat{v_t}=v_t/(1-\beta^t_2)$$

**5. 梯度更新**：$\gamma$是学习率
$$\theta_t = \theta_{t-1} -\gamma \hat{m_t}/(\sqrt {\hat v_t} + \epsilon)$$

### 2.2 AdamW

AdamW是对Adam的修正，修改了权重衰减的位置，权重衰减放到了最后的损失位置，而不是最开始的梯度位置。

**1. 计算梯度**:  $f_t$是模型函数，$θ_{t-1}$是上一步的参数，$\nabla_θ$是向量梯度计算，$\lambda$是权重衰减系数

$$g_t=\nabla_θ f_t (θ_{t-1})$$

**2. 计算动量**：$m_t$是当前动量，$m_{t-1}$上一步的动量，$\beta_1$是动量系数

$$m_t = \beta_1 m_{t-1} + (1-\beta_1)g_t $$

**3. 计算二阶动量**：$b_t$是当前动量，$b_{t-1}$上一步的动量，$\mu$是动量系数

$$v_t = \beta_2 v_{t-1} + (1-\beta_2)g^2_t $$

**4. 快速启动**：由于初始时$m_0=0, v_0=0,\beta \approx1 $，m和v更新很慢，需要很多步才能到正常值，需要进行偏差修正

$$\hat{m_t}=m_t/(1-\beta^t_1)$$

$$\hat{v_t}=v_t/(1-\beta^t_2)$$

**5. 梯度更新**：$\gamma$是学习率

$$\theta_t=\theta_{t-1} - \gamma\lambda θ_{t-1}$$

$$\theta_t = \theta_{t-1} -\gamma \hat{m_t}/(\sqrt {\hat v_t} + \epsilon)$$



## 3. AdaGrad/RMS prop

相当于动量系数$\beta_1$为0的Adam，根据参数之前的梯度作为当前参数的权重

