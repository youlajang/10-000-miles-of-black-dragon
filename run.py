import os
import pandas as pd 
from synthesize import synthesize_rgb, split_image_into_tiles
from prediction_code import tile_image, predict_tiles 
from calculate import parse_collected_gsd,  calculate_real_area,calculate_production

dataset_folder_path = 'E:/01_AIFactory/01_jejudata/00_basedataset/Clipping_unzip'
model_path = 'models/landcover_final_model_70000_128.hdf5'

# 위성 이미지 합성 및 9개 이미지로 split 한다. 
synthesized_img = synthesize_rgb(dataset_folder_path)
split_image_into_tiles(synthesized_img)


"""
예측하고 싶은 위치를 선택합니다 
        ['left_1', 'center_1', 'right_1']
        ['left_2', 'center_2', 'right_2'] 
        ['left_3', 'center_3', 'right_3']        
"""

# 9개 구역 중 예측 원하는 구역을 선택한다 
loc = 'center_2'
split_image = os.path.join('split_image', f'{loc}.tif')

# 예측한 이미지를 tile 로 자른 후 예측을 실행한다. 
tiles = tile_image(split_image)
predictions, df_predictions  = predict_tiles(tiles, model_path, num_class=9)


# 예측결과를 csv 파일로 저장한다.  
csv_file_path = f'prediction_{loc}_result.csv'
df_predictions.to_csv(csv_file_path)



# 이미지의 모든 라벨을 픽셀당 실제 면적으로 계산한다. 
production_df = calculate_production(csv_file_path, dataset_folder_path)
print(production_df)


# 라벨별로 실제 면적에 단위면적당 생산량을 곱하여 생산량을 계산한다. 
area_df = calculate_real_area(csv_file_path, dataset_folder_path)
print(area_df)

