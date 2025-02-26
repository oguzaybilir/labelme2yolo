# Project Title

## Description
This project is designed to convert labelme JSON label's to YOLO bounding box and polygon format.
It provides the ability to convert JSON label's to YOLO format with ease and accuracy.

## Installation
To install and set up the project, follow these steps:
```bash
# Clone the repository
git clone https://github.com/oguzaybilir/labelme2yolo.git

# Navigate to the project directory
cd labelme2yolo

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### Arguments

The script runs with specific arguments:

- `--path` : Specifies the source directory containing JSON files.
- `--target` : Specifies the target directory where the converted YOLO format files will be saved.
- `--task` : Selects the type of processing. Use `"detection"` for object detection (bounding box) or `"segmentation"` for segmentation (mask).

**For Object Detection (Detection):**  
Run the following command to convert JSON annotations to YOLO format:

```bash
python json_to_yolo_v1.py --path "path/to/source/directory" --target "path/to/target/directory" --task "detection"
```

**For Segmentation:**  
To convert segmentation data into YOLO format, use the following command:

```bash
python json_to_yolo_v1.py --path "path/to/source/directory" --target "path/to/target/directory" --task "segmentation"
```

This will convert the JSON files from the specified source directory into the appropriate YOLO format and save them in the target directory.


## Configuration
If there are any configuration settings, describe them here, such as environment variables, configuration files, or API keys.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m "Add new feature"`).
4. Push the changes (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the [License Name] - see the [LICENSE](LICENSE) file for details.

## Contact
For any inquiries, feel free to reach out to [your contact information].