---
title: Large-Scale Image Retrieval with Attentive Deep Local Features
date: 2020-07-3 15:28:12
tags:
 - 论文翻译
 - 随笔
typora-root-url: ..
typora-copy-images-to: ..\img
---

## 注意力深层局部特征的大规模图像检索

### 摘要

提出了一种适合于大规模图像检索的局部特征描述器，称为Deep-local-feature。新的特征是基于卷积神经网络，它只在地标图像数据集上使用图像级注释进行训练。为了识别在**语义上有用的图像检索局部特征**，我们还提出了一种用于关键点选择的**注意机制**，该机制**与描述符共享大部分网络层**。该框架可用于图像检索，作为其他**关键点检测器和描述符**的替代品，实现更精确的特征匹配和几何匹配验证。我们的系统产生可信的分数拒绝误报(FP)，尤其是它的健壮性针对数据库中没有正确匹配的查询。为了评估所提出的描述符，我们引入了一个新的大规模数据集，被称为谷歌地标(GLD)数据集，包括数据库和 查询搜索作为背景杂波，部分遮挡，多个地标、可变尺度的物体等DELF的成绩超过了全球和当地最先进的水平(SOTA)在大范围数据集中的描述符。可在以下网页找到项目代码：https://github.com/tensorflow/models/tree/master/research/delf。

<!--more-->

### 1. 介绍

大规模图像检索是计算机视觉中的一项基本任务，它直接关系到目标检测、视觉位置识别、产品识别等各种实际应用。在过去的几十年里，图像检索系统取得了巨大的进步，从手工制作的特征和索引算法[22,33,27,16]到最近的基于卷积神经网络（CNNs）的全局描述符学习方法[2,29,11]。

尽管基于CNN的全局描述符在中小型数据集中的图像检索方面取得了最新进展[27,28]，但在大规模数据集中观察到的各种具有挑战性的条件（如杂波<背景杂波>、遮挡和视点和照明的变化）可能会阻碍其性能。全局描述符缺乏在图像之间查找补丁级别匹配的能力。因此，在存在遮挡和背景杂波的情况下，基于部分匹配的图像检索非常困难。在最近的一个趋势中，基于CNN的局部特征被提出用于斑块级匹配[12,42,40]。然而，这些技术并没有特别针对图像检索进行优化，因为它们缺乏检测语义上有意义的特征的能力，并且在实际应用中显示出有限的准确性。

大多数现有的图像检索算法都是在**查询图像**较少的中小型数据集中进行评估的，即[27,28]中只有55张和[16]中只有500张，并且数据集中的图像在地标位置和类型方面的多样性有限。因此，我们认为，通过大规模的数据集来提高检索结果的综合性和有效性，可以使我们从中得到更具挑战性的大规模图像检索方法论。

本文的主要目标是开发一个基于CNN的特征描述子的大规模图像检索系统。为此，我们首先引入一个新的大规模数据集Google Landmarks(GLD)，它包含了来自近13K个独特地标的超过100万个地标图像。这个数据集覆盖了世界范围，因此比现有的数据集更加多样化和全面。查询集由额外的100K个具有各种特性的图像组成；特别是，我们在数据库中包含了不匹配(可能指数据库中不存在查询结果)的图像，这使得我们的数据集更具挑战性。这允许评估检索系统的健壮性通过查询不必要的地标描述。

然后，我们提出了一种基于CNN的有注意力机制的局部特征，它只使用图像级的类标签进行弱监督训练，而不需要对象级和补丁级的标注。这种新的特征描述符被称为DELF（Deep Local feature），图1说明了特征提取和图像检索的总体过程。在我们的方法中，注意力模型与所提取的描述符紧密耦合；它采用相同的CNN架构，并且只需很少的额外计算就可以生成特征分数（符合对象检测的最新进展[30]）。这使得本地描述符和关键点的提取都可以通过一个前向通道网络。结果表明，与基于全局和局部描述子的方法相比，基于DELF的图像检索系统具有更高的检索效率。

### 2. 相关工作

