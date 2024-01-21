import os
import numpy as np
from osgeo import gdal

def synthesize_rgb(dataset_folder):
    # 디렉토리에서 파일명 리스트 생성
    file_list = os.listdir(dataset_folder)

    # PR, PG, PB로 끝나는 파일을 찾아서 각각 불러오기
    pr_file = [file for file in file_list if file.endswith('PR.tif')][0]
    pg_file = [file for file in file_list if file.endswith('PG.tif')][0]
    pb_file = [file for file in file_list if file.endswith('PB.tif')][0]

    # 파일 경로
    pr_path = os.path.join(dataset_folder, pr_file)
    pg_path = os.path.join(dataset_folder, pg_file)
    pb_path = os.path.join(dataset_folder, pb_file)

    # Open tif file
    pr_ds = gdal.Open(pr_path)  # Red channel
    pg_ds = gdal.Open(pg_path)  # Green channel
    pb_ds = gdal.Open(pb_path)  # Blue channel

    # READ NUMPY AS ARRAY
    pr = pr_ds.ReadAsArray().astype(np.float32)
    pg = pg_ds.ReadAsArray().astype(np.float32)
    pb = pb_ds.ReadAsArray().astype(np.float32)

    # Combine channels to create RGB image
    rgb = np.dstack((pr, pg, pb))

    # Normalize the RGB data
    rgb_norm = ((rgb - np.min(rgb)) / (np.max(rgb) - np.min(rgb)) * 255).astype(np.uint8)

    # 기존 파일명에서 PG를 RGB로 바꾸기
    new_filename = pg_file.replace("_PG.tif", "_RGB.tif")

    # Create a new geotiff file with the same projection as the input file
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(new_filename, rgb_norm.shape[1], rgb_norm.shape[0], 3, gdal.GDT_Byte)

    # Write the data to the file
    for i in range(3):
        out_band = out_ds.GetRasterBand(i + 1)
        out_band.WriteArray(rgb_norm[:, :, i])

    # Close the file
    out_ds = None

    # 새롭게 생성한 파일의 이름을 반환합니다.
    return new_filename


from osgeo import gdal
import os

from osgeo import gdal
import os

def split_image_into_tiles(image_path, output_folder='split_image'):
    # 이미지 불러오기
    ds = gdal.Open(image_path)

    # 이미지를 3x3 그리드로 분할하기 위한 준비
    tile_size_x = ds.RasterXSize // 3
    tile_size_y = ds.RasterYSize // 3

    positions = [
        ['left_1', 'center_1', 'right_1'], 
        ['left_2', 'center_2', 'right_2'], 
        ['left_3', 'center_3', 'right_3']
    ]

    # output_folder가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(0, 3):
        for j in range(0, 3):
            xoff = j * tile_size_x
            yoff = i * tile_size_y

            # 새로운 파일 경로 생성
            output_path = os.path.join(output_folder, f'{positions[i][j]}.tif')

            # 새로운 파일 생성
            out_ds = gdal.GetDriverByName('GTiff').Create(output_path, tile_size_x, tile_size_y, ds.RasterCount)
            out_ds.SetGeoTransform((ds.GetGeoTransform()[0] + xoff, ds.GetGeoTransform()[1], 0, ds.GetGeoTransform()[3] - yoff, 0, ds.GetGeoTransform()[5]))

            for band in range(ds.RasterCount):
                data = ds.GetRasterBand(band+1).ReadAsArray(xoff, yoff, tile_size_x, tile_size_y)
                out_ds.GetRasterBand(band+1).WriteArray(data)
            
            # 파일 닫기
            out_ds = None

    # 원본 파일 닫기
    ds = None

    print(f"Image split into tiles and saved in '{output_folder}' directory.")
