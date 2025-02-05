---
title: Autoformer
parent: Time Series Forecasting
nav_order: 3
---


일단 Autoformer는 기존에 시계열 예측에 사용된 트랜스포머 모델에 시계열 순서 정보를 잃어버리는 고질적 문제를 해결하기 위해 제안되었습니다. 트랜스포머 계열은 시계열 데이터 본래 특징을 잃어버립니다. 시간 순서대로 연결되어 있는 데이터가 시계열 데이터인데 이러한 정보를 트랜스포머 모델들은 반영하지 못합니다. 그렇다면 어떻게 autoformer가 해결했는지 탐험해보겠습니다.

<!--more-->
## What is Autoformer?

Autoformer는 Auto-correlation + Transformer을 결합한 모델입니다. 시계열 데이터를 더 잘 학습하기 위해 Series Decomposition 적용합니다.

즉 아래와 같은 개념을 이해한다면 Autoformer를 써먹을 수 있습니다.

- Transformer
- Auto-correlation
- Series Decomposition

### Transformer

Transformer는 Self-attention을 통해 문장을 이해하고 해석하는데 특화된 모델입니다. GPT에 T가 트랜스포머 사용된 것을 알 수 있듯이 텍스트 데이터에 잘쓰이는 모델입니다.

트랜스포머 장점은 시계열 데이터에서 관계를 찾을 수 있다는 큰 장점이 있습니다. 그러므로 단어를 순서대로 연결되어있는 문장인 텍스트 데이터에 적합하다고 할 수 있습니다. 자세한 사항은 트랜스포머를 별도의 포스팅으로 설명 드리겠습니다.

정리하자면, 트랜스포머는 **시계열 데이터(t, t-1, t-2 …)간에 관계를 잘 찾아 학습하는 장점**이 있습니다. 예를 들어 t와 t-1 관계 혹은 t-2와 t-5, t-6, t-7의 관계라던지 여러 조합을 통해 무엇이 더 연관있는지 찾아 낼 수 있습니다.

### Auto-correlation

Auto-correlation은 **lagged time(t-1, t-2, ..)에 대해 correlation coefficients**를 구합니다. 쉽게 말해 시간 지연된 데이터와 상관 관계가 어느 정도 인지 -1부터 1까지 숫자로 나타낸 값입니다.

시계열 데이터에서는 빠질 수 없는 특징입니다. 예를 들어 카드 소비량 데이터를 보자면 금요일, 주말 이렇게 구매량이 늘어나는 것을 일별로 ACF(auto-correlation function) plot을 그려보면 한 눈에 파악할 수 있습니다.

정리하자면, 자기 상관은 시간 지연에 대해 상관 관계를 계산합니다.

### Series Decomposition

마지막으로 Series Decomposition이 남았습니다. 간단합니다. 시계열 분석에 기초라고 할 수 있는 Decomposition과 크게 다르지 않습니다. 있는 그대로 시계열 데이터를 사용하면 분석 혹은 예측이 부정확하기 때문에 **추세(trend), 계절성(seasonal), 그 외(remainer)로 나누어 예측할려고 시계열 데이터를 분해**합니다.

여기서 추세(꾸준히 증가하거나 감소), 계절성(계절마다 주기적으로 영향), 그외(나머지)를 의미합니다. 물론 cyclic이다 아니면 다른 것들로 분해하기도 합니다. 미국과 캐나다에서 개발한 X-11 decomposition, ARIMA를 위한 SEATS decomposition 등 다양한 시계열 분해가 존재하지만 이 논문에서는 추세, 계절성에만 집중합니다.

다시 3가지 개념을 정리해봅시다.

- 트랜스포머: 시계열 데이터 간에 관계를 학습하는 모델
- 자기상관: 시간 지연에 대해 상관관계를 계산
- 시계열 분해: 시계열 데이터에서 추세, 계절성을 나누는 방법

여기까지 오셨다면 거의 다 이해하셨습니다.

그렇다면 논문을 한 번 들여다 보면서 추가적으로 설명 드리겠습니다. 사실 아래 그림을 이해하면 다 이해한 것입니다.

## How does it work?

트랜스 포머 구조인 Encoder(해석하는 부분)와 Decoder(예측하는 부분)로 구성되어 있습니다(물론 딱 해석과 예측하는 부분이라고 할 수 없지만 이해를 위해 러프하게 설명합니다).

모든 블럭 사이에는 Series Decomposition이 있어 추세와 계절성을 분리하여 잘 해석합니다.

인코더는 Auto correlation을 계산해서 Feed forward을 시계열 데이터를 해석하는 부분입니다. 중간에 본래 시계열 데이터 정보를 잃지 않기 위해 skip connectiond을 사용합니다.

디코더는 인코더 정보와 합계 2개의 Auto correlation을 통해 마지막 feed forward로 최종 예측하는 형태입니다. Trend와 cyclic 데이터 정보를 활용하기 위해 skip connection으로 최종 예측에 반영합니다.

![main.png](/images/autoformer/main.png){:, .align-center}

