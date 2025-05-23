---
title: Mask2Former: Masked-attention Mask Transformer for Universal Image Segmentation
date: 2024-12-5 11:00:00
toc: true
tags:
 - 论文翻译
 - Mask2Former
 - AI
 - Segmentation
typora-root-url: ..
typora-copy-images-to: ..\img\mask2former
---



## 摘要



图像分割将具有不同语义（如类别或实例成员关系）的像素分组，每种语义选择定义了一项任务。虽然各项任务仅在语义上有所不同，但当前研究主要集中于为每个任务设计专门的架构。我们提出了掩码注意力掩码变换器（Mask2Former），这是一种能够处理任何图像分割任务（全景、实例或语义）的新架构。其关键组件包括掩码注意力，它通过将交叉注意力约束在预测掩码区域内来提取局部特征。除了将研究工作量至少减少三倍外，它在四个流行数据集上显著优于最佳专用架构。最值得注意的是，Mask2Former 在全景分割（COCO 上的 57.8 PQ）、实例分割（COCO 上的 50.1 AP）和语义分割（ADE20K 上的 57.7 mIoU）方面设定了新的最先进水平。

<!--more-->

## 1. 引言



图像分割研究像素分组问题。像素分组的不同语义，例如类别或实例成员关系，导致了不同类型的分割任务，如全景、实例或语义分割。虽然这些任务仅在语义上有所不同，但当前方法为每个任务开发专门的架构。基于全卷积网络（FCN）的逐像素分类架构用于语义分割，而预测一组与单个类别相关联的二进制掩码的掩码分类架构在实例级分割中占主导地位。尽管这些专门架构推动了各个任务的发展，但它们缺乏推广到其他任务的灵活性。例如，基于 FCN 的架构在实例分割方面表现不佳，导致与语义分割相比，实例分割发展出了不同的架构。因此，在每个任务的每个专门架构上都花费了重复的研究和（硬件）优化工作。



为了解决这种碎片化问题，近期的工作尝试设计通用架构，能够使用相同架构处理所有分割任务（即通用图像分割）。这些架构通常基于端到端的集合预测目标（如 DETR），并且在不修改架构、损失或训练过程的情况下成功处理多个任务。请注意，通用架构仍然针对不同任务和数据集分别进行训练，尽管它们具有相同的架构。除了灵活性之外，通用架构最近在语义和全景分割方面也取得了最先进的成果。然而，近期的工作仍然侧重于推进专用架构，这就提出了一个问题：为什么通用架构没有取代专用架构呢？



尽管现有通用架构足够灵活，可以处理任何分割任务，但如图 1 所示，在实践中它们的性能落后于最佳专用架构。例如，通用架构的最佳报告性能目前比实例分割的 SOTA 专用架构低（> 9 AP）。除了性能较差之外，通用架构也更难训练。它们通常需要更先进的硬件和更长的训练计划。例如，训练 MaskFormer 需要 300 个 epoch 才能达到 40.1 AP，并且在具有 32G 内存的 GPU 中只能容纳单张图像。相比之下，专用的 Swin - HTC++ 仅在 72 个 epoch 内就能获得更好的性能。性能和训练效率问题都阻碍了通用架构的部署。



在这项工作中，我们提出了一种名为掩码注意力掩码变换器（Mask2Former）的通用图像分割架构，它在不同分割任务上优于专用架构，同时在每个任务上仍然易于训练。我们基于一个简单的元架构构建，该架构由骨干特征提取器、像素解码器和 Transformer 解码器组成。我们提出了关键改进，以实现更好的结果和高效训练。首先，我们在 Transformer 解码器中使用掩码注意力，它将注意力限制在以预测片段为中心的局部特征上，这些片段可以根据分组的特定语义是对象或区域。与标准 Transformer 解码器中关注图像中所有位置的交叉注意力相比，我们的掩码注意力导致更快的收敛和改进的性能。其次，我们使用多尺度高分辨率特征，这有助于模型分割小对象 / 区域。第三，我们提出优化改进，例如切换自注意力和交叉注意力的顺序，使查询特征可学习，并去除丢弃法；所有这些都在不增加计算量的情况下提高了性能。最后，我们通过在少量随机采样点上计算掩码损失，在不影响性能的情况下节省了 3 倍的训练内存。这些改进不仅提高了模型性能，还使训练变得更加容易，使计算资源有限的用户更容易使用通用架构。



