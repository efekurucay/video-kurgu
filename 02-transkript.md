# Transkript

Bütün yöntem bunun üstüne kurulu: 4 saatlik konuşmayı zaman damgalı yazıya dökmek.

## Araç: Whisper

OpenAI'nin açık konuşma tanıma modeli. Bilgisayarda çalışır, internete ses gönderilmez, ücretsiz.
Türkçede iyi. İki yaygın çalıştırma yolu var, `kurgu/scripts/transkript.py` ikisini de destekler:

| Motor | Nerede iyi | Kurulum |
|---|---|---|
| **whisper.cpp** (`whisper-cli`) | Mac (Apple Silicon) çok hızlı; Windows'ta da var | Program + model dosyası |
| **faster-whisper** (Python) | Windows + NVIDIA kart | `pip install faster-whisper` |

Model: **large-v3-turbo**. Large modele yakın doğruluk, ondan birkaç kat hızlı. Bizim
kullandığımız bu. Hız makineye göre çok değişir; ilk sefer 5-10 dakikalık bir parçayla dene,
süreyi ölç, 4 saati ona göre başlat (gece çalışsın).

Hazır uygulamalar da aynı modeli kullanır (Mac'te MacWhisper, DaVinci'nin kendi transkripti,
CapCut'ın otomatik altyazısı). SRT verebilen herhangi biri iş görür:
`IS/transkript/001.srt` olarak koy, `python kurgu/scripts/tsview.py IS` aynı okunur görünümü üretir.

## Ayarlar (neden önemli)

- **Dil sabit: `tr`.** Otomatik dil tespiti sessiz ya da müzikli başlangıçta yanlış dil seçebilir.
- **Bağlam taşımayı kapat.** whisper.cpp'de `-mc 0`, faster-whisper'da
  `condition_on_previous_text=False`. Açık kalırsa uzun seste whisper bir cümleyi dakikalarca
  tekrar eden bir döngüye girebiliyor. Bizim uzun Türkçe kayıtlarda bu şarttı.
- **`--prompt` ile özel adlar.** Yer, kişi, marka adlarını virgülle ver. Yardım eder ama garanti
  etmez: testte "Göreme" prompt'ta olduğu halde "göremede" yazdı. Altyazıya gidecek metni baştan
  sona oku.

## Çıktılar

```
IS/
  kaynaklar.json      001, 002... her videonun yolu, süresi, çekim tarihi (çekim sırasına göre)
  ses/001.wav         16 kHz mono ses
  transkript/001.srt  zaman damgalı satırlar
  tsview.txt          hepsi tek dosyada, okunur
```

`tsview.txt` örneği:

```
===== 001  DJI_0012.MP4  süre 01:12:40  çekim 2026-10-01T06:00:00Z
[001 00:00:00] Günaydın arkadaşlar. Bugün Kapadokya'dayız ve sabah beşte kalktık.
[001 00:00:10] Evet, balonlar havalandı. Bu manzara gerçekten inanılmaz.
[001 00:03:41] --- 312 sn konuşma yok ---
```

"Konuşma yok" satırları vlogda önemli: oralar çoğu zaman yol, manzara, B-roll. Transkript onları
göremez, kare dökümü görür (`kurgu/scripts/kare.py`).

## Zaman damgalarının hassasiyeti

Whisper'ın satır başı/sonu zamanları **yaklaşıktır**, yarım saniye ile bir saniye kayabilir.
Testimizde whisper konuşmanın 10,46 sn'de başladığını yazdı, gerçek başlangıç 11,27 sn'ydi.

- faster-whisper'da satırlar daha uzun olabiliyor (testte bir satır iki cümleyi ve aradaki 6 sn'lik
  sessizliği kapsadı). Seçim için sorun değil.
- Seçim için (hangi dakikalar) yeterli.
- Kesim noktası için değil. Kesimi ses üzerinden ayarla: `sikilastir.py` sessizliği ölçerek keser;
  NLE'de dalga formuna bakarak kes.
- Kelime düzeyinde zaman lazımsa (tek bir "eee"yi kesmek gibi) dar bir pencereyi kelime kelime
  transkript et: whisper.cpp `-ml 1 -sow`, faster-whisper `word_timestamps=True`. Bütün 4 saate
  kelime düzeyi yapma, yavaş ve gereksiz.

## Birden çok konuşmacı

Whisper kimin konuştuğunu ayırmaz. Gerekirse WhisperX (pyannote ile konuşmacı ayrımı) var; kurulumu
daha zahmetli, Hugging Face hesabı ister. Vlogda çoğu zaman gerekmez.
