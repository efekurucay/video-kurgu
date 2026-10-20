"""Kesim listesindeki konuşma parçalarının içindeki uzun sessizlikleri atar (jump cut).

Kullanım:
    python3 sikilastir.py IS_KLASORU/kesim.json [--esik -35dB] [--min-sessizlik 0.7] [--pay 0.15]

Çıktı: kesim.sikilastirilmis.json (asıl liste bozulmaz; beğenmezsen silersin)

Nasıl çalışır:
    Her parçanın sesine ffmpeg silencedetect uygular. --min-sessizlik saniyeden uzun ve --esik
    seviyesinden sessiz aralıkları çıkarır, konuşmanın iki yanında --pay kadar nefes payı bırakır.

Dikkat:
    - Vlogda konuşmasız B-roll ve manzara parçaları da "sessiz" sayılır. Bir parça bu işlemle
      yarısından fazla kısalıyorsa script ona dokunmaz ve uyarır. Bir parçayı hiç elleme
      dersen kesim.json'da o parçaya "dokunma": true yaz.
    - 0,1-0,2 sn gibi çok kısa eşikler konuşanı robot gibi yapar. Vlogda 0,6-1,0 sn iyi başlangıç.
    - Ortam gürültüsü yüksekse (rüzgâr, kalabalık) sessizlik bulunmaz: --esik -30dB ya da -25dB dene.
"""
import argparse
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import gerekli, kesim_oku, zaman  # noqa: E402


def sessizlikler(dosya, a, d, esik, minsure):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", dosya, "-vn",
                        "-af", f"silencedetect=n={esik}:d={minsure}", "-f", "null", "-"],
                       capture_output=True, text=True)
    bas = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", r.stderr)]
    son = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    if len(son) < len(bas):
        son.append(d)  # parça sessizlikle bitiyor
    return [(max(0.0, x), min(d, y)) for x, y in zip(bas, son)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kesim")
    ap.add_argument("--esik", default="-35dB")
    ap.add_argument("--min-sessizlik", type=float, default=0.7)
    ap.add_argument("--pay", type=float, default=0.15)
    a = ap.parse_args()
    gerekli("ffmpeg")
    ham = json.load(open(a.kesim, encoding="utf-8"))
    k = kesim_oku(a.kesim)
    kok = os.path.dirname(os.path.abspath(a.kesim))
    kp = os.path.join(kok, "kaynaklar.json")
    kimlik = ({v["dosya"]: i for i, v in json.load(open(kp, encoding="utf-8")).items()}
              if os.path.exists(kp) else {})

    yeni, once, sonra = [], 0.0, 0.0
    for n, (p, hp) in enumerate(zip(k["parcalar"], ham["parcalar"]), 1):
        d = p["cikis"] - p["giris"]; once += d
        if hp.get("dokunma"):
            yeni.append(hp); sonra += d; continue
        kaynak = k["kaynaklar"][p["kaynak"]]
        # transkript.py'nin çıkardığı wav aynı zaman çizelgesindedir ve okuması çok daha hızlıdır
        wav = os.path.join(kok, "ses", kimlik.get(kaynak, "") + ".wav")
        dosya = wav if os.path.exists(wav) else kaynak
        sus = sessizlikler(dosya, p["giris"], d, a.esik, a.min_sessizlik)
        tut, t = [], 0.0
        for x, y in sus:
            if x > t:
                tut.append((t, x))
            t = y
        if t < d:
            tut.append((t, d))
        tut = [(max(0.0, x - a.pay), min(d, y + a.pay)) for x, y in tut]
        birlesik = []
        for x, y in tut:
            if birlesik and x <= birlesik[-1][1]:
                birlesik[-1] = (birlesik[-1][0], y)
            else:
                birlesik.append((x, y))
        kalan = sum(y - x for x, y in birlesik)
        if not birlesik or kalan < 0.5 * d:
            print(f"  {n:3d}. parça dokunulmadı: {d:.1f} sn'nin {kalan:.1f} sn'si kalıyordu (konuşmasız görüntü mü?)")
            yeni.append(hp); sonra += d; continue
        for j, (x, y) in enumerate(birlesik):
            q = {kk: vv for kk, vv in hp.items() if kk not in ("giris", "cikis")}
            if j:
                q.pop("bolum", None)
            q["giris"] = zaman(p["giris"] + x, True); q["cikis"] = zaman(p["giris"] + y, True)
            yeni.append(q)
        sonra += kalan
        if len(birlesik) > 1:
            print(f"  {n:3d}. parça: {len(birlesik)} parçaya bölündü, {d:.1f} -> {kalan:.1f} sn")

    ham["parcalar"] = yeni
    out = re.sub(r"\.json$", "", a.kesim) + ".sikilastirilmis.json"
    json.dump(ham, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"OK {out}\n   {zaman(once)} -> {zaman(sonra)}  ({once - sonra:.0f} sn sessizlik atıldı)")


if __name__ == "__main__":
    main()
