---
title: PatchTST
parent: Time Series Forecasting
nav_order: 5
---



<!--more-->

![PatchTST_img_00](/images/PatchTST/PatchTST_img_00.png){:, .align-center}

## 1. 연구자는 어떤 것을 달성하려고 했나요?

- 구조적 특징
    - patct를 이용해 각각 시계열을 나눔
    - 각 channel(multivariable 데이터에서 각 feature을 말함) 독립적으로 학습함.
- 장점
    - embedding을 통해 local 정보를 유지함
    - computation이나 memory 사용을 줄임
    - 더 많은 과거 데이터를 이용함.

## 2. 제시한 방법의 핵심은 무엇인가요?

- patch embedding
    - stride 간격으로 ReplicationPad1d를 이용하여 경계를 복사함 → patch.
    - 각 patch를 value embedding(projection)과 position embedding(위치 정보를 sin & cos화)
- independent channel transformer
    - transformer is used for each channel by changing dimensions

![PatchTST_img_01](/images/PatchTST/PatchTST_img_01.png){:, .align-center}

![PatchTST_img_02](/images/PatchTST/PatchTST_img_02.png){:, .align-center}

## 3. 결과는 어떤가요?

- 데이터, 인풋 데이터 길이에 상관 없이 좋은 성능을 나타냄

[결과 figure]

![PatchTST_img_03](/images/PatchTST/PatchTST_img_03.png){:, .align-center}

## 4. 이 방법의 장점과 단점이 무엇인가요?

- 결국 transformer 기반에 모델이라 computation과 memory의 절대적 한계 존재
- 데이터에 따라 channel indepentance가 유리할 수도 있고 아닐 수도 있음.

**References**

1.