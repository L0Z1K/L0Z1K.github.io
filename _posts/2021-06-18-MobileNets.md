---
layout: post
title: 'MobileNets: Efficient Convolutional Neural Networks'
category: research
---

<p align="center"><img width="600" alt="image" src="https://user-images.githubusercontent.com/64528476/122634365-cb96a580-d118-11eb-940f-0fdf75a5926a.png"></p>

This paper was published in April 2017. It was cited 8,465 times in total.

<h3 align="center">Abstract</h3>

MobileNets are based on a streamlined architecture that uses depthwise separable convolutions to build light weight deep neural networks. They introduce two simple global hyperparameters to allow the model builder to choose the right sized model for their application. MobileNets can reduce computational costs, but it still has strong performance compared to other popular models.

## 1. Introduction

<p align="center"><img width="638" alt="image" src="https://user-images.githubusercontent.com/64528476/122563298-fe8c5b00-d07e-11eb-8f5c-ef5dc2b8fa8d.png"></p>

Convolutional neural networks have become ubiquitous in computer vision. The general trend has been to make deeper and more complicated networks in order to achieve higher accuracy. BUT in many real world applications, we cannot use huge model because of computational cost.

<mark>We should make networks more efficient with respect to size and speed, too!</mark>

<h2>2. Depthwise Separable Convolution</h2>

<p align="center"><img width="400" alt="image" src="https://user-images.githubusercontent.com/64528476/122563932-c3d6f280-d07f-11eb-805e-d9690177a86c.png"></p>

Depthwise separable convolutions is a form of factorized convolutions which factorize a standard convolution into a depthwise convolution and a 1$$\times$$1 convolution(pointwise convolution).

Suppose the number of input channels is $$M$$, the number of output channels is $$N$$, the kernel size is $$D_{K} \times D_{K}$$, and the feature map size is $$D_{F} \times D_{F}$$. Also suppose that stride is one and padding.

Standard convolutions have the computational cost of:

$$
D_{K} \cdot D_{K} \cdot M \cdot N \cdot D_{F} \cdot D_{F}
$$

We need $$D_{K} \cdot D_{K}$$ cost for calculating one feature. Then we should calculate $$D_{F} \cdot D_{F}$$ features per $$(input, output)$$ channel pair. Finally, the above values are derived.

The filtering and combination steps can be plit into two steps for substantial reduction in computational cost.

We use depthwise convolutions to apply a single filter per each input channel. Pointwise convolution, a simple 1$$\times$$1 convolution, is then used to create a linear combination of the output of the depthwise layer.

<p align="center"><img width="250" alt="image" src="https://user-images.githubusercontent.com/64528476/122633052-61c6cd80-d111-11eb-990e-8990ca39e270.png"></p>

Depthwise convolution has a computational cost of:

$$
D_{K} \cdot D_{K} \cdot M \cdot D_{F} \cdot D_{F}
$$

Same with output channel is 1.

Pointwise convolution has a computational cost of:

$$
M \cdot N \cdot D_{F} \cdot D_{F}
$$

Same with kernel size is $$1\times 1$$.

Depthwise separable convolutions cost:

$$
D_{K} \cdot D_{K} \cdot M \cdot D_{F} \cdot D_{F} + M \cdot N \cdot D_{F} \cdot D_{F}
$$

We get a reduction in computation of:

$$
\cfrac{1}{N} + \cfrac{1}{D_{K}^{2}}
$$

## 3. MobileNet Structure

MobileNet uses $$3 \times 3$$ depthwise separable convolutions which uses between 8 to 9 times less computation than standard convolutions.

<p align="center"><img width="400" alt="image" src="https://user-images.githubusercontent.com/64528476/122632945-d9e0c380-d110-11eb-82a7-8eed87b9ca83.png"></p>

All layers are followed by a batchnorm and ReLU nonlinearity with the exception of final fully connected layer. Counting depthwise and pointwise convolutions as seperate layers. MobileNet has 28 layers.

<div align="center">
<img float="left" width="300" alt="image" src="https://user-images.githubusercontent.com/64528476/122633365-393fd300-d113-11eb-90ed-256aaa7a5dc6.png">
<img width="300" alt="image" src="https://user-images.githubusercontent.com/64528476/122633377-4fe62a00-d113-11eb-8495-0537c19b56d1.png">
</div>

