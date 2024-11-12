# 라이브러리 불러오기
import os
import random
import pandas as pd
from PIL import Image as PILImage
import numpy as np
from tqdm import tqdm
from IPython.display import display, HTML
import base64
import time

# 데이터셋 경로
dataset1_path = "path/to/A_data/root"
dataset2_path = "path/to/B_data/root"

def image_to_base64(image_path):
    """이미지 파일을 Base64 인코딩된 문자열로 변환합니다."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def compare_entire_image(img1, img2):
    """두 이미지의 모든 픽셀을 비교하여 동일한지 확인합니다."""
    if img1.size != img2.size:
        return False

    img1_array = np.array(img1)
    img2_array = np.array(img2)

    return np.array_equal(img1_array, img2_array)

def get_labels_from_text_file(labels_dir, image_file):
    """라벨 디렉토리에서 이미지 파일과 동일한 이름의 텍스트 파일에서 모든 라벨을 추출합니다."""
    label_file = os.path.join(labels_dir, os.path.splitext(image_file)[0] + '.txt')
    with open(label_file, 'r') as f:
        return f.read().strip().splitlines()

def partial_overlap(dataset1_path, dataset2_path, percentage=100):
    """하나라도 같은 라벨이 있으면 중복으로 처리하는 방식."""
    dataset1_images = os.path.join(dataset1_path, 'images')
    dataset1_labels = os.path.join(dataset1_path, 'labels')
    dataset2_images = os.path.join(dataset2_path, 'images')
    dataset2_labels = os.path.join(dataset2_path, 'labels')

    dataset1_files = os.listdir(dataset1_images)
    dataset2_files = os.listdir(dataset2_images)

    # A 데이터셋에서 비교할 이미지 수 결정
    num_to_compare = max(1, int(len(dataset1_files) * (percentage / 100)))
    selected_files = random.sample(dataset1_files, num_to_compare)

    results = []

    start_time = time.time()  # 시작 시간 기록

    for img1_file in tqdm(selected_files, desc="Partial Overlap"):
        img1_path = os.path.join(dataset1_images, img1_file)
        with PILImage.open(img1_path) as img1:
            for img2_file in dataset2_files:
                img2_path = os.path.join(dataset2_images, img2_file)
                with PILImage.open(img2_path) as img2:
                    if compare_entire_image(img1, img2):
                        labels1 = get_labels_from_text_file(dataset1_labels, img1_file)
                        labels2 = get_labels_from_text_file(dataset2_labels, img2_file)
                        if any(label1 == label2 for label1 in labels1 for label2 in labels2):
                            results.append({"standard_data": img1_file, "comparison_data": img2_file})
                            img1_base64 = image_to_base64(img1_path)
                            img2_base64 = image_to_base64(img2_path)
                            display(HTML(f"""
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <img src="data:image/jpeg;base64,{img1_base64}" style="width: 10%;">
                                    <img src="data:image/jpeg;base64,{img2_base64}" style="width: 10%;">
                                </div>
                            """))

    end_time = time.time()  # 종료 시간 기록
    elapsed_time = end_time - start_time  # 총 실행 시간 계산
    print(f"Execution Time: {elapsed_time:.2f} seconds")

    # 중복 이미지 개수
    duplicates_count = len(results)

    # 기준 데이터셋에서 비교한 이미지 수 대비 중복 비율
    standard_data_percentage = (duplicates_count / num_to_compare) * 100
    # 비교 데이터셋의 전체 이미지 수 대비 중복 비율
    comparison_data_percentage = (duplicates_count / len(dataset2_files)) * 100

    print(f"Standard Data Overlap: {standard_data_percentage:.2f}%")
    print(f"Comparison Data Overlap: {comparison_data_percentage:.2f}%")

    # 데이터프레임 생성
    df = pd.DataFrame(results)

    # 경로의 마지막 디렉토리 이름을 칼럼명으로 설정
    col1_name = os.path.basename(os.path.normpath(dataset1_path))
    col2_name = os.path.basename(os.path.normpath(dataset2_path))
    df.columns = [col1_name, col2_name]

    # CSV 파일 이름 설정
    csv_filename = f'duplicate_checks_for_{col1_name}_and_{col2_name}.csv'

    return df, csv_filename

partial_overlap_df, csv_filename = partial_overlap(dataset1_path, dataset2_path, percentage=100)

print("Partial Overlap Results:")
print(partial_overlap_df)

# 데이터프레임을 CSV 파일로 저장
partial_overlap_df.to_csv(csv_filename, index=False)
print("csv 파일 저장 완료!")