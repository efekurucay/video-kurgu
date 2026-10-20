"""Kesim listesinden düzenlenebilir CapCut projesi (masaüstü CapCut).

Kullanım:
    python3 capcut.py IS_KLASORU/kesim.json [--ad "Vlog 12 Kurgu"] [--taslaklar KLASOR] [--movies]

Kurulum: pip install pycapcut
    pycapcut normalde pymediainfo ister; bu script medya bilgisini ffprobe ile verir, o yüzden
    MediaInfo kütüphanesi kurulmasa da çalışır.

--taslaklar: CapCut'ın proje klasörü. Varsayılan:
    macOS   ~/Movies/CapCut/User Data/Projects/com.lveditor.draft
    Windows %LOCALAPPDATA%/CapCut/User Data/Projects/com.lveditor.draft
    Emin değilsen CapCut > Ayarlar > "Taslak konumu" (Draft location) ne diyorsa onu ver.

--movies (macOS): kaynak videoları ~/Movies/CapCut/<ad> Medya/ altına hard link olarak koyar ve
    projeyi oradan kurar. Bizim Mac'te CapCut (9.5) korumalı çalışıyordu ve elle seçilmemiş
    dosyalardan yalnız ~/Movies altını okuyordu; Masaüstü'ndeki dosyalar "File not accessible"
    oldu. Hard link kopya değildir, yer kaplamaz; ama aynı diskte olmalı (harici diskte kopyalar).

Bilinen sınırlar:
    - Proje açılışta listeye düşer: CapCut açıksa kapatıp aç.
    - Var olan projenin üstüne yazmaz, her çalıştırma yeni proje. Elle düzenlediğin projeyi korur.
    - CapCut sürümü değiştikçe proje formatı değişebiliyor (bazı sürümlerin dosyayı şifrelediği
      söyleniyor). Bizde 9.5'te çalıştı; önce kısa bir listeyle dene.
"""
import argparse
import json
import os
import re
import shutil
import sys
import time
import types
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import kesim_oku, probe, video_bilgi, zaman, zaman_cizelgesi  # noqa: E402


class _Iz:
    pass


class _MediaInfo:
    """pycapcut'ın pymediainfo'dan beklediği arayüz, ffprobe ile."""
    @staticmethod
    def can_parse():
        return True

    @staticmethod
    def parse(yol, **kw):
        d = probe(yol); fdur = float(d["format"].get("duration") or 0)
        mi = _MediaInfo(); mi.video_tracks, mi.audio_tracks, mi.image_tracks = [], [], []
        g = _Iz(); g.duration = fdur * 1000; mi.general_tracks = [g]
        for st in d["streams"]:
            t = _Iz(); t.duration = float(st.get("duration") or fdur) * 1000
            if st["codec_type"] == "video" and not mi.video_tracks:
                b = video_bilgi(yol); t.width, t.height = b["w"], b["h"]
                mi.video_tracks.append(t)
            elif st["codec_type"] == "audio" and not mi.audio_tracks:
                mi.audio_tracks.append(t)
        return mi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kesim")
    ap.add_argument("--ad")
    ap.add_argument("--taslaklar")
    ap.add_argument("--movies", action="store_true")
    a = ap.parse_args()

    shim = types.ModuleType("pymediainfo"); shim.MediaInfo = _MediaInfo
    sys.modules["pymediainfo"] = shim
    try:
        import pycapcut as cc
    except ImportError:
        sys.exit("HATA: pycapcut yok. Kur: pip install pycapcut")

    k = kesim_oku(a.kesim)
    if not k["parcalar"]:
        sys.exit("HATA: kesim.json'da parça yok.")
    if a.taslaklar:
        taslak = os.path.expanduser(a.taslaklar)
    elif sys.platform == "win32":
        taslak = os.path.join(os.environ.get("LOCALAPPDATA", ""), "CapCut", "User Data", "Projects", "com.lveditor.draft")
    else:
        taslak = os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft")
    if not os.path.isdir(taslak):
        sys.exit(f"HATA: CapCut taslak klasörü yok: {taslak}\n--taslaklar ile ver.")

    ad = a.ad or k.get("baslik", "Kurgu")
    if os.path.exists(os.path.join(taslak, ad)):
        n = 2
        while os.path.exists(os.path.join(taslak, f"{ad} {n}")):
            n += 1
        ad = f"{ad} {n}"

    kaynak = dict(k["kaynaklar"])
    if a.movies:
        med = os.path.expanduser(f"~/Movies/CapCut/{re.sub(r'[/:]', '-', ad)} Medya")
        os.makedirs(med, exist_ok=True)
        for i, yol in kaynak.items():
            hedef = os.path.join(med, os.path.basename(yol))
            if not os.path.exists(hedef):
                try:
                    os.link(yol, hedef)
                except OSError:  # farklı disk: hard link olmaz
                    print(f"  kopyalanıyor (farklı disk): {os.path.basename(yol)}")
                    shutil.copy2(yol, hedef)
            kaynak[i] = hedef

    ilk = video_bilgi(kaynak[k["parcalar"][0]["kaynak"]])
    fps = ilk["fps"]
    cizelge, toplam = zaman_cizelgesi(k, fps)
    us = lambda kare: int(round(kare / fps * 1e6))  # noqa: E731  CapCut zamanı mikrosaniye

    script = cc.DraftFolder(taslak).create_draft(ad, ilk["w"], ilk["h"], round(fps))
    ddir = os.path.join(taslak, ad)
    script.save_path = os.path.join(ddir, "draft_info.json")   # macOS CapCut bu adı okur
    script.add_track(cc.TrackType.video, "video")
    for p, (t, kare) in zip(k["parcalar"], cizelge):
        bas, d = us(t), us(t + kare) - us(t)                    # uçlar tam sayı: komşu parçalar binmez
        g = int(round(p["giris"] * 1e6))
        script.add_segment(cc.VideoSegment(kaynak[p["kaynak"]], cc.Timerange(bas, d),
                                           source_timerange=cc.Timerange(g, d)), "video")
    script.save()
    shutil.copy(script.save_path, os.path.join(ddir, "draft_content.json"))  # başka sürümler bu adı okuyor

    mp = os.path.join(ddir, "draft_meta_info.json")
    if os.path.exists(mp):
        meta = json.load(open(mp, encoding="utf-8")); simdi = int(time.time() * 1e6)
        meta.update({"draft_fold_path": ddir, "draft_name": ad, "draft_root_path": taslak,
                     "draft_id": str(uuid.uuid4()).upper(), "tm_draft_create": simdi,
                     "tm_draft_modified": simdi, "tm_duration": us(toplam)})
        json.dump(meta, open(mp, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"OK CapCut projesi: '{ad}'  {len(k['parcalar'])} parça, {zaman(toplam / fps)}\n"
          f"   CapCut açıksa kapatıp aç; proje listede görünür.")


if __name__ == "__main__":
    main()
