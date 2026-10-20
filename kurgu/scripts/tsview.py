"""transkript/*.srt dosyalarından tek, okunur bir görünüm yazar: IS_KLASORU/tsview.txt

Kullanım:
    python3 tsview.py IS_KLASORU

SRT'yi başka bir araçla ürettiysen (DaVinci, CapCut, faster-whisper, MacWhisper...) dosyayı
IS_KLASORU/transkript/<kimlik>.srt olarak koy, bu script aynı görünümü üretir.

Görünüm neden böyle:
    - whisper satırları birkaç saniyelik; arka arkaya olanlar ~20 sn'lik satırlarda birleşir, okuması kolay.
    - Her satırın başında [kaynak zaman] var; seçimi yapan (sen ya da yapay zeka) zamanı buradan okur.
    - 30 sn'den uzun konuşmasız bölümler ayrıca işaretlenir. Vlogda bunlar çoğu zaman yol, manzara,
      B-roll'dür; transkriptte görünmezler ama kare dökümünde (kare.py) görünürler.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import srt_oku, zaman  # noqa: E402

BIRLESTIR = 20.0   # sn: bir satırın en uzun süresi
KOPUK = 2.0        # sn: bundan uzun boşlukta yeni satır
SESSIZ = 30.0      # sn: bundan uzun konuşmasız bölüm işaretlenir


def tsview_yaz(IS):
    kaynaklar = json.load(open(os.path.join(IS, "kaynaklar.json"), encoding="utf-8"))
    out = []
    for i, v in kaynaklar.items():
        cues = srt_oku(os.path.join(IS, "transkript", i + ".srt"))
        out.append(f"\n===== {i}  {os.path.basename(v['dosya'])}  süre {zaman(v['sure'])}  çekim {v.get('cekim') or '?'}")
        satir, bas, son = [], None, 0.0
        for a, b, m in cues:
            if a - son > SESSIZ:
                if satir:
                    out.append(f"[{i} {zaman(bas)}] {' '.join(satir)}"); satir = []
                out.append(f"[{i} {zaman(son)}] --- {int(a - son)} sn konuşma yok ---")
            if satir and (a - son > KOPUK or b - bas > BIRLESTIR):
                out.append(f"[{i} {zaman(bas)}] {' '.join(satir)}"); satir = []
            if not satir:
                bas = a
            satir.append(m); son = b
        if satir:
            out.append(f"[{i} {zaman(bas)}] {' '.join(satir)}")
        if v["sure"] - son > SESSIZ:
            out.append(f"[{i} {zaman(son)}] --- {int(v['sure'] - son)} sn konuşma yok (sona kadar) ---")
    open(os.path.join(IS, "tsview.txt"), "w", encoding="utf-8").write("\n".join(out).strip() + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    tsview_yaz(os.path.abspath(sys.argv[1]))
    print(f"OK {sys.argv[1]}/tsview.txt")
