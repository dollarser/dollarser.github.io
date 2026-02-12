---
title: 深度学习常用损失函数
date: 2026-02-11 18:00:00
tags:
 - Loss
 - Python
typora-root-url: ../..
typora-copy-images-to: ../../img/loss
---



> 本文系统梳理深度学习各任务领域的核心损失函数，包含**精确数学公式、符号定义、特性分析及实践指南**，适用于研究参考与工程实现。

---

## 一、分类任务

### 1. 交叉熵损失（Cross-Entropy Loss）

#### 多分类（单标签）

$$
\mathcal{L} = -\frac{1}{N}\sum_{i=1}^{N}\sum_{c=1}^{C} y_{i,c} \log(p_{i,c})
$$

- **符号**：
  $N$=样本数，$C$=类别数，$y_{i,c}$=真实标签（one-hot），$p_{i,c}$=Softmax输出概率  
- **特性**：
  - 梯度 $\nabla \mathcal{L} \propto (p_{i,c} - y_{i,c})$，误差越大梯度越强  
  - *框架实现*：PyTorch `CrossEntropyLoss` = `LogSoftmax` + `NLLLoss`（输入为logits，避免数值不稳定）

#### 二分类

$$
\mathcal{L} = -\frac{1}{N}\sum_{i=1}^{N} \left[ y_i \log(\sigma(x_i)) + (1-y_i)\log(1-\sigma(x_i)) \right]
$$

- **符号**：$\sigma(x)=1/(1+e^{-x})$，$y_i \in \{0,1\}$  
- **实践**：优先使用 `BCEWithLogitsLoss`（融合Sigmoid+BCE，数值稳定）

#### 多标签分类
- 对每个类别独立计算BCE，$y_{i,c} \in \{0,1\}$（标签非互斥）

---

### 2. Focal Loss

$$
\mathcal{L}_{FL} = -\frac{1}{N}\sum_{i=1}^{N} \alpha_t (1 - p_t)^\gamma \log(p_t), \quad 
p_t = 
\begin{cases} 
p_i & \text{if } y_i=1 \\ 
1-p_i & \text{if } y_i=0 
\end{cases}
$$

- **符号**：$\alpha_t$=类别权重（平衡正负样本），$\gamma \geq 0$=聚焦参数  
- **作用**：$(1-p_t)^\gamma$ 压制易分样本梯度（如 $p_t=0.9, \gamma=2$ 时权重降至0.01）  
- **应用**：RetinaNet（目标检测）、严重不平衡分类（$\gamma=2, \alpha=0.25$ 常用）

---

### 3. Hinge Loss（二分类）
$$
\mathcal{L} = \max(0, 1 - y \cdot f(x)), \quad y \in \{-1, +1\}
$$
- **符号**：$f(x)$=模型原始输出（未归一化）  
- **特点**：SVM核心损失，要求分类间隔>1；深度学习中较少直接使用（需配合线性层）

---

##  二、回归任务

### 1. MSE (L2 Loss)

$$
\mathcal{L} = \frac{1}{N}\sum_{i=1}^{N} (y_i - \hat{y}_i)^2
$$

- **梯度**：$\nabla \mathcal{L} = 2(y_i - \hat{y}_i)$  
- **假设**：误差服从高斯分布；对异常值敏感（大误差梯度平方级增长）

---

### 2. MAE (L1 Loss)

$$
\mathcal{L} = \frac{1}{N}\sum_{i=1}^{N} |y_i - \hat{y}_i|
$$

- **梯度**：$\nabla \mathcal{L} = \text{sign}(y_i - \hat{y}_i)$（0点次梯度）  
- **优势**：对异常值鲁棒；**缺点**：0点不可导，收敛较慢

---

### 3. Huber Loss / Smooth L1

$$
\mathcal{L}_\delta = 
\begin{cases} 
\frac{1}{2}(y - \hat{y})^2 & \text{if } |y-\hat{y}| \leq \delta \\
\delta |y - \hat{y}| - \frac{1}{2}\delta^2 & \text{otherwise}
\end{cases}
$$

- **符号**：$\delta$=阈值（常用1.0）  
- **应用**：Faster R-CNN边界框回归（Smooth L1 = $\delta=1$ 的Huber）  
- **优势**：小误差用MSE（平滑），大误差用MAE（鲁棒）

---

### 4. Log-Cosh Loss

$$
\mathcal{L} = \frac{1}{N}\sum_{i=1}^{N} \log(\cosh(y_i - \hat{y}_i)), \quad \cosh(x)=\frac{e^x + e^{-x}}{2}
$$

- **特性**：  
  - $|e| \ll 1$ 时 $\approx \frac{1}{2}e^2$（MSE）  
  - $|e| \gg 1$ 时 $\approx |e| - \log 2$（MAE）  
- **优势**：全程二阶可导，对异常值鲁棒

---

## 三、图像分割 & 医学影像

### 1. Dice Loss

$$
\mathcal{L}_{Dice} = 1 - \frac{2\sum_i p_i g_i + \epsilon}{\sum_i p_i^2 + \sum_i g_i^2 + \epsilon}
$$

