---
title: 'Robust Minutiae Extractor:Integrating Deep Networks and Fingerprint Domain Knowledge'
date: 2020-12-21 16:25:00
categories: 论文解读
tags: [论文, 深度学习, 指纹识别]
mathjax: true
---

[论文原文下载链接](https://cdn.jsdelivr.net/gh/stxws/stxws.github.io/documnets/papers/MinutiaeNet.pdf)

# Abstract（摘要）
&emsp;&emsp;提出了一个基于深度神经网络的全自动指纹细节点提取器。
* **CoarseNet**: 粗糙的网络，基于卷积神经网络和指纹领域知识，估计细节点位置和方向。
* **FineNet**: 精细的网络，基于细节点的分数热力图对候选细节点位置进一步优化。

&emsp;&emsp;由于缺乏基于细节点标注的指纹数据集，本文提出的细节点检测方法将有助于训练基于网络的指纹匹配算法。


# Introduction（介绍）
&emsp;&emsp;**传统方法**：主要利用指纹领域知识和手工特征提取细节点。在质量好的指纹图像上效果好，但是在质量差的指纹上效果不好，尤其是现场指纹。

&emsp;&emsp;**深度学习方法**：
* 利用滑动窗口等方式，生成细节点的候选块，然后用分类器判断是不是细节点。缺点是比较耗时。
* FingerNet：将传统的细节点提取方法(包括方向场、分割、增强和细节点提取)映射到一个固定权值的网络。结合了指纹的领域知识和深度学习，比较有前景，不过使用的网络结构比较普通，非极大值抑制用的是硬阈值。

**作者的贡献**：
1. 提出了一种基于网络的细节点自动提取器，利用领域知识提供可靠的细节点位置和方向，不需要调硬阈值。
2. 一个鲁棒的基于块的细节点分类器，显著提高了候选块精度和召回率。这可以作为一个鲁棒的，带有紧凑细节点特征的细节点提取器。
3. 提出了一种非极大值抑制方法，用来获取候选块的精确位置。在FVC 2004和NIST SD27的实验评估表明，该方法在精度、召回率和F1分数等方面优于已发表的方法。


# Proposed framework（提出的框架）
&emsp;&emsp;提出了一个新的框架，结合指纹领域知识的深度神经网络来提取细节点，包括两个模块。
* **CoarseNet**: 基于残差学习的卷积神经网络，从输入指纹图像中生成包含细节的候选。以指纹图像为初始输入，以相应的增强图像、分割图、方向场作为次级输入，生成细节点分数图。通过与指纹方向场的比较，估计指纹的细节点方向。
* **FineNet**: 基于inception-resnet的细节点分类器，对CoarseNet输出的候选块进行分类。对每一个以候选细节点为中心的正方形区域进行处理，优化细节点分数图，回归细节点的方向。将分类结果作为最后得到的细节点。

![](/images/paper/minutiae_net/figure_2.png "图2 提出的自动细节点提取结构。CoarseNet以完整指纹图像作为输入，FineNet对CoarseNet输出的细节点块进行处理")

## CoarseNet for minutiae extraction（提取细节点的粗网）
![](/images/paper/minutiae_net/figure_3.png "图3 CoarseNet的结构")
&emsp;&emsp;将深度神经网络和领域知识结合。先生成指纹的分割图、方向图和增强图这些附产物，再根据这些附产物生成细节点分数图。目的是让模型更加鲁棒。

### Segmentation and orientation feature sharing（分割和方向场特征共享）
&emsp;&emsp;网络结构特点：
* 使用更深的残差结构来提取多尺度特征。
* 使用ASPP网络来融合网络的多层次输出，可以得到输入图像中各层次对应区域的概率图。

&emsp;&emsp;在CoarseNet中，指纹的分割和方向场估计共享卷积层。在进行方向场估计的时候，使用了Dictionary-based方法与CoarseNet的方向场预测融合，作为最后的方向场输出，融合权重比例1:3。

### Candidate generation（候选生成）
![](/images/paper/minutiae_net/figure_4.png "图4 候选块的处理映射。分数图的级别越低，它提供的细节就越多")
&emsp;&emsp;利用方向场和增强模块，将输入的原始图像增强，得到指纹的增强图，然后将增强图和分割图结合，作为细节点提取网络的输入。
&emsp;&emsp;细节点提取网络也用了残差结构和多层次结构。将第4层的分数图作为粗定位，将低层次的分数图作为精确定位。

### Non-maximum suppression（非极大值抑制）
&emsp;&emsp;常用的方法：对候选列表按分数排序，计算每个点对两两之间的位置和方向的L2距离，然后迭代的方法，将每个候选和列表里的其他候选比较，保留位置和方向的L2距离超过阈值，且分数高的候选。
&emsp;&emsp;作者提出的方法：对候选列表按分数排序，保留分数高的点，去掉分数比原先已选择的候选低，且与已选择的候选重叠区域超过50%的点。

### Training data for CoarseNet（粗网的训练数据）
&emsp;&emsp;训练分割和方向场模块时使用弱标签，细节点提取部分采用两个库的ground truth标签，使用了数据增强。

## FineNet（细网）
&emsp;&emsp;虽然粗网是可靠的，但它仍然不能识别真实的细节点或识别伪细节点。所以需要使用FineNet，一个对生成的候选块进行分类的细节点分类器。FineNet将CoarseNet输出的候选细节点作为输入，判读对应的10×10中心区域是否是个有效的细节点。

### FineNet architecture（细网结构）
![](/images/paper/minutiae_net/figure_5.png "图5 FineNet的架构。关于inception-resnet v1 块结构的详细信息，请参阅[20]")

&emsp;&emsp;FineNet的输入。提取了相同数量的细节和非细节块，大小为$t_1 \times t_1$，$t_1 = 45$。将提取的这些块，缩放成$t_2 \times t_2$的图像，这里$t_2 = 160$，之所以放大成160，是因为，图像太小无法训练复杂的网络结构，图像缩放太大会模糊一些微小的细节。
&emsp;&emsp;FineNet的训练数据。正样本是基于ground truth的细节点位置提取的块，负样本是随机采样的非细节点位置提取的块，负样本的中心区域(10×10)不包含部分或全部的细节点位置。使用了批量归一化、旋转、镜像、尺度变换和边界模糊等预处理方法。

### Losses and implementation details（loss函数和实施细节）

&emsp;&emsp;**Intra-Inter分类损失**（Intra-Inter class losses）：使用Center Loss[25]作为softmax loss的补充。softmax loss倾向于拉大不同类别特征的区别，而center loss倾向于将同一类别的特征拉的更近。具体的loss计算公式：
$$
L = \alpha L_C + (1 - \alpha) L_S + \beta L_O
$$

$L$是总的loss，$L_C$是center loss，$L_S$是softmax loss，$L_O$是细节点方向loss。
$\alpha$和$\beta$是各个loss的平衡常数，$\alpha = 0.5$，$\beta = 2$。

&emsp;&emsp;**参数设置**：

| 参数 | 值 |
| :---- | :---- |
| 网络参数初始化| $N(0, 0.01)$的随机高斯分布 |
| batch size | 100 |
| 学习率 | 初始学习率0.1，每迭代5万次除以10 |
| 最大迭代次数 | 20万 |
| 动量 | 0.9 |
| 权重衰减 | 0.0004 |


# Experimental results（实验结果）
## Datasets（数据集）
&emsp;&emsp;CoarseNet的训练数据包括FVC 2002数据集和用其增强后的数据，共8000张图像。FineNet的训练数据包括100K个细节点和非细节点块。

## Evaluation（评估）
&emsp;&emsp;评估的数据库是FVC 2004和NIST SD27。用$(l_p, o_p)$表示预测的细节点坐标和方向，$(l_{gt}, o_{gt})$表示ground truth细节点。如果预测的细节点满足以下条件，说明预测正确。
$$
\begin{cases}
	\parallel l_p - l_{gt} \parallel_2 \leq D \\\\
	\parallel o_p - o_{gt} \parallel_1 \leq O
\end{cases}
$$

&emsp;&emsp;$D$和$O$是位置偏差和角度偏差的阈值。
&emsp;&emsp;表2统计了$(D = 8, O = 10)$、$(D = 12, O = 20)$、$(D = 16, O = 30)$的准确率、召回率和F1分数。
![](/images/paper/minutiae_net/tabel_2.png "表2 不同的细节提取方法在FVC 2004和NIST SD27数据集的比较")

&emsp;&emsp;表3是使用FingerNet的非极大值抑制(NMS)和作者提出的非极大值抑制(NMS*)的比对，对比数据库是NIST SD27。
![](/images/paper/minutiae_net/table_3.png "表3 两种非极大值抑制方法的比较")

&emsp;&emsp;图6是不同方法的准确率和召回率曲线对比。
![](/images/paper/minutiae_net/figure_6.png "图6 不同方法的准确率和召回率曲线对比")

&emsp;&emsp;图7是细节点提取的效果图。
![](/images/paper/minutiae_net/figure_7.png "图7 细节点提取的效果图")

&emsp;&emsp;在某些情况下，提议的框架会遗漏了真细节点，或者提取了伪细节点。由于脊线的不连续，导致一些细节点检测错误(图像a)，或者由于细节点的位置靠近指纹边缘而漏检(图像c)。对于NIST SD27数据集的潜在指纹，该方法对严重的背景噪声(图像exiang指纹质量(图像g)比较敏感。对于FVC 2004数据集和NIST SD27数据集的滚动指纹，得到了接近ground truth的结果。
&emsp;&emsp;NIST SD27每张图片的运行时间约为1.5秒，FVC 2004每张图片的运行时间约为1.2秒。


# Conclusions（总结）
&emsp;&emsp;提出了两个细节点提取网络：CoarseNet和FineNet。提出了一个非极大抑制方法。

改进的地方：
1. 使用更大的包括现场指纹的训练集来训练。
2. 构建背景描述符来利用细节点周围的区域。
3. 改进处理时间。
4. 将细节点提取器整合到端到端指纹匹配框架中。
