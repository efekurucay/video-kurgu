# 4 saatten 25 dakikaya: Claude + DaVinci

Örnek vlog; podcast, eğitim ya da kısa kesitte adımlar aynı, hedef süre ve hikâye kuralı
[../08-icerik-turleri.md](../08-icerik-turleri.md) sayfasındaki gibi değişir.

Ücretsiz sürümde 1-4. adımlar ve 6. adım; Studio + MCP'de hepsi.

## 1. Proje ve klasör

```
D:/vlog12/
  ham/        kameradan kopyalanan dosyalar, hiç dokunulmaz
  is/         transkript, kareler, kesim.json, kaba kurgular
```

DaVinci'de yeni proje: adı `Vlog 12`, kare hızı kaynakla aynı (1-ucretsiz-fcpxml.md, adım 1).

## 2. Tarama ve seçim (DaVinci dışında, Claude Code ile)

Claude Code'u repo klasöründe aç (ya da `kurgu` skill'ini kur, bkz. ana README) ve:

```
D:/vlog12/ham klasöründeki çekimden 25 dakikalık bir YouTube vlogu çıkaracağız.
1. transkript.py ile transkript çıkar (Türkçe, özel adlar: Kapadokya, Göreme),
   kare.py ile 30 sn'de bir kare dökümü yap.
2. tsview.txt'yi saat saat oku, sahne haritasını is/harita.md'ye yaz.
   Kare sayfalarına bakıp görsel olarak güçlü aralıkları ekle.
3. Bana açılış için 3 aday ve bölüm yapısını göster. Onaylamadan kesim.json'a geçme.
```

Onaylayınca:

```
Onayladığım yapıyı is/kesim.json'a yaz. Cümle ortasında kesme, iki yanda 0,3 sn pay bırak,
her bloğun ilk parçasına bölüm adı koy. Sonra sikilastir.py ve render.py --taslak çalıştır.
```

`is/kaba-v1.mp4`'ü izle. Düzeltmeleri söyle ("3. bölüm uzun, yemek kısmını 1 dakikaya indir",
"açılışı 2. adayla değiştir"), Claude listeyi değiştirip yeniden üretsin. Beğenene kadar `v2`, `v3`.

## 3. DaVinci'ye aktar

```
resolve_fcpxml.py ile kesim.sikilastirilmis.json'dan fcpxml üret.
```

DaVinci: File > Import > Timeline. (Studio + MCP'de bunu da Claude'a yaptırabilirsin:
"Vlog 12 projesini aç ve D:/vlog12/is/Vlog-12.fcpxml zaman çizelgesini içe aktar.")

## 4. Elle kontrol

Kesim yerlerini dinleyerek bir tur geç. Yapay zekanın en çok hata yaptığı yer kesim noktaları:
yarım kalan nefes, kesilen kelime ucu.

## 5. Cila (Studio + MCP)

Her prompt'ta iki kural: **önce ne yapacağını listelesin, onaylayınca uygulasın** ve **mevcut zaman
çizelgesini çoğaltıp kopyada çalışsın.** Claude istemediğin şeyi yapmaz ama istediğini de tam
söylediğin kadar yapar; net ol.

**Duraklamalar**
```
"Vlog 12" zaman çizelgesini çoğalt, adı "Vlog 12 v2" olsun. Kopyada konuşma parçalarındaki
0,8 sn'den uzun duraklamaları kes, kesimin iki yanında 0,15 sn pay bırak. Konuşmasız manzara ve
drone parçalarına dokunma. Önce kaç kesim yapacağını ve toplam süreyi söyle.
```

**Tekrar edilen cümleler (aynı şeyi iki kez söylediğin yerler)**
```
Transkripte bak: aynı cümleyi birden fazla söylediğim yerleri listele (zamanlarıyla).
Her birinde en akıcı olanı öner, diğerlerini silmeden önce bana listeyi göster.
```

**İkinci kamera / telefon ekran kaydı**
```
D:/vlog12/ham/telefon_ekran.mp4'ü içe al. Ses dalgasını ana videoyla eşleştir,
görüntüsünü V2'ye koy, sesini alma.
```

**Bölüm işaretleri ve YouTube bölümleri**
```
Zaman çizelgesine şu bölüm adlarıyla işaret (marker) koy: [kesim.json'daki bölümler].
Sonra işaretleri "00:00 Başlık" formatında YouTube açıklaması için listele.
```

**Renk (LUT)**
```
V1'deki bütün klipleri tek renk grubuna al ve D:/LUT/benimlut.cube LUT'unu uygula.
```
LUT yolu tam yol olmalı. Claude LUT uygular ve klipleri gruplar ama Color sayfasına yeni node ve efekt
(glow, grain, halation) ekleyemiyor; onları elle yaparsın.

**Kontrol**
```
Zaman çizelgesini denetle: boşluklar, üst üste binen klipler, offline medya, kare hızı uyuşmazlığı.
Rapor ver, bir şey değiştirme.
```

**Render**
```
"Vlog 12 v2"yi YouTube için render kuyruğuna ekle: 4K H.265 ve 1080p H.264 iki ayrı dosya,
D:/vlog12/cikis/ klasörüne. Ayarları göster, onaylayınca başlat.
```

**Ses:** DaVinci'nin AI Audio Assistant'ı (Fairlight, "Auto Mix", YouTube ayarı) konuşma, müzik ve
efekt seviyelerini kendisi dengeliyor; bir videonun yapımcısı her videosunda kullandığını söylüyor. Arayüzden
çalışıyor, MCP'den çağrılabildiğini doğrulayamadık.

## 6. Son kontrol (insan)

- Baştan sona, kulaklıkla, bir kez telefonda izle.
- Altyazı metnini oku (whisper özel adları bozar).
- Müzik telifi: YouTube Content ID.
- Kapak, başlık, açıklama, bölümler.

## Hareketli grafik (isteğe bağlı)

Videolarda Claude bölüm geçiş animasyonları, ipucu kartları ve intro grafikleri de yapıyor
(HyperFrames ile HTML'den video). Dersleri:

- Serbest bırakınca uzun sürüyor: "istediğin kadar zaman al" deyince 1 saat 38 dakika, net bir tarifle
  (renk, stil, hangi klip, hangi süre, maksimum 30 dakika) yaklaşık 20 dakikada daha iyi sonuç.
- Yapay zekanın ürettiği grafik gösterişli ama "kanıt" değil. Gerçek ekran görüntüsü ve gerçek
  görüntüyle karıştır.
- Ses efektlerini sadece senin onayladığın bir klasörden seçtir.
