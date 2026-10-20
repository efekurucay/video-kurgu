# Uzun çekimden kurgu: genel yöntem

Bu bölüm araçtan bağımsız. Yapay zeka kullansan da kullanmasan da kurgunun kendisi bu adımlardan
geçer; script'ler sadece yavaş kısımları hızlandırır. Örnek vlog; podcast, eğitim ve kısa kesitlerde
neyin değiştiği [08-icerik-turleri.md](08-icerik-turleri.md) sayfasında.

## Oran ve beklenti

4 saatlik vlog çekiminden 25 dakika, kabaca 1'e 10. Bu oranda tek geçişte doğru seçim yapılmaz. İki eleme yap:

1. **Selects (bol seçim):** "İşe yarayabilir" dediğin her şey. 4 saat → 60-90 dk.
2. **Hikâye kurgusu:** selects'ten hikâyeyi kur. 60-90 dk → 25-30 dk.

İlk elemede cömert ol, ikincide acımasız. İkisini aynı anda yapmaya çalışmak en çok zaman yiyen hata.

## Adımlar

### 1. Toplama ve düzen (ingest)

- Bütün kartları tek klasöre kopyala: `ham/`. Asıl dosyaları hiç değiştirme, adını bile.
- Kamera, telefon, drone, harici mikrofon ayrı alt klasörlere.
- Harici mikrofonla çektiysen sesi videoyla eşle. DaVinci'de birden çok klibi seçip sağ tık
  > "Auto Sync Audio" > "Based on Waveform" ses dalgasına göre eşler.
- 4K / 10-bit / HEVC çekim kurgu sırasında bilgisayarı yorar. Kurguyu **proxy** (düşük çözünürlüklü
  kopya) ile yap, çıkışı aslından al. DaVinci'de klipleri seç > sağ tık > "Generate Proxy Media".

### 2. Tarama (logging)

Amaç: "nerede ne var" haritası. Klasik yöntem hızlandırılmış izleyip not almak. Hızlısı:

- **Konuşma:** transkript (02-transkript.md). 4 saati okumak, izlemekten kat kat hızlı.
- **Görüntü:** kare dökümü (`kurgu/scripts/kare.py`). Her 30 saniyeden bir kare, zaman yazılı sayfalar.
  Konuşmasız manzara, yol, yemek, gün batımı burada görünür.
- Haritaya her bölüm için: zaman aralığı, ne oluyor, enerji (1-5), hikâyeye katkı.

### 3. Hikâye

Çekim bir kayıt ama izleyici kayıt izlemez, hikâye izler. Vlog bir günlüktür, podcast bir sohbet,
ders bir anlatım; hepsinde sorulacak üç soru:

- **Bu bölümün sorusu ne?** "Balon turuna yetişebilecek miyiz?", "Bu şehir abartılıyor mu?" Bir
  soru, cevabı sona kadar bekletir.
- **Değişim ne?** Başta ne biliyordun / ne hissediyordun, sonda ne değişti.
- **Neyi atarsam hikâye bozulmaz?** Bozulmuyorsa at. Güzel ama hikâyesiz anlar ayrı bir kısa video olur.

Yapı (25 dakikalık vlog için kaba; diğer türler 08'de):

| Bölüm | Süre | İş |
|---|---|---|
| Açılış (hook) | 0:00-0:45 | En güçlü an ya da bölümün sorusu. Logo, uzun giriş, "merhaba arkadaşlar" sonra. |
| Kurulum | ~2-3 dk | Nerede, neden, plan ne |
| Gelişme | 3-5 blok × 3-5 dk | Her blokta bir olay, bir küçük gerilim ya da sürpriz |
| Doruk | ~2-3 dk | Günün en büyük anı |
| Kapanış | ~1 dk | Ne değişti, bir sonraki bölüme köprü |

YouTube'da ilk 30-60 saniye izleyicinin kalıp kalmayacağını belirler. Kronolojiyi bozmak serbest:
en güçlü anı başa koyup "bu ana nasıl geldik" diye geri dönmek klasik bir açılıştır.

### 4. Kaba kurgu (rough cut)

- Sadece sıralama ve uzunluk. Renk, müzik, efekt yok.
- Hedef sürenin %20-30 üstünde kalması normal; sıkıştırma sonraki adım.
- Bir kere baştan sona, durmadan izle. Sıkıldığın her yere not düş; sıkıldığın yer izleyicinin çıktığı yerdir.

### 5. Sıkılaştırma ve ince kurgu

- **Jump cut:** konuşmadaki duraklama, "eee", tekrar. Vlogda kabul görür ama her birini kesme;
  nefes alacak yer kalsın.
- **B-roll ile örtme:** jump cut'ın üstüne o anla ilgili görüntü koymak kesmeyi gizler.
- **J-cut / L-cut:** bir sonraki sahnenin sesi görüntüden önce başlar (J) ya da önceki sahnenin
  sesi görüntüden sonra biter (L). Kesmeler yumuşar, "kurgu" hissi azalır.
- **Tempo:** konuşma blokları arasında 5-15 sn'lik nefes (manzara + müzik) izleyiciyi dinlendirir.
- **Montaj:** hızlı geçen kısımlar (yol, hazırlık) 2-3 saniyelik planlarla müzik üstünde.

### 6. Ses

Görüntüden önemli. İzleyici kötü görüntüyü affeder, kötü sesi affetmez.

- Konuşma seviyesi bütün video boyunca eşit olmalı. Çıkışta YouTube için hedef yaklaşık -14 LUFS
  (YouTube sesi bu civara normalize eder).
- Müzik konuşmanın altında kısılır (ducking), konuşmasız yerde yükselir.
- Rüzgâr ve uğultu için önce hafif yöntem: düşük frekans kesme (high-pass ~80 Hz). Gürültü
  azaltma (denoise) güçlüyse sesi metalik yapar, dozunu dinleyerek ayarla.

### 7. Renk

- Önce **düzeltme** (her klip normal görünsün, kameralar birbirine uysun), sonra **görünüm** (genel his).
- LOG çektiysen kameranın LUT'u ile başla.

### 8. Altyazı, bölümler, kapak

- Altyazıyı videoya basmak yerine YouTube'a SRT olarak yükle: aranabilir, izleyici açıp kapatır.
- **YouTube bölümleri (chapters):** açıklamaya `00:00 Başlık` satırları. İlk satır 00:00 olmalı,
  en az 3 bölüm, her biri en az 10 saniye. `render.py` bunu kesim listesinden üretir.
- Kapak için videonun en güçlü 3-5 karesini aday çıkar, yüz + tek fikir + az yazı.

### 9. Son kontrol

- Telefonda ve kulaklıkla bir kez izle.
- Müzik telifi: YouTube'da telifli müzik Content ID'ye takılır, gelir hak sahibine gider ya da video
  engellenir. YouTube Audio Library ya da lisansı açık kütüphane kullan.
- Yüzü bulanıklaştırılması gereken kişiler, okunan plakalar, ekranda kalan kişisel bilgiler.

## Zamanı en çok kurtaran üç şey

1. İzleyerek değil okuyarak tara (transkript + kare dökümü).
2. Selects ile hikâyeyi ayrı geçişlerde yap.
3. Kurguyu bir listede tut (kesim.json ya da NLE projesi). Ham dosyaya dokunma, her denemeyi
   versiyonla (`kaba-v1`, `kaba-v2`...).
