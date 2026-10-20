---
name: kurgu
description: Uzun ham çekimden (1-5 saat, bir ya da çok dosya) izlenebilir video çıkarır: YouTube vlogu, podcast / röportaj (tam ya da özet), eğitim / ders kaydı, uzun videodan Reels / Shorts kesitleri. Transkript (whisper), kare dökümü, sahne haritası, insan onaylı hikâye seçimi, kesim listesi (kesim.json), sessizlik sıkılaştırma, ön izleme mp4, YouTube bölümleri ve altyazı; sonra DaVinci Resolve (FCPXML aktarma ya da Studio MCP) veya CapCut projesi. Kullanıcı "vlog kurgula", "4 saatlik videodan vlog çıkar", "podcast kurgula", "röportajı kes", "ders kaydını kısalt", "uzun videodan reels çıkar", "shorts kesitleri", "uzun çekimi kes", "kaba kurgu yap", "DaVinci'ye aktar", "CapCut projesi yap", "transkript çıkar", "rough cut", "long footage to vlog" dediğinde.
---

# kurgu

Uzun çekimi izleyerek değil okuyarak tara, seçimi bir listeye yaz, listeden kurgu üret.
Ham dosyalara asla dokunma; bütün kurgu `kesim.json` içinde.

Bu skill'in klasöründe `scripts/` var. Aşağıda `S` = bu SKILL.md'nin bulunduğu klasörün
`scripts` alt klasörü (tam yol). Windows'ta `python`, Mac'te `python3`.

Rehberin tamamı (yöntem, DaVinci, CapCut, dersler) skill'in geldiği reponun kökünde:
`README.md`, `01-...07-*.md`, `05-davinci/`. Kullanıcı yöntemi sorarsa oradan oku.

## Değişmez kurallar

- **Videoyu izleyemezsin, sesi duyamazsın.** Görüntüyü kare dökümünden, konuşmayı transkriptten
  okursun. Kurgunun "iyi olduğunu" iddia etme; neyi nasıl kontrol ettiğini söyle. Son izleme insanda.
- **İki onay noktası:** (1) hikâye yapısı ve seçilen aralıklar, (2) final. İkisini de kullanıcı verir.
  Onay almadan kesim listesini "son" sayma, DaVinci'de zaman çizelgesini değiştirme.
