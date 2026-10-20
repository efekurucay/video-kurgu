# Seçim: saatlerden dakikalara

Örnek: 4 saatlik vlog çekiminden 25 dakika. Podcast, eğitim ve kısa kesitlerde hedef süre ve hikâye
kuralı değişir, akış aynı kalır; türe özel prompt eklemeleri [08-icerik-turleri.md](08-icerik-turleri.md) sayfasında.

Transkript ve kare dökümü hazır. Şimdi en zor ve en insani kısım: ne kalacak, hangi sırayla.
Yapay zeka burada çok hızlandırır ama kararı vermez. Bizim akışta her zaman iki onay noktası vardı:
**seçim** (hangi anlar) ve **final** (izleyip onay). İkisini de insan verir.

## Akış

1. **Sahne haritası.** Transkripti saat saat bölümlere ayır: zaman aralığı, ne oluyor, enerji,
   kalsın / belki / at. (Prompt 1)
2. **Görsel notlar.** Kare sayfalarına bak (ya da bir görsel modele göster): konuşmasız güçlü
   görüntüler nerede. (Prompt 2)
3. **Hikâye iskeleti.** Haritadan 25 dakikalık yapı: açılış, bloklar, doruk, kapanış. (Prompt 3)
4. **Kesim listesi.** İskeleti `kesim.json`'a dök (format aşağıda).
5. **Kaba kurguyu izle**, listeyi düzelt, tekrar üret.

## Transkript ne kadar uzun?

4 saatlik Türkçe konuşma on binlerce kelime eder. Büyük bağlamlı modeller (Claude, Gemini, GPT)
tek seferde okuyabilir ama kalite saat saat çalışınca daha iyi: her saat için harita çıkar, sonra
haritaları birleştir. `tsview.txt` dosyası `=====` satırlarıyla kaynak kaynak bölünmüş durumda.

Claude Code gibi dosya okuyabilen bir ajan kullanıyorsan yapıştırmana gerek yok:
"`IS/tsview.txt`'yi oku, Prompt 1'i her saat için uygula, `IS/harita.md`'ye yaz" demen yeter.

## Prompt'lar

### Prompt 1: sahne haritası

```
Aşağıda bir [içerik türü: seyahat vlogu / podcast / ders kaydı...] ham çekiminin transkripti var. Satır başları [kaynak hh:mm:ss].
"konuşma yok" satırları konuşmasız görüntülerdir (yol, manzara vb.).

Her 2-6 dakikalık doğal bölüm için bir satır yaz:
| kaynak | başlangıç | bitiş | ne oluyor (tek cümle) | enerji 1-5 | hikâye değeri | karar: kalsın / belki / at |

Kurallar:
- Zamanları transkriptten oku, tahmin etme.
- Tekrar eden anları işaretle ("aynı şey 01:12'de daha iyi söyleniyor").
- Komik, duygusal, şaşırtıcı, gerilimli anları ayrıca listele (zamanıyla), bunlar açılış adayıdır.
- Bir şey anlaşılmıyorsa uydurma, "belirsiz" yaz.

[TRANSKRİPT]
```

### Prompt 2: görsel notlar (görsel okuyabilen model + kare sayfaları)

```
Bunlar aynı çekimin kare dökümü; her karenin altında [kaynak hh:mm:ss] var.
Görsel olarak güçlü aralıkları listele: manzara, ışık, hareket, yüz ifadesi, yemek, yol.
Her biri için: kaynak, yaklaşık aralık, ne görünüyor, B-roll mu ana sahne mi.
Bulanık, karanlık, sallantılı ya da tekrar eden aralıkları da "kullanma" diye işaretle.
```

### Prompt 3: hikâye iskeleti ve kesim listesi

```
Hedef: [25] dakikalık [YouTube vlogu / podcast bölümü / ders videosu]. Kanal tarzı: [samimi, komik, gezi rehberi...].
Elinde sahne haritası ve görsel notlar var (aşağıda).

1. Bu bölümün sorusunu ve değişimini bir cümleyle yaz.
2. Açılış için 3 aday ver (ilk 30-60 sn). Kronolojiyi bozabilirsin.
3. Bölüm yapısı: blok adı, süre, hangi aralıklar, neden.
4. Atılan iyi anları ayrıca listele (kısa video adayı).
5. Sonra yapıyı aşağıdaki JSON formatında kesim listesine çevir. Her parçanın girişi ve çıkışı
   konuşmanın ortasına denk gelmesin: cümle başı ve sonunda kes, iki yanda 0,3 sn pay bırak.
   Her bloğun ilk parçasına "bolum" adı koy (YouTube bölümleri bundan çıkar).

[HARİTA]
[GÖRSEL NOTLAR]
[kesim.json formatı]
```

## kesim.json formatı

```json
{
 "baslik": "Vlog 12 Kapadokya",
 "kaynaklar": {"001": "D:/vlog12/ham/DJI_0012.MP4", "002": "D:/vlog12/ham/DJI_0013.MP4"},
 "parcalar": [
  {"kaynak": "001", "giris": "00:41:10.5", "cikis": "00:41:32.0", "bolum": "Balonlar", "not": "açılış"},
  {"kaynak": "002", "giris": "00:02:00", "cikis": "00:02:14", "dokunma": true, "not": "drone, müzik altına"},
  {"kaynak": "001", "giris": 12.0, "cikis": 95.4, "bolum": "Sabah 5"}
 ]
}
```

- `kaynaklar`: `transkript.py` kendisi doldurur. Yol göreli olabilir (kesim.json'a göre).
- `giris` / `cikis`: `"hh:mm:ss.s"`, `"mm:ss"` ya da saniye.
- `bolum`: o parça yeni bir YouTube bölümü başlatır.
- `dokunma`: `sikilastir.py` bu parçadaki sessizlikleri kesmez (konuşmasız görüntü, müzikli montaj).
- `not`: serbest; DaVinci'de klibin adı olur.

Tam örnek: `ornek/kesim.json`.

## Seçerken

- Önce fazla seç, sonra kes. İlk liste hedefin %30 üstünde olsun.
- Her bloğun bir sorusu ya da olayı olsun; "sonra şuraya gittik" tek başına blok değildir.
- Aynı şeyi iki kere söylediğin yerde daha kısa ve enerjik olanı al.
- Açılışa logo, kanal tanıtımı, "abone olun" koyma; onlar ilk dakikadan sonra.
