"""Script'lerin ortak yardımcıları: zaman çevirme, ffprobe, kesim listesi, SRT okuma/yazma."""
import json
import os
import re
import shutil
import subprocess
import sys


def gerekli(*programlar):
    for p in programlar:
        if not shutil.which(p):
            sys.exit(f"HATA: '{p}' bulunamadı. Kurulum için README.md'ye bak.")


def saniye(x):
    """12.5 | "75.2" | "01:15.2" | "00:01:15.2" -> saniye (float)."""
    if isinstance(x, (int, float)):
        return float(x)
    p = [float(v.replace(",", ".")) for v in str(x).strip().split(":")]
    t = 0.0
    for v in p:
        t = t * 60 + v
    return t


def zaman(sn, kesirli=False):
    """saniye -> "hh:mm:ss" (kesirli=True ise "hh:mm:ss.ss")."""
    sn = round(max(0.0, sn), 2) if kesirli else int(max(0.0, sn))
    s = int(sn)
    m = f"{s // 3600:02d}:{s % 3600 // 60:02d}:"
    return m + (f"{sn - s // 60 * 60:05.2f}" if kesirli else f"{s % 60:02d}")


def probe(yol):
    r = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", yol],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"HATA: ffprobe okuyamadı: {yol}\n{r.stderr}")
    return json.loads(r.stdout)


def video_bilgi(yol):
    """Kurguda gereken her şey: boyut, kare hızı (kesir), süre, ses var mı, kaynak timecode'u."""
    d = probe(yol)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in d["streams"] if s["codec_type"] == "audio"), None)
    num, den = (int(x) for x in (v or {}).get("r_frame_rate", "30/1").split("/"))
    if num == 0:
        num, den = 30, 1
    w, h = (v or {}).get("width", 1920), (v or {}).get("height", 1080)
    # telefon çekimlerinde dikey video yatay saklanıp döndürme bilgisiyle gelir
    rot = abs(int((v or {}).get("tags", {}).get("rotate", 0)))
    for sd in (v or {}).get("side_data_list", []):
        rot = abs(int(sd.get("rotation", rot)))
    if rot in (90, 270):
        w, h = h, w
    tc = (d["format"].get("tags", {}).get("timecode")
          or next((s.get("tags", {}).get("timecode") for s in d["streams"] if s.get("tags", {}).get("timecode")), None))
    return {"yol": yol, "w": w, "h": h, "fps_num": num, "fps_den": den, "fps": num / den,
            "sure": float(d["format"].get("duration") or 0), "ses": a is not None,
            "kanal": int(a.get("channels", 2)) if a else 2, "timecode": tc,
            "cekim": d["format"].get("tags", {}).get("creation_time")}


def timecode_kare(tc, fps):
    """ "01:00:00:00" -> kare sayısı (timecode yoksa 0)."""
    if not tc:
        return 0
    p = [int(x) for x in re.split("[:;]", tc)]
    if len(p) != 4:
        return 0
    f = round(fps)
    return ((p[0] * 60 + p[1]) * 60 + p[2]) * f + p[3]


def kesim_oku(yol):
    """kesim.json'u okur, zamanları saniyeye çevirir, kaynak yollarını tam yola çevirir."""
    k = json.load(open(yol, encoding="utf-8"))
    kok = os.path.dirname(os.path.abspath(yol))
    k["kaynaklar"] = {i: os.path.normpath(os.path.join(kok, os.path.expanduser(p)))
                      for i, p in k["kaynaklar"].items()}
    for n, p in enumerate(k["parcalar"], 1):
        if p["kaynak"] not in k["kaynaklar"]:
            sys.exit(f"HATA: {n}. parçanın kaynağı '{p['kaynak']}' kaynaklar listesinde yok.")
        p["giris"], p["cikis"] = saniye(p["giris"]), saniye(p["cikis"])
        if p["cikis"] <= p["giris"]:
            sys.exit(f"HATA: {n}. parçada çıkış girişten önce: {p}")
    return k


def srt_oku(yol):
    if not os.path.exists(yol):
        return []
    out = []
    for blok in re.split(r"\n\s*\n", open(yol, encoding="utf-8", errors="ignore").read().strip()):
        s = blok.strip().splitlines()
        i = next((j for j, x in enumerate(s) if "-->" in x), None)
        if i is None:
            continue
        a, b = [saniye(x.strip().split(" ")[0]) for x in s[i].split("-->")]
        metin = " ".join(x.strip() for x in s[i + 1:]).strip()
        if metin:
            out.append((a, b, metin))
    return out


def srt_yaz(yol, cues):
    def t(x):
        ms = int(round(x * 1000))
        return f"{ms // 3600000:02d}:{ms % 3600000 // 60000:02d}:{ms % 60000 // 1000:02d},{ms % 1000:03d}"
    with open(yol, "w", encoding="utf-8") as f:
        for n, (a, b, m) in enumerate(cues, 1):
            f.write(f"{n}\n{t(a)} --> {t(b)}\n{m}\n\n")


def zaman_cizelgesi(k, fps):
    """Her parçanın kurgudaki başlangıcı. Süreler kare ızgarasına yuvarlanır: komşu parçalar binmez."""
    t, out = 0, []
    for p in k["parcalar"]:
        kare = max(1, round((p["cikis"] - p["giris"]) * fps))
        out.append((t, kare))
        t += kare
    return out, t
