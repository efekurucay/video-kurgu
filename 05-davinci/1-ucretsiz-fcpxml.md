# A. FCPXML aktarma (her sürümde)

Kesim listesini DaVinci'nin okuyabildiği standart bir zaman çizelgesi dosyasına çevirir.
Ücretsiz sürümde de çalışır, hiçbir ayar istemez.

```bash
python kurgu/scripts/resolve_fcpxml.py IS/kesim.sikilastirilmis.json
```

DaVinci'de:

1. Yeni proje aç. **File > Project Settings > Master Settings**: "Timeline frame rate" kaynağınla aynı
   olsun (telefon çoğu zaman 30 ya da 29.97, bazı kameralar 25 ya da 24). Kare hızı proje başında
   ayarlanır; içinde medya olan projede sonradan değiştirmek zor ya da imkânsız olabiliyor.
2. **File > Import > Timeline...** > `.fcpxml` dosyası. "Automatically import source clips into media
   pool" işaretli kalsın.
3. Kaynak videolar dosyada yazan yolda olmalı. Taşıdıysan klipler kırmızı (offline) görünür: Media
   Pool'da seç > sağ tık > **Relink Selected Clips** > klasörü göster.

Gelen: tek video izinde sırayla bütün parçalar, kaynağın kendi sesiyle. Her parça kaynağa bağlı;
uçlarını çekip uzatabilirsin, kalite kaybı yok.

Dosya yapısı auto-editor'ın DaVinci için ürettiği FCPXML 1.10 ile aynı. Biz DaVinci'de açıp
denemedik; önce 3-4 parçalık kısa bir listeyle dene.

## Sonra elle (ücretsiz sürümde de olanlar)

| İş | Nerede |
|---|---|
| Harici mikrofonu eşleme | Klipleri seç > sağ tık > Auto Sync Audio > Based on Waveform |
| Ağır 4K | Klipleri seç > sağ tık > Generate Proxy Media |
| Duraklama inceltme | Edit sayfası, kesim noktasında kenarı sürükle; `N` yapışmayı kapatır |
| Bölüm işaretleri | `M` ile işaret koy; işaret listesi YouTube bölümlerine dönüşür |
| Ses | Fairlight sayfası: seviye, EQ, müziği konuşmanın altında kısma |
| Renk | Color sayfası: önce düzeltme, sonra görünüm |
| Altyazı | `render.py`'nin ürettiği `.srt`'yi Media Pool'a sürükle, zaman çizelgesine at |

DaVinci 20/21'in kendi yapay zeka özellikleri de var (transkriptten kurgu, sessiz kısımları silme,
IntelliScript, IntelliCut, AI Audio Assistant). Hangisinin ücretsiz sürümde olduğu sürümden sürüme
değişiyor ve kaynaklar çelişiyor; kendi sürümünde menüde görünüyor mu, ona bak. Kesin liste
Blackmagic'in sitesindeki sürüm karşılaştırmasında.

## Alternatif: auto-editor

Tek bir uzun videodaki sessizlikleri kendisi kesip doğrudan DaVinci dosyası verir:

```bash
pip install auto-editor
auto-editor video.mp4 --margin 0.2sec --export resolve
```

Seçim (hangi dakikalar kalacak) yapmaz, sadece sessizlik keser. Seçenek adları sürüme göre değişti;
`auto-editor --help`.
