<<<<<<< HEAD
# VisionArm-AI: Vision-Based Autonomous Robotic Arm (V1)

VisionArm-AI, görüntü işleme tekniklerini kullanarak nesneleri renklerine göre sınıflandıran ve belirlenen konumlara taşıyan otonom bir "pick-and-place" robot kol sistemidir. Bu proje; **OpenCV**, **Python tabanlı otomasyon** ve **Arduino kontrollü donanım** entegrasyonunun bir sonucudur.
=======
# VisionArm: Vision-Based Autonomous Robotic Arm (V1)

VisionArm, görüntü işleme tekniklerini kullanarak nesneleri renklerine göre sınıflandıran ve belirlenen konumlara taşıyan otonom bir "pick-and-place" robot kol sistemidir. Bu proje; **OpenCV**, **Python tabanlı otomasyon** ve **Arduino kontrollü donanım** entegrasyonunun bir sonucudur.
>>>>>>> bb4ddb440dfd2f001c10c1e464a72613c60278f4

## 🚀 Genel Bakış

Sistem, tepeden bakan bir kamera aracılığıyla canlı video akışı yakalar, HSV renk maskeleme kullanarak nesneleri tanımlar ve nesnenin 2 saniye boyunca sabit kaldığından emin olduktan sonra Seri haberleşme üzerinden Arduino'ya komut göndererek taşıma işlemini gerçekleştirir.

### Ana Özellikler

* **Renk Tabanlı Sınıflandırma:** HSV renk uzayını kullanarak Kırmızı, Yeşil ve Mavi nesneleri tespit eder.
* **Stabilizasyon Mantığı:** Titreşim kaynaklı hataları önlemek için nesnenin 2 saniye boyunca sabit kalmasını bekleyen "Debouncing" algoritması.
* **Handshake Protokolü:** Python ve Arduino arasında "OK/Hazır" sinyali ile senkronize çalışma yapısı.
* **Modüler Mimari:** Görüntü işleme, haberleşme ve yapılandırma modüllerinin birbirinden temiz ayrımı.

---

## 🛠 Teknoloji Yığını

* **Yazılım:** Python 3.x, OpenCV, NumPy, PySerial.
* **Donanım:** Arduino (Uno/Mega), Servo Motorlar, USB Kamera.
* **İşletim Sistemi:** macOS (Apple Silicon) ve Linux (Pop!_OS) için optimize edilmiştir.

---

## 📂 Proje Yapısı

```text
Vision-Based-Robotic-Arm/
├── v1/
│   ├── src/
│   │   ├── config.py        # Global ayarlar (HSV, Portlar, Eşik Değerleri)
│   │   ├── communication.py # Seri haberleşme ve Handshake mantığı
│   │   ├── vision.py        # Görüntü işleme ve Renk tespiti
│   │   └── main.py          # Ana otomasyon döngüsü (State Machine)
│   ├── test-images/         # Kalibrasyon için statik görseller
│   └── arduino_v1/
│       └── arduino_v1.ino   # Arduino firmware (Servo kontrolü)
└── README.md

```

---

## 🛠 Geliştirme Süreci ve Yol Haritası (Roadmap)

Bu proje şu anda geliştirme aşamasındadır. Derinlik sensörleri (3D/Depth Sensing) yerine, saf görüntü işleme ve matematiksel koordinat dönüşümleriyle yüksek hassasiyet hedeflenmektedir.

### 📍 Versiyon 1 (Mevcut Durum) - Temel Otomasyon

* **Sabit Nokta Operasyonu:** Robot, nesneleri önceden belirlenmiş sabit bir toplama noktasından alır.
* **Renk Ayrıştırma:** Nesneler baskın renklerine (RGB) göre sınıflandırılır.
* **Handshake:** Python ve Arduino arasında senkronize çalışma yapısı kuruldu.

### 🚀 Versiyon 2 (Gelecek Hedef) - Dinamik 2D Koordinat Eşleme

* **Pixel-to-Real World Mapping:** Kameradan alınan (x, y) piksel koordinatları, robotun çalışma alanındaki gerçek (mm) koordinatlarına çevrilecek.
* **Dinamik Toplama:** Robot, nesne masanın neresinde olursa olsun (z yüksekliği sabit) nesneyi tam merkezinden yakalayabilecek.
* **YOLOv8 Entegrasyonu:** Renk maskeleme yerine, nesneleri türlerine göre tanıyan derin öğrenme modelleri eklenecek.

### 🧠 Versiyon 3 (Vizyon) - Gelişmiş Kinematik ve Optimizasyon

* **Ters Kinematik (Inverse Kinematics):** Robotun eklemleri açı bazlı değil, kartezyen (X, Y, Z) koordinat verilerine göre otomatik hesaplanan açılarla hareket edecek.
* **Yörünge Planlama:** Servoların daha yumuşak ve doğal hareket etmesi için ivme kontrollü hareket algoritmaları.
* **Hata Telafisi:** Nesne düzgün kavranamazsa, kameradan gelen geri bildirimle pozisyon anlık olarak revize edilebilecek.

---

## 🚀 Başlangıç

### 1. Gereksinimler

Sanal ortamı kurun ve gerekli kütüphaneleri yükleyin:

```bash
cd v1
python3 -m venv .venv
source .venv/bin/activate
pip install opencv-python numpy pyserial

```

### 2. Çalıştırma

1. Arduino'yu bağlayın ve `arduino_v1.ino` dosyasını yükleyin.
2. Otomasyon betiğini çalıştırın:

```bash
python3 src/main.py

```

---

## 👨‍💻 Yazar

**Berkay ILIKOBA** *Bilgisayar Mühendisliği Öğrencisi | Çukurova Üniversitesi* Yapay Zeka, Robotik ve Otonom Sistemler üzerine çalışmalar yürütmektedir.

---
