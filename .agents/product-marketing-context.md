# Product Marketing Context

*Last updated: 2026-04-23*

## Product Overview
**One-liner:** Türkiye için gerçek zamanlı deprem bildirim ve haritası — uygulama indirmeden, konumuna göre.

**What it does:** Kandilli ve AFAD verilerini canlı çeker, Türkiye'deki son depremleri harita üzerinde gösterir. Kullanıcı konumunu paylaşırsa "yakınındaki depremler"i listeler. Push bildirimleriyle yeni deprem olduğunda haber verir. Twitter'da 4.0+ depremleri otomatik paylaşan bot çalışır.

**Product category:** Deprem bildirim servisi / Acil durum bilgi platformu (web tabanlı).

**Product type:** Ücretsiz kamu hizmeti web uygulaması (static frontend + FastAPI backend).

**Business model:** Şu an tamamen ücretsiz, reklamsız. İlerideki plan: yalnızca **reklam** (Google AdSense / direct sponsor). Premium/bağış/ortaklık planı yok — açık ve basit: kullanıcı kitlesi büyüdükten sonra reklam ekle.

## Target Audience
**Target audience:** Türkiye'de yaşayan, deprem kaygısı taşıyan genel nüfus. Özellikle 6 Şubat 2023 Kahramanmaraş depremi sonrası artan hassasiyetle bildirim/takip ihtiyacı olan kullanıcılar.

