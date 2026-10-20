# CapCut

Biz kurgularımızı CapCut masaüstünde bitirdik: script kesim listesinden CapCut projesi üretti, ince
ayarı CapCut'ta elle yaptık. CapCut'ın resmi bir API'si yok; proje dosyası düz bir JSON ve onu
açık kaynak **pyCapCut** kütüphanesi yazıyor.

## Kesim listesinden CapCut projesi

```bash
pip install pycapcut
python kurgu/scripts/capcut.py IS/kesim.sikilastirilmis.json --ad "Vlog 12 Kurgu"
```

- Proje CapCut'ın taslak klasörüne yazılır. CapCut açıksa **kapatıp aç**, açılışta listede görünür.
- Varsayılan taslak klasörü:
  - Windows: `%LOCALAPPDATA%\CapCut\User Data\Projects\com.lveditor.draft`
  - macOS: `~/Movies/CapCut/User Data/Projects/com.lveditor.draft`

  Farklıysa CapCut > Ayarlar > "Taslak konumu" (Draft location) neyi gösteriyorsa onu
  `--taslaklar` ile ver.
- Gelen: tek video izinde sırayla bütün parçalar, kaynağın kendi sesiyle. Her parçanın ucu
  kaynağa bağlı, CapCut'ta çekip uzatabilirsin.
- Müzik, altyazı, efekt CapCut'ta: otomatik altyazı CapCut'ın kendi özelliğiyle daha rahat.

## Tuzaklar (bizde yaşandı)

- **Medya erişimi (Mac).** Bizim Mac'te CapCut korumalı çalışıyordu: elle seçmediğin dosyalardan
  sadece `~/Movies` altını okuyordu. Proje açıldı ama her parça kırmızı "File not accessible" oldu.
  Çözüm `--movies`: kaynakları `~/Movies/CapCut/<ad> Medya/` altına hard link olarak koyar (kopya
  değil, yer kaplamaz). Windows'ta bu sorunu yaşamadık, denemedik.
- **Açık projeye yazma.** Script var olan projenin üstüne yazmaz, her çalıştırma yeni proje.
  CapCut'ta elle düzenlemeye başladığın proje ana kopyadır; listeden yeniden üretirsen elle
  yaptıkların yeni projeye taşınmaz.
- **Sürüm.** CapCut'ın proje formatı sürümden sürüme değişiyor; bazı sürümlerin proje dosyasını
  şifrelediği söyleniyor. Bizde CapCut 9.5 (Mac) ile çalıştı. Kendi sürümünde önce 3-4 parçalık
  bir listeyle dene.
- **Ses seviyesi.** CapCut'ta otomatik loudness yok, seviyeleri elle eşitlersin.
- **Uzun proje.** 25 dakikalık, yüzlerce parçalı projede CapCut yavaşlayabilir. DaVinci uzun
  vlogda daha rahat; CapCut kısa videoda (Shorts, Reels) güçlü.

## Ne zaman CapCut, ne zaman DaVinci

| | CapCut | DaVinci Resolve |
|---|---|---|
| 25-30 dk vlog | Olur, uzun projede ağırlaşabilir | Bunun için yapılmış |
| Hazır efekt, geçiş, şablon, trend yazılar | Çok güçlü | Az, elle |
| Otomatik altyazı | Çok kolay | Var (transkripsiyon) |
| Ses (Fairlight), renk | Temel | Profesyonel |
| Dışarıdan proje üretme | pyCapCut (resmi değil) | FCPXML (her sürüm); Studio 21.1+ da Claude doğrudan sürer (MCP) |

Vlogdan Shorts / Reels çıkarırken CapCut iyi bir ikili: uzun video DaVinci'de, kısa kesitler CapCut'ta.
