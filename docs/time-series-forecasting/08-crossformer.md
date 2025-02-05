---
title: Crossformer
parent: Time Series Forecasting
nav_order: 8
---


기존 트랜스포머 기반 모델들은 cross time dependency 있다는 문제가 있습니다. crossformer는 이러한 cross time dependency를 해결하면서 cross dimension dependency 또한 개선하면서 기존 트랜스포머에 비해 성능을 개선했습니다. 그렇다면 어떻게 해결했는지 살펴봅시다.

<!--more-->

![main.png](/images/crossformer/main.png){:, .align-center}
## Why crossformer is important?

인트로에서 이야기 했듯이 cross time dependency를 해결한 모델이 crossformer 입니다. 그렇다면 cross time dependency가 무엇일까요?
![time_dep.png](/images/crossformer/time_dep.png){:, .align-center}
왼쪽 그림과 같이 데이터를 처리할 때 같은 시간대로 잘라서 입력값으로 반영합니다. 여기서 같은 시간대라는 제약이 걸립니다. 현재는 토요일이고 하루 후 일요일 전기 수요 예측을 한다고 가정하고, 전기 수요 시계열 데이터, 날씨 시계열 데이터가 있다고 가정해봅시다. 미래 전기 수요 예측할 때 꼭 같은 날 수요일 수요 데이터와 시점이 일치한 수요일 날씨 데이터가 들어가야할까요?

이 논문은 여기서 의문을 가집니다. 미래를 예측할 때 수요일 날씨가 아니라 목요일 금요일 날씨가 들어가면 안되는 건가?라는 생각입니다.

다른 시간대의 데이터를 넣는다는 생각 즉 이 논문에서는 DSW와 TSA로 해결합니다. cross dependency를 해결합니다.

그렇다면 DSW와 TSA가 무엇일까요?

## What is conformer?

conformer는 시계열 데이터를 잘라서 임베딩(벡터형태로 만드는)하는 **DSW(dimension-segmevwise embedding)**과 실제로 transformer을 구현하는 **TSA(two-stage-attention)**이 있습니다. 이 TSA 트랜스포머는 간단히 말해 DSW를 통해 나누어진 time segment들을 잘 섞는 cross time 부분과 feature들을 잘 섞는 cross dimension 부분으로 총 2개 stage로 구성된 attention을 사용합니다.

쉽게 말해, time segment를 만들어 서로다른 time의 조합을 만들어서 학습하고 feature의 조합을 만들어 학습하는 구조라고 이해하시면 됩니다.

그러면 좀 더 자세히 DSW와 TSA를 이해해보죠

## How does it work?

### DSW

DSW은 시계열 데이터를 time segment(시간을 기준으로 자름)를 만들어 embedding한다고 했습니다.
![dsw.png](/images/crossformer/dsw.png){:, .align-center}
아래 그림과 같이 Segment length만큼 seq_y를 선택하여 Feed forward에 넣어 차원을 줄여 embedding을 합니다. 여기서 중요한 것은 DSW 의미입니다. DSW는 time segment를 만들어 새로운 축을 만든 것과 같습니다. 단순하게 이야기하자면 시간 축으로 잘 잘라 벡터화 만들었나고 이해하시면 됩니다.


```python
class DSW_embedding(nn.Module):
    def __init__(self, seg_len, d_model):
        super(DSW_embedding, self).__init__()
        self.seg_len = seg_len

        self.linear = nn.Linear(seg_len, d_model)

    def forward(self, x):
        batch, ts_len, ts_dim = x.shape

        x_segment = rearrange(x, 'b (seg_num seg_len) d -> (b d seg_num) seg_len', seg_len = self.seg_len)
        x_embed = self.linear(x_segment)
        x_embed = rearrange(x_embed, '(b d seg_num) d_model -> b d seg_num d_model', b = batch, d = ts_dim)
        
        return x_embed
```

### TSA

TSA는 말 그대로 2개의 stage가 존재하는데 cross time과 cross dimension입니다.

**[cross time stage]**