我们在三个图像分割任务（全景、实例和语义分割）上使用四个流行数据集（COCO、Cityscapes、ADE20K 和 Mapillary Vistas）评估 Mask2Former。首次在所有这些基准测试中，我们的单一架构在性能上与专用架构相当或更好。Mask2Former 在 COCO 全景分割上使用完全相同的架构达到了 57.8 PQ 的新最先进水平，在 COCO 实例分割上达到了 50.1 AP，在 ADE20K 语义分割上达到了 57.7 mIoU。



通用架构随着 DETR 的出现而兴起，并表明具有端到端集合预测目标的掩码分类架构对于任何图像分割任务都足够通用。MaskFormer 表明基于 DETR 的掩码分类不仅在全景分割上表现良好，而且在语义分割上也达到了最先进水平。K - Net 进一步将集合预测扩展到实例分割。不幸的是，这些架构未能取代专用模型，因为它们在特定任务或数据集上的性能仍然比最佳专用架构差（例如，MaskFormer 不能很好地分割实例）。据我们所知，Mask2Former 是第一个在所有考虑的任务和数据集上优于最先进专用架构的架构。

### 图 1. 最先进的分割架构通常专门针对每个图像分割任务。尽管最近的工作提出了尝试所有任务并在语义和全景分割上具有竞争力的通用架构，但它们在分割实例方面存在困难。我们提出了 Mask2Former，它首次在多个数据集的三个研究分割任务上优于最佳专用架构。

### 1.1 研究现状



专门的语义分割架构通常将任务视为逐像素分类问题。基于 FCN 的架构独立地为每个像素预测类别标签。后续方法发现上下文对于精确的逐像素分类起着重要作用，并专注于设计定制的上下文模块或自注意力变体。专门的实例分割架构通常基于 “掩码分类”。它们预测一组与单个类别标签相关联的二进制掩码。开创性的工作 Mask R - CNN 从检测到的边界框生成掩码。后续方法要么专注于检测更精确的边界框，要么寻找生成动态数量掩码的新方法，例如使用动态核或聚类算法。尽管在每个任务中的性能都有所提高，但这些专门的创新缺乏从一个任务推广到另一个任务的灵活性，导致重复的研究工作。例如，尽管已经提出了多种构建特征金字塔表示的方法，但正如我们在实验中所示，BiFPN 在实例分割方面表现更好，而 FaPN 在语义分割方面表现更好。全景分割被提出以统一语义和实例分割任务。全景分割架构要么将专门的语义和实例分割架构的最佳部分组合成一个单一框架，要么设计平等对待语义区域和实例对象的新目标。尽管有这些新架构，研究人员仍在继续为不同的图像分割任务开发专门的架构。我们发现全景架构通常只报告在单个全景分割任务上的性能，这不能保证在其他任务上的良好性能（图 1）。例如，全景分割不测量架构对实例分割预测进行排名的能力。因此，我们避免将仅针对全景分割进行评估的架构称为通用架构。相反，在这里，我们在所有研究任务上评估我们的 Mask2Former，以保证其通用性。

## 2. 掩码注意力掩码变换器



我们现在介绍 Mask2Former。我们首先回顾 Mask2Former 所基于的掩码分类元架构。然后，我们介绍我们带有掩码注意力的新 Transformer 解码器，这是实现更好收敛和结果的关键。最后，我们提出训练改进措施，使 Mask2Former 高效且易于使用。

### 2.1 掩码分类基础



