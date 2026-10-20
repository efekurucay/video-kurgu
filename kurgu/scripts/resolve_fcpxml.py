"""Kesim listesinden DaVinci Resolve'a (ve Final Cut Pro'ya) aktarılabilir FCPXML zaman çizelgesi.

Kullanım:
    python3 resolve_fcpxml.py IS_KLASORU/kesim.json [--cikti kurgu.fcpxml]

DaVinci'de: File > Import > Timeline... > kurgu.fcpxml seç.
    "Automatically import source clips into media pool" işaretli kalsın. Kaynak videolar dosyada
    yazan yolda olmalı; taşıdıysan Resolve "Relink" ister, klasörü göstermen yeter.

Ne gelir: tek video izinde, sırayla bütün parçalar, kaynağın kendi sesiyle. Her parçanın uçları
kaynağa bağlı kalır; Resolve'da uçları çekip uzatabilir, kısaltabilirsin (kayıpsız, yeniden kodlama yok).

Yapı, auto-editor'ın "--export resolve" çıktısıyla aynı (FCPXML 1.10). Zamanlar kare sayısıyla
kesir olarak yazılır ("1001/30000s" gibi), yuvarlama hatası birikmez.
"""
import argparse
import os
import re
import sys
from pathlib import Path
from xml.sax.saxutils import quoteattr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import kesim_oku, timecode_kare, video_bilgi, zaman, zaman_cizelgesi  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kesim")
    ap.add_argument("--cikti")
    a = ap.parse_args()
    k = kesim_oku(a.kesim)
    if not k["parcalar"]:
        sys.exit("HATA: kesim.json'da parça yok.")
    kok = os.path.dirname(os.path.abspath(a.kesim))
    cikti = a.cikti or os.path.join(kok, re.sub(r"\W+", "-", k.get("baslik", "kurgu")).strip("-") + ".fcpxml")

    kullanilan = []
    for p in k["parcalar"]:
        if p["kaynak"] not in kullanilan:
            kullanilan.append(p["kaynak"])
    bilgi = {i: video_bilgi(k["kaynaklar"][i]) for i in kullanilan}
    ilk = bilgi[k["parcalar"][0]["kaynak"]]
    num, den = ilk["fps_num"], ilk["fps_den"]          # zaman çizelgesinin kare hızı
    fps = num / den

    def kesir(kare):                                    # kare sayısı -> FCPXML zamanı
        return "0s" if kare == 0 else f"{kare * den}/{num}s"

    res, ref = [], {}
    for n, i in enumerate(kullanilan):
        b = bilgi[i]
        fid, aid = f"r{2 * n + 1}", f"r{2 * n + 2}"
        ref[i] = (aid, timecode_kare(b["timecode"], fps))
        res.append(f'    <format id="{fid}" name="FFVideoFormatRateUndefined" frameDuration="{kesir(1)}" '
                   f'width="{b["w"]}" height="{b["h"]}" colorSpace="1-1-1 (Rec. 709)"/>')
        res.append(f'    <asset id="{aid}" name={quoteattr(Path(b["yol"]).stem)} start="{kesir(ref[i][1])}" '
                   f'hasVideo="1" format="{fid}" hasAudio="{1 if b["ses"] else 0}" audioSources="1" '
                   f'audioChannels="{b["kanal"]}" duration="{kesir(int(b["sure"] * fps))}">\n'
                   f'      <media-rep kind="original-media" src={quoteattr(Path(b["yol"]).as_uri())}/>\n'
                   f'    </asset>')

    cizelge, toplam = zaman_cizelgesi(k, fps)
    klipler = []
    for p, (t, kare) in zip(k["parcalar"], cizelge):
        aid, tc0 = ref[p["kaynak"]]
        ad = p.get("bolum") or p.get("not") or Path(k["kaynaklar"][p["kaynak"]]).stem
        klipler.append(f'          <asset-clip name={quoteattr(ad)} ref="{aid}" offset="{kesir(t)}" '
                       f'duration="{kesir(kare)}" start="{kesir(round(p["giris"] * fps) + tc0)}" tcFormat="NDF"/>')

    baslik = k.get("baslik", "Kurgu")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.10">
  <resources>
{chr(10).join(res)}
  </resources>
  <library>
    <event name={quoteattr(baslik)}>
      <project name={quoteattr(baslik)}>
        <sequence format="r1" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k">
          <spine>
{chr(10).join(klipler)}
          </spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>
"""
    open(cikti, "w", encoding="utf-8").write(xml)
    print(f"OK {cikti}\n   {len(klipler)} parça, {zaman(toplam / fps)}, {fps:.3f} fps. "
          f"DaVinci: File > Import > Timeline")


if __name__ == "__main__":
    main()
