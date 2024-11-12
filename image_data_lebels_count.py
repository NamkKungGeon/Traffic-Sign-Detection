#라이브러리 불러오기
import os
import pandas as pd
import cv2 as cv
import sys
import matplotlib.pyplot as plt
%matplotlib inline

# 데이터 경로
labels_root = "path/to/labels/data/root" # image labels data root
classes_root = "path/to/classes/root" # class root
classes2_root ="path/to/classes/root" # index root

f = open(classes_root, "r")
data = f.read().split()

f = open(classes2_root, "r")
data2 = f.read().split()

first_values = []

for filename in os.listdir(labels_root) :
    file_path = os.path.join(labels_root, filename)

    if filename.endswith('.txt') :
        with open(file_path, "r", encoding = "utf-8") as file :
            lines = file.readlines()

        for line in lines :
            first_value = line.split()[0]
            first_values.append(first_value)

# 각 라벨 요소 별 개수 추가
label_count = []
for i in data2 :
    label_count.append(first_values.count(i))

# 라벨 데이터프레임화 (칼럼에 라벨을 숫자로 쓰지않고 문자 예를 들어, U-Turn 등으로 바꿀 필요가 있으므로 횡으로 바꿀 필요 있음)
label = pd.DataFrame(label_count, columns = ["label_count"])
label

# 그래프 사이즈 설정
plt.figure(figsize=(15, 6))

# 그래프 제목 설정
plt.title("graph_name")

x = data
y = label["label_count"]
bar = plt.bar(x, y, color="skyblue")

# x축 레이블 회전
plt.xticks(rotation=20)

for rect in bar:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%.1f' % height, ha='center', va='bottom', size=8)

# 총합 계산 및 그래프에 표시
total_count = sum(label["label_count"])
plt.text(len(x) - 1, max(y) * 1.05, f'Total: {total_count}', ha='center', va='bottom', size=10, fontweight='bold', color='red')

# 그래프 저장 (선택사항)
plt.savefig("saving_name.png")
plt.show()