掩码分类架构通过预测 N 个二进制掩码以及 N 个相应的类别标签将像素分组为 N 个片段。掩码分类通过为不同片段分配不同语义（例如类别或实例），足以处理任何分割任务。然而，挑战在于为每个片段找到良好的表示。例如，Mask RCNN 使用边界框作为表示，这限制了其在语义分割中的应用。受 DETR 启发，图像中的每个片段可以表示为一个 c 维特征向量（“对象查询”），并可以由 Transformer 解码器处理，通过集合预测目标进行训练。一个简单的元架构将由三个组件组成。一个骨干网络，从图像中提取低分辨率特征。一个像素解码器，将骨干网络输出的低分辨率特征逐步上采样，以生成高分辨率的逐像素嵌入。最后一个 Transformer 解码器，对图像特征进行操作以处理对象查询。最终的二进制掩码预测从带有对象查询的逐像素嵌入中解码得到。这种元架构的一个成功实例是 MaskFormer，我们建议读者参考 [14] 以获取更多详细信息。

### 2.2 带掩码注意力的 Transformer 解码器



Mask2Former 采用上述元架构，用我们提出的 Transformer 解码器（图 2 右侧）取代标准的 Transformer 解码器。我们的 Transformer 解码器的关键组件包括一个掩码注意力算子，它通过将交叉注意力约束在每个查询的预测掩码的前景区域内来提取局部特征，而不是关注整个特征图。为了处理小对象，我们提出一种有效的多尺度策略来利用高分辨率特征。它以循环方式将像素解码器的特征金字塔中的连续特征图输入到连续的 Transformer 解码器层中。最后，我们纳入优化改进措施，在不引入额外计算的情况下提高模型性能。我们现在详细讨论这些改进。

#### 图 2. Mask2Former 概述。Mask2Former 采用与 MaskFormer 相同的元架构，包括骨干网络、像素解码器和 Transformer 解码器。我们提出一种带有掩码注意力的新 Transformer 解码器，而不是标准的交叉注意力（3.2.1 节）。为了处理小对象，我们提出一种有效的方法，通过每次将多尺度特征的一个尺度输入到一个 Transformer 解码器层来利用像素解码器的高分辨率特征（3.2.2 节）。此外，我们切换自注意力和交叉注意力的顺序（即我们的掩码注意力），使查询特征可学习，并去除丢弃法以使计算更有效（3.2.3 节）。请注意，为了清晰起见，此图中省略了位置嵌入和来自中间 Transformer 解码器层的预测。

#### 2.2.1 掩码注意力



上下文特征已被证明对图像分割很重要。然而，最近的研究表明，基于 Transformer 的模型收敛缓慢是由于交叉注意力层中的全局上下文，因为交叉注意力需要许多训练 epoch 才能学会关注局部对象区域。我们假设局部特征足以更新查询特征，并且上下文信息可以通过自注意力收集。为此，我们提出掩码注意力，这是交叉注意力的一种变体，它仅关注每个查询的预测掩码的前景区域内。



标准交叉注意力（带有残差路径）计算：。这里， 是层索引， 指的是第 层的 个 维查询特征，。 表示输入到 Transformer 解码器的查询特征。， 是分别在变换 和 下的图像特征， 和 是我们将在 3.2.2 节中介绍的图像特征的空间分辨率。， 和 是线性变换。



我们的掩码注意力通过以下方式调制注意力矩阵：。此外，特征位置 处的注意力掩码 为：。这里， 是前一个（）Transformer 解码器层的调整大小后的掩码预测的二值化输出（阈值为 0.5）。它被调整为与 相同的分辨率。 是从 获得的二进制掩码预测，即在将查询特征输入到 Transformer 解码器之前。

#### 2.2.2 高分辨率特征



