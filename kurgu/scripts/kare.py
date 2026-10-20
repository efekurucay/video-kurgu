"""Kare dökümü: her videodan N saniyede bir kare alır, zaman yazılı ızgara sayfaları yapar.

Kullanım:
    python3 kare.py IS_KLASORU [--aralik 30] [--sutun 8] [--satir 6] [--kaynak 001] [--bas 00:10:00 --son 00:20:00]

Çıktı: IS_KLASORU/kareler/001_s01.jpg, 001_s02.jpg ...  (her karenin altında "001 00:12:30")

Neden: 4 saatlik videoyu baştan izlemeden "nerede ne oluyor" haritası çıkarır. Transkriptin
göremediği her şeyi (manzara, yemek, yol, konuşmasız anlar) gösterir. Bir yapay zekaya da bu
sayfaları gösterip "hangi aralıklar görsel olarak güçlü" diye sorabilirsin.

Her kare için videonun o noktasına atlar (-ss), videoyu baştan sona çözmez; 4K bir 4 saatlik
dosyada bile dakikalar sürer, saatler değil. Pillow gerekir: pip install pillow
"""
import argparse
import io
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import gerekli, saniye, zaman  # noqa: E402

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("HATA: Pillow yok. Kur: pip install pillow")

GEN = 320  # bir karenin genişliği (px)


def kare_al(dosya, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", dosya, "-frames:v", "1",
                        "-vf", f"scale={GEN}:{GEN}:force_original_aspect_ratio=decrease",
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    return Image.open(io.BytesIO(r.stdout)).convert("RGB") if r.stdout else None


def font(boy):
    for f in ("/System/Library/Fonts/Supplemental/Arial.ttf", "C:/Windows/Fonts/arial.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, boy)
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("is_klasoru")
    ap.add_argument("--aralik", type=float, default=30)
    ap.add_argument("--sutun", type=int, default=8)
    ap.add_argument("--satir", type=int, default=6)
    ap.add_argument("--kaynak", help="sadece bu kimlik (örn. 001)")
    ap.add_argument("--bas", default="0")
    ap.add_argument("--son")
    a = ap.parse_args()
    gerekli("ffmpeg")
    IS = os.path.abspath(a.is_klasoru)
    os.makedirs(os.path.join(IS, "kareler"), exist_ok=True)
    kaynaklar = json.load(open(os.path.join(IS, "kaynaklar.json"), encoding="utf-8"))
    F = font(20)

    for i, v in kaynaklar.items():
        if a.kaynak and i != a.kaynak:
            continue
        son = min(saniye(a.son), v["sure"]) if a.son else v["sure"]
        anlar, t = [], saniye(a.bas)
        while t < son - 0.5:
            anlar.append(t); t += a.aralik
        with ThreadPoolExecutor(4) as ex:
            kareler = list(ex.map(lambda t: kare_al(v["dosya"], t), anlar))
        ornek = next((k for k in kareler if k), None)
        if not ornek:
            print(f"  {i}: kare alınamadı (video yok mu?)"); continue
        w, h = ornek.size; etiket = 26
        sayfa_boy = a.sutun * a.satir
        for s in range(0, len(anlar), sayfa_boy):
            parca = list(zip(anlar, kareler))[s:s + sayfa_boy]
            satir = (len(parca) + a.sutun - 1) // a.sutun
            img = Image.new("RGB", (a.sutun * (w + 4), satir * (h + etiket + 4)), "white")
            d = ImageDraw.Draw(img)
            for n, (t, k) in enumerate(parca):
                x, y = n % a.sutun * (w + 4), n // a.sutun * (h + etiket + 4)
                if k:
                    img.paste(k, (x, y))
                d.text((x + 4, y + h + 2), f"{i} {zaman(t)}", fill="black", font=F)
            yol = os.path.join(IS, "kareler", f"{i}_s{s // sayfa_boy + 1:02d}.jpg")
            img.save(yol, quality=80)
        print(f"  {i}: {len(anlar)} kare, {(len(anlar) + sayfa_boy - 1) // sayfa_boy} sayfa")
    print(f"OK {IS}/kareler/")


if __name__ == "__main__":
    main()
