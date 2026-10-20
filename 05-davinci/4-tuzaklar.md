# DaVinci + Claude: tuzaklar ve sınırlar

YouTube'daki dört kurulum videosundan, iki skill reposundan ve topluluk MCP'sinin belgelerinden
toplananlar.

## Kurulum

- **Studio şart (B ve C yolları için).** 21.1 ile Python scripting ücretsiz sürümden tamamen kalktı.
  Blackmagic'in gerekçesi: Python API ücretsiz sürüme Studio özelliklerini taşımak için kullanılıyordu.
  Ücretsizde FCPXML aktarma yolu çalışır.
- **External scripting = Local** (C yolu): Preferences > System > General. Ayar yoksa Claude bağlanamaz.
- **DaVinci açık ve bir proje yüklü olmalı.** Kapalıysa MCP "cevap yok" der.
- **Mac'te Python (sadece kendi script'lerin için):** DaVinci Python'u yalnız `PYTHON3HOME` ortam
  değişkeninde ya da `/usr/local/bin/python3`'te arar; Homebrew Python'u görmez.

## Kurgu

- **Kare hızı uyuşmazlığı.** Bir videoda skill 24 fps varsayıyordu, proje 30 fps'ti; kesimler kaydı.
  Proje kare hızını kaynakla aynı yap, Claude'a da söyle.
- **Zaman çizelgesi 01:00:00:00'dan başlar.** Script ile klip yerleştirirken başlangıç karesi sıfır
  değil, zaman çizelgesinin başlangıç karesi (`timeline.GetStartFrame()`) esas alınır. Sıfıra
  konan klip API'de var görünür ama Edit sayfasında boş zaman çizelgesi görürsün.
- **İstediğin kadarını yapar.** Bir videoda Claude en iyi çekimleri seçti ama duraklamaları bırakmıştı,
  çünkü istenmemişti. İstediğini tek tek yaz.
- **Aynı adlı klipler.** Media Pool'da aynı adlı eski klip varsa yanlış sürüm zaman çizelgesine
  girebiliyor. Her denemede yeni bin ya da klip yolunu kontrol ettir.
- **Kesim noktaları.** Kaba kurguyu hızlı yapıyor, kesim yerinde nefes, kelime ucu, ses sıçraması
  bırakıyor. Kesimleri dinleyerek bir tur elle geç.

## Renk ve efekt

- LUT uygular, klipleri gruplar; **Color sayfasına node ve efekt ekleyemez** (glow, grain, halation elle).
  Fusion'da ekleyebiliyor.
- LUT yolu tam yol olmalı, göreli yol "LUT path not found" verir.
- Yapay zeka renge "bakamaz"; kendi ürettiği LUT kötü sonuç veriyor. Hazır, beğendiğin bir LUT ver.

## Erişilemeyenler

- IntelliCut ve IntelliScript arayüzden çalışıyor, MCP'den çağrılamıyor (topluluk skill'inin notu).
- MCP sadece API'nin açtığı işlevleri yapabilir; arayüzdeki her düğme API'de yok.

## Maliyet ve hız

- Uzun özerk görevler pahalı ve yavaş: serbest grafik geçişi 1 saat 38 dakika sürdü. Süre ve stil sınırı ver.
- Videolarda 20 dolarlık Claude planında limitlere takılınabildiği, uzun işler için 100 dolarlık planın
  önerildiği söyleniyor.
- 4 saatlik klibi DaVinci'ye transkript ettirmek de zaman alır; seçimi dışarıda (whisper + kesim.json)
  yapmak hem ucuz hem kontrol edilebilir.

## Güvenlik ve yedek

- Claude'un oluşturduğu script'ler asistanın yetkileriyle çalışır (disk, ağ). İzinleri bilerek ver.
- İlk denemeler atılacak bir projede.
- Her büyük işlemden önce zaman çizelgesini çoğalt; projeyi düzenli dışa aktar (File > Export Project).

## Satış videoları hakkında

Dört videonun dördü de ücretli bir topluluk ya da hazır paket satıyor. Ücretsiz çekirdek hepsinde aynı:
MCP + whisper + ffmpeg (+ HyperFrames). Bu repodaki akış o çekirdeğin üstüne kurulu; paket gerekmez.
