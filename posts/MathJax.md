---
title: MathJax
date: 2019-06-30 22:42:17
tags: 
 - 随笔
 - 学习笔记
---

### 基本数学公式语法(of MathJax)[^queto1]

[^queto1]: CSDN: [作者: ethmery](https://blog.csdn.net/ethmery/article/details/50670297)

## 概述
在markdown中输入数学公式需要LaTaX语法的支持。
## 基本语法
### 呈现位置
+ 正文（inline）中的LaTeX公式用`$...$`定义
   + 例句为：`$\sun_{i=0}^N \int_{a}^{b} g(t,i)\text{d}t$`
   + 显示为：$\sum_{i=0}^N \int_{a}^{b} g(t,i)\text{d}t$
+ 单独显示（display）的LaTeX公式用`$$...$$`定义，此时公式居中独立成块显示
   + 例句为：`$$\sum_{i=0}^N \int_{a}^{b} g(i,t)\text{d}t$$`
   + 显示为：$$\sum_{i=0}^N \int_{a}^{b} g(i,t)\text{d}t$$
+ *下列描述语句中若非特别指出均省略`$`*

<!--more-->

### 希腊字母

显示|命令|显示|命令
:-:|:-:|:-:|:-:
$\alpha$|\alpha|$\beta$|\beta
$\gamma$|\gamma|$\delta$|\delta
$\epsilon$|\epslion|$\zeta$|\zeta

-若需要大写希腊字母，将命令首字母大写即可
-`\Gamma`显示为$\Gamma$
-若需要斜体希腊字母，将命令前加上前缀`var`即可
-`varGamma`显示为$\varGamma$

### 字母修饰
#### 上下标
+ 上标：`^`
+ 下标：`_`
+ 举例：`C_n^2`显示为$C_n^2$
#### 矢量
+ `\vec a`显示为$\vec a$
+ `\overrightarrow{xy}`显示为$\overrightarrow{xy}$
#### 字体
+ Typewriter:`\mathtt{A}`显示为$\mathtt{A}$
   + $\mathtt{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$
#### 分组
+ 使用`{}`将具有相同等级的内容扩入其中，成组处理
+ 举例：`10^{10}`显示为$10^{10}$, 而`10^10`显示为$10^10$
#### 括号
+ 小括号：`()`显示为$()$
+ 中括号：`[]`显示为$[]$
+ 尖括号：`\langle,\rangle`显示为$\langle\rangle$
   + 此处与分组符号`{}`相区别，使用转义字符`\`
+ 使用`\left(`和`\right)`使符号大小与相邻的公式自适应；该语法适用于所有括号类型
   + `(\frac{x}{y})`显示为$(\frac{x}{y})$
   + 而`\left(\frac{x}{y}\right)`显示为$\left(\frac{x}{y}\right)$
#### 求和、极限与积分
+ 求和：`sum`
   + 举例：`\sum_{i=1}^n{a_i}`显示为$\sum_{i=1}^n{a_i}$
+ 极限：`\to`
   +举例： `\lim_{x\to 0}`显示为$\lim_{x\to 0}$
+ 积分：`\int`
   + 举例：`\int_0^\infty{f(x)dx}`显示为$\int_0^\infty{f(x)dx}$
#### 分式和根式
+ 分式（fractions）:`frac{公式1}{公式2}`显示为$frac{公式1}{公式2}$
+ 根式：`\sqrt[x]{y+2}`显示为$\sqrt[x]{y+2}$
#### 特殊函数
+ `\函数名`
+ 举例：`\sin x`,`\ln x`,`\max(A,B,C)`显示为$\sin x，\ln x，\max(A,B,C)$
#### 特殊符号

显示|命令
:-:|:-:
$\infty$|\infty
$\cup$|\cup
$\cap$|\cap


#### 空格
+ LaTeX语法本身会忽略空格的存在
+ 小空格：`a\ b`显示为$a\ b$
+ 4格空格：`a\quad b`显示为$a\quad b$

### 矩阵
#### 基本语法
#### 矩阵边框
#### 省略元素
#### 阵列
#### 方程组


## 流程图


```flow
st=>start: 开始
op=>operation: 操作
cond=>condition: 是或否?
e=>end: 结束
st->op->cond
cond(yes)->e
cond(no)->op
```