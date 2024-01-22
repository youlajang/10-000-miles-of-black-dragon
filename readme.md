# 🚩2023년도 제주 위성데이터 활용 경진대회 
* **대회 개요** :  [링크](https://aifactory.space/task/2709/overview)



## 🚩 2023년도 제주 위성데이터 활용 경진대회 
* **팀명** : 흑룡만리
* **주제** : 제주 농산물 생산량 예측 AI 모델 개발 프로젝트
* **개발 기간**: 2023/12/27 ~ 2024/01/22



## 🚩 서비스 흐름도
<img width="80%" src="https://github.com/youlajang/10-000-miles-of-black-dragon/assets/137852127/e5075d3c-7158-4d52-80ec-a7747552fd34"/>

* **`dataset`** 폴더에 위성 이미지 압축 파일 압축 해제
* **`train.ipynb`** : 모델 train 
* **`run.py`** : 테스트를 실행

* **함수 정의** 
   * `synthesize.py` : 위성 이미지 RGB 를 합성하여 컬러 이미지로 만드는 함수가 정의
   * `prediction_code.py` : synthesize.py 에서 만든 RGB 합성 이미지를 타일로 만드는 함수, 타일로 만든 numpy 배열을 기반으로 예측하는 함수 정의
   * `calculate.py` :  예측된 결과를 기반으로 실제 면적과 예상 수확량을 계산하는 함수 정의
 


##  🚩 Simple prediction pipeline
    
    dataset_folder_path = 'dataset'
    model_path = 'models/landcover_final_model_70000_128.hdf5'
    
    # 위성 이미지 합성 및 9개 이미지로 분할
    synthesized_img = synthesize_rgb(dataset_folder_path)
    split_image_into_tiles(synthesized_img)
    
    
    """
    예측하고 싶은 위치를 선택합니다 
            ['left_1', 'center_1', 'right_1']
            ['left_2', 'center_2', 'right_2'] 
            ['left_3', 'center_3', 'right_3']        
    """
    
    # 9개 구역 중 예측 원하는 구역을 선택한
    loc = 'center_2'
    split_image = os.path.join('split_image', f'{loc}.tif')
    
    # 예측한 이미지를 tile 로 자른 후 예측을 실행
    tiles = tile_image(split_image)
    predictions, df_predictions  = predict_tiles(tiles, model_path, num_class=9)
    
    
    # 예측결과를 csv 파일로 저장
    csv_file_path = f'prediction_{loc}_result.csv'
    df_predictions.to_csv(csv_file_path)
    
    
    # 이미지의 모든 라벨을 픽셀당 실제 면적으로 계산
    production_df = calculate_production(csv_file_path, dataset_folder_path)
    print(production_df)
    
    
    # 라벨별로 실제 면적에 단위면적당 생산량을 곱하여 생산량을 계산
    area_df = calculate_real_area(csv_file_path, dataset_folder_path)
    print(area_df)



 
## 🚩 Resources

이 프로젝트에서는 다음과 같은 주 모델과 라이브러리들을 참고했습니다.
- [Unet](https://arxiv.org/abs/1505.04597)
- [EfficientNet](https://arxiv.org/abs/1905.11946)
- [Segmentation_Models](https://github.com/qubvel/segmentation_models)
- [TensorFlow.Keras](https://keras.io/)
- [GDAL](https://gdal.org/index.html)
