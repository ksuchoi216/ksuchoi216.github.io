---
title: Tsmixer
parent: Time Series Forecasting
nav_order: 6
---

Transformer가 GPT로 뛰어난 성능을 냈지만 일반적인 시계열 데이터에서 Transformer 모델보단 MLP가 성능이 더 좋라고 이야기하는 논문인 TSMixer를 살펴봅시다.

<!--more-->
![tsmixer_main.png](/images/tsmixer/tsmixer_main.png){:, .align-center}
## 1. 이 방법이 이루고자 한 것은(Why)?
![abs.png](/images/tsmixer/abs.png){:, .align-center}
이 논문이 나오기 전 시계열 예측 연구는 NLP에서 대유행시킨 transformer를 이용한 시계열 예측이 전반적인 연구 였었습니다. 이러한 NLP에서 사용하는 transformer는 문장이라는 추상적 데이터를 이해하고 관계성을 찾아가며 시계열 예측을 하기 위해 사용합니다. 하지만 일반적인 시계열 예측에서는 이러한 추상적인 데이터가 아니라 int, float인 데이터 자체의 이해가 필요하지 않는 데이터이기에 적절하지 않습니다.
다시 말해 transformer보다 linearly connection되어 있는 MLP(multi linear perceptron)이 더 시계열에 적합하는 이야기를 이 논문에서 이야기합니다. 그렇다면 어떻게 MLP를 적용했는지 계속해서 설명드리겠습니다.

참고로, Transformer는 추상적인 데이터를 인코더 레이어를 거치면서 데이터 간에 관련성을 추출하며 데이터를 이해합니다. 그렇게 추출된 특징을 가지고 예측하는 모델입니다.


## 2. 접근 방식의 핵심 요소는 무엇이었습니까(What-How)?
시계열 예측을 잘하기 위해 Transformer은 입력에 대해 잘 조합해서 새로운 특징 벡터를 만들어냅니다. 시계열 예측에서는 서로 다른 시간간에 조합과 서로 다른 특징간 조합 2가지로 나눌 수 있습니다. 이 논문에서는 어떻게 잘 조합했을까요?

먼저 그림 부터 보시면 Mixing Layer라고 Time-mixing MLP와 Feature-mixing MLP를 한 Layer라고 생각합니다. 
![mixer.png](/images/tsmixer/mixer.png){:, .align-center}


Time-mixing MLP은 데이터를 입력을 같은 시간이면서 서로 다른 특징을 가지고 있는 데이터를 MLP에 넣어 학습하는 모델입니다. 다시 말해, 시간을 잘 섞는 MLP입니다.
Feature-mixing MLP는 데이터 입력을 같은 특징을 가지면서 서로 다른 시간에 데이터를 MLP에 넣어 학습하는 모델입니다. 다시 말해, 특징을 잘 섞는 MLP입니다.
![mlp_block.png](/images/tsmixer/mlp_block.png){:, .align-center}
왼쪽이 time mixing MLP며 오른쪽이 feature mixing MLP입니다.

이러한 Time mixing MLP, Feature-mixing MLP을 여러번 통과한 데이터는 마지막에 특징을 추출하면서 최종적으로 예측 값에 가까이 가기 위해 temporal projection MLP를 사용합니다. 구조상으로는 time mixing MLP와 크게 다르지 않습니다.
![temp_proj.png](/images/tsmixer/temp_proj.png){:, .align-center}

정리하자면, TSMixer는 서로다른 시간, 서로다른 특징을 조합하는 각각 모델을 이용해 잘 섞어서 예측을 잘 해볼려는 모델입니다.

## 3. 그래서 어떤 결과를 냈나요(So what)?

결론만 말씀드리자면, former계열(시계열 Transformer)를 Multivariate 예측에서 압도적인 성능을 냅니다.
물론 데이터에 따라 목적에 따라 성능은 다르지만, 흔히 시계열 예측에서 많이 사용하는 데이터에서는 성능이 좋다는 이야기입니다.
더 놀라운 것은 TSMixer는 단순한 MLP 조합이기 때문에 연산량이나 속도 면에서 매우 뛰어납니다.

![res.png](/images/tsmixer/res.png){:, .align-center}

## 4. 참고 자료
- 2023 11 TSMixer An All-MLP Architecture for Time Series Forecasting
