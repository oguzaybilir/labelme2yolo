import os
from PIL import Image

def convert_tiff_to_png(input_folder, output_folder):
    # Klasörleri kontrol et
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # TIFF dosyalarını bul ve dönüştür
    for filename in os.listdir(input_folder):
        if filename.endswith('.tiff') or filename.endswith('.tif'):
            tiff_path = os.path.join(input_folder, filename)
            png_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.png")
            
            # TIFF dosyasını aç ve PNG olarak kaydet
            with Image.open(tiff_path) as img:
                img.save(png_path, 'PNG')

# Kullanım örneği
input_folder = '/home/comp1/gaiatech-kodlar/datav3/yolo-labels-segmentation'  # TIFF dosyalarının bulunduğu klasör
output_folder = '/home/comp1/gaiatech-kodlar/datav3/yolo-labels-png'  # PNG dosyalarının kaydedileceği klasör
convert_tiff_to_png(input_folder, output_folder)
