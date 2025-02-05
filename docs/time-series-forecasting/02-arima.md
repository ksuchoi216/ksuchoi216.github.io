---
title: ARIMA
parent: Time Series Forecasting
nav_order: 2
---



이 글을 읽는다면 아래 내용을 얻어가게 됩니다.
- ARIMA가 무엇인지
- 자기회기(AR) 모델이 무엇인지
- 이동평균(MA) 모델이 무엇인지
- ARIMA 파이썬 실행법

![main.png](/images/arima/main.png){:, .align-center}
## ARIMA

ARIMA 모델을 이해하기 위해 영어 약자를 풀어 설명하면 쉬워요. \ AutoRegressive Integrated Moving Average = AutoRegressive + Moving Average를 합친 모델이구나. \ 우린 이제 Autoregressive 모델과 Moving average 모델이 무엇인지 알기만 하면 됩니다.

### 시계열 예측 모델에서 중요한 점?

모델은 어떤 입력을 통해 어떤 출력을 만들어 낼 수 있는 함수(박스)를 말합니다. 아래 그림과 같이 이해하면 편하죠.

시계열 예측 모델도 마찬가지입니다. 어떤 입력으로 미래를 예측할 수 있을까?(모델 가정) 대답이 시계열 모델입니다. 일반적으로 어떤 입력을 쓰일까요? 과거값을 가지고 미래를 예측해보자라는 생각으로 만든 것이 자기 회기(AR) 모델입니다. 과거 예측 오차로 미래를 예측해보자가 이동 평균(MA) 모델입니다. 이 두 가지를 다 섞은게 ARIMA입니다. 그럼 하나 씩 살펴보죠.

### Autoregressive(자기회기) 모델

Auto(자기 스스로)+regressive(회기 모델)입니다. Auto는 Autocorrelation 처럼 시간 지연(lagged)된 값을 입력으로 들어간다는 말입니다. 시간 지연은 $y_{t-1}, y_{t-2}, \cdots$ 같은 t(현재시점)보다 뒤에 있는 과거 이야기합니다. 정리해봅시다. 쉽게 말해, Autoregressive 모델은 시간 지연 ($y_{t-1}, y_{t-2}, \cdots$)을 입력으로 하는 회기 모델입니다.

$$ y_{t} = c + \phi_{1}y_{t-1} + \phi_{2}y_{t-2} + \dots + \phi_{p}y_{t-p} + \varepsilon_{t}, $$

이러한 모델을 AR(p) 모델이라 한다. 여기서 p는 얼만큼 시간 지연된 값을 입력으로 넣을 것인가를 나타낸다. 예를 들어 p=2이면 아래와 같은 모델을 사용합니다.

$$ y_{t} = c + \phi_{1}y_{t-1} + \phi_{2}y_{t-2} $$

### Moving average 모델

자기회기 모델과 다르게 과거 값(시간 지연 된 값) 대신 과거 예측 에러로 회기 모델을 만듭니다. 과거 예측 에러로 회기모델을 만든다라는 말을 좀 더 쉽게 서명해봅시다.

$$ y_{t} = c + \varepsilon_t + \theta_{1}\varepsilon_{t-1} + \theta_{2}\varepsilon_{t-2} + \dots + \theta_{q}\varepsilon_{t-q}, $$

### ARIMA 모델

ARIMA 모델은 앞에서 설명했듯이 Autoregression 모델과 Moving Average 모델을 결합한 모델입니다. 추가적으로 데이터 자체를 차분에 대한 값도 반영합니다. 말이 어려우니 수식으로 보시죠.

$$ y'_{t} = c + \phi_{1}y'_{t-1} + \cdots + \phi_{p}y'*{t-p}

- \theta*{1}\varepsilon_{t-1} + \cdots + \theta_{q}\varepsilon_{t-q} + \varepsilon_{t}, \tag{9.1} $$

$y'$은 차분 값을 나타냅니다. $\phi$는 자기회기(AR) 모델의 과거 값을 말하며 $\varepsilon$은 이동평균(MA)의 과거 예측 에러라고 보시면 됩니다. 다시 말해 식을 아래와 같이 정리할 수 있습니다.

얼마나 차분을 할래?에 대한 결정을 상수 d를 선택하여 \ $$ p \rightarrow y' \rightarrow \textit{difference(차분) 결정} $$

얼마나 과거값을 사용할래?에 대한 결정을 상수 p를 선택하여 \ $$ p \rightarrow y'_{t-p} \rightarrow \textit{AR model 결정} $$

얼마나 과거 예측 에러를 사용할래?에 대한 결정을 상수 q를 선택하여 \ $$ p \rightarrow \varepsilon_{t-q} \rightarrow \textit{MA model 결정} $$

## 지금까지 배운 것 복습!

ARIMA는 자기회기 모델(AR)과 이동평균 모델(MA) 및 차분을 조합해 예측하는 모델이다.

## 참고 자료
fpp3 - https://otexts.com/fpp3/arima.html