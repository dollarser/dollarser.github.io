---
title: YOLOV8代码阅读
date: 2024-05-22 20:00:00
tags:
 - python
 - 深度学习
typora-root-url: ..
typora-copy-images-to: ../img/python
---

# YOLOV8代码阅读



<!--more-->



## YOLO 训练参数

官网地址：[训练参数](https://docs.ultralytics.com/modes/train/#train-settings)

| Argument      | Default | Description                                                  |
| :------------ | :------ | :----------------------------------------------------------- |
| model         | None    | Specifies the model file for training. Accepts a path to either a .pt pretrained model or a .yaml configuration file. Essential for defining the model structure or initializing weights. |
| data          | None    | Path to the dataset configuration file (e.g., coco8.yaml). This file contains dataset-specific parameters, including paths to training and validation data, class names, and number of classes. |
| epochs        | 100     | Total number of training epochs. Each epoch represents a full pass over the entire dataset. Adjusting this value can affect training duration and model performance. |
| time          | None    | Maximum training time in hours. If set, this overrides the epochs argument, allowing training to automatically stop after the specified duration. Useful for time-constrained training scenarios. |
| patience      | 100     | Number of epochs to wait without improvement in validation metrics before early stopping the training. Helps prevent overfitting by stopping training when performance plateaus. |
| batch         | 16      | Batch size, with three modes: set as an integer (e.g., batch=16), auto mode for 60% GPU memory utilization (batch=-1), or auto mode with specified utilization fraction (batch=0.70). |
| imgsz         | 640     | Target image size for training. All images are resized to this dimension before being fed into the model. Affects model accuracy and computational complexity. |
| save          | True    | Enables saving of training checkpoints and final model weights. Useful for resuming training or model deployment. |
| save_period   | -1      | Frequency of saving model checkpoints, specified in epochs. A value of -1 disables this feature. Useful for saving interim models during long training sessions. |
| cache         | False   | Enables caching of dataset images in memory (True/ram), on disk (disk), or disables it (False). Improves training speed by reducing disk I/O at the cost of increased memory usage. |
| device        | None    | Specifies the computational device(s) for training: a single GPU (device=0), multiple GPUs (device=0,1), CPU (device=cpu), or MPS for Apple silicon (device=mps). |
| workers       | 8       | Number of worker threads for data loading (per RANK if Multi-GPU training). Influences the speed of data preprocessing and feeding into the model, especially useful in multi-GPU setups. |
| project       | None    | Name of the project directory where training outputs are saved. Allows for organized storage of different experiments. |
| name          | None    | Name of the training run. Used for creating a subdirectory within the project folder, where training logs and outputs are stored. |
| exist_ok      | False   | If True, allows overwriting of an existing project/name directory. Useful for iterative experimentation without needing to manually clear previous outputs. |
| pretrained    | True    | Determines whether to start training from a pretrained model. Can be a boolean value or a string path to a specific model from which to load weights. Enhances training efficiency and model performance. |
| optimizer     | ‘auto’  | Choice of optimizer for training. Options include SGD, Adam, AdamW, NAdam, RAdam, RMSProp etc., or auto for automatic selection based on model configuration. Affects convergence speed and stability. |
| seed          | 0       | Sets the random seed for training, ensuring reproducibility of results across runs with the same configurations. |
| deterministic | True    | Forces deterministic algorithm use, ensuring reproducibility but may affect performance and speed due to the restriction on non-deterministic algorithms. |
| single_cls    | False   | Treats all classes in multi-class datasets as a single class during training. Useful for binary classification tasks or when focusing on object presence rather than classification. |
| rect          | False   | Enables rectangular training, optimizing batch composition for minimal padding. Can improve efficiency and speed but may affect model accuracy. |
| cos_lr        | False   | Utilizes a cosine learning rate scheduler, adjusting the learning rate following a cosine curve over epochs. Helps in managing learning rate for better convergence. |
| close_mosaic  | 10      | Disables mosaic data augmentation in the last N epochs to stabilize training before completion. Setting to 0 disables this feature. |
| resume        | False   | Resumes training from the last saved checkpoint. Automatically loads model weights, optimizer state, and epoch count, continuing training seamlessly. |
| amp           | True    | Enables Automatic Mixed Precision (AMP) training, reducing memory usage and possibly speeding up training with minimal impact on accuracy. |
| fraction        | 1.0     | 指定用于训练的数据集的比例。允许在完整数据集的子集上进行训练，在资源有限或进行实验时非常有用。 |
| profile         | False   | 启用ONNX和TensorRT在训练期间的速率分析，有助于优化模型部署。 |
| freeze          | None    | 冻结模型的前N层或通过索引指定的层，减少可训练参数的数量。对于微调或迁移学习非常有用。 |
| lr0             | 0.01    | 初始学习率（例如，SGD=1E-2，Adam=1E-3）。调整这个值对于优化过程至关重要，影响模型权重的更新速度。 |
| lrf             | 0.01    | 最终学习率作为初始率的分数 =（lr0 * lrf），与调度器结合使用，随着时间的推移调整学习率。 |
| momentum        | 0.937   | SGD或Adam优化器的动量因子，影响当前更新中过去梯度的融合。    |
| weight_decay    | 0.0005  | L2正则化项，惩罚大权重以防止过拟合。                         |
| warmup_epochs   | 3.0     | 学习率热身期的周期数，从低值逐渐增加到初始学习率，以在训练初期稳定训练。 |
| warmup_momentum | 0.8     | 热身阶段的初始动量，逐渐调整到设定的动量。                   |
| warmup_bias_lr  | 0.1     | 热身阶段偏置参数的学习率，帮助在初始周期稳定模型训练。       |
| box             | 7.5     | 损失函数中框损失组件的权重，影响准确预测边界框坐标的重视程度。 |
| cls             | 0.5     | 总损失函数中分类损失的权重，影响正确类别预测相对于其他组件的重要性。 |
| dfl             | 1.5     | 分布焦点损失的权重，用于某些YOLO版本进行细粒度分类。         |
| pose            | 12.0    | 在用于姿态估计的模型中姿态损失的权重，影响准确预测姿态关键点的重视程度。 |
| kobj            | 2.0     | 姿态估计模型中关键点目标性损失的权重，平衡检测置信度与姿态准确性。 |
| label_smoothing | 0.0     | 应用标签平滑，将硬标签软化为目标标签和均匀分布标签的混合，可以提高泛化能力。 |
| nbs             | 64      | 用于损失标准化的名义批量大小。                               |
| overlap_mask    | True    | 确定是否应该将对象掩码合并为单个掩码进行训练，或者为每个对象保持单独的掩码。在重叠的情况下，较小的掩码在合并期间覆盖在较大的掩码之上。 |
| mask_ratio      | 4       | 分段掩码的下采样比率，影响训练期间使用的掩码的分辨率。       |
| dropout         | 0.0     | 分类任务中的正则化丢弃率，通过在训练期间随机省略单元来防止过拟合。 |
| val             | True    | 启用训练期间的验证，允许定期在独立数据集上评估模型性能。     |
| plots           | False   | 生成并保存训练和验证度量的图表以及预测示例，提供模型性能和学习进展的可视化洞察。 |



## YOLO 数据增强

官网地址：[数据增强参数](https://docs.ultralytics.com/modes/train/#augmentation-settings-and-hyperparameters)

| Argument   | Type    | Default | Range       | Description                                                                             |
|:-----------|:--------|:--------|:------------|:--------------------------------------------------------------------------------------------|
| hsv_h      | float   | 0.015   | 0.0 - 1.0   | 调整图像的色调，引入色彩变化。有助于模型在不同光照条件下泛化。               |
| hsv_s      | float   | 0.7     | 0.0 - 1.0   | 通过分数改变图像的饱和度，影响色彩强度。对于模拟不同环境条件有用。                           |
| hsv_v      | float   | 0.4     | 0.0 - 1.0   | 通过分数修改图像的明度（亮度），帮助模型在各种光照条件下表现良好。                            |
| degrees    | float   | 0.0     | -180 - +180 | 在指定的角度范围内随机旋转图像，提高模型识别不同方向物体的能力。                             |
| translate  | float   | 0.1     | 0.0 - 1.0   | 按照图像大小的分数水平和垂直平移图像，有助于学习检测部分可见的物体。                          |
| scale      | float   | 0.5     | >=0.0       | 通过增益因子缩放图像，模拟不同距离下的物体。                                                 |
| shear      | float   | 0.0     | -180 - +180 | 通过指定角度剪切图像，模仿从不同角度观察物体的效果。                                         |
| perspective| float   | 0.0     | 0.0 - 0.001 | 对图像应用随机透视变换，增强模型理解三维空间中物体的能力。                                    |
| flipud     | float   | 0.0     | 0.0 - 1.0   | 以指定概率上下翻转图像，增加数据多样性，不影响物体特征。                                     |
| fliplr     | float   | 0.5     | 0.0 - 1.0   | 以指定概率左右翻转图像，对于学习对称物体和增加数据集多样性有用。                              |
| bgr        | float   | 0.0     | 0.0 - 1.0   | 以指定概率将图像通道从RGB切换到BGR，对于增加对错误通道顺序的鲁棒性有用。                     |
| mosaic     | float   | 1.0     | 0.0 - 1.0   | 将四个训练图像组合成一个，模拟不同的场景构成和物体互动。对于复杂场景理解非常有效。            |
| mixup      | float   | 0.0     | 0.0 - 1.0   | 混合两个图像及其标签，创建复合图像。通过引入标签噪声和视觉变化，增强模型泛化能力。             |
| copy_paste | float   | 0.0     | 0.0 - 1.0   | 从一个图像复制物体并粘贴到另一个图像上，对于增加物体实例和学习物体遮挡有用。                 |
| auto_augment| str    | randaugment | - | 自动应用预定义的增强策略（randaugment, autoaugment, augmix），通过多样化视觉特征优化分类任务。 |
| erasing    | float   | 0.4     | 0.0 - 0.9   | 在分类训练期间随机擦除图像的一部分，鼓励模型关注于不太明显的特征以进行识别。                  |
| crop_fraction| float | 1.0     | 0.1 - 1.0   | 将分类图像裁剪为其大小的分数，强调中心特征，适应物体尺度，减少背景干扰。                    |