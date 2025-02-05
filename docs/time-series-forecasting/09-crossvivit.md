---
title: Crossvivit
parent: Time Series Forecasting
nav_order: 9
---


<!--more-->
![Pasted image 20240214210215.png](/images/crossvivit/Pasted image 20240214210215.png){:, .align-center}

## 1. 연구자가 이루고자 한 것은 무엇인가요(Why)?
시계열 이미지와 시계열 데이터를 통해 예측을 하고 싶은 문제들이 있습니다. 이 논문에서는 Solar Irradiance(일사량)라는 문제를 해결하고 싶었습니다.
시계열 이미지는 동영상에서 프레임 단위 이미지라고 생각하면 쉽습니다. t=1 시점에 frame 이미지과 t=2 시점 frame 이미지를 생각하면 이 2개 이미지는 시계열 관계에 있습니다. 일사량에서 보자면 위성 사진을 생각할 수 있습니다.
일사량에서는 시계열 데이터는 날씨 데이터를 생각할 수 있습니다. 바람 방향, 온도, 습도 등 다양한 데이터는 정해진 시간 간격으로 관측 됩니다. 우리 기상청도 마찬가지로 하고 있습니다. 

그렇다면, 시계열 이미지와 시계열 데이터를 어떻게 처리했을까요?

## 2. 접근 방식의 핵심 요소는 무엇인가요(What-How)?
결론부터 말하자면, 시계열 이미지은 Vision Transformer로 처리하고 시계열 데이터는 일반적으로 Transformer로 처리합니다. 아래 그림을 보면 이해가 더 쉽습니다.
Tokenizer는 Dimension mapping이라고 생각하면 쉽습니다. 예를 들어 
$$
Image \in \mathbb{R}^{T \times C \times H \times W} \rightarrow \mathbb{R}^{T \times N \times d}
$$
이렇게 "Channel, Height, Width"인 이미지인 dimension에서 Nxd라는 dimension으로 mapping을 위해 Tokenize라고 이해하시면 됩니다.
Rotary Positional Embedding을 통해 context와 time series을 잘 섞습니다.
그러고 나서 이미지와 시계열 각각 트랜스포머로 처리한다.


![Pasted image 20240214210244.png](/images/crossvivit/Pasted image 20240214210244.png){:, .align-center}

이렇게 처리된 데이터를 합쳐서 Crossformer를 이용해 mixing합니다. 
![Pasted image 20240214211108.png](/images/crossvivit/Pasted image 20240214211108.png){:, .align-center}

마지막으로 Decoder인 트랜스포머를 통해 처리합니다.
여기서 정리하자면, 이미지와 시계열 데이터를 시계열적인 문맥을 이해하고 데이터끼리 섞어가며 추상 벡터를 생성하는 것이 CrossViViT이 핵심이다.

마지막으로 이러한 추상 벡터를 이용해 예측하여 quantile loss를 이용해 정답을 맞춘다. quantile loss는 아래와 같습니다.
$$L_{\alpha}(y, \hat{y}) =\max\{\alpha(\hat{y}-y), (1-\alpha)(\hat{y}-y)\}$$


## 3. 그래서 어떤 결과를 냈나요(So what)?

![Pasted image 20240214211919.png](/images/crossvivit/Pasted image 20240214211919.png){:, .align-center}
