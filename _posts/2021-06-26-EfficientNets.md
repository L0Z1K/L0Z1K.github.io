---
layout: post
title: 'EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks'
category: research
---

<p align="center"><img width="200" alt="image" src="https://user-images.githubusercontent.com/64528476/123504380-dbbc0100-d693-11eb-8d95-90b19375728a.png"></p>

This paper was published in May 2019. It was cited 2,489 times in total.

<h3 align="center">Abstract</h3>

Convolutional Neural Networks(ConvNets) are commonly developed at a fixed resource budget, and then scaled up for better accuracy if more resources are available. They propose a new scaling method that uniformly scales all dimensions of depth/width/resolution using a simple yet highly effective *compound coefficient*.

They use neural architecture search to design a new baseline network and scale it up to obtain a family of models, called *EfficientNets*.

<h2>1. Introduction</h2>

Scaling up ConvNets is widely used to achieve better accuracy. The common way is to scale up ConvNets by their depth(#layers) or width(#channels) or image resolution. Though it is possible to scale two or three dimensions arbitrarily, it requires tedious manual tuning to find sub-optimal accuracy and efficiency.

Their method uniformly scales network width, depth, and resolution with a set of fixed scaling coefficients. They called it, *compound scaling method*.

<h2>2. Compound Model Scaling</h2>

<p align="center"><img width="800" alt="image" src="https://user-images.githubusercontent.com/64528476/123504721-d3fd5c00-d695-11eb-8ce2-6b78fbaf266a.png"></p>

<h3>2.1. Scaling Dimensions</h3>

The optimal $$d$$(depth), $$w$$(width), $$r$$(resolution) depend on each other and the values change under different resource constraints. <mark>Due to this difficulty, conventional methods mostly scale ConvNets in one of these dimensions.</mark>

<strong>Depth ($$d$$):</strong> Intuitively, deeper ConvNet can capture richer and more complex features, and generalize well on new tasks. However, deeper networks occurs the vanishing gradient problem. For example, ResNet-1000 has similar accuracy as ResNet-101 even though it has much more layers.

<strong>Width ($$w$$):</strong> Scaling network width is commonly used for small size models. Wider networks can capture more fine-grained features and are easier to train. However, extremely wide but shallow networks can be hard to capture higher level features.

<strong>Resolution ($$r$$):</strong> With higher resolution images, ConvNets can capture more fine-grained patterns. However, the accuracy gain diminishes for very high resolutions.

<p align="center"><img width="800" alt="image" src="https://user-images.githubusercontent.com/64528476/123505042-d6f94c00-d697-11eb-8dea-88f8a4cf9dfc.png"></p>

The above Figure shows that scaling up any dimension of $$d$$, $$w$$, $$r$$ improves accuracy, <mark>but the accuracy gain diminishes for bigger models.</mark>

<h3>2.2. Compound Scaling</h3>

They empirically observe that $$d$$, $$w$$, $$r$$ are not independent. Intuitively, for higher resolution images, we should increase network depth for capturing similar features that include more pixels in bigger images. We should also increase network width when resolution is higher.

<p align="center"><img width="400" alt="image" src="https://user-images.githubusercontent.com/64528476/123505190-a5cd4b80-d698-11eb-8879-df51b4e9a450.png"></p>

If we only scale network width $$w$$ without changing $$d$$ and $$r$$, the accuracy saturates quickly. In order to pursue better accuracy and efficiency, <mark>it is critical to balance all dimension</mark> of $$w$$, $$d$$, $$r$$ during ConvNet scaling.

In this paper, they propose a new compound scaling method, which use a compound coefficient $$\phi$$ to uniromly scales network width, depth, and resolution in a principled way:

<p align="center"><img width="250" alt="image" src="https://user-images.githubusercontent.com/64528476/123505251-fb095d00-d698-11eb-8907-9c256f328c18.png"></p>

where $$\alpha, \beta, \gamma$$ are constants.

The FLOPS of a regular convolution op is proportional to $$d$$, $$w^{2}$$, $$r^{2}$$. So with $$\phi$$, it increase total FLOPS by $$(\alpha \cdot \beta^{2} \cdot \gamma^{2})^{\phi} \approx 2^{\phi}$$.

<h2>3. EfficientNet Architecture</h2>

Since model scaling does not change layer in baseline network, <mark>having a good baseline network is also critical.</mark>

They use a multi-objective neural architecture search that optimizes both accuracy and FLOPS. If you want to study more about neural architecture search, please refer to [2].

They use $$ACC(m) \times [FLOPS(m)/T]^{w}$$ as the optimization goal, where $$ACC(m)$$ and $$FLOPS(m)$$ denote the accuracy and FLOPS of model $$m$$. $$T$$ is the target FLOPS and $$w$$ is a hyperparameter for controlling the trade-off between accuracy and FLOPS. 

<p align="center"><img width="400" alt="image" src="https://user-images.githubusercontent.com/64528476/123505520-8800e600-d69a-11eb-99d1-51bd4eacf20d.png"></p>

Starting from the baseline EfficientNet-B0, they apply compound scaling method with two steps:

* STEP 1: Fix $$\phi$$ to 1, and do a small grid search of $$\alpha, \beta, \gamma$$.
* STEP 2: Fix $$\alpha, \beta, \gamma$$, scale up the network with $$\phi$$. 

They split the method to two steps because searching for $$\alpha, \beta, \gamma$$ directly around a large model, search cost is too expensive.

<h3>3.1. Train</h3>

They train EfficientNet models on ImageNet using RMSProp optimizer with decay 0.9 and momentum 0.9, batch norm momentum 0.99, weight decay 1e-5, initial learning rate 0.256 that decays by 0.97 every 2.4 epochs. They also use SiLU activation. They linearly increase dropout ratio from 0.2 for EfficientNet-B0 to 0.5 for B7.

<h2>4. Experiments</h2>

<p align="center"><img width="400" alt="image" src="https://user-images.githubusercontent.com/64528476/123505612-1d9c7580-d69b-11eb-8cca-42efb19f6812.png"></p>

Compared to other single-dimension scaling methods, compound scaling method improves the accuracy.

<div align="center">
<img float="left" width="350" alt="image" src="https://user-images.githubusercontent.com/64528476/123505753-d5318780-d69b-11eb-9995-ae1deaf852c3.png">
<img width="350" alt="image" src="https://user-images.githubusercontent.com/64528476/123505793-0c079d80-d69c-11eb-8fd8-2107d2190bf3.png">
</div>

Scaled EfficientNet models achieve better accuracy with much fewer parameters and FLOPS than other ConvNets.

<p align="center"><img width="700" alt="image" src="https://user-images.githubusercontent.com/64528476/123505916-7f111400-d69c-11eb-8765-66a30d7b22e2.png"></p>

Why their compound scaling method is better than others? As shown in the above figure, <mark>the model with compound scaling tends to focus on more relevant regions with more object details.</mark>

<h2>5. Conclusion</h2>

They propose a simple and highly effective compound scaling method, which enables us to easily scale up a baseline ConvNet while maintaining model efficiency. They demonstrate that a mobile-size EfficientNet model can be scaled up very effectively, surpassing state-of-the-art accuracy with fewer parameters and FLOPS on ImageNet.

<h3>References</h3>

[1] [EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks](https://arxiv.org/pdf/1905.11946.pdf)

[2] [MnasNet: Platform-Aware Neural Architecture Search for Mobile](https://openaccess.thecvf.com/content_CVPR_2019/papers/Tan_MnasNet_Platform-Aware_Neural_Architecture_Search_for_Mobile_CVPR_2019_paper.pdf)

- - -

<h3>Comments</h3>

친구랑 얘기 중에 EfficientNet이 언급되었고 이전에 보았던 MobileNet하고 비슷한 느낌인 것 같아서 논문을 읽게 되었다. Compound Scaling Method라는 새로운 방법을 알게 되어서 좋았고 계속해서 논문 읽는 것이 습관화되면 좋겠다. 글을 적다보니 리뷰 느낌이 아닌 Summary가 되었는데 뭐 나름 좋다고 생각한다. 논문을 리뷰하다가 자칫 주관적인 생각이 들어가 저자의 의도를 해칠 가능성이 있는 것보단 주요한 쟁점들만 따로 summary하는 것도.. 나쁘지 않다고 본다. 

- - -