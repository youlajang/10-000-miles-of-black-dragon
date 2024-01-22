# 2023년도 제주 위성데이터 활용 경진대회

* **팀명** : 흑룡만리
* **주제** : 제주 농산물 생산량 예측 AI 모델 개발 프로젝트
* **개발 기간**: 2023/12/27 ~ 2024/01/22




# 프로젝트 설정 방법
🚩 서비스 흐름도

* dataset 폴더에 원하는 위성 이미지 압축 파일을 풀어줍니다.
    * synthesize.py : 위성 이미지 RGB 를 합성하여 컬러 이미지로 만드는 함수가 정의되어 있습니다. 
    * prediction_code.py : synthesize.py 에서 만든 RGB 합성 이미지를 타일로 만드는 함수, 타일로 만든 numpy 배열을 기반으로 예측하는 함수가 포함되어 있습니다. 
    * 계산식이 포함되어 있습니다. 
    * run.py : 테스트를 실행합니다
 
🚩 서비스 흐름도
