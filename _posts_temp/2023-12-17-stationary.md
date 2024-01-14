---
title: '시간에 따라 변하는 시계열 데이터는 안돼! - 정상성'
excerpt_separator: '<!--more-->'
categories:
   - Time-series
tags:
   - None
# image:
#     path: ./images/2023-12-17-0.jpg
#     thumbnail: ./images/2023-12-17-0.jpg
#     caption: 
# hidden: true
---

시계열 분석 및 예측에 기초 중 기초 정상성에 대해 알아봅시다.
이 글을 읽는다면 아래 내용을 얻어가게 됩니다.
* 정상성이 무엇인지 그리고 왜 필요한지
* 어떻게 정상성을 확인 할 수 있는지
* 정상성인 시계열 데이터를 다루는 법

<!--more-->

들어가기 전에, 새로운 용어가 나왔을 때는 어원이나 한자를 보는게 이해에 도움이 된다.
한자로는 정할 정에 항상 항을 항상 변한지 않는다(영어로는 station 머물러 있는 느낌)라고 이해하면 쉽겠다.

## 1. 정상성
### 1.1. 정상성(Stationary)이란?
정상성은 과거 시간에 변함 없음을 나타내는 통계량이다. 현재가 과거 시간에 영향을 받는지는 시계열 예측을 하는데 있어 중요하다.
왜냐하면 시계열 예측은 과거의 패턴이 현재에도 유지되어 동일하거나 비슷하게 나타난다라고 가정을 하기 때문이다.
예를 들어, 여름에 증가하고 봄 가을에 줄어드는 전기 사용량을 보면 1년을 주기로 반복되는 계절성(Seasonality)이 있기에 정상성이지 않으며 시계열 예측이 잘 된다.
반대로 노이즈는 어떠한가? 노이즈는 어느 시간 대나 일정하다. 내가 하루 전에 노이즈를 측정한다고 달라지지 않는다. 그래서 노이즈는 정상성이다고 말한다.

### 1.2. 우린 정상성을 이해했다. 그런데 왜 정상성을 이해해야할까?
눈치 빠른 독자라면 앞에 예시를 드는 것을 보고 눈치 챘을 것이다. 정상성을 확인하는 이유는 시계열 패턴이 있어 예측이 가능한지 안한지를 확인 하기 위함이다.

### 1.3. 어떻게 정상성을 확인 할 수 있을까?
ACF(Auto-correlation Function) plot(한국어로 그래프 느낌)과 PACF(Partial Auto-Correlation Function) plot을 보고 체크하면 된다.
<!-- TODO: ACF and PACF -->

<!-- ![acf-normal](./images/20231217/acf.jpg){: .align-center} -->
<!-- ![acf-diff](./images/20231217/acf.jpg){:, .align-center} -->

왼쪽은 정상성이 아닌 시계열 데이터이며 오른쪽은 정상성인 시계열 데이터이다. 파란색 영역이 p-value 0.05이하를 나타낸다.
<!-- TODO: p-value 설명 -->

```python
data = google["2015":"2015"]
close_data = data["Close"]
sm.graphics.tsa.plot_acf(close_data)
plt.show()

diff_close_data = data["Close"].diff().dropna()
sm.graphics.tsa.plot_acf(diff_close_data, lags=np.r_[1:31])
plt.show()
```

**만약 정상성인 시계열 데이터를 다룬다면 어떻게 할까?**
답부터 말하자면 차분(differencing)을 하면 된다. 차분은 정상성이 아닌(non-sationary) 시계열 데이터를 만드는 가장 쉬운 방법인다.
<!-- ![acf-normal](./images/20231217/acf.jpg){: .align-center} -->
<!-- ![acf-diff](./images/20231217/acf.jpg){:, .align-center} -->
왼쪽은 정상성이 아닌(시간에 따라 달라진다) 시계열 데이터 오른쪽은 정상성인 시계열 데이터이다. 

## 2. 지금까지 배운 것 복습!
정상성(시간에 따라 변화하지 않는다)인 시계열 데이터이면 예측이 더 정확해진다. 만약 정상성이 확보되지 않는 시계열 데이터라면, 차분을 이용해 정상성을 확보해보자.

## 3. 참고 자료
시계열 예측에 있어 바이블인 Rob Hyndman 교수님의 책 'Forecasting principles and practice 3rd' 내용을 바탕으로 내용을 구성했습니다.
자세한 사항은 [**FPP 3rd**](https://otexts.com/fpp3/) 참조해주세요.
