var store = [{
        "title": "Papers",
        "excerpt":"요즘 공부하고 있는 논문들을 정리한 목록입니다. 시계열 예측, 전력 예측 등에 관심이 있어 공부하고 있습니다. General Forecasting 2023 11 TSMixer An All-MLP Architecture for Time Series Fore- casting.pdf #ts What did the authors try to accomplish? univariate linear models can outperform deep learning stacking MLP What were the key elements...","categories": ["papers"],
        "tags": ["papers"],
        "url": "http://localhost:4000/papers/2020/01/01/papers.html"
      },{
        "title": "통계 기반 예측 기본 - 아리마 ARIMA",
        "excerpt":"이 글을 읽는다면 아래 내용을 얻어가게 됩니다. ARIMA가 무엇인지 자기회기(AR) 모델이 무엇인지 이동평균(MA) 모델이 무엇인지 ARIMA 파이썬 실행법 ARIMA ARIMA 모델을 이해하기 위해 영어 약자를 풀어 설명하면 쉬워요. \\ AutoRegressive Integrated Moving Average = AutoRegressive + Moving Average를 합친 모델이구나. \\ 우린 이제 Autoregressive 모델과 Moving average 모델이 무엇인지 알기만...","categories": ["time-series"],
        "tags": ["stat"],
        "url": "http://localhost:4000/time-series/2023/12/06/arima.html"
      },{
        "title": "1D CNN을 더 길게 만들어보자 TCN",
        "excerpt":"TCN은 CNN kernel의 간격을 넓혀 보다 넓은 시계열 데이터를 사용하기 위해 만들었습니다.CNN가 어떻게 다른지 한 번 보시죠. Why TCN is suggested? 연구진은 RNN, LSTM같은 recurrent networks보다 성능이 더 뛰어난 변형된 CNN을 개발했습니다. 아시다시피 CNN은 1989년도에 Yann LeCun 처음 제안되어 이미지 쪽에 혁신적인 성과를 낸 모델입니다. 하지만 CNN 자체는 localization(커널로 주변과...","categories": ["time-series"],
        "tags": ["cnn"],
        "url": "http://localhost:4000/time-series/2024/01/10/tcn.html"
      },{
        "title": "\"Auto-correlation을 활용한 트랜스포머: Autoformer\"",
        "excerpt":"일단 Autoformer는 기존에 시계열 예측에 사용된 트랜스포머 모델에 시계열 순서 정보를 잃어버리는 고질적 문제를 해결하기 위해 제안되었습니다. 트랜스포머 계열은 시계열 데이터 본래 특징을 잃어버립니다. 시간 순서대로 연결되어 있는 데이터가 시계열 데이터인데 이러한 정보를 트랜스포머 모델들은 반영하지 못합니다. 그렇다면 어떻게 autoformer가 해결했는지 탐험해보겠습니다. What is Autoformer? Autoformer는 Auto-correlation + Transformer을 결합한...","categories": ["time-series"],
        "tags": ["transformer"],
        "url": "http://localhost:4000/time-series/2024/01/28/autoformer.html"
      },{
        "title": "시간도 섞고 피쳐도 섞는 crossformer",
        "excerpt":"기존 트랜스포머 기반 모델들은 cross time dependency 있다는 문제가 있습니다. crossformer는 이러한 cross time dependency를 해결하면서 cross dimension dependency 또한 개선하면서 기존 트랜스포머에 비해 성능을 개선했습니다. 그렇다면 어떻게 해결했는지 살펴봅시다. Why crossformer is important? 인트로에서 이야기 했듯이 cross time dependency를 해결한 모델이 crossformer 입니다. 그렇다면 cross time dependency가 무엇일까요?왼쪽 그림과...","categories": ["time-series"],
        "tags": ["transformer"],
        "url": "http://localhost:4000/time-series/2024/02/03/crossformer.html"
      },{
        "title": "뒤로도 예측 해볼 수 있지 않을까?(backcast) NBEATS",
        "excerpt":"거의 모든 시계열 예측은 forecast라는 앞을 예측을 기반으로 만들어졌다. 그렇다면 backcast라는 현재 기준으로 뒤를 예측을 활용하면 좋지 않을까?즉, NBEATS에서는 forecast과 backcast을 잘 활용하면 더 예측을 향상시키고 싶어했다.그렇다면 어떻게 활용하는지 알아보자. 1. 이루고자 한 것은 무엇인가요? 거의 모든 시계열 예측은 forecast라는 앞을 예측을 기반으로 만들어졌다. 그렇다면 backcast라는 현재 기준으로 뒤를 예측을...","categories": ["time-series"],
        "tags": [],
        "url": "http://localhost:4000/time-series/2024/02/03/nbeats.html"
      },{
        "title": "시간에 따라 변하는 시계열 데이터 판단 - 정상성",
        "excerpt":"시계열 분석 및 예측에 기초 중 기초, 정상성에 대해 알아봅시다.이 글을 읽는다면 아래 내용을 얻어가게 됩니다. 정상성이 무엇인지 그리고 왜 필요한지 어떻게 정상성을 확인 할 수 있는지 정상성인 데이터를 비정상성으로 만드는 법들어가기 전에, 새로운 용어가 나왔을 때는 어원이나 한자를 보는게 이해에 도움이 됩니다.한자로는 정할 정에 항상 항을 항상 변하지 않는다(영어로는...","categories": ["time-series"],
        "tags": ["stat"],
        "url": "http://localhost:4000/time-series/2024/02/03/stationary.html"
      },{
        "title": "시계열 Transformer 보다 Linear mixer가 더 좋아 TSMixer",
        "excerpt":"Transformer가 GPT로 뛰어난 성능을 냈지만 일반적인 시계열 데이터에서 Transformer 모델보단 MLP가 성능이 더 좋라고 이야기하는 논문인 TSMixer를 살펴봅시다. 1. 이 방법이 이루고자 한 것은(Why)? 이 논문이 나오기 전 시계열 예측 연구는 NLP에서 대유행시킨 transformer를 이용한 시계열 예측이 전반적인 연구 였었습니다. 이러한 NLP에서 사용하는 transformer는 문장이라는 추상적 데이터를 이해하고 관계성을 찾아가며...","categories": ["time-series"],
        "tags": ["ts"],
        "url": "http://localhost:4000/time-series/2024/02/07/tsmixer.html"
      }]
