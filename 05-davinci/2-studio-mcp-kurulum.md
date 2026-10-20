# Studio: Claude'un DaVinci'yi doğrudan sürmesi

İki yol var. 21.1 ya da daha yeni Studio'daysan **B** ile başla, kurulacak ek bir şey yok.

## B. DaVinci'nin kendi MCP sunucusu (Studio 21.1+)

DaVinci Resolve 21.1 (8 Eylül 2026) kendi MCP sunucusuyla geliyor. Kurulum ekranında listelenen
asistanlar: Claude (masaüstü uygulaması), Claude Code, ChatGPT Codex, Google Antigravity, Grok.

### Kurulum (Claude masaüstü uygulamasıyla)

1. Claude masaüstü uygulamasını kur (claude.com > indir). Giriş yap.
2. DaVinci Resolve Studio'yu aç. Sürümü 21.1 ya da üstü olmalı.
3. **File > Setup AI Assistants**. DaVinci bilgisayardaki Claude'u bulur.
4. Claude açılır ve "DaVinci Resolve Studio" eklentisini kurmayı sorar: **Install**.
5. **Configure**: okuma araçları için ve yazma/silme araçları için izin ver ("Always allow" ya da "Allow all").
6. Kapanırsa ya da sonradan değiştirmek istersen: Claude > Settings > **Extensions** > DaVinci Resolve
   Studio > Configure.

Deneme: Claude'a "DaVinci'de 'Deneme' adlı yeni bir proje oluştur" de. Proje açılıyorsa bağlantı tamam.

Claude Code ile kullanacaksan: Setup AI Assistants ekranında Claude Code da listede; ekran ne
gösteriyorsa onu izle. Bu repodaki script'leri ve skill'i kullanmak için Claude Code daha uygun,
çünkü dosya okuyup komut çalıştırabiliyor.

### Donanım (Blackmagic'in 21.1 notları)

- Studio'nun AI araçları: Windows ve Linux'ta en az **16 GB ekran kartı belleği**, Mac'te 16 GB bellek.
- Arka planda render ve analiz için 32 GB RAM + 12 GB ekran kartı belleği.
- NVIDIA: Windows'ta Studio sürücüsü 581.57 ya da daha yeni.

### Güvenlik

Claude'un DaVinci içinde oluşturduğu script'ler, asistanın kendisiyle aynı disk, ağ ve sistem
yetkilerine sahip. İlk denemeleri müşteri ya da asıl proje üzerinde değil, **atılacak bir deneme
projesinde** yap.

## C. Topluluk köprüsü: `samuelgursky/davinci-resolve-mcp`

DaVinci'nin kendi MCP'si gelmeden önce herkesin kullandığı açık kaynak köprü (MIT, GitHub'da
binlerce yıldız, sık güncelleniyor). DaVinci'nin resmi scripting API'si üzerinden çalışır.
21.0 ve öncesi Studio'da tek yol bu. 21.1'de de kullanılabilir; kendi MCP'sinden fazla aracı ve
kontrol paneli var.

Gerekenler: Node.js (`npx` için), Python 3.10+, **Studio**.

1. DaVinci Studio'yu aç: **Preferences > System > General > External scripting using > Local**. Kaydet.
2. Terminalde:

   ```bash
   npx davinci-resolve-mcp setup
   ```

   Kurulum Python ortamını hazırlar, DaVinci'nin yollarını bulur ve seçtiğin istemciyi (Claude Code,
   Claude Desktop, Cursor, Codex...) ayarlar.
3. DaVinci açık ve bir proje yüklüyken Claude'a "DaVinci'nin sürümünü söyle" de. Cevap geliyorsa tamam.

Varsayılan mod 37 birleşik araçla çalışır (bağlamı az kullanır). Ayrıntı: reponun README'si ve
`docs/install.md`.

Ücretsiz sürüm: köprünün ücretsiz sürüm için bir "uygulama içi köprü" yolu vardı, ama 21.1 Python'u
ücretsiz sürümden kaldırdığı için o yol sadece 21.0.x'te çalışıyor. Ücretsiz sürümdeysen A (FCPXML) yolunu kullan.

## DaVinci'yi script ile kendin yönetmek

Studio'da DaVinci'nin Python API'si var: proje, Media Pool, zaman çizelgesi, render kuyruğu. Belgeler
programın içinde: **Help > Documentation > Developer** (Scripting klasöründeki README). MCP de bunun
üstüne kurulu. Aynı işi her hafta tekrarlıyorsan (her vlogda aynı proje yapısı, aynı render ayarları)
kendi script'ini yazmaya değer; yoksa MCP'ye söylemek yeter.

## Bakılacak kaynaklar

- DaVinci Resolve 21.1 Reference Manual: "Using DaVinci Resolve with AI Assistants" bölümü (resmi kaynak).
- github.com/samuelgursky/davinci-resolve-mcp
- github.com/ChaiWithJai/davinci-resolve-claude-skills: DaVinci için Claude skill'leri (MIT). En iyi
  fikri: Blackmagic'in ücretsiz eğitim PDF'lerini (Editor's Guide, Colorist Guide, Fairlight Guide...)
  özetleyen notlar ve her skill'de PDF sayfa numarası. Yapay zeka şaşırınca o sayfayı okuyup kendini
  düzeltiyor. PDF'ler: blackmagicdesign.com/products/davinciresolve/training
- github.com/heygen-com/hyperframes: Claude'un hareketli grafikleri HTML olarak tasarlayıp videoya
  çevirdiği açık kaynak araç (bölüm geçişleri, alt yazı kartları, intro).