- **符号**：$p_i$=预测概率（0~1），$g_i$=真实标签（0/1），$\epsilon=10^{-5}$（平滑项）  
- **关键**：训练用“软Dice”（概率值），非二值化；对小目标/不平衡数据敏感  
- **变体**：Dice系数 = $1 - \mathcal{L}_{Dice}$

---

### 2. IoU (Jaccard) Loss
$$
\mathcal{L}_{IoU} = 1 - \frac{\sum_i p_i g_i}{\sum_i p_i + \sum_i g_i - \sum_i p_i g_i + \epsilon}
$$

- **特点**：分母为并集，与评估指标IoU直接对齐  
- **注意**：无重叠时梯度为0，需加$\epsilon$或改用Generalized IoU Loss

---

### 3. Tversky Loss

$$
\mathcal{L}_{Tversky} = 1 - \frac{\sum p_i g_i}{\sum p_i g_i + \beta \sum p_i(1-g_i) + \gamma \sum (1-p_i)g_i + \epsilon}
$$

- **符号**：$\beta$=假阳性(FP)权重，$\gamma$=假阴性(FN)权重 

- **医学应用**：$\gamma > \beta$（如 $\beta=0.3, \gamma=0.7$）强化减少漏检（FN惩罚更高）

---

### 4. Combo Loss

$$
\mathcal{L} = \alpha \cdot \mathcal{L}_{BCE} + (1-\alpha) \cdot \mathcal{L}_{Dice}, \quad \alpha \in [0,1]
$$

- **目的**：BCE提供像素级梯度，Dice优化区域重叠（$\alpha=0.5$ 常用）  
- **场景**：医学分割（如U-Net变体）

---

## 四、序列与结构化预测

### 1. CTC Loss

$$
\mathcal{L}_{CTC} = -\log \sum_{\pi \in \mathcal{B}^{-1}(\mathbf{y})} P(\pi | \mathbf{x})
$$

- **符号**： 

  $\mathbf{x}$=输入序列（如音频帧），$\mathbf{y}$=目标标签序列，  

  $\mathcal{B}^{-1}(\mathbf{y})$=所有合法对齐路径（含blank符号）  

- **核心**：动态规划计算路径概率和，解决输入/输出长度不匹配  

- **应用**：语音识别（DeepSpeech）、OCR（CRNN）

---

### 2. NLL Loss（Negative Log Likelihood）

$$
\mathcal{L} = -\frac{1}{N}\sum_{i=1}^{N} \log(p_{i, y_i})
$$

- **前提**：输入需经 `LogSoftmax`（$p_{i,y_i}$ 为对数概率）  
- **关系**：`CrossEntropyLoss` = `LogSoftmax` + `NLLLoss`

---

## 五、生成模型 & 对抗学习

### 1. GAN系列
#### 原始GAN (Minimax)

$$
\min_G \max_D V(D,G) = \mathbb{E}_{x}[\log D(x)] + \mathbb{E}_{z}[\log(1 - D(G(z)))]
$$

- **实践改进**：生成器常用 $-\log D(G(z))$（避免初期梯度消失）

#### LSGAN

$$
\begin{aligned}
\mathcal{L}_D &= \frac{1}{2}\mathbb{E}_x[(D(x)-b)^2] + \frac{1}{2}\mathbb{E}_z[(D(G(z))-a)^2] \\
\mathcal{L}_G &= \frac{1}{2}\mathbb{E}_z[(D(G(z))-c)^2]
\end{aligned}
$$

- **参数**：$(a,b,c)$ 常取 $(0,1,1)$，用最小二乘替代对数损失，训练更稳定

#### WGAN-GP

$$
\begin{aligned}
\mathcal{L}_D &= \mathbb{E}_z[D(G(z))] - \mathbb{E}_x[D(x)] + \lambda \mathbb{E}_{\tilde{x}}[(\|\nabla_{\tilde{x}} D(\tilde{x})\|_2 - 1)^2] \\
\mathcal{L}_G &= -\mathbb{E}_z[D(G(z))]
\end{aligned}
$$

- **符号**：$\tilde{x} = \epsilon x + (1-\epsilon)G(z)$, $\epsilon \sim U(0,1)$, $\lambda=10$  
- **优势**：梯度惩罚替代权重裁剪，解决模式崩溃

---

### 2. VAE Loss

$$
\mathcal{L} = \underbrace{\mathbb{E}_{q(z|x)}[\log p(x|z)]}_{\text{重构损失}} - \beta \cdot \underbrace{KL(q(z|x) \| p(z))}_{\text{正则项}}
$$

- **重构损失**：连续数据用MSE，二值图像用BCE  
- **KL项**：$p(z) = \mathcal{N}(0,I)$，$\beta$ 控制隐空间约束（$\beta$-VAE中 $\beta>1$）

---

### 3. Perceptual Loss

$$
\mathcal{L}_{perc} = \sum_{l} \lambda_l \|\phi_l(I^{hr}) - \phi_l(I^{sr})\|_2^2
$$

