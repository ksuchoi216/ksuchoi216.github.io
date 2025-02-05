---
title: TCN
parent: Time Series Forecasting
nav_order: 3
---


TCN은 CNN kernel의 간격을 넓혀 보다 넓은 시계열 데이터를 사용하기 위해 만들었습니다.
CNN가 어떻게 다른지 한 번 보시죠.

<!--more-->
## Why TCN is suggested?

연구진은 RNN, LSTM같은 recurrent networks보다 성능이 더 뛰어난 변형된 CNN을 개발했습니다.

아시다시피 CNN은 1989년도에 Yann LeCun 처음 제안되어 이미지 쪽에 혁신적인 성과를 낸 모델입니다.

하지만 CNN 자체는 localization(커널로 주변과 같이 계산하는 특징)로 1D CNN으로 시계열을 학습할 수 있지 않을까라는 시도가 있었습니다. 하지만 결과적으로 시계열에 있어서 RNN, LSTM 같은 시계열적 특성을 반영한 모델들이 더 뛰어난 성능을 보여 CNN은 시계열쪽에서 적용되지 못했습니다.

TCN는 CNN을 변형시켜 RNN, LSTM을 뛰어넘은 모델입니다.

## What is TCN?

결론만 말하자면, CNN의 convolution 간격을 늘린 모델입니다. 그림으로 이해하면 간편합니다.

![main.png](/images/tcn/main.png){:, .align-center}

그림처럼 TCN 2 Layer가 존재한다고하면 CNN과 다르게 kernel 개별 간격이 넓게 가져갑니다.

예를 들어, [1,2,3,4,5,6,7]라는 데이터가 있다고 가정하면 4 데이터를 중심으로 kernel size가 3이라면 [3, 4, 5]이렇게 convolution을 합니다. TCN는 간격을 2이라고하면 [2, 4, 6]이렇게 convolution을 합니다.

왜 이렇게 CNN에 간격을 늘렸을까요?

답은 간단합니다. 시계열 데이터에서 CNN을 이용하면 근처에 있는 데이터만 convolution하기 때문에 시계열 특징을 잘 찾아내지 못합니다. 반대로 TCN은 보다 넓은 영역의 데이터를 이용하기 때문에 시계열 데이터에 유리합니다.

## How does it work?

동작은 보통의 CNN과 동일합니다. 물론 논문에서는 아래와 같이 1D CNN의 skip connection을 option으로 제안하긴 하지만 결국 TCN-Normalization-Activation-Dropout 같은 기존과 비슷한 구조를 가집니다.

![structure.png](/images/tcn/structure.png){:, .align-center}

## Results

아래 그래프를 보시면 입력 시계열 길이가 늘어도 TCN이 성능이 좋은 것을 알 수 있습니다.

![res1.png](/images/tcn/res1.png){:, .align-center}

또한 Accuarcy관점에서 봐도 LSTM, GRU를 압도합니다.
![res2.png](/images/tcn/res2.png){:, .align-center}

물론 LSTM은 시계열적 특징을 잘 잡아냅니다. 그래서 이후 TCN+LSTM 이나 CNN+LSTM같은 시계열 데이터 특징을 추출하는 TCN, CNN 모델과 LSTM을 결합하여 예측하는 모델도 많이 연구되었습니다.

## References
An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling
