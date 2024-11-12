# 라이브러리 불러오기
import csv
import xml.etree.ElementTree as ET
import os
from PIL import Image

# 데이터 경로
csv_file_path = "path/to/csv/name.csv"
output_dir = "path/to/saving/directory"
image_path = "path/to/images/root"

def get_image_size(image_path):
    with Image.open(image_path) as img:
        return img.size  # (width, height)

def csv_to_voc_xml(csv_file_path, output_dir):
    # 출력 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 이미지별 객체 정보를 저장할 딕셔너리 초기화
    images = {}

    # CSV 파일 읽기
    with open(csv_file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        headers = next(csvreader)  # 첫 번째 행은 헤더로 사용
        for row in csvreader:
            image_path, x1, y1, x2, y2, class_name = row

            if image_path not in images:
                images[image_path] = []

            images[image_path].append({
                'class_name': class_name,
                'bndbox': (int(float(x1)), int(float(y1)), int(float(x2)), int(float(y2)))
            })

    # 각 이미지에 대해 XML 파일 생성
    for image_path, objects in images.items():
        annotation = ET.Element('annotation')
        
        ET.SubElement(annotation, 'folder').text = os.path.dirname(image_path)
        ET.SubElement(annotation, 'filename').text = os.path.basename(image_path)
        ET.SubElement(annotation, 'path').text = image_path
        
        source = ET.SubElement(annotation, 'source')
        ET.SubElement(source, 'database').text = 'Unknown'
        
        size = ET.SubElement(annotation, 'size')
        
        # 이미지 크기 추출 및 설정
        width, height = get_image_size(image_path)
        ET.SubElement(size, 'width').text = str(width)
        ET.SubElement(size, 'height').text = str(height)
        ET.SubElement(size, 'depth').text = '3'  # 보통 컬러 이미지의 경우 3
        
        ET.SubElement(annotation, 'segmented').text = '0'
        
        for obj in objects:
            obj_elem = ET.SubElement(annotation, 'object')
            ET.SubElement(obj_elem, 'name').text = obj['class_name']
            ET.SubElement(obj_elem, 'pose').text = 'Unspecified'
            ET.SubElement(obj_elem, 'truncated').text = '0'
            ET.SubElement(obj_elem, 'difficult').text = '0'
            
            bndbox = ET.SubElement(obj_elem, 'bndbox')
            x1, y1, x2, y2 = obj['bndbox']
            ET.SubElement(bndbox, 'xmin').text = str(x1)
            ET.SubElement(bndbox, 'ymin').text = str(y1)
            ET.SubElement(bndbox, 'xmax').text = str(x2)
            ET.SubElement(bndbox, 'ymax').text = str(y2)
        
        # XML 파일 저장
        xml_filename = os.path.join(output_dir, os.path.splitext(os.path.basename(image_path))[0] + '.xml')
        tree = ET.ElementTree(annotation)
        tree.write(xml_filename, encoding='utf-8', xml_declaration=True)
        
# 함수 호출
csv_to_voc_xml(csv_file_path, output_dir)