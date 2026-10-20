"""Videolardan sesi çıkarır, Türkçe transkript üretir, okunur özet (tsview) yazar.

Kullanım:
    python transkript.py IS_KLASORU video1.mp4 video2.mov ...   (ya da bir klasör: IS_KLASORU D:/Cekimler/gun1)

İki motor var, ikisi de bilgisayarda çalışır, internete bir şey gitmez:
    --motor whisper-cpp      (varsayılan) whisper.cpp'nin whisper-cli programı. Mac'te çok hızlı.
    --motor faster-whisper   Python paketi (pip install faster-whisper). Windows + NVIDIA kartta hızlı.

Ne üretir (IS_KLASORU altında):
    kaynaklar.json        her videoya kısa bir kimlik (001, 002...), çekim sırasına göre
    ses/001.wav           16 kHz mono ses
    transkript/001.srt    zaman damgalı transkript
    tsview.txt            hepsi tek dosyada, okunur: [001 00:12:03] metin
    kesim.json            boş kesim listesi (yoksa); seçimleri buraya yazarsın

Seçenekler:
    --model         whisper-cpp: ggml model dosyası (varsayılan ~/.cache/whisper-models/ggml-large-v3-turbo.bin
                    ya da $WHISPER_MODEL). faster-whisper: model adı (varsayılan large-v3-turbo; ilk sefer indirir)
    --whisper-cli   whisper-cli programının yolu, PATH'te değilse (Windows'ta: C:/whisper/whisper-cli.exe)
    --dil tr        konuşma dili
    --prompt "..."  whisper'ın sık bozduğu özel adlar: "Kapadokya, Göreme, DJI Osmo"
    --yeniden       var olan transkriptleri de baştan üret
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import gerekli, srt_yaz, video_bilgi  # noqa: E402
from tsview import tsview_yaz  # noqa: E402

UZANTI = (".mp4", ".mov", ".m4v", ".mkv", ".mts", ".avi", ".mxf", ".mp3", ".wav", ".m4a")


def whisper_cpp(a, wav, cikti):
    # -mc 0: önceki metni bağlam olarak taşıma; uzun seste whisper'ın aynı cümleyi döngüye sokmasını engeller
    cmd = [a.whisper_cli, "-m", a.model, "-l", a.dil, "-mc", "0", "-bs", "5", "-osrt", "-of", cikti, "-f", wav]
    if a.prompt:
        cmd += ["--prompt", a.prompt]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        sys.exit(f"HATA: whisper-cli çalışmadı:\n{r.stderr[-2000:]}")


_fw = None


def faster_whisper(a, wav, cikti):
    global _fw
    if _fw is None:
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            sys.exit("HATA: faster-whisper yok. Kur: pip install faster-whisper")
        _fw = WhisperModel(a.model, device="auto", compute_type="default")
    segs, _ = _fw.transcribe(wav, language=a.dil, beam_size=5, initial_prompt=a.prompt or None,
                             condition_on_previous_text=False, vad_filter=True)  # whisper-cpp'deki -mc 0'ın karşılığı
    srt_yaz(cikti + ".srt", [(s.start, s.end, s.text.strip()) for s in segs])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("is_klasoru")
    ap.add_argument("videolar", nargs="+")
    ap.add_argument("--motor", choices=["whisper-cpp", "faster-whisper"], default="whisper-cpp")
    ap.add_argument("--model")
    ap.add_argument("--whisper-cli", default=os.environ.get("WHISPER_CLI", "whisper-cli"))
    ap.add_argument("--dil", default="tr")
    ap.add_argument("--prompt", default="")
    ap.add_argument("--yeniden", action="store_true")
    a = ap.parse_args()
    gerekli("ffmpeg", "ffprobe")
    if a.motor == "whisper-cpp":
        a.model = a.model or os.environ.get(
            "WHISPER_MODEL", os.path.expanduser("~/.cache/whisper-models/ggml-large-v3-turbo.bin"))
        if not (shutil.which(a.whisper_cli) or os.path.exists(a.whisper_cli)):
            sys.exit(f"HATA: whisper-cli bulunamadı ({a.whisper_cli}). --whisper-cli ile yolunu ver "
                     f"ya da --motor faster-whisper kullan. README.md > Kurulum")
        if not os.path.exists(a.model):
            sys.exit(f"HATA: model yok: {a.model}\nİndir: README.md > Kurulum")
        yaz = whisper_cpp
    else:
        a.model = a.model or "large-v3-turbo"
        yaz = faster_whisper

    dosyalar = []
    for v in a.videolar:
        v = os.path.expanduser(v)
        if os.path.isdir(v):
            dosyalar += sorted(f for f in glob.glob(os.path.join(v, "*")) if f.lower().endswith(UZANTI))
        else:
            dosyalar.append(v)
    if not dosyalar:
        sys.exit("HATA: video bulunamadı.")

    IS = os.path.abspath(a.is_klasoru)
    for d in ("ses", "transkript"):
        os.makedirs(os.path.join(IS, d), exist_ok=True)

    # çekim sırası: kameranın yazdığı tarih, yoksa dosya adı
    bilgi = [video_bilgi(os.path.abspath(f)) for f in dosyalar]
    bilgi.sort(key=lambda b: (b["cekim"] or "", os.path.basename(b["yol"])))
    kp = os.path.join(IS, "kaynaklar.json")
    kaynaklar = json.load(open(kp, encoding="utf-8")) if os.path.exists(kp) else {}
    bilinen = {v["dosya"] for v in kaynaklar.values()}
    for b in bilgi:
        if b["yol"] not in bilinen:
            kaynaklar[f"{len(kaynaklar) + 1:03d}"] = {"dosya": b["yol"], "sure": round(b["sure"], 2),
                                                      "cekim": b["cekim"], "ses": b["ses"]}
    json.dump(kaynaklar, open(kp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    toplam = sum(v["sure"] for v in kaynaklar.values())
    print(f"{len(kaynaklar)} kaynak, toplam {toplam / 3600:.2f} saat")
    for i, v in kaynaklar.items():
        srt = os.path.join(IS, "transkript", i)
        if os.path.exists(srt + ".srt") and not a.yeniden:
            continue
        if not v.get("ses", True):  # drone, timelapse: ses izi yok
            srt_yaz(srt + ".srt", []); print(f"  {i} ses yok, atlandı"); continue
        wav = os.path.join(IS, "ses", i + ".wav")
        if not os.path.exists(wav) or a.yeniden:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", v["dosya"], "-vn", "-ac", "1", "-ar", "16000",
                            "-c:a", "pcm_s16le", wav], check=True)
        print(f"  {i} transkript çıkarılıyor ({v['sure'] / 60:.1f} dk) ...", flush=True)
        yaz(a, wav, srt)

    tsview_yaz(IS)
    kes = os.path.join(IS, "kesim.json")
    if not os.path.exists(kes):
        json.dump({"baslik": os.path.basename(IS),
                   "kaynaklar": {i: v["dosya"] for i, v in kaynaklar.items()},
                   "parcalar": []}, open(kes, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"OK {os.path.join(IS, 'tsview.txt')}  (seçimleri {os.path.join(IS, 'kesim.json')} içine yaz)")


if __name__ == "__main__":
    main()
