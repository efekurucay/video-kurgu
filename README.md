# Uzun çekimden kurgu: transkript + yapay zeka + DaVinci / CapCut

Saatlerce süren ham çekimden izlenebilir video çıkarmak için kullandığımız yöntem: vlog, podcast,
röportaj, eğitim ya da ders kaydı, uzun videodan Reels / Shorts kesitleri. Kendi videolarımızı
(röportajdan Reels, skeç, reklam, egzersiz videoları) bu yöntemle kurguladık; burada projemizden
bağımsız, genelleştirilmiş hali var. En ayrıntılı örnek: 4 saatlik çekimden 25 dakikalık YouTube vlogu.
Türlere göre neyin değiştiği [08-icerik-turleri.md](08-icerik-turleri.md) sayfasında.

Ana fikir: **4 saati izleyerek değil, okuyarak tara.** Konuşmayı yazıya dök, görüntüyü kare
sayfalarına dök, seçimi yazının üstünde yap (istersen yapay zekayla), seçimi bir listeye yaz, o
listeden DaVinci ya da CapCut projesi üret, ince işi orada elle yap.

```
ham çekim ──► transkript + kare dökümü ──► seçim (sen + yapay zeka) ──► kesim.json
                                                                          │
                     ┌────────────────────────────────────────────────────┼─────────────────┐
                     ▼                                                    ▼                 ▼
          kaba kurgu mp4 (izle)                         DaVinci Resolve (.fcpxml)   CapCut projesi
          + YouTube bölümleri + altyazı                 ince kurgu, renk, ses        ince kurgu
```

## Dosyalar

| Dosya | Ne anlatıyor |
|---|---|
| [01-genel-yontem.md](01-genel-yontem.md) | Uzun çekim kurgusunun klasik yöntemi (yapay zekasız da geçerli): seçim, hikâye, tempo, ses, renk |
| [02-transkript.md](02-transkript.md) | Konuşmayı yazıya dökme: whisper, ayarlar, uzun dosya, Türkçe sorunları |
| [03-hikaye-secimi.md](03-hikaye-secimi.md) | 4 saatten 25 dakikaya: yapay zekayla seçim, hazır prompt'lar, kesim listesi formatı |
| [04-kesim-ses-altyazi.md](04-kesim-ses-altyazi.md) | Sessizlik kesme, ses seviyesi, altyazı, YouTube bölümleri, ffmpeg komutları |
| [05-davinci/](05-davinci/README.md) | DaVinci Resolve: hangi sürümde ne çalışır, FCPXML aktarma, Studio'da Claude'un DaVinci'yi MCP ile sürmesi, vlog akışı ve prompt'lar, tuzaklar |
| [06-capcut.md](06-capcut.md) | Listeyi CapCut projesine çevirme ve CapCut'ın tuzakları |
| [07-dersler.md](07-dersler.md) | Bizim kurgularda canımızı yakan şeyler |
| [08-icerik-turleri.md](08-icerik-turleri.md) | Vlog, podcast / röportaj, eğitim, Reels / Shorts kesiti: türe göre süre, hikâye kuralı, ayar, prompt |
| [kurgu/](kurgu/SKILL.md) | Claude Code skill'i + Python script'leri (Windows ve Mac) |
| `ornek/kesim.json` | Kesim listesi örneği |

## Kurulum

### Windows

PowerShell'de:

```powershell
winget install Python.Python.3.12      # kurulumda "Add to PATH" işaretli olsun
winget install Gyan.FFmpeg              # ffmpeg + ffprobe
pip install pillow                      # kare dökümü için
pip install faster-whisper              # transkript (aşağıdaki not)
pip install pycapcut                    # sadece CapCut kullanacaksan
```

Transkript için iki seçenek var, birini kur:

- **faster-whisper** (yukarıda kuruldu). NVIDIA ekran kartı varsa onu kullanır. GPU için CUDA 12 ve
  cuDNN 9 kütüphaneleri gerekir; faster-whisper'ın GitHub sayfasındaki Windows notuna bak. Kart
  yoksa ya da kütüphaneler eksikse işlemcide çalışır, sadece yavaştır. İlk çalıştırmada modeli
  kendisi indirir.