말 그대로 시간 segment를 잘 섞어 주는 부분이라고 보시면 됩니다. 어떻게 섞을 것이냐라고 하면 차원을 조정해서 self-attention의 입력인 Query, Key, Value로 각각 넣게 됩니다.

차원 조정을 텐서로 보자면 (batch, feat, seg, emb) → ((batch, feat), **seg,** emb) 이런 식으로 합니다. 여기서 batch는 batch size이며 feat은 feature dimension이고 seg은 time segment 개수이고 emb은 embedding dimension입니다.

뒤에 seg, emb만 잘 섞기 위해 이렇게 차원을 조정하는 구나 정도 이해하지면 됩니다. time segment가 잘 섞이므로 cross time이라고 논문에서는 이야기하고 있습니다.

```python
  #Cross Time Stage: Directly apply MSA to each dimension
  batch = x.shape[0]
  time_in = rearrange(x, 'b ts_d seg_num d_model -> (b ts_d) seg_num d_model')
  time_enc = self.time_attention(
      time_in, time_in, time_in
  )
  dim_in = time_in + self.dropout(time_enc)
  dim_in = self.norm1(dim_in)
  dim_in = dim_in + self.dropout(self.MLP1(dim_in))
  dim_in = self.norm2(dim_in)
```

**[cross dimension stage]**

비슷한 방식으로 차원 조정을 통해 self-attention 입력을 조정해서 차원을 잘 섞습니다.

((batch, feat), seg, emb) → ((batch, seg), **feat,** emb) 이런 식으로 잘 섞어 줍니다.

위와 마찬가지로 batch는 batch size이며 feat은 feature dimension이고 seg은 time segment 개수이고 emb은 embedding dimension입니다.

```python
#Cross Dimension Stage: use a small set of learnable vectors to aggregate and distribute messages to build the D-to-D connection
dim_send = rearrange(dim_in, '(b ts_d) seg_num d_model -> (b seg_num) ts_d d_model', b = batch)
batch_router = repeat(self.router, 'seg_num factor d_model -> (repeat seg_num) factor d_model', repeat = batch)
dim_buffer = self.dim_sender(batch_router, dim_send, dim_send)
dim_receive = self.dim_receiver(dim_send, dim_buffer, dim_buffer)
dim_enc = dim_send + self.dropout(dim_receive)
dim_enc = self.norm3(dim_enc)
dim_enc = dim_enc + self.dropout(self.MLP2(dim_enc))
dim_enc = self.norm4(dim_enc)

final_out = rearrange(dim_enc, '(b seg_num) ts_d d_model -> b ts_d seg_num d_model', b = batch)
```

물론 차원 복잡도를 낮추기 위해 cross dimension stage에서 router를 사용합니다.

아래 그림을 보시면 (b)가 router를 쓰기전 (c)가 router를 쓴 후인데 일종에 고정된 파라미터 수 안에서 입력을 만들어 경우의 수를 줄였습니다. attention에서 입력으로 Query, Key, Value로 각각 넣게 되는데 Query은 모든 조합이 아니라 router를 이용해 만든 입력을 넣게 됩니다.


![cross_dim.png](/images/crossformer/cross_dim.png){:, .align-center}
## Result

이렇게 시간도 잘 조합하고 차원도 잘 조합하니 다른 트랜스포머 보다 좋은 결과를 다양한 데이터에서 냈습니다.

![res1.png](/images/crossformer/res1.png){:, .align-center}
DSW와 TSA가 예측 정확도에 영향을 주는 것도 확인 할 수 있습니다.

![res2.png](/images/crossformer/res2.png){:, .align-center}
## References

**Transformer Utilizing Cross-Dimension Dependency for Multivariate Time Series Forecasting**

```
@inproceedings{wang2021crossformer,
  title = {CrossFormer: A Versatile Vision Transformer Hinging on Cross-scale Attention},
  author = {Wenxiao Wang and Lu Yao and Long Chen and Binbin Lin and Deng Cai and Xiaofei He and Wei Liu},
  booktitle = {International Conference on Learning Representations, {ICLR}},
  url = {<https://openreview.net/forum?id=_PHymLIxuI>},
  year = {2022}
}
```