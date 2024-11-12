# 라이브러리 불러오기
import os
import csv

# 데이터 경로
input_directory = "path/to/labels/root"
output_csv_file1 = "name1.csv" # 변환된 csv 파일의 이름1
output_csv_file2 = "name2.csv" # 변환된 csv 파일의 이름2

# 실제 클래스 이름 리스트
names = ["real_class_name"]

def convert_polygon_to_rectangle(polygon_points):
    x_coordinates = polygon_points[0::2]
    y_coordinates = polygon_points[1::2]
    
    x1 = min(x_coordinates)
    y1 = min(y_coordinates)
    x2 = max(x_coordinates)
    y2 = max(y_coordinates)
    
    return x1, y1, x2, y2

def process_txt_files_to_csv(input_directory, output_csv_file1, names, image_subdirectory="images"):
    with open(output_csv_file1, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write header
        csv_writer.writerow(['filename', 'x1', 'y1', 'x2', 'y2', 'class_label'])
        
        for txt_filename in os.listdir(input_directory):
            if txt_filename.endswith('.txt'):
                # Create the image filename with subdirectory
                image_filename = os.path.join(image_subdirectory, txt_filename).replace('.txt', '.jpg')
                image_filename = image_filename.replace('\\', '/')  # Ensure consistent path format

                file_path = os.path.join(input_directory, txt_filename)
                with open(file_path, 'r') as txt_file:
                    for line in txt_file:
                        parts = line.strip().split()
                        label_index = int(parts[0])  # 라벨 인덱스
                        class_label = names[label_index]  # 인덱스를 통해 클래스 이름 획득
                        polygon_points = list(map(float, parts[1:]))
                        
                        x1, y1, x2, y2 = convert_polygon_to_rectangle(polygon_points)
                        
                        csv_writer.writerow([image_filename, x1, y1, x2, y2, class_label])

def save_names_to_csv(names, output_csv_file2):
    with open(output_csv_file2, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write header
        csv_writer.writerow(['names', 'label'])
        
        # Write data
        for index, name in enumerate(names):
            csv_writer.writerow([name, index])

process_txt_files_to_csv(input_directory, output_csv_file1, names, image_subdirectory="images")
save_names_to_csv(names, output_csv_file2)