高分辨率特征可提高模型性能，特别是对于小对象。然而，这在计算上要求很高。因此，我们提出一种有效的多尺度策略，在控制计算量增加的同时引入高分辨率特征。我们不是始终使用高分辨率特征图，而是利用由低分辨率和高分辨率特征组成的特征金字塔，并一次将多尺度特征的一个分辨率输入到一个 Transformer 解码器层。



具体来说，我们使用像素解码器生成的分辨率为原始图像的 1/32、1/16 和 1/8 的特征金字塔。对于每个分辨率，我们添加一个正弦位置嵌入 （遵循 [5]）和一个可学习的尺度级别嵌入 （遵循 [66]）。我们按照从最低分辨率到最高分辨率的顺序将它们用于相应的 Transformer 解码器层，如图 2 左侧所示。我们重复这个 3 层 Transformer 解码器 次。因此，我们最终的 Transformer 解码器有 层。更具体地说，前三层接收分辨率为 ，， 和 ，， 的特征图，其中 和 是原始图像分辨率。这个模式以循环方式对所有后续层重复。

#### 2.2.3 优化改进



标准 Transformer 解码器层由三个模块组成，按以下顺序处理查询特征：自注意力模块、交叉注意力模块和前馈网络（FFN）。此外，查询特征 在输入到 Transformer 解码器之前被零初始化，并与可学习的位置嵌入相关联。此外，在残差连接和注意力图上都应用了丢弃法。



为了优化 Transformer 解码器设计，我们进行了以下三项改进。首先，我们切换自注意力和交叉注意力（我们新的 “掩码注意力”）的顺序，以使计算更有效：输入到第一个自注意力层的查询特征与图像无关，并且没有来自图像的信号，因此应用自注意力不太可能丰富信息。其次，我们也使查询特征 可学习（我们仍然保留可学习的查询位置嵌入），并且可学习的查询特征在用于 Transformer 解码器预测掩码 之前直接受到监督。我们发现这些可学习的查询特征的功能类似于区域提议网络，并且具有生成掩码提议的能力。最后，我们发现丢弃法不是必需的，并且通常会降低性能。因此，我们在解码器中完全去除了丢弃法。

### 2.3 提高训练效率



训练通用架构的一个限制是由于高分辨率掩码预测导致的大内存消耗，这使得它们比更节省内存的专用架构更难使用。例如，MaskFormer 在具有 32G 内存的 GPU 中只能容纳单张图像。受 PointRend 和 Implicit PointRend 的启发，它们表明可以通过在 个随机采样点上计算掩码损失而不是在整个掩码上计算来训练分割模型，我们在匹配和最终损失计算中都使用采样点计算掩码损失。更具体地说，在构建二分匹配成本矩阵的匹配损失中，我们为所有预测掩码和真实掩码统一采样相同的 个点集。在预测与匹配的真实掩码之间的最终损失中，我们使用重要性采样为不同的预测掩码和真实掩码对采样不同的 个点集。我们设置 ，即 112×112 个点。这种新的训练策略有效地将训练内存减少了 3 倍，从每张图像 18GB 减少到 6GB，使 Mask2Former 对于计算资源有限的用户更容易使用。

## 3. 实验



我们通过在标准基准上与专用的最先进架构进行比较，证明 Mask2Former 是通用图像分割的有效架构。我们通过在所有三个任务上进行消融实验来评估我们提出的设计决策。最后，我们表明 Mask2Former 可以推广到标准基准之外，在四个数据集上获得最先进的结果。

### 3.1 数据集



我们使用四个广泛使用的支持语义、实例和全景分割的图像分割数据集来研究 Mask2Former：COCO（80 个 “事物” 和 53 个 “物品” 类别）、ADE20K（100 个 “事物” 和 50 个 “物品” 类别）、Cityscapes（8 个 “事物” 和 11 个 “物品” 类别）和 Mapillary Vistas（37 个 “事物” 和 28 个 “物品” 类别）。全景和语义分割任务在 “事物” 和 “物品” 类别的并集上进行评估，而实例分割仅在 “事物” 类别上进行评估。