有标准的数据集通常用于评价图像检索技术。**Oxford5K**[27]有5062个在牛津拍摄的建筑图像，其中55个查询图像。**Paris6k**[28]由6412幅巴黎地标图片组成，也有55幅查询图片。这两个数据集通常使用来自Flickr100k数据集[27]的**Flickr100k**图像进行扩充，后者分别构建**Oxford105k**和**Paris106k**数据集。另一方面，**Holidays dataset**数据集[16]提供了1491张图片，包括500张查询图片，这些图片来自个人假日照片。这三个数据集都非常小，尤其是查询图像的数量非常少，这使得在这些数据集中测试的性能很难**通用化**。虽然**Pitts250k**[35]比较大，但它专门用于具有重复图案的视觉区域，可能不适合一般的图像检索任务。

实例检索是近十年来研究的热点问题。最近的调查见[43]。早期的系统依赖于手工制作的局部特征[22,5,8]，再加上使用**KD树**或**词汇树**的**近似最近邻搜索方法**[6,25]。时至今日，这种基于特征的技术与几何重排序相结合，在检索系统需要高精度操作时提供了强大的性能。

最近，许多研究集中在局部特征的聚集方法上(应该指使用局部描述符聚合成全局描述符)，其中包括一些流行的技术，如**VLAD**[18]和**Fisher Vector**（FV）[19]。这种全局描述符的主要优点是能够以紧凑的索引提供高性能的图像检索。

在过去的几年中，一些基于cnn的全局描述符被提出使用预先训练的[4,34]或学习网络[2,29,11]。为了保持相关图像和无关图像之间的排序，这些全局描述符最常用三元组损失进行训练。一些使用这些基于CNN的全局描述符的检索算法利用深度局部特征作为传统聚集技术（如VLAD或FV）中手工构建的特征的替代品[24,36]。其他的工作已经重新评估和提出了不同的特征聚合方法使用这些深的局部特征[3，21]。

CNN也被用来检测、表示和比较局部图像特征。Verdie等人[37]学习了**可重复关键点检测**的回归函数。Yi等人[41]提出了一种基于CNN的通用技术来估计局部特征的典型方向，并成功地将其应用到多个不同的描述符上。**MatchNet**[12]和**Deep Compare**[42]提出联合学习块表达和相关的指标。最近，LIFT[40]提出了一个端到端的框架来检测关键点、估计方向和计算描述符。与我们的工作不同的是，这些技术不是为图像检索应用而设计的，因为它们没有学习**选择语义上有意义的特征**。

许多视觉识别问题都采用了基于深层神经网络的视觉注意力，包括目标检测[45]、语义分割[14]、图像捕获[38]、视觉问题回答[39]等。然而，视觉注意力在图像检索应用中的学习视觉特征还没有被积极探索。

### 3. 谷歌地标数据集

我们的数据集是基于[44]中描述的算法构造的。与现有的用于图像检索的数据集[27,28,16]相比，新的数据集要大得多，包含多个地标，并且涉及大量挑战。它包含来自12894个地标的1 060 709个图像，以及111 036个其他查询图像。数据集中的图像被捕捉到世界上不同的位置，每个图像都与一个GPS坐标相关联。图2和图3分别示出了示例图像及其地理分布。虽然现有数据集中的大多数图像都是以地标为中心的，这使得全局特征描述子工作得很好，但是我们的数据集包含了更真实的图像，包括前景/背景杂波、遮挡、部分视野外的对象等。由于我们的查询图像是从个人照片库中收集的，其中一些可能不包含任何地标，因此不应该从数据库中检索任何图像。我们称这些查询图像为*distractors*分心器，它在评估算法对无关和噪声查询的鲁棒性方面起着至关重要的作用。

我们使用视觉特征和GPS坐标来构建 地面真相 。数据库中的所有图像都使用这两种信息进行聚类，并为每个簇分配一个地标标识符。如果查询图像的位置与与检索到的图像相关联的簇中心之间的物理距离小于阈值，我们假设这两个图像属于同一个地标。请注意，地面真实性注释非常具有挑战性，特别是考虑到很难预先定义什么是地标，地标有时不明显，并且在一个图像中可能有多个实例。显然，由于GPS误差的影响，这种地面真相构建方法存在噪声。另外，一些地标（如埃菲尔铁塔、金门大桥）的照片可以从很远的地方拍摄到，因此照片位置可能与实际地标位置相对较远。然而，在手工检查数据子集时，我们发现很少出现阈值为25km的错误注释。即使有很少的小错误，它也不成问题，特别是在相对评估中，因为算法不太可能在地标之间混淆，如果它们的视觉外观足够歧视的话。

