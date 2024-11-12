#라이브러리 불러오기
import os
import pandas as pd

# 데이터 경로
dataset_labels = 'path/to/your/labels/root'

def get_labels_from_text_file(labels_dir, label_file):
    """라벨 디렉토리에서 텍스트 파일에서 모든 라벨을 추출합니다."""
    file_path = os.path.join(labels_dir, label_file)
    with open(file_path, 'r') as f:
        return set(line.strip() for line in f if line.strip())

def find_internal_duplicates_as_dataframe(labels_dir):
    """데이터셋 내부에서 중복 라벨을 가진 파일 쌍과 중복 라벨을 데이터프레임으로 반환합니다."""
    files = os.listdir(labels_dir)
    labels_dict = {}
    duplicate_entries = []

    # 모든 파일의 라벨 수집
    for label_file in files:
        labels = get_labels_from_text_file(labels_dir, label_file)
        labels_dict[label_file] = labels

    # 각 파일의 라벨과 다른 모든 파일의 라벨을 비교
    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            file_i = files[i]
            file_j = files[j]
            common_labels = labels_dict[file_i].intersection(labels_dict[file_j])
            if common_labels:
                duplicate_entries.append({
                    'File 1': file_i,
                    'File 2': file_j,
                    'Common Labels': ', '.join(common_labels)
                })

    # 데이터프레임 생성
    df_duplicates = pd.DataFrame(duplicate_entries)
    return df_duplicates

df_duplicates_in_dataset = find_internal_duplicates_as_dataframe(dataset_labels)

print("Duplicates in Dataset")
print(df_duplicates_in_dataset)
