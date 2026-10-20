# DaVinci Resolve + Claude

Bu klasörün sayfaları:

| Sayfa | Ne |
|---|---|
| Bu sayfa | Hangi yol sende çalışır |
| [1-ucretsiz-fcpxml.md](1-ucretsiz-fcpxml.md) | Her sürümde çalışan yol: kesim listesi → DaVinci zaman çizelgesi |
| [2-studio-mcp-kurulum.md](2-studio-mcp-kurulum.md) | Studio'da Claude'un DaVinci'yi doğrudan sürmesi: kurulum |
| [3-vlog-akisi.md](3-vlog-akisi.md) | 4 saatten 25 dakikaya (vlog örneği), Claude + DaVinci ile adım adım, hazır prompt'lar |
| [4-tuzaklar.md](4-tuzaklar.md) | Videolarda ve repolarda görülen hatalar, sınırlar |

## Önce: sende hangi sürüm var?

DaVinci'yi aç, üst menüden **DaVinci Resolve > About DaVinci Resolve**. Açılan pencerede:

- **"DaVinci Resolve Studio"** yazıyorsa: Studio (ücretli). Bütün yollar açık.
- Sadece **"DaVinci Resolve"** yazıyorsa: ücretsiz sürüm.

Sürüm numarasına da bak (örn. 21.1). Aşağıdaki MCP özelliği 21.1'de geldi.

## Üç yol

| | Ücretsiz sürüm | Studio |
|---|---|---|
| **A. FCPXML aktarma** (kesim listesinden zaman çizelgesi dosyası, File > Import > Timeline) | Çalışır | Çalışır |
| **B. DaVinci'nin kendi MCP sunucusu** (21.1+, File > Setup AI Assistants) | Yok | Var |
| **C. Topluluk MCP köprüsü** (`samuelgursky/davinci-resolve-mcp`) | 21.1'de kapandı | Var |
| DaVinci'yi Python ile dışarıdan yönetmek | Yok (21.1'de ücretsizden tamamen kaldırıldı) | Var |

**MCP** (Model Context Protocol): Claude gibi bir yapay zekanın başka bir programın içindeki
işlevleri çağırmasını sağlayan açık standart. DaVinci'de MCP açıkken Claude'a "projeyi aç, şu klibi
içe al, duraklamaları kes" dersin, Claude bunu DaVinci'nin kendi API'si üzerinden yapar. Ekrana
tıklamaz; API'nin izin verdiği her şeyi yapar, vermediğini yapamaz.

### Hangisini kullanayım

- **Ücretsiz sürüm:** A. Seçimi Claude Code ile dışarıda yaparsın (bu repodaki akış), DaVinci'ye
  hazır kaba kurgu olarak girer, ince işi elle yaparsın. Gayet yeterli.
- **Studio 21.1+:** A + B. Seçimi yine dışarıda yap (4 saatte kontrol sende kalsın), aktar, cilayı
  (duraklama kesme, ikinci kamera eşleme, işaretler, LUT, render) Claude'a DaVinci içinde yaptır.
  B kurulumu en kolayı, ek program yok.
- **Studio 21.0 ya da daha eski:** A + C.
- **Studio alayım mı?** Tek seferlik lisans 295 dolar, Blackmagic Cloud'da aylık 30 dolarlık abonelik
  var (videolardaki fiyatlar). Önce A ile başla; MCP cilası zaman kazandırıyorsa sonra al.

## Neden seçimi DaVinci içinde değil dışarıda yapıyoruz

Studio'da Claude 4 saatlik klibi DaVinci'ye transkript ettirip seçimi de orada yapabilir; bir
videoda 2 saatlik çekim tek komutla 27-31 dakikaya inmiş. Ama:

- Seçim bir dosyada (`kesim.json`) olunca okunur, düzeltilir, versiyonlanır; "neden bu kısım atıldı"
  sorusunun cevabı ortada durur.
- DaVinci sürümü, lisansı ya da MCP değişse de akış bozulmaz.
- Claude'un DaVinci'de yaptığı her işlem zaman çizelgesini değiştirir; dışarıdaki liste ise sadece bir
  metin dosyası, deneme yapmak bedava.

Kısa ve tek kameralı işlerde (10-20 dakikalık konuşma) doğrudan DaVinci içinde yaptırmak daha hızlı
olabilir. Uzun vlogda dışarıda seç, içeride cilala.
