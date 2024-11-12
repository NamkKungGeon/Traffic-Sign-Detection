#라이브러리 불러오기
import os
import shutil
import pandas as pd

# 데이터 경로
csv_file = 'path/to/your/csv/file'
A_data_path = "path/to/A_data/path"
B_data_path = "path/to/B_data/path"
output_path = "path/to/output/path"

def create_dataset_without_duplicates(csv_file, dataset1_path, dataset2_path, output_path):
    """중복을 제외한 데이터셋을 생성하고, 중복 데이터셋을 별도로 저장합니다."""
    # CSV 파일을 읽어 중복 이미지 정보를 로드
    df = pd.read_csv(csv_file)

    # 경로 설정
    A_data_images = os.path.join(A_data_path, 'images')
    A_data_labels = os.path.join(A_data_path, 'labels')
    B_data_images = os.path.join(B_data_path, 'images')
    B_data_labels = os.path.join(B_data_path, 'labels')

    # 중복 이미지 파일 목록
    duplicated_images_A = set(df.iloc[:, 0])  # 기준 데이터셋의 중복 이미지
    duplicated_images_B = set(df.iloc[:, 1])  # 비교 데이터셋의 중복 이미지

    # 출력 경로 설정
    os.makedirs(output_path, exist_ok=True)
    output_images_no_dup_A = os.path.join(output_path, 'dataset1_no_duplicates', 'images')
    output_labels_no_dup_A = os.path.join(output_path, 'dataset1_no_duplicates', 'labels')
    output_images_dup_A = os.path.join(output_path, 'dataset1_duplicates', 'images')
    output_labels_dup_A = os.path.join(output_path, 'dataset1_duplicates', 'labels')
    output_images_no_dup_B = os.path.join(output_path, 'dataset2_no_duplicates', 'images')
    output_labels_no_dup_B = os.path.join(output_path, 'dataset2_no_duplicates', 'labels')
    output_images_dup_B = os.path.join(output_path, 'dataset2_duplicates', 'images')
    output_labels_dup_B = os.path.join(output_path, 'dataset2_duplicates', 'labels')

    # 디렉토리 생성
    os.makedirs(output_images_no_dup_A, exist_ok=True)
    os.makedirs(output_labels_no_dup_A, exist_ok=True)
    os.makedirs(output_images_dup_A, exist_ok=True)
    os.makedirs(output_labels_dup_A, exist_ok=True)
    os.makedirs(output_images_no_dup_B, exist_ok=True)
    os.makedirs(output_labels_no_dup_B, exist_ok=True)
    os.makedirs(output_images_dup_B, exist_ok=True)
    os.makedirs(output_labels_dup_B, exist_ok=True)

    # 기준 데이터셋 처리
    for img_file in os.listdir(A_data_images):
        label_file = os.path.splitext(img_file)[0] + '.txt'
        if img_file in duplicated_images_A:
            shutil.copy(os.path.join(A_data_images, img_file), output_images_dup_A)
            shutil.copy(os.path.join(A_data_labels, label_file), output_labels_dup_A)
        else:
            shutil.copy(os.path.join(A_data_images, img_file), output_images_no_dup_A)
            shutil.copy(os.path.join(A_data_labels, label_file), output_labels_no_dup_A)

    # 비교 데이터셋 처리
    for img_file in os.listdir(B_data_images):
        label_file = os.path.splitext(img_file)[0] + '.txt'
        if img_file in duplicated_images_B:
            shutil.copy(os.path.join(B_data_images, img_file), output_images_dup_B)
            shutil.copy(os.path.join(B_data_labels, label_file), output_labels_dup_B)
        else:
            shutil.copy(os.path.join(B_data_images, img_file), output_images_no_dup_B)
            shutil.copy(os.path.join(B_data_labels, label_file), output_labels_no_dup_B)

create_dataset_without_duplicates(csv_file, A_data_path, B_data_path, output_path)