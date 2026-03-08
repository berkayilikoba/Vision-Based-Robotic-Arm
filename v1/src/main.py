import cv2 as cv
import numpy as np
# Kendi modüllerini import ediyorsun
from config import COLOR_THRESHOLD_MAP
from vision import processFrame

def testOnImage():
    # 1. Test edilecek resmi oku (Dosya yolunu kendine göre ayarla)
    # MacBook'ta resim masaüstündeyse: "/Users/berkay/Desktop/test_image.jpg"
    imagePath = "/Users/berkayilikoba/Desktop/Vision-Based-Robotic-Arm/v1/test-images/testImage1.jpeg" 
    frame = cv.imread(imagePath)

    if frame is None:
        print("Hata: Resim dosyası bulunamadı!")
        return

    # 2. Fonksiyonu çalıştır ve hedefleri al
    targets = processFrame(frame, COLOR_THRESHOLD_MAP)

    print(f"Tespit edilen nesne sayısı: {len(targets)}")

    # 3. Sonuçları görselleştir
    for index, target in enumerate(targets):
        cX, cY = target["center"]
        colorName = target["colourName"]
        distance = target["distance"]

        # Kutunun etrafına kontur çiz
        cv.drawContours(frame, [target["contour"]], -1, (0, 255, 0), 2)
        
        # Merkezine nokta koy
        cv.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
        
        # Üzerine sıralama ve mesafe bilgisini yaz
        infoText = f"#{index+1} {colorName.upper()} (Dist: {int(distance)})"
        cv.putText(frame, infoText, (cX - 20, cY - 20), 
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        print(f"Sıra {index+1}: {colorName} - Merkeze Uzaklık: {distance:.2f} piksel")

    # 4. Sonucu ekranda göster
    cv.imshow("Test Sonucu - En Yakindan En Uzaga", frame)
    print("\nKapatmak için bir tuşa basın...")
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == "__main__":
    testOnImage()