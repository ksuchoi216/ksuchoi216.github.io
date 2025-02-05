---
title: NBEATS
parent: Time Series Forecasting
nav_order: 4
---


거의 모든 시계열 예측은 forecast라는 앞을 예측을 기반으로 만들어졌다. 
그렇다면 backcast라는 현재 기준으로 뒤를 예측을 활용하면 좋지 않을까?
즉, NBEATS에서는 forecast과 backcast을 잘 활용하면 더 예측을 향상시키고 싶어했다.
그렇다면 어떻게 활용하는지 알아보자.

<!--more-->

## 1. 이루고자 한 것은 무엇인가요?
거의 모든 시계열 예측은 forecast라는 앞을 예측을 기반으로 만들어졌다. 
그렇다면 backcast라는 현재 기준으로 뒤를 예측을 활용하면 좋지 않을까?
즉, NBEATS에서는 forecast과 backcast을 잘 활용하면 더 예측을 향상시키고 싶어했다.
그렇다면 어떻게 활용하는지 알아보자.
![nbeats.png](/images/nbeats/nbeats.png){:, .align-center}

## 2. 접근 방식의 핵심 요소는 무엇인가요?
위에서도 언급했듯이 forecast와 backcast를 Linear(FCNN)을 통해 예측합니다. 
아래는 GenericBlock의 코드와 논문에서 언급한 그림(빨간 박스 부분)입니다.
![genericblock.png](/images/nbeats/genericblock.png){:, .align-center}
```python
class GenericBlock(Block):
    def __init__(
        self,
        units,
        thetas_dim,
        device,
        backcast_length=10,
        forecast_length=5,
        nb_harmonics=None,
    ):
        super(GenericBlock, self).__init__(
            units, thetas_dim, device, backcast_length, forecast_length
        )

        self.backcast_fc = nn.Linear(thetas_dim, backcast_length)
        self.forecast_fc = nn.Linear(thetas_dim, forecast_length)

    def forward(self, x):
        # no constraint for generic arch.
        x = super(GenericBlock, self).forward(x)

        theta_b = self.theta_b_fc(x)
        theta_f = self.theta_f_fc(x)

        backcast = self.backcast_fc(theta_b)  # generic. 3.3.
        forecast = self.forecast_fc(theta_f)  # generic. 3.3.

        return backcast, forecast
```
```python

```

**이렇게 나온 backcast와 forecast을 어떻게 활용할까요?**
일단 과거예측값(backcast)는 과거 실제값을 빼주어 계속 되는 block에 넣어줍니다.  다시말해 아래 식처럼 실제 값과 위에 Genericblock을 이용하여 나온 예측 값을 빼주어 다음 블록 입력으로 넣어줍니다.
$$
x_{next} = true_{backcast} - pred_{backcast}
$$
이게 무슨 의미가 있냐면, 다음 블록에게 "과거 예측을 해보니 이정도 오류가 있었어 오류가 줄어들는 방향으로 학습해보자"라고 이야기하는 것입니다. 만약 이렇게 입력을 넣지 않으면 다음 블록은 스스로 판단해야합니다. 한 마디로 다음 블록에 오류까지 계산해서 떠먹여주는 것이지요.

![backcast_block_.png](/images/nbeats/backcast_block_.png){:, .align-center}
그림으로 보면 더 명확해집니다. 표시한 것처럼 error를 계산해 넣어줍니다.

한편 미래예측값(forecast)는 실제 예측을 위해 차곡차곡 모아서 최종 예측에 반영합니다. residual connection을 이용해 모두 모아서 반영합니다.

![forecast_block.png](/images/nbeats/forecast_block.png){:, .align-center}

논문에서는 3가지 버전의 block이 있습니다. 이들을 잘 조합하면 더 좋은 결과를 낼 수 있다고 합니다.
seasonality block은 다름이 아니라 seasonality가 계절적으로 주기성을 띄는 성분이므로 이것을 반영하기 위해 주기함수인 사인함수(sin wave)으로 모델링합니다.
```python
def seasonality_model(thetas, t, device):
    p = thetas.size()[-1]
    assert p <= thetas.shape[1], "thetas_dim is too big."
    p1, p2 = (p // 2, p // 2) if p % 2 == 0 else (p // 2, p // 2 + 1)
    s1 = torch.tensor(
        np.array([np.cos(2 * np.pi * i * t) for i in range(p1)])
    ).float()  # H/2-1
    s2 = torch.tensor(np.array([np.sin(2 * np.pi * i * t) for i in range(p2)])).float()
    S = torch.cat([s1, s2])
    return thetas.mm(S.to(device))
```

Trend block은 trend를 계산하기 위해 $t^i$을 계산해 지수 증가되는 부분을 모델링합니다.
```python
def trend_model(thetas, t, device):
    p = thetas.size()[-1]
    assert p <= 4, "thetas_dim is too big."
    T = torch.tensor(np.array([t**i for i in range(p)])).float()
    return thetas.mm(T.to(device))
```

## 3. 결과는 어떤가요?
결과적으로 I+G 즉 모든 걸 잘 조합한게 성능이 좋았습니다. 물론 tourism 데이터에서는 G 모델이 성능이 좋았습니다.
![res.png](/images/nbeats/res.png){:, .align-center}

아래와 같은 점이 이 논문은 신선했습니다.
- backcast를 활용한다는 점
- 모든 블록 결과값의 residual connection으로 예측에 반영한다는 점.

## 4. 참고 자료
2019 855 N-BEATS NEURAL BASIS EXPANSION ANALYSIS FOR INTERPRETABLE TIME SERIES FORECASTING