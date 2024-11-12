# 라이브러리 불러오기
import os
import xml.etree.ElementTree as ET
from PIL import Image
import yaml

# 데이터 경로
yaml_file_path = 'path/to/data_yaml/path/name.yaml'
txt_dir = 'path/to/labels/root'
image_dir = 'path/to/images/root'
output_dir = 'path/to/saving/root'

def load_class_names(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)
        return data['names']

def create_xml(class_name, x_min, y_min, x_max, y_max, image_name, image_width, image_height, output_dir):
    annotation = ET.Element("annotation")
    
    folder = ET.SubElement(annotation, "folder")
    folder.text = "images"
    
    filename = ET.SubElement(annotation, "filename")
    filename.text = image_name
    
    # Extract the last part of the output directory path to determine train, test, or valid
    last_dir_name = os.path.basename(os.path.normpath(output_dir))
    path = ET.SubElement(annotation, "path")
    path.text = f"images/{last_dir_name}/{image_name}"
    
    source = ET.SubElement(annotation, "source")
    database = ET.SubElement(source, "database")
    database.text = "Unknown"
    
    size = ET.SubElement(annotation, "size")
    width = ET.SubElement(size, "width")
    width.text = str(image_width)
    height = ET.SubElement(size, "height")
    height.text = str(image_height)
    depth = ET.SubElement(size, "depth")
    depth.text = "3"  # Assuming RGB images
    
    segmented = ET.SubElement(annotation, "segmented")
    segmented.text = "0"
    
    obj = ET.SubElement(annotation, "object")
    name = ET.SubElement(obj, "name")
    name.text = class_name
    
    pose = ET.SubElement(obj, "pose")
    pose.text = "Unspecified"
    
    truncated = ET.SubElement(obj, "truncated")
    truncated.text = "0"
    
    difficult = ET.SubElement(obj, "difficult")
    difficult.text = "0"
    
    bndbox = ET.SubElement(obj, "bndbox")
    xmin = ET.SubElement(bndbox, "xmin")
    xmin.text = str(x_min)
    ymin = ET.SubElement(bndbox, "ymin")
    ymin.text = str(y_min)
    xmax = ET.SubElement(bndbox, "xmax")
    xmax.text = str(y_max)
    ymax = ET.SubElement(bndbox, "ymax")
    ymax.text = str(y_max)
    
    tree = ET.ElementTree(annotation)
    xml_file_path = os.path.join(output_dir, f"{os.path.splitext(image_name)[0]}.xml")
    tree.write(xml_file_path)
    
    print(f"XML file saved: {xml_file_path}")

def convert_all_txt_to_xml(txt_dir, image_dir, output_dir, class_names):
    for txt_file in os.listdir(txt_dir):
        if txt_file.endswith('.txt'):
            txt_file_path = os.path.join(txt_dir, txt_file)
            image_name = txt_file.replace('.txt', '.jpg')  # Assuming image files are .jpg and named similarly to text files
            image_path = os.path.join(image_dir, image_name)
            
            # Open the image to get its size
            with Image.open(image_path) as img:
                image_width, image_height = img.size
            
            with open(txt_file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split()
                    class_id = int(parts[0])
                    
                    if len(parts) < 5:
                        print("Skipping line due to insufficient data:", line)
                        continue

                    # Assuming parts contain class_id, followed by x, y pairs
                    try:
                        x_values = [float(parts[i]) for i in range(1, len(parts), 2)]
                        y_values = [float(parts[i]) for i in range(2, len(parts), 2)]
                        
                        # Find the bounding box coordinates
                        x_min = int(min(x_values) * image_width)
                        y_min = int(min(y_values) * image_height)
                        x_max = int(max(x_values) * image_width)
                        y_max = int(max(y_values) * image_height)
                        
                        # Get class name from class_id
                        class_name = class_names[class_id] if class_id < len(class_names) else "unknown"
                        
                        create_xml(class_name, x_min, y_min, x_max, y_max, image_name, image_width, image_height, output_dir)
                    
                    except ValueError as e:
                        print(f"Skipping line due to error: {e}, line content: {line}")

# Load class names from the YAML file
class_names = load_class_names(yaml_file_path)

convert_all_txt_to_xml(txt_dir, image_dir, output_dir, class_names)