MobileNet spends 95% of it's computation time in $$1 \times 1$$ convolutions which also has 75% of the parameters.

MobileNet models were trained in TensorFlow using RMSprop with asynchronous gradient descent.

They use less regularization and data augmentation techniques because small models have less trouble with overfitting. Also, <mark>it is important to put very little or no weight decay on the depthwise filters</mark> since their are so few parameters in them.

## 4. Width Multiplier and Resolution Multiplier

For a given layer and width multiplier $$\alpha$$, the number of input channels $$M$$ becomes $$\alpha M$$ and the number of output channels $$N$$ becomes $$\alpha N$$. The computational cost with width multiplier $$\alpha$$ is:

$$
D_{K} \cdot D_{K} \cdot \alpha M \cdot D_{F} \cdot D_{F} + \alpha M \cdot \alpha N \cdot D_{F} \cdot D_{F}
$$

It reduces computational cost and the number of parameters quadratically by roughly $$\alpha ^{2}$$. In serveral results, computation costs and parameters are significantly reduced, but accuracy is rarely reduced.

We apply resolution multiplier $$\rho$$ to the input image. The computational cost with width multiplier $$\alpha$$ and resolution multiplier $$\rho$$ is:

$$
D_{K} \cdot D_{K} \cdot \alpha M \cdot \rho D_{F} \cdot \rho D_{F} + \alpha M \cdot \alpha N \cdot \rho D_{F} \cdot \rho D_{F}
$$

Resolution multiplier has the effect of reducing computational cost by $$\rho ^{2}$$. 

## 5. Experiments

<div align="center">
<img float="left" width="350" alt="image" src="https://user-images.githubusercontent.com/64528476/122633990-7bb6df00-d116-11eb-8a60-05654ad667da.png">
</div>

<mark>MobileNet only reduces accuracy by 1% on ImageNet was saving temendously on mult-adds and parameters.</mark>

<div align="center">
<img float="left" width="300" alt="image" src="https://user-images.githubusercontent.com/64528476/122633996-86717400-d116-11eb-98e2-be73f0e494f8.png">
<img width="300" alt="image" src="https://user-images.githubusercontent.com/64528476/122634001-8d988200-d116-11eb-83b0-4b5ed7190493.png">
</div>

Accuracy drops off smoothly across width multiplier and resolution multiplier.

<div align="center">
<img float="left" width="300" alt="image" src="https://user-images.githubusercontent.com/64528476/122634068-19aaa980-d117-11eb-9231-8b28737ba16f.png">
<img width="300" alt="image" src="https://user-images.githubusercontent.com/64528476/122634077-20d1b780-d117-11eb-8cd6-c635a7503d55.png">
</div>

Compared with popular models, MobileNet is nearly as accurate as them while being smaller and less compute intensive.

## 6. Conclusion

They proposed a new model architecture call MobileNets based on depthwise separable convolutions. They then demonstrated how to build smaller and faster MobileNets using width multiplier and resolution multiplier.

### References

[1] [MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications](https://arxiv.org/pdf/1704.04861.pdf)

[2] [A Survey of the Recent Architectures of Deep Convolutional Neural Networks](https://arxiv.org/pdf/1901.06032.pdf)

[3] [Depthwise Separable Convolution 설명 및 pytorch 구현](https://wingnim.tistory.com/104)

[4] [CNN, Convolutional Neural Network 요약](http://taewan.kim/post/cnn/)

[5] [딥러닝 용어정리, RMSProp, Adam 설명](https://light-tree.tistory.com/141)

- - -

### Comments

어쩌다 이 논문을 접하고 내용도 짧고 오랜만에 논문 정리도 해볼겸 해서 시도해봤다. 이 논문을 다룬 블로그를 하나도 참고하지 않고 오직 내가 논문에서 얻은 내용으로만 정리해보았다. 생각보다 논문을 읽음으로써 오랜만에 CNN도 다시 공부하고 좋은 경험이었다. 요즘 정말로 모델의 크기만 키우는 데에 급급하고 1%의 정확도를 위해 파라미터 수를 몇 배 키우는 거에 서슴치 않는다. 그런 느슨해진 우리에게 다시 긴장감을 불어넣는 그런 논문이었던 것 같다. 모델 구조도 자세하게 적혀있어서 시간이 허락한다면 모델 구현도 해서 논문 검증도 해보고 싶다.

- - -