### 4. 使用DELF图像检索

我们的大规模检索系统可以分解为四个主要模块：

（i）密集的局部特征提取；

（ii）关键点选择；

（iii）降维；

（iv）索引和检索。

这一部分详细介绍了DELF特征提取和学习算法以及我们的索引和检索过程。

#### 4.1 密集局部特征提取

我们采用一个完全卷积网络（FCN）从图像中提取密集特征，该网络是利用训练后的CNN的特征提取层构造的。我们使用一个取自ResNet50[13]模型的FCN，使用conv4x卷积块的输出。为了处理尺度的变化，我们显式地构造了一个图像金字塔，并对每个层次独立地应用FCN。将得到的特征映射视为局部描述子的密集网格。基于接收场对特征进行局部定位，可通过考虑FCN卷积层和池层的结构来计算特征。我们使用感受野中心的像素坐标作为特征定位。图像在原始尺度下的感受野大小为291×291。利用图像金字塔，我们得到了描述不同大小图像区域的特征。

我们使用在ImageNet[31]上训练的原始ResNet50模型作为基线，并对其进行微调，以增强我们的局部描述符的辨别力。由于我们考虑了一个地标识别应用，我们使用地标图像的注释数据集[4]，并使用**标准交叉熵损失**对网络进行训练，以便进行图像分类，如图4（a）所示。输入图像最初被中心裁剪以生成方形图像，然后重新缩放到250 x 250。然后随机使用224 x 224部分进行训练。作为训练的结果，局部描述符隐式学习与地标检索问题更相关的表示。以这种方式，对象级和补丁级的标签都不需要即可获得改进的局部描述符。

#### 4.2 基于注意力的关键点选择

与直接使用密集提取的特征进行图像检索不同，我们设计了一种有效地选择特征子集的技术。由于密集提取的特征中有相当一部分与我们的识别任务无关，并且可能会增加杂波(背景杂波)，分散检索过程的注意力，因此关键点的选择对于检索系统的准确性和计算效率都非常重要。

##### 4.2.1 弱监督学习

我们建议训练一个地标分类器来显式地测量局部特征描述子的相关性分数。为了训练函数，特征一个加权和池化，其中权重由注意力网络预测。培训程序与第4.1描述的损失函数和数据集相似，如图4（b）所示，其中注意力网络以黄色突出显示。这将生成整个输入图像的嵌入，然后用于训练基于softmax的地标分类器。

更确切地说，我们制定如下训练计划。用$f_n\in R^d, n=1,...,N$，这d维特征与注意模型联合学习。我们的目标是学习每个特征的得分函数$\alpha(f_n ;\theta )$，其中$\theta$表示函数$\alpha(\cdot)$的参数。网络的输出逻辑y由特征向量的加权和生成，该加权和由

(1)$$y=W(\sum_n\alpha(f_n;\theta)\cdot f_n)$$

式中$W\in R^{M\times d}$表示训练用于预测M类的CNN最终完全连接层的权重。

对于训练，我们使用交叉熵损失，它由

$$L=-y^* \cdot log(\frac{exp(y)}{1^T exp(y)})$$

式中$y^*$ 是one-hot之后的ground-truth向量，1是一向量[N维1向量]。分数函数$\alpha(\cdot)$中的参数通过反向传播进行训练，其中梯度由

$$\frac{\partial L}{\partial\theta}=\frac{\partial L}{\partial y}\sum_n \frac{\partial y}{\partial\alpha_n}\frac{\partial \alpha_n}{\partial\theta}=\frac{\partial L}{\partial y}\sum_n Wf_n \frac{\partial \alpha_n}{\partial\theta}$$

