# JSON to YOLO Converter

Bu proje, LabelMe tarafından oluşturulan JSON formatındaki anotasyonları YOLO formatına dönüştürmek için geliştirilmiştir. Model eğitimi için anotasyonları hızla ve kolayca dönüştürmek isteyen araştırmacılar ve mühendisler için kullanışlı bir araçtır.

## Özellikler
- **Detection ve Segmentation Desteği**: Nesne tespiti (detection) veya segmentasyon için anotasyonları dönüştürebilirsiniz.
- **Otomatik Klasör Yönetimi**: Dönüştürülen veriler belirtilen hedef klasöre kaydedilir.
- **Etiket Haritalama**: JSON'daki etiketleri otomatik olarak YOLO formatına dönüştürür.

## Gereksinimler
Bu proje aşağıdaki kütüphaneleri gerektirir:

```bash
pip install opencv-python argparse labelme
```

## Kurulum
1. **Projeyi Klonlayın:**

   ```bash
   git clone https://github.com/kullanici_adi/json-to-yolo.git
   cd json-to-yolo
   ```

2. **Bağımlılıkları Yükleyin:**

   ```bash
   pip install -r requirements.txt
   ```

## Kullanım
Komut satırından aşağıdaki gibi çalıştırabilirsiniz:

```bash
python json-to-yolo-v1.py --path "veri_klasoru" --target "cikis_klasoru" --task "detection"
```

### Parametreler
- `--path`: JSON ve TIFF dosyalarının bulunduğu kaynak klasör.
- `--target`: Dönüştürülmüş YOLO formatındaki verilerin kaydedileceği hedef klasör.
- `--task`: `detection` veya `segmentation` seçeneklerinden biri (nesne tespiti veya segmentasyon için).

## Örnek Kullanım
Örnek bir çalıştırma senaryosu:

```bash
python json-to-yolo-v1.py --path "./dataset" --target "./yolo_dataset" --task "detection"
```

Bu komut, `./dataset` içinde bulunan JSON anotasyonlarını YOLO formatına çevirir ve `./yolo_dataset` klasörüne kaydeder.

## Çıktı Formatı
Dönüştürülen YOLO formatındaki `txt` dosyaları şu formatta olur:

```
[class_id] [x_center] [y_center] [width] [height]
```

Her satır bir nesneyi temsil eder ve koordinatlar 0-1 arasında normalize edilir.

## Katkıda Bulunma
Projeye katkıda bulunmak isterseniz, lütfen bir **pull request** gönderin veya bir **issue** açın!

## Lisans
MIT Lisansı altında yayınlanmıştır.


