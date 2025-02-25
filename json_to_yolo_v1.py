import os
from glob import glob
import json
import shutil
import argparse 
import sys

class JsonToYolo(object):
    def __init__(self, path, target, task):
        self.path = path 
        self.target = os.path.join(target + "/" + task)
        
        self.label_mapping = {
            'benign': 0,
            'DCIS': 1,
            'kalsifikasyon': 2,
            'malign': 3
        }
        
        os.makedirs(self.target, exist_ok=True) 
        self._create_classes_file()

    def _create_classes_file(self):
        classes_file_path = os.path.join(self.target, 'classes.txt')
        with open(classes_file_path, 'w') as classes_file:
            for class_name in self.label_mapping.keys():
                classes_file.write(f"{class_name}\n")
        print(f"Created: {classes_file_path}")  # Debug statement

    def _read_tiff_and_json_files(self):
        """
        Reads all TIFF and corresponding JSON files in the specified directory.

        Returns:
            list: A list of tuples, each containing the path to a TIFF file and its corresponding JSON file.
        """
        tiff_files = sorted(glob(os.path.join(self.path, '*/*.tiff'), recursive=True))
        json_files = sorted(glob(os.path.join(self.path, '*/*.json'), recursive=True))

        file_pairs = []
        for tiff, json in zip(tiff_files, json_files):
            file_pairs.append((tiff, json))
        return file_pairs
    
    def _convert_json_to_yolo_detection_format(self, pairs):
        os.makedirs(self.target, exist_ok=True)
        
        for tiff, json_file in pairs:
            print(f"Processing: {json_file}")
            with open(json_file) as f:
                data = json.load(f)

            image_width = data['imageWidth']
            image_height = data['imageHeight']
            yolo_labels = []

            for shape in data['shapes']:
                label = shape['label']
                print(f"Processing label: {label}")
                points = shape['points']
                
                x_coords = [point[0] for point in points]
                y_coords = [point[1] for point in points]
                
                x_center = sum(x_coords) / len(x_coords)
                y_center = sum(y_coords) / len(y_coords)
                
                x_center /= image_width
                y_center /= image_height
                width = (max(x_coords) - min(x_coords)) / image_width
                height = (max(y_coords) - min(y_coords)) / image_height
                
                encoded_label = self.label_mapping.get(label, -1)
                
                yolo_labels.append(f"{encoded_label} {x_center} {y_center} {width} {height}")

            yolo_txt_file = os.path.join(self.target, os.path.basename(json_file).replace('.json', '.txt'))
            with open(yolo_txt_file, 'w') as out_file:
                out_file.write("\n".join(yolo_labels))
            
            print(f"Created: {yolo_txt_file}") 

            image_file = os.path.join(os.path.dirname(json_file), data['imagePath'])
            if os.path.exists(image_file):
                shutil.copy(image_file, self.target)
                print(f"Moved image: {image_file} to {self.target}") 
            else:
                print(f"Image not found: {image_file}") 
                
    def _convert_json_to_yolo_polygon_format(self, pairs):
        os.makedirs(self.target, exist_ok=True)
        
        for tiff, json_file in pairs:
            print(f"Processing: {json_file}")  
            with open(json_file) as f:
                data = json.load(f)

            image_width = data['imageWidth']
            image_height = data['imageHeight']
            yolo_labels = []

            for shape in data['shapes']:
                label = shape['label']
                print(f"Processing label: {label}")  
                points = shape['points']
                
                normalized_points = []
                for point in points:
                    x_normalized = point[0] / image_width
                    y_normalized = point[1] / image_height
                    normalized_points.append(f"{x_normalized} {y_normalized}")

                encoded_label = self.label_mapping.get(label, -1) 
                
                yolo_labels.append(f"{encoded_label} {' '.join(normalized_points)}")

            yolo_txt_file = os.path.join(self.target, os.path.basename(json_file).replace('.json', '.txt'))
            with open(yolo_txt_file, 'w') as out_file:
                out_file.write("\n".join(yolo_labels))
            
            print(f"Created: {yolo_txt_file}")  

            image_file = os.path.join(os.path.dirname(json_file), data['imagePath'])
            if os.path.exists(image_file):
                shutil.copy(image_file, self.target)
                print(f"Moved image: {image_file} to {self.target}")  
            else:
                print(f"Image not found: {image_file}")  

    def _get_label_from_mapping(self, encoded_label):
        return {v: k for k, v in self.label_mapping.items()}.get(encoded_label, "unknown") 
    
    def _is_bbox_or_polygon(self, label):
        data = list(map(float, label.split()))
        class_id = data[0]
        values = data[1:]
        
        if len(values) == 4:
            return "Detection (BBox)"
        
        elif len(values) > 4:
            return "Segmentation (Polygon)"
        
        elif len(values) >= 6:
            return "Segmentation (Polygon)"

        return None
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path",
                        type=str,
                        help="path to the directory",
                        required=True)
    
    parser.add_argument("--target",
                        type=str,
                        help="path to the directory",
                        required=True)
    
    parser.add_argument("--task",
                        type=str,
                        choices=["segmentation", "detection"],
                        help="detection or segmentation ?",
                        required=True)
    
    args = parser.parse_args(sys.argv[1:])
    json_to_yolo = JsonToYolo(args.path, args.target, args.task)
    files = json_to_yolo._read_tiff_and_json_files()
    
    if args.task == "detection":
        outputs = json_to_yolo._convert_json_to_yolo_detection_format(files)
    elif args.task == "segmentation":
            outputs = json_to_yolo._convert_json_to_yolo_polygon_format(files)