트랜스포머를 자세히 설명하지 않았지만 시계열 데이터간에 관계를 계산하기 위해 Query, Key, Value라는 개념이 있습니다. 단순하게 말하자면, 어떻게 시계열 데이터끼리 여러 경우의 수를 matrix 형태로 조합해 계산할까하다가 아 3개 matrix로 행렬 곱으로 잘 조합해서 관계 score을 구해 어떤 데이터끼리 더 영향이 있는 가를 계산합니다.

이 논문에서는 이 시계열 데이터 간에 관계성을 Auto correlation을 반영해서 계산해보자가 핵심입니다. 물론 Series Decomposition을 통해 시계열 데이터를 좀 더 정확하게 분석하고 예측하게 만들었습니다.

## Details

### Series decomposition block

흔히 복잡한 시간 패턴을 학습하기 위해 시계열을 추세(trend), 계절성(seasonality)으로 분리합니다.

$$ X_t = AvgPool(Padding(X)), X\in \mathbb{R}^{L \times d} \\ X_s = X - X_t $$

Average Pooling은 사실 Moving average랑 다르지 않습니다. 그러므로 Average Pooling을 통해 데이터를 Smoothing해 트랜드를 계산 할 수 있습니다.

```python
class moving_avg(nn.Module):
    """
    Moving average block to highlight the trend of time series
    """

    def __init__(self, kernel_size, stride):
        super(moving_avg, self).__init__()
        self.kernel_size = kernel_size
        self.avg = nn.AvgPool1d(kernel_size=kernel_size, stride=stride, padding=0)

    def forward(self, x):
        # padding on the both ends of time series
        front = x[:, 0:1, :].repeat(1, (self.kernel_size - 1) // 2, 1)
        end = x[:, -1:, :].repeat(1, (self.kernel_size - 1) // 2, 1)
        x = torch.cat([front, x, end], dim=1)
        x = self.avg(x.permute(0, 2, 1))
        x = x.permute(0, 2, 1)
        return x
```

위와 같이 코딩할 수 있습니다.

### Auto correlation block

자세한 방법은 아래 그림처럼 논문에 잘 설명 되어 있기에 참조하시기 바랍니다.

![auto-correlation.png](/images/autoformer/auto-correlation.png){:, .align-center}

위에도 말씀드렸듯이, Auto correlation을 계산하는 부분이 핵심이라고 했습니다. 흥미로운 부분만 언급 드리겠습니다.

논문에도 언급했지만 FFT를 통해 Auto correlation을 계산합니다. 왜냐하면 수학적으로 용이하기 때문입니다. 자세히는 설명안하지만 언급하자면 Fourier Transform은 시간 영역에 있는 데이터를 주파수 영역으로 Mapping하는 변환입니다. Auto-correlation을 모두다 계산하려면 Convolution 계산과 비슷합니다. 하지만 Convolution 계산량은 상당하죠. 그런데 FT는 시간 영역의 convolution 계산을 주파수 영역에서 단순 곱셈으로 만듭니다. 단순 곱셈으로 auto correlation을 구하고 다시 시간영역에 inverse시키면 우리가 원하는 Auto correlation을 계산량 적게 구할 수 있습니다.

FT 개념이 어렵다면 이렇게 이해하시길 바랍니다. “자기 상관을 간단하게 계산하기 위해 FT를 사용했다”

```python
# period-based dependencies
        q_fft = torch.fft.rfft(queries.permute(0, 2, 3, 1).contiguous(), dim=-1)
        k_fft = torch.fft.rfft(keys.permute(0, 2, 3, 1).contiguous(), dim=-1)
        print(f"q_fft: {q_fft.shape}")
        res = q_fft * torch.conj(k_fft)
        corr = torch.fft.irfft(res, n=L, dim=-1)
```

위와 같이 torch.fft.rfft를 통해 간단히 계산할 수 있습니다.

## Result

아래 표를 보시면 알 수 있듯이 Informer, logtrans, reformer같은 transformer계열보다 MSE, MAE가 낮은 것을 확인 할 수 있습니다. 즉 시계열 정보를 잃어버리지 않고 잘 추출해서 트랜스포머를 구성한 것을 유추해볼 수 있습니다.

![result.png](/images/autoformer/result.png){:, .align-center}

## Summary

다시 정리해봅시다.

Autoformer는 기존에 트랜스포머 계열이 시계열 고유 정보를 잃어 버리는 것을 해결하기 위해 제안 되었습니다.

어떻게 해결했나요? Auto-correlation, skip-connection, series decomposition을 사용해서 해결 했습니다.

다른 장점은 없나요? auto-corration과 series decomposition을 사용했기 때문에 시계열적 특징도 적절히 추출 되었습니다.

### Reference
논문 - [https://proceedings.neurips.cc/paper/2021/hash/bcc0d400288793e8bdcd7c19a8ac0c2b-Abstract.html](https://proceedings.neurips.cc/paper/2021/hash/bcc0d400288793e8bdcd7c19a8ac0c2b-Abstract.html)