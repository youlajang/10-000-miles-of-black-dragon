import os
import glob
import xml.etree.ElementTree as ET
import pandas as pd

pd.options.display.float_format = None




def parse_collected_gsd(dataset_folder_path):
    # 'dataset' 폴더 안에서 .xml 확장자를 가진 파일의 경로 찾기
    xml_file_paths = glob.glob(os.path.join(dataset_folder_path, '*.xml'))

    # 첫 번째 xml 파일의 경로를 선택
    file_path = xml_file_paths[0]

    # XML 파일 파싱
    tree = ET.parse(file_path)
    root = tree.getroot()

    # <CollectedGSD> 태그 찾기
    collected_gsd = root.find('.//CollectedGSD')

    # <Column>과 <Row> 태그의 값 가져오기
    column = float(collected_gsd.find('Column').text)
    row = float(collected_gsd.find('Row').text)

    return column, row


def calculate_real_area(csv_file_path, dataset_folder_path):
    # csv 파일 읽기
    df = pd.read_csv(csv_file_path)

    # 첫 번째 열(행 이름)을 제외한 나머지 열의 합계 계산
    column_sums = df.iloc[:, 1:].sum()

    # 'tile_total'이라는 행 이름과 함께 결과 저장
    result_df = pd.DataFrame(column_sums).transpose()
    result_df.insert(0, "", 'tile_total')

    column, row = parse_collected_gsd(dataset_folder_path)
    pixel_area = column * row

    # 결과 데이터프레임의 모든 값을 픽셀당 실제 면적으로 변환
    real_area_df = result_df.iloc[:, 1:].multiply(pixel_area)

    # 열 이름 변경
    label_dict = {
        "0": '흰 배경',
        "1": '무',
        "2" : '당근',
        "3": '양배추',
        "4": '마늘',
        "5": '양파',
        "6": '브로콜리',
        "7": '기타(농경작지)',
        "8": '기타(기타)'
    }
    real_area_df.rename(columns=label_dict, inplace=True)

    return real_area_df





def calculate_production(csv_file_path, dataset_folder_path):
    # calculate_real_area 함수를 호출하여 실제 면적 데이터프레임을 얻음
    real_area_df = calculate_real_area(csv_file_path, dataset_folder_path)

    # 라벨 이름과 생산량 매핑
    product_dict = {
        '흰 배경': 0,
        '무': 6.960,
        '당근': 3.399,
        '양배추': 5.885,
        '마늘': 1.400,
        '양파': 5.705,
        '브로콜리': 0,
        '기타(농경작지)': 0,
        '기타(기타)': 0
    }

    # 라벨별로 실제 면적에 단위면적당 생산량을 곱하여 생산량을 계산
    for label, production in product_dict.items():
        if label in real_area_df.columns:
            real_area_df[label] = real_area_df[label] * production

    return real_area_df
