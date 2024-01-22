# 🚩2023년도 제주 위성데이터 활용 경진대회 

* **대회 개요** :  [링크](https://aifactory.space/task/2709/overview)
* **팀명** : 흑룡만리
* **주제** : 제주 농산물 생산량 예측 AI 모델 개발 프로젝트
* **개발 기간**: 2023/12/27 ~ 2024/01/22



# 🚩 서비스 흐름도
<img width="80%" src="https://github.com/youlajang/10-000-miles-of-black-dragon/assets/137852127/e5075d3c-7158-4d52-80ec-a7747552fd34"/>

* **dataset** 폴더에 위성 이미지 압축 파일 압축 해제
* **train.ipynb** : 모델 train 
* **run.py** : 테스트를 실행

* **함수 정의** 
   * synthesize.py : 위성 이미지 RGB 를 합성하여 컬러 이미지로 만드는 함수가 정의
   * prediction_code.py : synthesize.py 에서 만든 RGB 합성 이미지를 타일로 만드는 함수, 타일로 만든 numpy 배열을 기반으로 예측하는 함수 정의
   * calculate.py :  예측된 결과를 기반으로 실제 면적과 예상 수확량을 계산하는 함수 정의
 


* Quick start

 
# 🚩 Resources

이 프로젝트에서는 다음과 같은 주 모델과 라이브러리들을 참고했습니다.
- [Unet](https://arxiv.org/abs/1505.04597)
- [EfficientNet](https://arxiv.org/abs/1905.11946)
- [Segmentation_Models](https://github.com/qubvel/segmentation_models)
- [tf.keras](https://keras.io/)
- [GDAL](https://gdal.org/index.html)
