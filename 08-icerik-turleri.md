# İçerik türleri: ne değişir

Akış her türde aynı: transkript + kare dökümü → harita → hikâye (onay) → `kesim.json` → kaba kurgu
→ DaVinci / CapCut. Değişen dört şey: hedef süre, hikâyenin omurgası, sıkılaştırma ayarı ve
seçim prompt'una eklenecek kurallar. Prompt eklemelerini 03-hikaye-secimi.md'deki Prompt 3'ün
sonuna yapıştır.

## Özet

| Tür | Tipik oran | Omurga | `sikilastir.py` | B-roll / görüntü |
|---|---|---|---|---|
| Vlog | 4 sa → 25 dk | Bölümün sorusu + değişim, olay olay | `--min-sessizlik 0.7`, manzaraya `dokunma` | Çok; konuşmasız anlar kare dökümünden |
| Podcast / röportaj | 2 sa → 60-90 dk (tam) ya da 10-20 dk (özet) | Fikirler, konu konu | `--min-sessizlik 1.0` (sohbet nefes ister) | Az; kamera açısı değişimi |
| Eğitim / ders kaydı | 60 dk → 8-15 dk | Öğrenme sırası, adım adım | `--min-sessizlik 0.5` | Ekran kaydı, yakın plan |
| Reels / Shorts kesiti | 1 uzun video → 5-15 kesit × 30-60 sn | Tek fikir, tek vuruş | `--min-sessizlik 0.4` | Altyazı, ilk karede yüz |

## Vlog

Rehberin ana örneği; ayrıntı 01 ve 03'te.

- Kronoloji bozulabilir: en güçlü an başa, "buraya nasıl geldik" diye geri dön.
- Konuşmasız manzara, yol, yemek bölümleri müzik altında 2-3 sn'lik planlarla akar; `"dokunma": true`.
- Bölümler (YouTube chapters) yer ya da olay adıyla.

Prompt eklemesi:
```
Tür: seyahat / günlük vlog. Konuşmasız güzel görüntüleri (kare notlarından) bloklar arasına
5-15 sn'lik nefes olarak yerleştir. Aynı yerde geçen tekrarlayan anlardan en enerjik olanı al.
```

## Podcast / röportaj

İki ayrı ürün çıkar, hangisini istediğine baştan karar ver:

- **Tam bölüm (60-90 dk):** az kesilir. Sadece teknik duraklamalar, konu dışı uzun sapmalar,
  tekrarlanan sorular ve "bunu yayınlamayalım" denen yerler atılır. Sıra bozulmaz.
- **Özet / en iyi anlar (10-20 dk):** fikir fikir seçilir, sıra konuya göre kurulabilir.

Kurallar:
- Soruyu kesme: cevap tek başına anlaşılmıyorsa soruyu ya da kısa bir bağlam cümlesini koru.
- Konuşanın sözünü ortadan kesip başka yere bağlama; anlamı değiştirebilir. Kesim, fikir bitince.
- Çok kameralıysa açı değişimi kesmeyi gizler: kesim yerinde diğer kişiye ya da geniş plana geç
  (DaVinci'de multicam). Tek kameralıysa yakınlaştırma (punch-in) aynı işi görür.
- Whisper konuşmacıları ayırmaz; gerekirse transkripte isimleri sen ekle ya da WhisperX kullan.

Prompt eklemesi:
```
Tür: podcast / röportaj, [tam bölüm | 15 dakikalık özet]. Konuşmacılar: [A], [B].
Her fikri tamamlanmış haliyle al; soru olmadan anlaşılmayan cevaplarda soruyu da al.
Söyleneni çarpıtacak birleştirme yapma. Özetse: bölüm açılışına en çarpıcı tek cümleyi koy.
```

## Eğitim / ders kaydı / ekran kaydı

- Omurga öğrenme sırası: kronoloji genelde korunur, çünkü adımlar birbirine bağlı.
- Atılanlar: hatalı denemeler, "bir saniye, şunu açayım" beklemeleri, tekrar anlatılan yerlerden kötü olanı.
- Uzun bekleme (yükleme, render) hızlandırılır ya da "birkaç dakika sonra" kartıyla atlanır.
- Ekran kaydı varsa sesi ana kamerayla dalga formundan eşle; görüntüyü üst ize koy.
- Bölümler adım adlarıyla ("1. Kurulum", "2. İlk proje"); eğitimde bölümler en çok tıklanan yer.

Prompt eklemesi:
```
Tür: eğitim videosu. Kronolojiyi koru. Hatalı denemeleri ve beklemeleri at; aynı şeyin iki kez
anlatıldığı yerde daha net olanı al. Her bölüm bir adım olsun, bölüm adı adımın adı.
İzleyicinin takip etmesi gereken hiçbir adımı atma; şüpheliysen "belki" işaretle.
```

## Uzun videodan Reels / Shorts kesitleri

Bir uzun videodan çok sayıda dikey kısa video. Seçim kuralları uzun videodan farklı:

- **Tek fikir, tek vuruş.** 30-60 sn'de bir şey anlatır ve biter. Bağlam gerektiren an uygun değil.
- **İlk 1-2 saniye her şey.** Kesit, konunun ortasından değil en çarpıcı cümleden başlar. Ekranda
  ilk karede yüz olsun.
- **Sona kadar izletme:** son cümle bir sonuç, espri ya da ters köşe olsun; kesit açıkta kalmasın.
- **Altyazı şart.** Çoğu kişi sessiz izler. Kısa satırlar, kelime kelime ya da cümle cümle.
- **Dikey kadraj:** 16:9 kaynaktan 9:16 kırpılır; konuşan kadrajın ortasında kalmalı. DaVinci'de
  zaman çizelgesi 1080×1920 + Smart Reframe, CapCut'ta oran 9:16 + otomatik kadraj.
- Sıkılaştırma daha agresif (0,4 sn) ama robotlaşma sınırı burada da var; röportajda 0,45 sn'de karar kıldık.

Bu repodaki script'ler kesiti seçer ve keser (`kesim.json`'da her kesit için ayrı bir dosya ya da
tek dosyada ayrı parçalar); dikey kırpma ve altyazı basma NLE'de (DaVinci / CapCut) yapılır.

Prompt eklemesi:
```
Tür: [uzun video adı]'ndan Reels/Shorts kesitleri. 30-60 sn'lik, kendi başına anlaşılan
[10] an bul. Her biri için: başlangıç-bitiş, ilk cümle (hook), son cümle (vuruş), neden
paylaşılır, ekrana yazılacak 3-6 kelimelik başlık. Bağlam isteyen anları alma.
Her kesit için ayrı bir kesim listesi yaz: is/kesit-01.json, is/kesit-02.json ...
```

## Diğerleri (kısaca)

- **Etkinlik / düğün / konser:** müzik omurgadır; kesimler müziğin vuruşuna göre, konuşma az. Transkript
  burada daha az işe yarar, kare dökümü ve ses (alkış, müzik) daha çok.
- **Belgesel / mülakat derlemesi:** birden çok kişiden aynı soruya verilen cevapları yan yana koymak;
  harita aşamasında her cevabı konu etiketiyle işaretle.
- **Canlı yayın (stream) özeti:** saatlerce yayından en iyi anlar; sohbet (chat) kaydı varsa en çok
  tepki alan dakikalar iyi bir ön elemedir.
