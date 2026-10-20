# Kesim, ses, altyazı, bölümler

## Sessizlik kesme (`kurgu/scripts/sikilastir.py`)

Konuşma parçalarındaki uzun duraklamaları atar, konuşmanın iki yanında nefes payı bırakır.

```bash
python kurgu/scripts/sikilastir.py IS/kesim.json --esik -35dB --min-sessizlik 0.7 --pay 0.15
```

- Çıktı ayrı dosya: `kesim.sikilastirilmis.json`. Asıl liste değişmez.
- **Eşik süresi:** vlogda 0,6-1,0 sn iyi başlangıç. 0,1-0,3 sn gibi çok kısa eşik konuşanı robot
  gibi yapar (bir Reels "0,1 sn bile boşluk kes" diyordu; röportajda denedik, olmadı).
- **Eşik seviyesi:** rüzgâr, kalabalık, trafik varsa sessizlik bulunmaz. `-30dB`, `-25dB` dene.
- Konuşmasız görüntü (B-roll, manzara) "sessiz" sayılır. Bir parça yarıdan fazla kısalacaksa script
  ona dokunmaz ve uyarır. Kesin elleme dediğin parçaya `"dokunma": true` yaz.

Hazır alternatif: **auto-editor** (`pip install auto-editor`). Tek videodaki sessizlikleri atıp
doğrudan DaVinci zaman çizelgesi verir:

```bash
auto-editor video.mp4 --margin 0.2sec --export resolve
```

Seçenek adları sürümden sürüme değişti (eski sürümlerde `--frame_margin`, `--export_to_resolve`);
`auto-editor --help` ile kendi sürümüne bak. Fark: auto-editor bütün videoya uygular, bizim script
sadece senin seçtiğin parçalara.

## Kaba kurgu (`kurgu/scripts/render.py`)

```bash
python kurgu/scripts/render.py IS/kesim.sikilastirilmis.json --taslak --cikti IS/kaba-v1.mp4
```

- `--taslak`: 720p, hızlı. İzleyip karar vermek için. 4 saatlik 4K kaynakta bile dakikalar sürer,
  çünkü sadece seçilen parçalar kodlanır.
- Farklı kameralar (boyut, kare hızı) ilk parçanın ayarına çekilir; sesi olmayan klibe (drone)
  sessiz ses izi eklenir.
- Her kesimin iki ucunda 10-20 ms ses yumuşatma var: kesim yerinde "tık" sesi çıkmaz.
- Yanında `kaba-v1.bolumler.txt` (YouTube bölümleri) ve `kaba-v1.srt` (kurguya göre kaydırılmış
  altyazı) çıkar.

Bu dosya ön izleme. Asıl kurgu NLE'de (DaVinci ya da CapCut) biter.

## Ses

| İş | Nasıl |
|---|---|
| Seviye | Hedef yaklaşık -14 LUFS (YouTube bu civara normalize eder). `render.py --ses-seviye` ön izlemede yapar; finalde NLE'de |
| Uğultu, rüzgâr | Önce high-pass (~80 Hz). ffmpeg: `-af highpass=f=80` |
| Gürültü azaltma | Dikkatli. Güçlü denoise (ffmpeg `afftdn` ve benzerleri) konuşmayı metalik yapar. Bizde varsayılan değildi, sadece gerçekten gürültülü kayıtta |
| Müzik altında konuşma | NLE'de ducking: DaVinci Fairlight'ta sidechain / otomatik ducking, CapCut'ta ses seviyesi anahtar kareleri |
| Seviye ölçme | `ffmpeg -i video.mp4 -af ebur128=framelog=quiet -f null -` → "Integrated loudness" |

## Altyazı

- `render.py` kaynak transkriptleri kurgunun zamanına kaydırıp `.srt` yazar. YouTube Studio >
  Altyazılar > Dosya yükle.
- Whisper'ın yazdığı metni yüklemeden önce oku: özel adları, sayıları bozar.
- Videoya gömülü altyazı istersen NLE'de yap (DaVinci'de SRT'yi Media Pool'a sürükle, zaman
  çizelgesine at; CapCut'ta otomatik altyazı).

## YouTube bölümleri

`kesim.json`'da `"bolum"` alanı olan her parça bir bölüm başlatır. `render.py` açıklamaya
yapıştırılacak listeyi yazar:

```
00:00 Balonlar
02:41 Sabah 5
09:12 Göreme
```

YouTube'un kuralı: ilk satır 00:00, en az 3 bölüm, her bölüm en az 10 sn. Script uymayanları uyarır.

## İşe yarar ffmpeg komutları

```bash
# bilgi
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of csv=p=0 video.mp4

# tek kare (hızlı: dosyada atlar)
ffmpeg -ss 01:23:45 -i video.mp4 -frames:v 1 kare.jpg

# bir aralığı kayıpsız kes (anahtar kareye denk gelir, sınır birkaç kare kayabilir)
ffmpeg -ss 00:10:00 -i video.mp4 -t 60 -c copy parca.mp4

# bir aralığı kare doğruluğuyla kes (yeniden kodlar)
ffmpeg -ss 00:10:00 -i video.mp4 -t 60 -c:v libx264 -crf 18 -c:a aac parca.mp4

# sessizlikleri listele
ffmpeg -i video.mp4 -af silencedetect=n=-35dB:d=0.7 -f null - 2>&1 | grep silence_

# sahne geçişlerini bul (görüntü değişimi)
ffmpeg -i video.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep pts_time

# proxy (kurgu için hafif kopya)
ffmpeg -i video.mp4 -vf scale=-2:720 -c:v libx264 -preset veryfast -crf 23 -c:a aac proxy.mp4
```
