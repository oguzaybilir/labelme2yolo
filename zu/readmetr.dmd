# JSON to YOLO Format Converter

Bu proje, JSON formatında etiketlenmiş verileri YOLO formatına dönüştüren bir Python betiğidir. YOLO formatı, nesne tespiti modelleri için yaygın olarak kullanılan bir format olup, bu betik sayesinde JSON etiketlerini hızlı ve doğru bir şekilde dönüştürebilirsiniz.

## Özellikler
- JSON formatındaki etiket verilerini YOLO formatına dönüştürür.
- Etiketleri belirtilen sınıf isimleriyle ilişkilendirir.
- Görsellerin boyutlarını kontrol ederek dönüşümü doğru şekilde gerçekleştirir.
- İşlenen verileri belirtilen çıktı dizinine kaydeder.
- Python'un temel kütüphaneleriyle çalışır, ek bağımlılıklara ihtiyaç duymaz.

## Gereksinimler
Bu betiği çalıştırmak için aşağıdaki yazılımlara ihtiyacınız vardır:
- Python 3.x
- `json` ve `os` gibi Python'un standart kütüphaneleri

## Kurulum
1. **Depoyu klonlayın**
   ```sh
   git clone https://github.com/kullaniciadi/proje-adi.git
   cd proje-adi
   ```
2. **Gerekli bağımlılıkları yükleyin** (Eğer varsa)
   ```sh
   pip install -r requirements.txt
   ```

## Kullanım
Betiği çalıştırmak için aşağıdaki komutu kullanabilirsiniz:

```sh
python convert.py --json_path "veriler/etiketler.json" --output_path "yolo_labels" --classes "siniflar.txt"
```

### Komut Satırı Argümanları
- `--json_path` : JSON formatındaki etiket dosyasının yolu.
- `--output_path` : Dönüştürülen YOLO etiketlerinin kaydedileceği klasör.
- `--classes` : Sınıf isimlerini içeren metin dosyasının yolu.

## Örnek Kullanım
Eğer `data/annotations.json` adlı bir dosyanız varsa ve `output` klasörüne YOLO formatında çıktı almak istiyorsanız şu komutu kullanabilirsiniz:

```sh
python convert.py --json_path "data/annotations.json" --output_path "output" --classes "classes.txt"
```

## Çıktı Formatı
YOLO formatında her etiket satırı şu şekildedir:

```
<class_id> <x_center> <y_center> <width> <height>
```

- `class_id`: Nesnenin sınıf kimliği (0'dan başlayarak).
- `x_center`, `y_center`: Nesnenin görüntüdeki merkez koordinatları (normalleştirilmiş).
- `width`, `height`: Nesnenin genişlik ve yüksekliği (normalleştirilmiş).

## Lisans
Bu proje açık kaynaklıdır ve MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına göz atabilirsiniz.

## Katkıda Bulunma
Projeye katkıda bulunmak isterseniz aşağıdaki adımları takip edebilirsiniz:
1. Depoyu forklayın.
2. Yeni bir dal (branch) oluşturun: `git checkout -b yeni-ozellik`
3. Değişiklikleri yapın ve commit atın: `git commit -m 'Yeni özellik eklendi'`
4. Değişiklikleri gönderin: `git push origin yeni-ozellik`
5. Bir pull request (PR) oluşturun.

Her türlü geri bildirim ve katkı için teşekkürler!

