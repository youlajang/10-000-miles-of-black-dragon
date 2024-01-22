# 🚩2023년도 제주 위성데이터 활용 경진대회 
* **대회 개요** : 위성데이터를 활용하여 제주섬의 문제를 발견하고 이를 해결할 수 있는 아이디어 및 사업모델 제안 [링크](https://aifactory.space/task/2709/overview)



## 🚩 2023년도 제주 위성데이터 활용 경진대회 
* **팀명** : 흑룡만리
* **주제** : 제주 농산물 생산량 예측 AI 모델 개발 프로젝트
* **개발 기간**: 2023/12/27 ~ 2024/01/22



## 🚩 서비스 흐름도
<img width="80%" src="https://github.com/youlajang/10-000-miles-of-black-dragon/assets/137852127/e5075d3c-7158-4d52-80ec-a7747552fd34"/>


   1. Pan-sharpened Image File 을 합성하여 RGB 파일 생성(.tif)
   2. RGB 파일을 9개 구역으로 나누어 원하는 구역 선택. Model 에 input 할 수 있게 128*128 타일로 분할 
   3. 모델을 통해 픽셀별 라벨값 예측 
   4. Auxiliary File의 <CollectedGSD> 값을 사용하여 라벨별 실제 면적 예측
   5. 제주 농업 기술 센터 단위 면적당 생산량을 활용한 예상 생산량 도출 


## 🚩 파일 구성 

* **`dataset`** 폴더에 위성 이미지 압축 파일 압축 해제
* **`train_code`** : 모델 train 코드
* **`models`** : 학습된 모델 다운로드 (구글드라이브 링크) 

* **`run.py`** : 테스트를 실행

* **함수 정의** 
   * `synthesize.py` : 위성 이미지 RGB 를 합성하여 컬러 이미지로 만드는 함수가 정의
   * `prediction_code.py` : synthesize.py 에서 만든 RGB 합성 이미지를 타일로 만드는 함수, 타일로 만든 numpy 배열을 기반으로 예측하는 함수 정의
   * `calculate.py` :  예측된 결과를 기반으로 실제 면적과 예상 수확량을 계산하는 함수 정의


 
## 🚩 Resources

이 프로젝트에서는 다음과 같은 주 모델과 라이브러리들을 참고했습니다.
- [Unet](https://arxiv.org/abs/1505.04597)
- [EfficientNet](https://arxiv.org/abs/1905.11946)
- [Segmentation_Models](https://github.com/qubvel/segmentation_models)
- [TensorFlow.Keras](https://keras.io/)
- [GDAL](https://gdal.org/index.html)
