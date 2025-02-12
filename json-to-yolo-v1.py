import os
from glob import glob
import json
import shutil
import cv2
import argparse 
import sys
import math
from collections import OrderedDict
from labelme import utils

class JsonToYolo(object):
    def __init__(self, path, target, task):
        self.path = path 
        self.target = os.path.join(target + "/" + task)
        
        # Define label mapping as a class attribute
        self.label_mapping = {
            'benign': 0,
            'DCIS': 1,
            'kalsifikasyon': 2,
            'malign': 3
        }
        
        # Create target directory if it doesn't exist
        os.makedirs(self.target, exist_ok=True)  # Ensure the target directory exists
        
        # Create classes.txt file
        self._create_classes_file()

    def _create_classes_file(self):
        # Write class names to classes.txt
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
            # Assuming the JSON file has the same base name as the TIFF file
            file_pairs.append((tiff, json))
        return file_pairs
    
    def _convert_json_to_yolo_detection_format(self, pairs):
        os.makedirs(self.target, exist_ok=True)  # Create the directory if it doesn't exist
        
        for tiff, json_file in pairs:
            print(f"Processing: {json_file}")  # Debug statement
            with open(json_file) as f:
                data = json.load(f)

            image_width = data['imageWidth']
            image_height = data['imageHeight']
            yolo_labels = []

            for shape in data['shapes']:
                label = shape['label']
                print(f"Processing label: {label}")  # Debug statement to check the label being processed
                points = shape['points']
                
                # Convert polygon points to YOLO format
                x_coords = [point[0] for point in points]
                y_coords = [point[1] for point in points]
                
                # Calculate the center of the bounding box
                x_center = sum(x_coords) / len(x_coords)
                y_center = sum(y_coords) / len(y_coords)
                
                # Normalize coordinates
                x_center /= image_width
                y_center /= image_height
                width = (max(x_coords) - min(x_coords)) / image_width
                height = (max(y_coords) - min(y_coords)) / image_height
                
                # Use the label mapping to get the encoded label
                encoded_label = self.label_mapping.get(label, -1)  # Accessing the class attribute
                
                # Append to YOLO labels
                yolo_labels.append(f"{encoded_label} {x_center} {y_center} {width} {height}")

            # Write to YOLO format .txt file
            yolo_txt_file = os.path.join(self.target, os.path.basename(json_file).replace('.json', '.txt'))
            with open(yolo_txt_file, 'w') as out_file:
                out_file.write("\n".join(yolo_labels))
            
            print(f"Created: {yolo_txt_file}")  # Debug statement

            # Move the image to the new directory
            image_file = os.path.join(os.path.dirname(json_file), data['imagePath'])
            if os.path.exists(image_file):
                shutil.copy(image_file, self.target)
                print(f"Moved image: {image_file} to {self.target}")  # Debug statement
            else:
                print(f"Image not found: {image_file}")  # Debug statement
                
    def _convert_json_to_yolo_polygon_format(self, pairs):
        os.makedirs(self.target, exist_ok=True)  # Create the directory if it doesn't exist
        
        for tiff, json_file in pairs:
            print(f"Processing: {json_file}")  # Debug statement
            with open(json_file) as f:
                data = json.load(f)

            image_width = data['imageWidth']
            image_height = data['imageHeight']
            yolo_labels = []

            for shape in data['shapes']:
                label = shape['label']
                print(f"Processing label: {label}")  # Debug statement to check the label being processed
                points = shape['points']
                
                # Normalize polygon points for YOLO format
                normalized_points = []
                for point in points:
                    x_normalized = point[0] / image_width
                    y_normalized = point[1] / image_height
                    normalized_points.append(f"{x_normalized} {y_normalized}")

                # Use the label mapping to get the encoded label
                encoded_label = self.label_mapping.get(label, -1)  # Accessing the class attribute
                
                # Append to YOLO labels in polygon format
                yolo_labels.append(f"{encoded_label} {' '.join(normalized_points)}")

            # Write to YOLO format .txt file
            yolo_txt_file = os.path.join(self.target, os.path.basename(json_file).replace('.json', '.txt'))
            with open(yolo_txt_file, 'w') as out_file:
                out_file.write("\n".join(yolo_labels))
            
            print(f"Created: {yolo_txt_file}")  # Debug statement

            # Move the image to the new directory
            image_file = os.path.join(os.path.dirname(json_file), data['imagePath'])
            if os.path.exists(image_file):
                shutil.copy(image_file, self.target)
                print(f"Moved image: {image_file} to {self.target}")  # Debug statement
            else:
                print(f"Image not found: {image_file}")  # Debug statement

    def _get_label_from_mapping(self, encoded_label):
        # Use the class attribute for label mapping
        return {v: k for k, v in self.label_mapping.items()}.get(encoded_label, "unknown")  # Default to "unknown" if label not found

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, help="path to the directory", required=True)
    parser.add_argument("--target", type=str, help="path to the directory", required=True)
    parser.add_argument("--task", type=str, help="detection or segmentation ?", required=True)
    args = parser.parse_args(sys.argv[1:])
    json_to_yolo = JsonToYolo(args.path, args.target, args.task)
    files = json_to_yolo._read_tiff_and_json_files()
    
    if args.task == "detection":
        outputs = json_to_yolo._convert_json_to_yolo_detection_format(files)
    elif args.task == "segmentation":
            outputs = json_to_yolo._convert_json_to_yolo_polygon_format(files)