**Primary segment (#1 hedef):** **Birinci derece deprem bölgelerinde yaşayan kullanıcılar** — İstanbul, İzmir, Kahramanmaraş, Hatay, Adıyaman, Malatya, Gaziantep, Kocaeli, Sakarya, Düzce, Bolu, Van, Bingöl, Elazığ. Tüm marketing mesajlaması ve içerik stratejisi bu kitleye odaklanacak.

**Secondary segments (sonra):**
- Aileli ebeveynler (uzaktaki sevdiklerinin bölgesinde deprem oldu mu)
- Deprem kaygısı olan gençler (18-30, sürekli kontrol davranışı)
- Afet gönüllüleri / AKUT / hobiyen deprem takipçileri

**Primary use case:** "Bir sarsıntı hissettim, deprem miydi, büyüklüğü neydi, merkezi neredeydi?" → 30 saniye içinde cevap al.

**Jobs to be done:**
- Son depremin büyüklüğünü ve merkezini anlık öğrenmek
- "Benim şehrimde/ilçemde deprem oldu mu?" sorusuna bakmak
- Ailesini/sevdiklerini uzakta olduğunda takip etmek ("İzmir'de yaşayan anneme deprem ne kadar yakındı?")
- Bildirim almak (özellikle uyurken/işteyken)
- Deprem öncesi/sonrası ne yapılmalı bilgisini okumak
- Sosyal medyada paylaşım için kaynak kullanmak

**Use cases:**
- Sarsıntı hissettikten sonra doğrulama
- Haber sitelerinden önce bilgi alma (hız avantajı)
- Ailede/arkadaş grubunda "deprem oldu mu" WhatsApp cevabı için link paylaşımı
- Belirli şehirlerin deprem geçmişini araştırma (SEO trafiği)

## Problems & Pain Points
**Core problem:** Türkiye'de her gün 30-100 deprem oluyor ama insanlar hangisinin gerçekten önemli olduğunu, nerede olduğunu ve ne kadar yakın olduğunu hızlıca öğrenemiyor.

**Why alternatives fall short:**
- **AFAD uygulaması**: Uygulama indirmek gerekir, UX ağır, güncellemeler geç, push bildirimleri tutarsız
- **Kandilli web sitesi**: 1990'lardan kalma arayüz, mobil uyumlu değil, harita yok, bildirim yok
- **Twitter (@DepremDairesi)**: kronolojik feed, konum bağlamı yok, sessiz mod'da kaybolur
- **Üçüncü parti app'ler**: Play Store/App Store reklamla dolu, pay-to-remove-ads, izin gereksinimi fazla

**What it costs them:**
- Haber sitelerinde 10-15 dakika arama → panik süresi uzar
- "Büyük mü, küçük mü?" belirsizliği stres yaratır
- Uzaktaki sevdiklerinden haber alamama
- Küçük depremlerden sonra "asıl deprem gelecek mi" kaygısı

**Emotional tension:** Korku, belirsizlik, "elimden bir şey gelmeyecek mi" çaresizliği, 2023 depremi travması.

## Competitive Landscape
**Direct:**
- **AFAD Deprem uygulaması** — resmi, veri güvenilir ama UX kötü, web yok, push bildirimleri güvenilmez
- **Kandilli Rasathanesi web** — veri kaynağı olarak iyi ama kullanıcı deneyimi 90'lar seviyesinde
- **Earthquake Network (global app)** — Türkiye özel değil, AFAD/Kandilli entegrasyonu yok
- **LastQuake (EMSC)** — global odaklı, Türkçe sınırlı

**Secondary (aynı problem, farklı çözüm):**
- **Haber siteleri** (Hürriyet/Sözcü deprem kategorisi) — yavaş, reklam yoğun
- **@AFADDeprem Twitter hesabı** — chronological, bağlamsız
- **WhatsApp grupları** — rumor/yanlış bilgi riski yüksek

**Indirect:**
- **Hiçbir şey yapmamak** — "nasılsa önemliyse duyarım"
- **Haberlere güvenmek** — pasif yaklaşım

## Differentiation
**Key differentiators:**
- **İndirme yok, sadece web** — saniyeler içinde kullanmaya başla
- **Konum-farkında**: "deprem bana ne kadar yakın" sorusuna cevap
- **Harita entegre**: Leaflet tabanlı görsel yaklaşım
- **Push bildirim**: web push (OneSignal), uygulama gerektirmez
- **Türkiye'ye özel**: sadece Türkiye depremleri, Türkçe arayüz, Türkiye haritası
- **Şehir bazlı SEO sayfaları**: her il için ayrı sayfa (133 sayfa), Google'dan organik trafik
- **Hızlı**: static HTML + Cloudflare CDN, 1 saniyede yüklenir
- **Reklamsız, kayıt gerektirmez**

**Why customers choose us:** "Telefonumda 3 deprem uygulaması var, hiçbirine girmiyorum çünkü uygulama açmak zaman alıyor. Yakınımdaki Deprem'i WhatsApp'a kaydetmişim, 5 saniyede açılıyor."

## Objections & Anti-Persona
| Objection | Response |
|---|---|
| "AFAD zaten var, niye bunu kullanayım?" | AFAD resmi kaynak ama arayüzü ve bildirimleri kullanışsız. Biz AFAD verisini alıp hızlı gösteriyoruz — iki kaynak birbirini tamamlar, alternatif değil. |
| "Uygulamalar daha güvenli" | Web push güvenli ve OneSignal standart. Üstelik uygulama = depolama, izinler, güncellemeler. Web = anında aç. |
| "Konum paylaşmak istemiyorum" | Konum paylaşmak opsiyonel, sitenin %80'i konumsuz çalışır. |
| "Veriler doğru mu?" | Direkt Kandilli ve AFAD'dan çekiliyor, üzerine analiz eklemiyoruz. |

**Anti-persona:**
- Deprem-skeptik / "zaten önemsizse gerek yok" diyenler
- Uygulama fetişisti (her şey app olmalı diyenler)
- Tamamen offline kalmak isteyenler

## Switching Dynamics (JTBD Four Forces)
**Push (mevcut çözümden uzaklaştıran):**
- AFAD uygulaması push'ları geç geliyor veya hiç gelmiyor
- Kandilli web sitesi mobilde kullanılmıyor
- Haber sitelerinde reklam/pop-up çokluğu
- WhatsApp gruplarında yanlış bilgi

**Pull (bizi çeken):**
- Link tıkla, anında harita
- WhatsApp'tan arkadaş paylaştığı için keşif
- "Konumuma yakın mı" sorusuna tek cevap veren yer
- Twitter botundan gelen tweetlerde link

**Habit:**
- "Zaten AFAD'ım var" alışkanlığı
- Ekşi Sözlük/Twitter'da kontrol etme refleksi

**Anxiety:**
- "Bildirim izni verince spam gelir mi?" (hayır, sadece deprem)
- "Site güvenli mi, gerçek mi?" (HTTPS, açık kaynak kanıtı yok — trust signals eksik)
- "Kapanır mı, bir gün kaybolur mu?" (sürdürülebilirlik endişesi)

## Customer Language
**How they describe the problem (verbatim tahmini, Ekşi/Twitter/Reddit araştırmayla doğrulanmalı):**
- "Deprem mi oldu lan, sallandı gibi?"
- "İstanbul'da deprem oldu mu şimdi?"
- "Kaç büyüklüğündeydi?"
- "Annem İzmir'de, deprem ona yakın mı?"
- "AFAD uygulaması yine bildirim atmamış"

**How they describe our solution:**
- "Yakınımdaki deprem var ya, oraya bakıyorum"
- "Harita olan site"
- "Konumu gösteriyor, süper"

**Words to use:** yakın, anında, harita, konum, güvenli, ücretsiz, Türkiye, şehir, il, hızlı, açık, bildir, sarsıntı, büyüklük, merkez, derinlik.

**Words to avoid:** gelişmiş algoritma, yapay zeka destekli (şu an değil, sahte görünür), premium (ücretsizlik vurgusu), uygulama (biz web'iz), tahmin (deprem tahmin edilemez, yanlış anlaşılmaması için).

**Glossary:**
| Term | Meaning |
|---|---|
| Yakın deprem | Kullanıcının konumuna 100 km yarıçapındaki depremler |
| Büyüklük | Richter ölçeğindeki magnitude değeri |
| Merkez | Deprem episantrı (enlem/boylam + il/ilçe) |
| Derinlik | Yer yüzeyinin altındaki km cinsinden mesafe |
| Geçmiş olsun | Türkçe deprem sonrası geleneksel temenni |

## Brand Voice
**Tone:** Samimi, güven veren, telaşsız ama ciddi. Paniklemeyen ama hafife almayan. Teknik jargonsuz.

**Style:** Kısa cümleler, Türkçe doğal, emoji'leri yerinde kullan (🚨📍⏱️). "Geçmiş olsun" kullan — duygusal bağ kurar.

**Personality:** Güvenilir komşu, teknik bilen arkadaş, sakin ama hazırlıklı, Türkiyeli, dayanışmacı.

## Proof Points
**Metrics (2026-04 itibariyle — ERKEN AŞAMA):**
- **Google Search Console (son 7 gün):** 27 tıklama, 3.389 impression, ortalama pozisyon 7-13
- **En güçlü sorgular:** "yakınımdaki deprem" (2132 impression, pozisyon 7.6), "sismik harita canlı" (CTR %33), "anlık deprem" (541 impression, pozisyon 11.8)
- **GA4 (son 7 gün):** ~24 tekil kullanıcı/hafta (8 organic search, 6 direct, 6 unassigned, 4 social)
- **En çok ziyaret edilen sayfa:** `/` (19 user, 80 view, 211 sn ortalama süre, %43 engagement)
- **Twitter:** 3-4 takipçi, arada lajos/like
- **133 SEO sayfası** canlıda (her il + blog)
- **SEO audit (2026-04-21):** 100 sayfa tarandı, 3 minor issue
- **Altyapı:** Cloudflare CDN + HTTPS + Full Strict SSL, Caddy reverse proxy

**Customers/logos:** Yok — ürün pazar tanınırlığı aşamasında.

**Testimonials:** Henüz yok. Twitter'da seyrek like'lar var, sistematik toplanmıyor.

**Büyüme durumu:** Ürün çalışıyor, SEO temeli atıldı, şimdi **bilinirlik/distribution** aşaması kritik. "Build" bitti, "awareness" başlamalı.

**Value themes:**
| Theme | Proof |
|---|---|
| Hız | 1 saniyede yükleniyor, CDN edge |
| Kapsayıcılık | 81 il sayfası, Türkiye'nin tamamı |
| Güvenilirlik | Direkt Kandilli/AFAD datası |
| Ücretsiz | Reklam yok, kayıt yok, hep ücretsiz olacak |

## Goals
**Primary business goal:** Türkiye'deki deprem kaygısı olan insanlara en hızlı/kullanışlı cevap olmak → aylık aktif kullanıcı sayısını büyütmek → uzun vadede sürdürülebilir bağış/sponsor modeliyle yaşatmak.

**Key conversion action:**
- **Birinci öncelik:** Push bildirim subscribe (OneSignal)
- **İkinci öncelik:** Twitter bot takibi (@ hesabı)
- **Üçüncü öncelik:** "WhatsApp'ta paylaş" → viral loop

**Current metrics (2026-04, 7 günlük pencere):**
- Weekly Active Users: ~24
- Search Console tıklama: 27
- Search Console impression: 3.389
- Twitter followers: 3-4
- Top channel: Organic Search (8 user) + Direct (6 user)
- En güçlü keyword: "yakınımdaki deprem" (zaten domain match, kolay win)

**Büyüme darboğazı:** Distribution. SEO temeli var ama kimse henüz bilmiyor. "Nasıl ölçüyorum" değil, "nasıl duyururum" sorusu öncelikli.

**Target (6 ay):** Deprem olduğunda Türkiye'de ilk akla gelen "ne oldu" kaynağı olmak. Yani Ekşi'de "deprem oldu mu nerden bakacağım" sorusuna cevap olarak yakinimdakideprem.com yazılsın.