式中反向传播的输出分数 $\alpha_n==\alpha(f_n;\theta)$相对于$\theta$与标准多层感知器相同。

我们将$\alpha(\cdot )$限制为非负，以防止它学习负权重。score函数使用2层CNN设计，顶部使用softplus[9]激活（限制为非负）。为了简单起见，我们采用了尺寸为1 x 1的卷积滤波器，这在实践中效果良好。一旦注意力模型被训练出来，就可以用来评估模型所提取特征的相关性。

##### 4.2.2 训练注意力

在该框架中，描述子和注意模型都是通过图像级标签进行隐式学习的。不幸的是，这给学习过程带来了一些挑战。当特征表示和分数函数可以通过反向传播联合训练时，我们发现这种方法在实际应用中产生了弱模型。因此，我们采用两步训练策略。首先，我们通过微调学习描述符，如第4.1节所述。在给定固定的描述子的情况下，学习得分函数。

另一个改进是在注意力训练过程中通过随机图像重缩放来实现的。这是直观的，因为注意力模型应该能够为不同尺度的特征生成有效的分数。在这种情况下，输入图像最初被中心裁剪以产生方形图像，然后重新缩放到900 x 900。然后随机抽取720 x 720个输出，最后用系数$\gamma<=1$随机缩放。

##### 4.2.3 特点

我们系统的一个非传统的方面是，关键点选择是在描述符提取之后进行的，这与现有的技术（例如SIFT[22]和LIFT[40]）不同，后者首先检测到关键点，然后再进行描述。传统的关键点检测器只根据关键点的低电平特性，在不同成像条件下对关键点进行重复检测。然而，对于像图像检索这样的高级识别任务，选择能够区分不同对象实例的关键点也是至关重要的。该流程通过训练一个在特征映射中编码高级语义的模型，以及学习如何为分类任务选择有区别的特征来达到这两个目的。这与最近提出的学习关键点检测器的技术（即LIFT[40]）相反，后者根据SIFT匹配收集训练数据。虽然我们的模型不受约束地学习姿势和视点的不变性，但它隐含地学习这样做，类似于基于CNN的图像分类技术。

#### 4.3 降维

我们降低所选特征的维数以提高检索精度，这是常见的做法[15]。首先，对选取的特征进行L2标准化，通过PCA将其维数降到40，在紧凑性和区分性之间取得了很好的折衷。最后，这些特征再次经过L2标准化。

#### 4.4 图片检索系统

我们从查询图像和数据库图像中提取特征描述子，从中选择每个图像中具有**最高关注分数**的预定义数量的局部特征。我们的图像检索系统是基于**最近邻搜索**的，它是由**KD树**[7]和**乘积量化**（PQ）[17]相结合来实现的。我们使用PQ将每个描述子编码成50位编码，每个40D特征描述子被分成10个子向量，每个子向量用k均值聚类法识别25个聚类中心，实现50位编码。我们执行非对称距离计算，其中查询描述符不进行编码，以提高最近邻检索的准确性。为了加快最近邻搜索的速度，我们使用8K码本构造了一个描述符的倒排索引，为了减少编码错误，我们使用KD树对每个Voronoi(类似VLAD的聚类中心范围)单元进行划分，并对每个特征小于30K的子树使用局部优化的乘积量化器[20]。

当给定一个查询时，我们对从查询图像中提取的每个局部描述符执行近似近邻搜索。然后，对于从索引中检索到的前K个最近的局部描述符，我们将每个数据库图片的所有匹配项集合起来。最后，我们使用**RANSAC**[10]进行几何验证，并使用inliner(样本点)的数量作为检索图像的分数。这个几何验证步骤拒绝了许多分心器查询，因为分心器的特征可能与地标图像的特征不一致。

这个流程索引10亿个描述符需要的内存少于8GB，这足以处理我们的大型地标数据集。在我们的实验设置下，使用单个CPU，最近邻搜索的延迟小于2秒，我们在每个查询中软分配5个聚类中心，并在每个倒排索引树中搜索多达10K个叶节点。

### 5 实验

