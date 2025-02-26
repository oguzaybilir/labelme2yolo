# LabelMe2YOLO

## Overview
This project is designed to convert **LabelMe JSON annotations** into **YOLO bounding box** and **YOLO polygon segmentation** formats. If you are working on a segmentation task and your labels are in LabelMe format, this tool will help you seamlessly transform them into a format compatible with YOLO-based models.

## Why Use This?
- **Seamless Conversion**: Automatically convert LabelMe JSON annotations into YOLO-compatible labels.
- **Supports Both Bounding Boxes & Segmentation**: Choose between YOLO **bounding box** or **polygon-based segmentation**.
- **Simplifies Workflow**: Avoid the hassle of manually converting annotations.

## Installation
To install this repository, follow these steps:

```bash
# Clone the repository
git clone https://github.com/oguzaybilir/labelme2yolo.git

# Navigate to the repository directory
cd labelme2yolo
```

## Usage
The script requires three command-line arguments:
- `--path` : Specifies the **source directory** containing JSON files.
- `--target` : Specifies the **destination directory** where converted YOLO labels will be saved.
- `--task` : Determines the type of conversion. Use **"detection"** for bounding boxes or **"segmentation"** for mask-based segmentation.

### Example Commands
#### Convert LabelMe JSON to YOLO Bounding Boxes
```bash
python3 labelme2yolo.py --path /path/to/source/directory --target /path/to/target/directory --task "detection"
```

#### Convert LabelMe JSON to YOLO Polygon Segmentation
```bash
python3 labelme2yolo.py --path /path/to/source/directory --target /path/to/target/directory --task "segmentation"
```

### Expected Output
After running the script, your target directory will contain YOLO-formatted label files:
- **Bounding Box Output (detection task)**:
  ```
  class_id x_center y_center width height
  ```
- **Polygon Segmentation Output (segmentation task)**:
  ```
  class_id x1 y1 x2 y2 ... xn yn
  ```

## Example Input & Output
### Sample LabelMe JSON Input
```json
{
  "shapes": [
    {
      "label": "car",
      "points": [[50, 60], [200, 300]],
      "shape_type": "rectangle"
    }
  ]
}
```

### Corresponding YOLO Output (Bounding Box)
```txt
0 0.39 0.46 0.58 0.47
```

## Contact
For any inquiries, feel free to reach out via:
- GitHub: [your GitHub profile](https://github.com/oguzaybilir)
- LinkedIn: [your LinkedIn profile](https://linkedin.com/in/oguzaybilir)
- Email: [your email address](mailto:oguzaybilir@gmail.com)

---

This README should now better communicate your project's purpose and usage while keeping your original writing style intact. 🚀