- **Zamanı transkriptten oku, tahmin etme.** Anlaşılmayan yeri "belirsiz" diye işaretle.
- **Cümle ortasında kesme.** Whisper satır zamanları 0,5-1 sn kayar; kesim noktasını sesle doğrula
  (`sikilastir.py` sessizliği ölçer; şüpheli yerde 2-3 sn'lik pencereyi tek başına transkript et).
- **Her deneme versiyonlu:** `kaba-v1.mp4`, `kaba-v2.mp4`; DaVinci'de zaman çizelgesini çoğalt.
- Kurulum eksikse (ffmpeg, whisper, pillow) kullanıcıya reponun README'sindeki Kurulum bölümünü göster.

## Akış

### 1. Kaynaklar ve iş klasörü

Kullanıcıdan: **içerik türü** (vlog, podcast/röportaj, eğitim, Reels/Shorts kesitleri), ham çekim
klasörü, iş klasörü (`IS`), hedef süre, kanal tarzı, özel adlar (yer,
kişi), DaVinci mi CapCut mı, DaVinci ise sürümü (Studio mu, ücretsiz mi; bkz. 5. adım).

### 2. Transkript + kare dökümü

```bash
python S/transkript.py IS HAM_KLASORU --prompt "özel, adlar"            # Mac: whisper-cpp (varsayılan)
python S/transkript.py IS HAM_KLASORU --motor faster-whisper --prompt "..."  # Windows / NVIDIA
python S/kare.py IS --aralik 30
```

Uzun çekimde önce 5-10 dakikalık bir dosyayla süreyi ölç, sonra hepsini başlat (arka planda).
Çıktılar: `IS/kaynaklar.json`, `IS/transkript/*.srt`, `IS/tsview.txt`, `IS/kareler/*.jpg`, boş `IS/kesim.json`.

### 3. Sahne haritası

`tsview.txt`'yi kaynak kaynak (`=====` satırları) ya da saat saat oku. `IS/harita.md`'ye yaz:

| kaynak | başlangıç | bitiş | ne oluyor | enerji 1-5 | hikâye değeri | kalsın/belki/at |

Ayrıca: açılış adayı anlar (komik, duygusal, şaşırtıcı, gerilimli), tekrar edilen anlar
("aynı şey 01:12'de daha iyi"). "konuşma yok" satırlarını kare sayfalarıyla eşle: görsel olarak
güçlü aralıkları (manzara, ışık, yemek, yol) B-roll adayı olarak not et; bulanık/karanlık olanları ele.

### 4. Hikâye (ONAY 1)

Türe göre omurga, hedef süre ve sıkılaştırma ayarı reponun `08-icerik-turleri.md` sayfasında
(vlog: olay olay, kronoloji bozulabilir; podcast: fikir fikir, soruyu koru, söyleneni çarpıtma;
eğitim: kronoloji korunur, hatalı denemeler atılır; Reels/Shorts: kendi başına anlaşılan 30-60 sn,
her kesit ayrı `kesit-NN.json`). Sayfa yoksa bu özeti uygula.

Kullanıcıya göster:
- Bölümün sorusu ve değişimi (bir cümle).
- 3 açılış adayı (ilk 30-60 sn; kronoloji bozulabilir, en güçlü an başa).
- Bölüm yapısı: blok adı, süre, aralıklar, neden.
- Atılan iyi anlar (kısa video adayı).

İlk liste hedefin ~%30 üstünde olsun. Onaydan sonra `IS/kesim.json`:

```json
{"baslik": "...", "kaynaklar": {"001": "..."},
 "parcalar": [{"kaynak": "001", "giris": "00:41:10.5", "cikis": "00:41:32.0", "bolum": "Balonlar", "not": "açılış"},
              {"kaynak": "003", "giris": 65, "cikis": 77, "dokunma": true, "not": "drone"}]}
```

`bolum`: YouTube bölümü başlatır. `dokunma`: sıkılaştırma kesmez (konuşmasız görüntü, müzikli montaj).
Parça uçlarını cümle başı/sonuna koy, iki yanda ~0,3 sn pay.

### 5. Üretim

```bash
python S/sikilastir.py IS/kesim.json --min-sessizlik 0.7        # konuşmadaki uzun duraklamalar
python S/render.py IS/kesim.sikilastirilmis.json --taslak --cikti IS/kaba-v1.mp4
```

`render.py` yanına `kaba-v1.bolumler.txt` (YouTube bölümleri) ve `kaba-v1.srt` (kurguya göre altyazı) yazar.
Kendi kontrolün: çıktıyı yeniden transkript et (cümleler doğru sırada mı), kare dökümüne bak
(`kare.py` yerine `ffmpeg -i kaba-v1.mp4 -vf "fps=1/20,scale=320:-2,tile=8x4" -frames:v 1 kontrol.jpg`).
Kullanıcı izler, düzeltme ister, listeyi değiştir, `v2` üret.

Sonra düzenlenebilir proje:

- **DaVinci (her sürüm):** `python S/resolve_fcpxml.py IS/kesim.sikilastirilmis.json` → DaVinci'de
  File > Import > Timeline. Proje kare hızını önce kaynakla aynı yaptır.
- **DaVinci Studio + MCP araçların varsa** (DaVinci'nin 21.1 MCP'si ya da `davinci-resolve-mcp`):
  aktarmayı ve cilayı sen yap. Her işlemden önce zaman çizelgesini çoğalt, ne yapacağını listele,
  onay al. Yapabildiklerin: içe aktarma, duraklama kesme, ses dalgasıyla ikinci kamera eşleme,
  işaretler, LUT (tam yol), denetim raporu, render kuyruğu. Yapamadıkların: Color sayfasına node/efekt
  eklemek, IntelliCut/IntelliScript. Script ile klip yerleştirirken başlangıç karesi
  `timeline.GetStartFrame()` (genelde 01:00:00:00), sıfır değil. Ayrıntı: `05-davinci/`.
- **CapCut:** `python S/capcut.py IS/kesim.sikilastirilmis.json` (`pip install pycapcut`).
  Mac'te CapCut medyayı sadece `~/Movies` altından okuyabiliyorsa `--movies`. CapCut'ı kapatıp açtır.
  Var olan projenin üstüne yazılmaz.

### 6. Final (ONAY 2)

Kullanıcıya hatırlat: kulaklıkla bir tur izle, altyazı metnini oku (whisper özel adları bozar),
müzik telifi (YouTube Content ID), bölümler (ilk satır 00:00, en az 3, her biri en az 10 sn).

## Rapor

Her turda: çıktı yolları, süre, neyi nasıl kontrol ettiğin, neyi kontrol edemediğin (ses, akış,
renk). "Hazır", "mükemmel" deme; kontrol ettiğini söyle.