- **whisper.cpp**: github.com/ggml-org/whisper.cpp > Releases > Windows zip'i (NVIDIA varsa adında
  `cublas` geçen). İçinden `whisper-cli.exe` çıkar. Model dosyasını ayrıca indir:
  `https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin`
  Script'e `--whisper-cli C:\whisper\whisper-cli.exe --model C:\whisper\ggml-large-v3-turbo.bin` ver.

Türkçe karakterlerde konsol sorunu çıkarsa bir kere: `setx PYTHONUTF8 1` (sonra terminali kapatıp aç).

Script'ler Mac'te uçtan uca test edildi, Windows'ta hiç çalıştırılmadı. Hata çıkarsa hata çıktısını
ve ilgili script'i bir yapay zeka ajanına (Claude Code vb.) ver; kod kısa ve her dosyanın başında ne
yaptığı yazıyor, düzeltmesi kolay.

### macOS

```bash
brew install ffmpeg whisper-cpp
mkdir -p ~/.cache/whisper-models && curl -L -o ~/.cache/whisper-models/ggml-large-v3-turbo.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
pip3 install pillow pycapcut
```

## Hızlı akış

Windows'ta `python`, Mac'te `python3` yaz. `IS` her vlog için ayrı bir çalışma klasörü.

```bash
# 1) transkript (bütün çekim klasörü verilebilir)
python kurgu/scripts/transkript.py D:/vlog12/is D:/vlog12/ham --motor faster-whisper --prompt "Kapadokya, Göreme"

# 2) kare dökümü: her 30 sn'den bir kare, zaman yazılı sayfalar
python kurgu/scripts/kare.py D:/vlog12/is --aralik 30

# 3) seçim: tsview.txt + kareler/ okunur, kesim.json yazılır (03-hikaye-secimi.md)

# 4) konuşma parçalarındaki uzun sessizlikleri at (isteğe bağlı)
python kurgu/scripts/sikilastir.py D:/vlog12/is/kesim.json

# 5) izlenebilir kaba kurgu + YouTube bölümleri + altyazı
python kurgu/scripts/render.py D:/vlog12/is/kesim.sikilastirilmis.json --taslak --cikti D:/vlog12/is/kaba-v1.mp4

# 6) düzenlenebilir proje
python kurgu/scripts/resolve_fcpxml.py D:/vlog12/is/kesim.sikilastirilmis.json     # DaVinci: File > Import > Timeline
python kurgu/scripts/capcut.py D:/vlog12/is/kesim.sikilastirilmis.json             # CapCut
```

Her script'in en üstünde ne yaptığı ve seçenekleri yazıyor; `python kurgu/scripts/<ad>.py -h` de gösterir.

Ham dosyalara hiçbir script dokunmaz. Bütün kurgu `kesim.json` içinde durur; beğenmezsen listeyi
değiştirip yeniden üretirsin.

## Claude Code ile: `kurgu` skill'i

`kurgu/` klasörü bir Claude Code skill'i: akışı, kuralları ve script'leri tek yerde tutar.
Kurunca Claude Code'a "D:/vlog12/ham'daki çekimden 25 dakikalık vlog çıkar" demen yeter; skill
transkripti çıkarır, sahne haritasını yazar, hikâye yapısını sana onaylatır, kaba kurguyu ve
DaVinci / CapCut projesini üretir.

Kurulum (klasörü Claude Code'un skill klasörüne kopyala):

```powershell
# Windows (PowerShell)
Copy-Item -Recurse kurgu "$env:USERPROFILE\.claude\skills\kurgu"
```

```bash
# macOS (güncellemeleri git pull ile almak için kopya yerine bağlantı)
ln -s "$(pwd)/kurgu" ~/.claude/skills/kurgu
```

Skill olmadan da olur: Claude Code'u bu klasörde açıp "README'yi oku, şu çekimden 25 dakikalık vlog
çıkar" de. Her iki durumda da Claude **videoyu izleyemez, sesi duyamaz**: görüntüyü kare dökümünden,
konuşmayı transkriptten okur. Son karar ve son dinleme senin (07-dersler.md).

DaVinci Studio 21.1+ kullanıyorsan Claude DaVinci'yi doğrudan da sürebilir (MCP):
[05-davinci/2-studio-mcp-kurulum.md](05-davinci/2-studio-mcp-kurulum.md).