- **符号**：$\phi_l$=预训练VGG第$l$层特征图，$I^{hr}$=高清图，$I^{sr}$=生成图  
- **优势**：匹配高层语义特征，避免MSE导致的模糊（超分、风格迁移）

---

### 4. Style Loss

$$
\mathcal{L}_{style} = \sum_{l} \lambda_l \|G_l^{\hat{}} - G_l\|_F^2, \quad G_l = \phi_l \phi_l^\top
$$

- **符号**：$G_l$=Gram矩阵（捕获通道间相关性）  
- **应用**：Gatys风格迁移、AdaIN

---

## 六、度量学习 & 对比学习

### 1. Triplet Loss

$$
\mathcal{L} = \max( \|f(a)-f(p)\|_2 - \|f(a)-f(n)\|_2 + \text{margin},\ 0 )
$$



- **符号**：$a$=锚点，$p$=正样本（同类），$n$=负样本（异类）  
- **关键**：难样本挖掘（semi-hard mining）提升效率

---

### 2. Contrastive Loss

$$
\mathcal{L} = (1-y) \cdot d^2 + y \cdot \max(\text{margin} - d,\ 0)^2, \quad y \in \{0,1\}
$$

- **符号**：$y=0$=同类对，$y=1$=异类对，$d$=样本对距离

---

### 3. InfoNCE Loss

$$
\mathcal{L} = -\log \frac{\exp(q \cdot k_+ / \tau)}{\sum_{i=0}^{K} \exp(q \cdot k_i / \tau)}
$$

- **符号**：$q$=查询向量，$k_+$=正样本键，$\{k_i\}$=1正+$K$负，$\tau$=温度参数  
- **基石**：SimCLR、MoCo、CLIP等对比学习框架核心（$\tau=0.07$ 常用）

---

## 七、其他关键损失

### 1. KL散度

$$
KL(P\|Q) = \sum_i P(i) \log \frac{P(i)}{Q(i)} \quad \text{(离散)} \quad / \quad \int p(x)\log\frac{p(x)}{q(x)}dx \quad \text{(连续)}
$$

- **特性**：非对称（$KL(P\|Q) \neq KL(Q\|P)$）  
- **应用**：知识蒸馏（教师$P$→学生$Q$）、VAE正则项

---

### 2. Center Loss

$$
\mathcal{L}_c = \frac{1}{2} \sum_{i=1}^{m} \|x_i - c_{y_i}\|_2^2
$$

- **符号**：$x_i$=样本特征，$c_{y_i}$=类别$y_i$中心（可学习）  
- **联合训练**：$\mathcal{L} = \mathcal{L}_{softmax} + \lambda \mathcal{L}_c$（$\lambda=0.01$）  
- **效果**：增强类内紧凑性（人脸识别）

---

### 3. 目标检测组合损失（Faster R-CNN示例）

$$
\mathcal{L} = \underbrace{\mathcal{L}_{cls}(p, p^*)}_{\text{分类}} + \lambda \cdot \underbrace{\mathbb{I}(p^* \geq 0.5) \cdot \mathcal{L}_{reg}(t, t^*)}_{\text{回归}}
$$

- **符号**：$\mathcal{L}_{cls}$=交叉熵，$\mathcal{L}_{reg}$=Smooth L1，$\mathbb{I}$=指示函数  
- **权重**：$\lambda=1.0$（平衡分类与回归）

---

## 实践核心建议表


| 问题场景          | 推荐损失函数                     | 关键参数提示               |
|-------------------|----------------------------------|--------------------------|
| 严重类别不平衡    | Focal Loss / Dice Loss          | $\gamma=2$, $\alpha=0.25$ |
| 医学小目标分割    | Tversky Loss ($\gamma > \beta$) | $\beta=0.3, \gamma=0.7$   |
| 生成图像质量      | Perceptual + Style Loss         | VGG16 relu3_3层加权       |
| 对比学习          | InfoNCE                         | $\tau=0.07$, 负样本量$K$↑ |
| 边界框回归        | Smooth L1                       | $\delta=1.0$             |
| 知识蒸馏          | $\alpha \cdot CE + (1-\alpha) \cdot KL$ | $\alpha=0.3$       |

---

## 黄金准则（必读）

1. **激活-损失配套**：Softmax + CrossEntropy，Sigmoid + BCE  
2. **数值稳定性**：优先用封装函数（`BCEWithLogitsLoss` > `Sigmoid + BCELoss`）  
3. **损失≠评估指标**：优化目标（Loss）与评估指标（Accuracy/F1/mAP）需区分  
4. **组合损失常态**：分割（BCE+Dice）、检测（Cls+Reg）、蒸馏（CE+KL）  
5. **超参敏感**：Focal Loss的$\gamma$、InfoNCE的$\tau$需网格搜索验证  
6. **框架差异**：  
   - PyTorch `CrossEntropyLoss` 接收logits  
   - TensorFlow `SparseCategoricalCrossentropy` 支持整数标签  

> 📌 **最后建议**：初学者从任务标准损失入手（分类→CrossEntropyLoss），根据数据问题（不平衡、噪声）迭代调整。所有公式符号已明确定义，可直接用于论文写作或代码实现。建议结合具体任务进行消融实验验证！