本节主要讨论与我们数据集中现有的全局和局部特征描述符相比，DELF的性能。此外，我们还展示了如何使用DELF在现有数据集中获得良好的精度。

#### 5.1 实施细节

**多尺度描述子提取**  我们使用相距$\sqrt2$倍的尺度来构造图像金字塔。对于范围从0.25到2.0的一组比例尺，使用7种不同的比例尺。感受野的大小与尺度成反比；例如，对于2.0尺度，网络的感受野覆盖146 x 146像素。

**训练**  我们使用landmarks数据集[4]来微调描述符和训练关键点选择。在数据集中，有“完整”版本，称为LF（在删除了Oxf5k / Par6k的重叠类之后，通过[11]），包含586个地标的140372个图像，以及通过基于SIFT的匹配过程[11]获得的“干净”版本(LC)，包含586个地标的35382个图像。我们使用LF训练我们的注意模型，并使用LC对图像检索的网络进行微调。

**参数**  我们为一个查询中的每个特征确定最接近的K（=60）个近邻，并从每个图像中提取多达1000个局部特征，每个特征是40维的。

#### 5.2 算法比较

DELF与最近的几个全局和局部描述符进行了比较。虽然有各种与图像检索相关的研究成果，但我们相信以下方法要么与我们的算法相关，要么由于其良好的性能而对评估至关重要。

**深度图像检索(DIR)**  这是一个最新的全局描述符，它在多个现有数据集中达到了最先进的性能。DIR特征描述符为2048维，所有情况下都使用多分辨率描述符。我们还使用查询扩展（QE）进行评估，这通常可以提高标准数据集的准确性。我们使用发布的源代码来实现ResNet101[13]版本。在检索方面，采用了暴力搜索的并行实现，避免了近似近邻搜索的错误造成的惩罚。

**siaMAC**  这是一个最新的全局描述符，可以在现有数据集中获得高性能。我们使用发布的源代码与暴力搜索的并行实现。基于VGG16[32]的CNN提取512维全局描述子。我们还对DIR中的查询扩展（QE）进行了实验。

**CONGAS**  CONGAS是一个40D的手工构建的局部特征，已被广泛应用于实例级图像匹配和检索[1,44]。该特征描述子是通过在检测到的关键点的尺度和方向上采集Gabor小波响应来提取的，并且与SIFT等基于梯度的局部描述子具有非常相似的性能和特性。采用拉普拉斯高斯关键点检测器

**LIFT**  LIFT[40]是最近提出的一种特征匹配流程，它将关键点检测、方向估计和关键点描述结合起来学习。特征是128维的。我们使用公开的源代码。

#### 5.3 评估

图像检索系统通常是基于平均平均精度（mAP）来评估的，平均平均精度是通过按每个查询的相关性降序对图像进行排序并平均每个查询的AP来计算的。然而，对于带有干扰查询的数据集，这种评估方法并不具有代表性，因为确定每个图像是否与查询相关很重要。在我们的例子中，使用绝对检索分数来估计每个图像的相关性。对于性能评估，我们使用了一个改进版本的精度（PRE）和召回（REC），方法是同时考虑所有查询图像，由

$$P_{RE}=\frac{|R_q^{TP}|}{|R_q|} 和 R_{EC}=\sum_q |R_q^{TP}|$$

式中$R_q$表示给定阈值的查询q的一组检索图像，$R_q^{TP}(\subseteq R_q)$是一组真正类。这与[26]中引入的micro-AP指标类似。请注意，在我们的例子中，在最终评分中只考虑每个地标的最高得分图像。我们更喜欢非标准化的回调值，它表示检索到的真阳性数。

#### 5.4 定量结果

图5显示了与其他方法相比，DELF（用DELF+FT+ATT表示）的精确召回曲线。由于特征提取速度非常慢，无法进行大规模实验，因此无法显示LIFT的结果。DELF明显优于所有其他技术。全局特征描述符，比如DIR，在我们富有挑战性的数据集中受到了影响。特别是，由于查询集中存在大量干扰因素，使用QE的DIR会显著降低准确性。CONGAS做得相当不错，但仍然比DELF差很多。

