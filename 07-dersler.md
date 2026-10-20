# Dersler: canımızı yakan şeyler

Kendi videolarımızı (röportajdan 10 Reels, 35 sn'lik skeç, reklam, 37 egzersiz videosu) bu yöntemle
kurgularken öğrendiklerimiz. Çoğu vlog için de geçerli.

## Yapay zekayla çalışırken

- **Yapay zeka videoyu izleyemez, sesi duyamaz.** Kare dökümüne bakar, transkripti okur. Kurgu
  "kare dökümünde doğru görünüyor" ama bir kesim yerinde ses patlıyor ya da müzik konuşmayı
  bastırıyor olabilir. Son izleme ve dinleme insanda.
- **Kontrol yöntemi:** çıkan videoyu yeniden transkript et. Cümleler doğru sırada ve eksiksiz mi,
  okuyarak kontrol edersin. Görüntü için çıktının kare dökümüne bak.
- **İki onay noktası.** (1) Hangi anlar seçildi, (2) final. Arada her şey otomatik olabilir, bu ikisi olamaz.
- **Önce küçük dene.** Yeni bir ayar ya da araç 4 saatte değil, 5 dakikalık parçada denenir.
- **Uydurmasın.** Prompt'a "zamanı transkriptten oku, tahmin etme", "anlaşılmıyorsa belirsiz yaz" koy.

## Transkript

- `-mc 0` (bağlam taşıma kapalı) olmadan uzun Türkçe seste whisper aynı cümleyi döngüye sokabiliyor.
- Özel adları bozar: prompt'a yazsan bile ("Göreme" → "göremede"). Altyazıyı baştan sona oku.
- Satır zamanları yarım-bir saniye kayar. Seçim için yeter, kesim için sesle (sessizlik, dalga formu) düzelt.
- Kesim noktası kelime ortasına düşmesin. Kaba segment sınırı bir kelimeyi bölebilir; şüphedeysen
  o 2-3 saniyelik pencereyi tek başına transkript et, kelimeyi doğrula.

## Kesim

- Sessizlik eşiği çok kısa olunca konuşma robotlaşır. Röportajda 0,45 sn'de karar kıldık; vlogda
  0,6-1,0 sn daha doğal.
- Her kesimin ucuna 10-20 ms ses yumuşatma koy, yoksa "tık" duyulur.
- Ham dosyaya dokunma. Kurgu bir listede (kesim.json / NLE projesi) dursun, her deneme versiyonlu
  (`v1`, `v2`...). Geri dönmek dosya açmak kadar kolay olur.
- Telefon videolarında dikey görüntü yatay saklanıp "döndür" bilgisiyle gelir; boyutu okurken buna
  bak (script'ler bakıyor).
- 4K uzun dosyadan kare almak için videoyu baştan çözme, o saniyeye atla (`-ss` girişten önce).
  Fark saatler ile dakikalar arası.

## Ses

- Güçlü gürültü azaltma (denoise) konuşmayı metalik yapıyor. Varsayılan: high-pass + seviye eşitleme.
- Farklı çekimlerin seviyesi farklı. Her parçayı ölç (`ebur128`), aynı seviyeye çek.
- Müzik konuşmanın altında kısık, konuşmasız yerde yüksek. Konuşma varken müzik sabit seviyede kalırsa
  konuşmayı yer.

## Telif

- Meme sesleri, film müziği, dizi sahneleri: organik paylaşımda pratikte çok kullanılıyor; reklamda
  platformlar reddedebiliyor.
- **YouTube farklı:** Content ID telifli müziği ve sahneyi otomatik tanır; gelir hak sahibine gider
  ya da video bazı ülkelerde engellenir. Uzun vlogda müziği YouTube Audio Library'den ya da lisansı
  açık kütüphaneden al.

## CapCut

- Mac'te yalnız `~/Movies` altını okuyordu ("File not accessible"); hard link ile çözüldü.
- Yeni proje ancak CapCut kapatılıp açılınca listede görünüyor.
- Elle düzenlenmiş projenin üstüne yazılmaz; her üretim yeni proje.

## Genel

- Logo, font gibi marka öğelerini uydurma, gerçek dosyayı kullan. Uydurma "yapay zeka işi" gibi
  duruyor, izleyici fark ediyor.
- Kronolojiyi bozmaktan korkma: en güçlü an başa, sonra "buraya nasıl geldik".
