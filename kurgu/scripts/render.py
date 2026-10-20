"""Kesim listesinden izlenebilir kaba kurgu (mp4) + YouTube bölümleri + kurguya göre kaydırılmış altyazı.

Kullanım:
    python3 render.py IS_KLASORU/kesim.json [--cikti kaba-v1.mp4] [--taslak] [--ses-seviye]

Seçenekler:
    --taslak      720p, hızlı kodlama. Kaba kurguyu izlemek için yeter, 4K'dan çok daha hızlı.
    --ses-seviye  sesi -14 LUFS'a çeker (YouTube'un normalize ettiği seviye). Asıl ses işi NLE'de yapılır.

Ne üretir (kesim.json'un yanında):
    <cikti>.mp4            parçalar sırayla, aynı boyut ve kare hızında
    <cikti>.bolumler.txt   YouTube açıklamasına yapıştırılacak bölüm listesi ("bolum" alanlarından)
    <cikti>.srt            kaynak transkriptlerden, kurgunun zamanına kaydırılmış altyazı

Bu dosya bir ön izleme. Asıl kurgu NLE'de (DaVinci / CapCut) biter: resolve_fcpxml.py ve capcut.py
aynı kesim listesinden düzenlenebilir proje üretir.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import gerekli, kesim_oku, srt_oku, srt_yaz, video_bilgi, zaman, zaman_cizelgesi  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kesim")
    ap.add_argument("--cikti")
    ap.add_argument("--taslak", action="store_true")
    ap.add_argument("--ses-seviye", action="store_true")
    a = ap.parse_args()
    gerekli("ffmpeg", "ffprobe")
    k = kesim_oku(a.kesim)
    if not k["parcalar"]:
        sys.exit("HATA: kesim.json'da parça yok.")
    kok = os.path.dirname(os.path.abspath(a.kesim))
    cikti = os.path.abspath(a.cikti or os.path.join(kok, "kaba-kurgu.mp4"))
    taban = re.sub(r"\.mp4$", "", cikti)

    bilgi = {i: video_bilgi(p) for i, p in k["kaynaklar"].items() if any(q["kaynak"] == i for q in k["parcalar"])}
    ilk = bilgi[k["parcalar"][0]["kaynak"]]
    fps = ilk["fps"]; fps_s = f"{ilk['fps_num']}/{ilk['fps_den']}"
    W, H = ilk["w"], ilk["h"]
    if a.taslak:  # uzun kenar 1280
        r = 1280 / max(W, H); W, H = int(W * r) // 2 * 2, int(H * r) // 2 * 2
    cizelge, toplam = zaman_cizelgesi(k, fps)
    print(f"{len(k['parcalar'])} parça, kurgu {zaman(toplam / fps)}, {W}x{H} @ {fps:.3f}")

    with tempfile.TemporaryDirectory() as td:
        liste = []
        for n, (p, (_, kare)) in enumerate(zip(k["parcalar"], cizelge), 1):
            b = bilgi[p["kaynak"]]; d = kare / fps
            o = os.path.join(td, f"{n:04d}.mp4")
            cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{p['giris']:.3f}", "-t", f"{d:.4f}", "-i", b["yol"]]
            if not b["ses"]:  # sesi olmayan kaynak (drone, timelapse): sessiz ses izi ekle, birleştirme bozulmasın
                cmd += ["-f", "lavfi", "-t", f"{d:.4f}", "-i", "anullsrc=r=48000:cl=stereo"]
            vf = (f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,"
                  f"fps={fps_s},format=yuv420p")
            af = "aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.01,afade=t=out:st=" \
                 f"{max(0, d - 0.02):.3f}:d=0.02"  # uçlarda 10-20 ms yumuşatma: kesimde "tık" sesi olmasın
            cmd += ["-map", "0:v:0", "-map", "1:a:0" if not b["ses"] else "0:a:0", "-vf", vf, "-af", af,
                    "-c:v", "libx264", "-preset", "veryfast" if a.taslak else "medium", "-crf", "23" if a.taslak else "18",
                    "-c:a", "aac", "-b:a", "192k", "-frames:v", str(kare), o]
            subprocess.run(cmd, check=True)
            liste.append(o)
            print(f"\r  {n}/{len(k['parcalar'])}", end="", flush=True)
        print()
        lst = os.path.join(td, "liste.txt")
        open(lst, "w", encoding="utf-8").write("".join(f"file '{x.replace(os.sep, '/')}'\n" for x in liste))
        birlesik = os.path.join(td, "birlesik.mp4") if a.ses_seviye else cikti
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                        "-movflags", "+faststart", birlesik], check=True)
        if a.ses_seviye:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", birlesik, "-c:v", "copy",
                            "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k",
                            "-movflags", "+faststart", cikti], check=True)

    # YouTube bölümleri: ilk satır 00:00 olmalı, en az 3 bölüm, her biri en az 10 sn
    bolumler = [(t / fps, p["bolum"]) for p, (t, _) in zip(k["parcalar"], cizelge) if p.get("bolum")]
    if bolumler:
        if bolumler[0][0] > 0:
            bolumler.insert(0, (0.0, "Giriş"))
        satirlar = [f"{zaman(t)[3:] if toplam / fps < 3600 else zaman(t)} {ad}" for t, ad in bolumler]
        open(taban + ".bolumler.txt", "w", encoding="utf-8").write("\n".join(satirlar) + "\n")
        kisa = [ad for (t, ad), nxt in zip(bolumler, bolumler[1:] + [(toplam / fps, "")]) if nxt[0] - t < 10]
        if len(bolumler) < 3 or kisa:
            print("  UYARI: YouTube bölümleri için en az 3 bölüm ve her biri 10 sn gerekir.", kisa or "")

    # altyazı: her parçanın kaynak aralığına düşen satırları kurgu zamanına taşı
    kaynak_srt = {}
    kp = os.path.join(kok, "kaynaklar.json")
    if os.path.exists(kp):
        for i, v in json.load(open(kp, encoding="utf-8")).items():
            kaynak_srt[v["dosya"]] = srt_oku(os.path.join(kok, "transkript", i + ".srt"))
    cues = []
    for p, (t, kare) in zip(k["parcalar"], cizelge):
        bas, d = t / fps, kare / fps
        for x, y, m in kaynak_srt.get(k["kaynaklar"][p["kaynak"]], []):
            x2, y2 = max(x, p["giris"]), min(y, p["giris"] + d)
            if y2 - x2 > 0.3:
                cues.append((bas + x2 - p["giris"], bas + y2 - p["giris"], m))
    if cues:
        srt_yaz(taban + ".srt", cues)
    print(f"OK {cikti}" + (f"\n   {taban}.bolumler.txt" if bolumler else "") + (f"\n   {taban}.srt" if cues else ""))


if __name__ == "__main__":
    main()