为了分析精细调整和注意力对图像检索的好处，我们比较了我们的完整模型（DELF+FT+ATT）及其变体：DELF-noFT、DELF+FT和DELFnoFT+ATT。DELF-noFT是指提取的特征基于ImageNet上预训练的CNN，而不需要精细调整和注意力学习。DELF+FT表示有微调但没有注意建模的模型，DELFnoFT+ATT对应于未经微调但使用注意力的模型。如图5所示，微调和注意力建模都对性能改进做出了重大贡献。特别要注意的是，注意力的使用比微调更重要。这表明，所提出的注意层可以有效地学习为检索任务选择最有区别的特征，即使这些特征只是在ImageNet上预先训练过的。

在内存需求方面，DELF、CONGAS和DIR几乎同样复杂。DELF和CONGAS采用相同的特征维数和每个图像的最大特征数；它们需要大约8GB的内存。DIR描述符需要每个图像8KB，加起来大约8GB来索引整个数据集。

#### 5.5 定量结果

我们给出定性的结果来说明DELF与两种基于全局和局部特征的竞争算法DIR和CONGAS的性能比较。同时，通过可视化分析了基于注意力的关键点检测算法。

**DELF vs. DIR** 图6显示了检索结果，其中DELF的性能优于DIR。DELF得到图像中特定局部区域之间的匹配，这对于在不同成像条件下找到同一目标具有重要意义。DIR的常见故障案例发生在数据库包含类似的对象或场景时，例如方尖碑、山脉、港口，如图6所示。在许多情况下，DIR无法区分这些特定的对象或场景；尽管它发现语义上相似的图像，但它们通常与感兴趣的实例不对应。DIR和其他全局描述符的另一个缺点是它们不善于识别感兴趣的小对象。图7显示了DIR优于DELF的情况。虽然DELF能够在不同的图像上匹配局部模式，但当不同地标的地板砖或植被相似时，这会导致错误。

**DELF vs. CONGAS**  与CONGAS相比，DELF的主要优势在于它的召回率；它比CONGAS检索到更多相关的地标，这表明DELF描述符更具辨别力。我们没有观察到CONGAS优于DELF的显著例子。图8显示了来自查询和数据库的成对图像，这些图像通过DELF成功匹配，但被CONGAS忽略，其中特征对应通过连接用于匹配特征的接收字段的中心来呈现。由于感受野可能相当大，一些特征似乎局限于无差别的区域，例如海洋或天空。然而，在这些情况下，这些特征会考虑到邻近区域中更具歧视性的区域。

**关键点检测方法分析**  图9显示了关键点检测的三种变化，其中我们的注意模型的好处被清楚地定性地说明，而微调特征的L2范数与未经微调的L2范数略有不同。

#### 5.6 现有数据集中的结果

为了完整性，我们展示了DELF在现有数据集中的性能，比如Oxf5k、Par6k及其扩展Oxf105k和Par106k。对于这个实验，我们简单地使用所提出的方法来获得每幅图像的分数，并通过计算两个标准化分数的加权平均值来与DIR的分数进行后期融合，其中DELF的权重设置为0.25。结果显示在表1中，我们提出了现有方法的准确性在他们的原始论文和我们的复制使用公共源代码，这是非常接近。当与DIR结合使用时，DELF显著地提高了数据集中的准确性，尽管它本身并没有显示出最好的性能。这一事实表明，DELF能够对全局特征描述符中不可用的补充信息进行编码。

### 6 结论

本文提出了一种新的局部特征描述子DELF，它是专门为大规模图像检索应用而设计的。DELF是在弱监督下学习的，只使用图像级别的标签，并与我们的新的注意机制的语义特征选择相结合。在所提出的基于CNN的模型中，一次前向传递就足以获得关键点和描述符。为了正确评估大规模图像检索算法的性能，我们引入了Google Landmarks数据集，该数据集由超过1M个数据库图像、13K个唯一路标和100K个查询图像组成。在这样一个大规模的环境下的评估表明，DELF的性能远远超过现有的全局和局部描述符。在已有的数据集上，我们也给出了结果，并表明当与全局描述符相结合时，DELF具有良好的性能。