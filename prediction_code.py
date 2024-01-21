
import os
import cv2
import numpy as np
from glob import glob
from scipy.io import loadmat
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import shutil

from zipfile import ZipFile
import tempfile

import segmentation_models as sm
from tensorflow.keras.metrics import MeanIoU
import random
from osgeo import gdal

from sklearn.preprocessing import MinMaxScaler
from keras.utils import to_categorical

def tile_image(image_path, tile_size=(128, 128)):
    """ 이미지를 지정된 크기의 타일로 분할하는 함수 """

    # Open tif file and read as array
    image_ds = gdal.Open(image_path)
    image = image_ds.ReadAsArray().astype(np.float32)
    
    tiles = []
    for y in range(0, image.shape[1], tile_size[0]):
        for x in range(0, image.shape[2], tile_size[1]):
            if (y + tile_size[0] > image.shape[1]) or (x + tile_size[1] > image.shape[2]):
                # If the tile size exceeds the image size, skip this tile
                continue
            tile = image[:, y:y+tile_size[0], x:x+tile_size[1]]
            
            # 축 변경 (CHW -> HWC)
            tile = np.transpose(tile, (1, 2, 0))

            # 정규화
            tile = tile / np.max(tile)
            
            tiles.append(tile)
    return tiles



def predict_tiles(tiles, model_path, num_class=9):
    from sklearn.preprocessing import MinMaxScaler
    from keras.utils import to_categorical
    from tensorflow.keras.applications.efficientnet import preprocess_input
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.models import load_model
    import segmentation_models as sm
    import tensorflow as tf
    import pandas as pd
    import numpy as np
    from tensorflow.keras.layers import Dropout 
    import cv2

    #Scale images
    BACKBONE = 'efficientnetb7'

    def preprocess_data(img, num_class):
        img = preprocess_input(img)  #Preprocess based on the pretrained backbone...
        return img

    def testGenerator(tiles, num_class):
        for img in tiles:
            blurred = cv2.GaussianBlur(img, (0, 0), 2.0)  # 이미지를 블러링하여 흐릿하게 만듦
            img = cv2.addWeighted(img, 2.5, blurred, -1.5, 0)  # 원본 이미지와 흐릿한 이미지를 섞어 선명도를 높임
            img = preprocess_data(img, num_class)
            img = np.expand_dims(img, axis=0)  # Add batch dimension
            yield img

    test_img_gen = testGenerator(tiles, num_class)

    # 모델 로드
    model = load_model(model_path, compile=False, custom_objects={'FixedDropout': Dropout})

    # 모델 컴파일
    model.compile('Adam', loss=sm.losses.categorical_focal_jaccard_loss, metrics=[sm.metrics.iou_score])

    # 모델 예측
    steps = int(len(tiles))
    predictions = model.predict(test_img_gen, steps=steps) 

    # 데이터프레임 초기화
    df_predictions = pd.DataFrame(columns=[str(i) for i in range(num_class)])

    # 예측 결과를 데이터프레임으로 변환
    for i in range(len(predictions)):
        prediction = predictions[i]
        predicted_img_array = np.argmax(prediction, axis=-1).astype('uint8')
        pixel_counts = {str(label): np.sum(predicted_img_array == label) for label in range(num_class)}
        df_temp = pd.DataFrame(pixel_counts, index=[f"tile_{i}"])
        df_predictions = pd.concat([df_predictions, df_temp], axis=0)


    return predictions, df_predictions
