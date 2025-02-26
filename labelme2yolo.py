import os
from glob import glob
import json
import shutil
import argparse 
import sys
import datetime
from typing import List, Tuple, Dict, Optional, Union

class JsonToYolo:
    def __init__(self, path: str, target: str, task: str):
        """
        The constructor of the JsonToYolo Class.
        
        Args:
            path: The path to the source directory containing the files.
            target: The path to the target directory where the converted files will be saved.
            task: The task type ('detection' or 'segmentation').
        """
        self.path = path 
        self.target = os.path.join(target, task)
        self.task = task
        self.error_log_path = os.path.join(target, "label_errors.txt")
        
        # Define label mapping as a class attribute
        self.label_mapping = {
            'label1': 0,
            'label2': 1,
            'label3': 2,
            'label4': 3
        }
        
        # Create target directory if it doesn't exist
        os.makedirs(self.target, exist_ok=True) 
        self._create_classes_file()
        
        # Define statistics as a class attribute
        self.stats = {
            "processed_files": 0,
            "successful_files": 0,
            "error_files": 0,
            "processed_labels": 0,
            "invalid_labels": 0
        }

    def _create_classes_file(self) -> None:
        """
        Creates a file containing the class names for mostly labelimg labeling tool.
        """
        classes_file_path = os.path.join(self.target, 'classes.txt')
        with open(classes_file_path, 'w') as classes_file:
            for class_name in self.label_mapping.keys():
                classes_file.write(f"{class_name}\n")
        print(f"Created: {classes_file_path}")

    def _read_tiff_and_json_files(self) -> List[Tuple[str, str]]:
        """
        Reads all TIFF and corresponding JSON files in the specified directory.
        
        Returns:
            list: A list of tuples, each containing the path to a TIFF file and its corresponding JSON file.
        """
        tiff_files = sorted(glob(os.path.join(self.path, '*/*.tiff'), recursive=True))
        json_files = sorted(glob(os.path.join(self.path, '*/*.json'), recursive=True))

        if len(tiff_files) != len(json_files):
            print(f"UYARI: TIFF ({len(tiff_files)}) ve JSON ({len(json_files)}) dosya sayıları eşleşmiyor!")
            self._log_error(None, f"TIFF ({len(tiff_files)}) ve JSON ({len(json_files)}) dosya sayıları eşleşmiyor!")
        
        file_pairs = []
        for tiff, json_path in zip(tiff_files, json_files):
            tiff_base = os.path.splitext(os.path.basename(tiff))[0]
            json_base = os.path.splitext(os.path.basename(json_path))[0]
            
            # Check if the file names match with json's names
            if tiff_base != json_base:
                print(f"[WARNING]: File names do not match: {tiff} and {json_path}")
                self._log_error(None, f"File names do not match: {tiff} and {json_path}")
            
            file_pairs.append((tiff, json_path))
        return file_pairs
    
    def _convert_json_to_yolo_detection_format(self, pairs: List[Tuple[str, str]]) -> None:
        """
        Converts JSON label files to YOLO detection label format.
        
        Args:
            pairs: A list of tuples, each containing the path to a TIFF file and its corresponding JSON file.
        """
        os.makedirs(self.target, exist_ok=True)
        
        for tiff, json_file in pairs:
            self.stats["processed_files"] += 1
            print(f"Processing: {json_file}")
            
            try:
                with open(json_file) as f:
                    data = json.load(f)

                image_width = data.get('imageWidth', 0)
                image_height = data.get('imageHeight', 0)
                
                if image_width <= 0 or image_height <= 0:
                    error_msg = f"Invalid image dimensions: {image_width}x{image_height}"
                    print(f"[WARNING]: {error_msg}")
                    self._log_error(json_file, error_msg)
                    self.stats["error_files"] += 1
                    continue
                
                yolo_labels = []

                for shape in data.get('shapes', []):
                    self.stats["processed_labels"] += 1
                    label = shape.get('label', '')
                    points = shape.get('points', [])
                    
                    if not label or not points:
                        self._log_error(json_file, f"Etiket veya nokta verisi yok: {shape}")
                        self.stats["invalid_labels"] += 1
                        continue
                    
                    try:
                        x_coords = [point[0] for point in points]
                        y_coords = [point[1] for point in points]
                        
                        x_center = sum(x_coords) / len(x_coords)
                        y_center = sum(y_coords) / len(y_coords)
                        
                        x_center /= image_width
                        y_center /= image_height
                        width = (max(x_coords) - min(x_coords)) / image_width
                        height = (max(y_coords) - min(y_coords)) / image_height
                        
                        # Check if the normalized coordinates are valid
                        if not (0 <= x_center <= 1 and 0 <= y_center <= 1 and 0 <= width <= 1 and 0 <= height <= 1):
                            error_msg = f"Normalized coordinates are invalid: {x_center}, {y_center}, {width}, {height}"
                            print(f"[WARNING]: {error_msg}")
                            self._log_error(json_file, error_msg)
                            self.stats["invalid_labels"] += 1
                            continue
                        
                        encoded_label = self.label_mapping.get(label, -1)
                        if encoded_label == -1:
                            print(f"[WARNING]: Unknown label: {label}")
                            self._log_error(json_file, f"Unknown label: {label}")
                            self.stats["invalid_labels"] += 1
                            continue
                            
                        yolo_label = f"{encoded_label} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
                        
                        # Check if the label is in the correct format
                        if self._is_bbox_or_polygon(yolo_label, json_file) != "Detection (BBox)":
                            error_msg = f"The label is not in the correct format: {yolo_label}"
                            print(f"[WARNING]: {error_msg}")
                            self._log_error(json_file, error_msg)
                            self.stats["invalid_labels"] += 1
                            continue
                            
                        yolo_labels.append(yolo_label)
                        
                    except Exception as e:
                        error_msg = f"Label conversion error: {str(e)}"
                        print(f"[WARNING]: {error_msg}")
                        self._log_error(json_file, error_msg)
                        self.stats["invalid_labels"] += 1
                        continue

                if not yolo_labels:
                    print(f"[WARNING]: {json_file} file does not contain a valid label")
                    self._log_error(json_file, "Label not found")
                    self.stats["error_files"] += 1
                    continue
                
                # Write out the converted labels to a text file
                yolo_txt_file = os.path.join(self.target, os.path.basename(json_file).replace('.json', '.txt'))
                with open(yolo_txt_file, 'w') as out_file:
                    out_file.write("\n".join(yolo_labels))
                
                print(f"Created: {yolo_txt_file}") 

                # Copy the image file to the target directory
                image_path = data.get('imagePath', '')
                image_file = os.path.join(os.path.dirname(json_file), image_path) if image_path else ''
                
                if image_file and os.path.exists(image_file):
                    shutil.copy(image_file, self.target)
                    print(f"Moved image: {image_file} to {self.target}") 
                    self.stats["successful_files"] += 1
                else:
                    error_msg = f"Image file not found: {image_file}"
                    print(f"WARNING: {error_msg}")
                    self._log_error(json_file, error_msg)
                    self.stats["error_files"] += 1
                    
            except Exception as e:
                error_msg = f"File processing error: {str(e)}"
                print(f"[ERROR]: {error_msg}")
                self._log_error(json_file, error_msg)
                self.stats["error_files"] += 1
                
    def _convert_json_to_yolo_polygon_format(self, pairs: List[Tuple[str, str]]) -> None:
        """
        Converts JSON label files to YOLO polygon label format.
        
        Args:
            pairs: A list of tuples, each containing the path to a TIFF file and its corresponding JSON file.
        """
        os.makedirs(self.target, exist_ok=True)
        
        for tiff, json_file in pairs:
            self.stats["processed_files"] += 1
            print(f"Processing: {json_file}")
            
            try:
                with open(json_file) as f:
                    data = json.load(f)

                image_width = data.get('imageWidth', 0)
                image_height = data.get('imageHeight', 0)
                
                if image_width <= 0 or image_height <= 0:
                    error_msg = f"Invalid image dimensions: {image_width}x{image_height}"
                    print(f"[WARNING]: {error_msg}")
                    self._log_error(json_file, error_msg)
                    self.stats["error_files"] += 1
                    continue
                    
                yolo_labels = []

                for shape in data.get('shapes', []):
                    self.stats["processed_labels"] += 1
                    label = shape.get('label', '')
                    points = shape.get('points', [])
                    
                    if not label or not points:
                        self._log_error(json_file, f"Label or point data is missing: {shape}")
                        self.stats["invalid_labels"] += 1
                        continue
                    
                    # The polygon must have at least 3 points
                    if len(points) < 3:
                        error_msg = f"Polygon has too few points: {len(points)}"
                        print(f"[WARNING]: {error_msg}")
                        self._log_error(json_file, error_msg)
                        self.stats["invalid_labels"] += 1
                        continue
                    
                    try:
                        normalized_points = []
                        invalid_coords = False
                        
                        for point in points:
                            x_normalized = point[0] / image_width
                            y_normalized = point[1] / image_height
                            
                            # Check if the normalized coordinates are valid
                            if not (0 <= x_normalized <= 1 and 0 <= y_normalized <= 1):
                                error_msg = f"Normalized coordinate is invalid: ({x_normalized}, {y_normalized})"
                                print(f"[WARNING]: {error_msg}")
                                self._log_error(json_file, error_msg)
                                invalid_coords = True
                                break
                                
                            normalized_points.append(f"{x_normalized:.6f} {y_normalized:.6f}")

                        if invalid_coords:
                            self.stats["invalid_labels"] += 1
                            continue
                            
                        encoded_label = self.label_mapping.get(label, -1) 
                        if encoded_label == -1:
                            print(f"[WARNING]: Unknown label: {label}")
                            self._log_error(json_file, f"Unknown label: {label}")
                            self.stats["invalid_labels"] += 1
                            continue
                            
                        yolo_label = f"{encoded_label} {' '.join(normalized_points)}"
                        
                        # Check if the label is in the correct format
                        if self._is_bbox_or_polygon(yolo_label, json_file) != "Segmentation (Polygon)":
                            error_msg = f"The label is not in the correct format: {yolo_label}"
                            print(f"[WARNING]: {error_msg}")
                            self._log_error(json_file, error_msg)
                            self.stats["invalid_labels"] += 1
                            continue
                            
                        yolo_labels.append(yolo_label)
                        
                    except Exception as e:
                        error_msg = f"Label conversion error: {str(e)}"
                        print(f"HATA: {error_msg}")
                        self._log_error(json_file, error_msg)
                        self.stats["invalid_labels"] += 1
                        continue

                if not yolo_labels:
                    print(f"[WARNING]: {json_file} file does not contain a valid label")
                    self._log_error(json_file, "Geçerli etiket bulunamadı")
                    self.stats["error_files"] += 1
                    continue
                    
                # Write out the converted labels to a text file
                yolo_txt_file = os.path.join(self.target, os.path.basename(json_file).replace('.json', '.txt'))
                with open(yolo_txt_file, 'w') as out_file:
                    out_file.write("\n".join(yolo_labels))
                
                print(f"Created: {yolo_txt_file}")

                # Copy the image file to the target directory
                image_path = data.get('imagePath', '')
                image_file = os.path.join(os.path.dirname(json_file), image_path) if image_path else ''
                
                if image_file and os.path.exists(image_file):
                    shutil.copy(image_file, self.target)
                    print(f"Moved image: {image_file} to {self.target}")
                    self.stats["successful_files"] += 1
                else:
                    error_msg = f"Image file not found: {image_file}"
                    print(f"WARNING: {error_msg}")
                    self._log_error(json_file, error_msg)
                    self.stats["error_files"] += 1
                    
            except Exception as e:
                error_msg = f"File processing error: {str(e)}"
                print(f"[ERROR]: {error_msg}")
                self._log_error(json_file, error_msg)
                self.stats["error_files"] += 1

    def _get_label_from_mapping(self, encoded_label: int) -> str:
        """
        Maps the encoded label to its corresponding text label.
        
        Args:
            encoded_label: The encoded label.
        """
        return {v: k for k, v in self.label_mapping.items()}.get(encoded_label, "unknown") 
    
    def _is_bbox_or_polygon(self, label: str, filename: Optional[str] = None) -> Optional[str]:
        """
        Checks if the label belongs to the bounding box or polygon format.
        
        Args:
            label: The label line in YOLO format.
            filename: The file that the label belongs to (for error logging).
            
        Returns:
            str: "Detection (BBox)" or "Segmentation (Polygon)" or None (invalid label)
        """
        # Check if the label is empty or invalid
        if not label or not label.strip():
            self._log_error(self.error_log_path, filename, "Empty label")
            return None
        
        try:
            data = list(map(float, label.split()))
            
            # At least one class ID is required
            if len(data) < 2:
                self._log_error(self.error_log_path, filename, "Insufficient data: At least one class ID and one coordinate is required")
                return None
            
            # The first value is the class ID, the rest are the coordinates
            class_id = int(data[0])  # The class ID should be an integer
            values = data[1:]
            
            # The YOLO bbox label format is checked: exactly 4 values (x, y, w, h)
            if len(values) == 4:
                # Check if the values are within the range of 0 to 1
                if all(0 <= val <= 1 for val in values):
                    return "Detection (BBox)"
                elif all(val >= 0 for val in values):
                    return "Detection (BBox)"
                else:
                    self._log_error(self.error_log_path, filename, "Bbox coordinates are out of range")
                    return None
            
            # Check if the coordinates are in YOLO polygon format : at least 6 values (3 points) and an even number of them
            elif len(values) >= 6 and len(values) % 2 == 0:
                invalid_coords = []
                for i in range(0, len(values), 2):
                    x, y = values[i], values[i+1]
                    if not (0 <= x <= 1 and 0 <= y <= 1):
                        if x < 0 or y < 0:
                            invalid_coords.append(f"({x},{y})")
                
                if invalid_coords:
                    self._log_error(self.error_log_path, filename, f"Invalid polygon coordinates: {', '.join(invalid_coords)}")
                    return None
                return "Segmentation (Polygon)"
            
            else:
                self._log_error(self.error_log_path, filename, f"Unsupported coordinate number: {len(values)}")
                return None
            
        except Exception as e:
            self._log_error(self.error_log_path, filename, f"Process Error: {str(e)}")
            return None
    
    def _log_error(self, filename: Optional[str], error_message: str) -> None:
        """
        Writes error messages to the error log file.
        
        Args:
            filename: The name of the file that caused the error.
            error_message: The error message.
        """
        with open(self.error_log_path, "a", encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file_info = f"File: {filename}" if filename else "Unknown file"
            f.write(f"[{timestamp}] {file_info} - {error_message}\n")
    
    def process(self) -> Dict[str, int]:
        """
        Converts all JSON label files to the specified task format.
        
        Returns:
            Dict: The statistics of the conversion process.
        """
        print(f"[Started at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        print(f"JSON files converted to YOLO {self.task} format...")
        files = self._read_tiff_and_json_files()
        
        if self.task == "detection":
            self._convert_json_to_yolo_detection_format(files)
        elif self.task == "segmentation":
            self._convert_json_to_yolo_polygon_format(files)
        
        print("\nConversion Complete!")
        print(f"Number of processed files: {self.stats['processed_files']}")
        print(f"Number of successful files: {self.stats['successful_files']}")
        print(f"Number of error files: {self.stats['error_files']}")
        print(f"Number of processed labels: {self.stats['processed_labels']}")
        print(f"Number of invalid labels: {self.stats['invalid_labels']}")  
        print(f"Detailed error report: {self.error_log_path}")
        
        return self.stats

def main():
    parser = argparse.ArgumentParser(description="Converts JSON label files to the specified task format")
    parser.add_argument("--path",
                        type=str,
                        help="The path to the source directory containing the files.",
                        required=True)
    
    parser.add_argument("--target",
                        type=str,
                        help="The path to the target directory where the converted files will be saved.",
                        required=True)
    
    parser.add_argument("--task",
                        type=str,
                        choices=["segmentation", "detection"],
                        help="The task type: detection or segmentation.",
                        required=True)
    
    args = parser.parse_args()
    
    try:
        json_to_yolo = JsonToYolo(args.path, args.target, args.task)
        json_to_yolo.process()
    except Exception as e:
        print(f"Error: An unexpected error occurred during the process: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())