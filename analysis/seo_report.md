# Screaming Frog Issues Overview Analizi

Bu rapor, `analysis/issues_overview.csv` dosyasındaki Screaming Frog "Issues Overview" verilerini temel alır ve yakinimdakideprem.com'un teknik SEO durumunu özetler. Aşağıdaki bulgular; öncelik dağılımı, en kritik beş sorun, düzeltme önerileri, eğilim analizi ve görsel özetleri içerir.

## Öncelik Bazlı Özet

Aşağıdaki tablo; her öncelik düzeyindeki toplam sorun sayısını, etkilenen URL toplamını ve öne çıkan notları gösterir (toplam 19 sorun incelendi).

| Öncelik | Sorun Sayısı | Toplam URL | Öne Çıkan Not |
| --- | --- | --- | --- |
| High | 3 | 35 | Başlık ve canonical etiketleri kritik hataların büyük kısmını oluşturuyor. |
| Medium | 7 | 76 | İçerik kalitesi, meta verilerin konum/piksel sınırları ve görsel boyutları için iyileştirme gerekiyor. |
| Low | 9 | 111 | Güvenlik başlıkları, çoklu/duble H2'ler ve okunabilirlik fırsatları yaygın. |

Toplamda 222 URL bulguya takılıyor. Öncelik düzeylerine göre etkilenen URL miktarının metin tabanlı çubuk grafik özeti aşağıdadır (her blok ≈2 URL'yi temsil eder):

```
High   ████████████████ 35 URL
Medium ████████████████████████████████ 76 URL
Low    ██████████████████████████████████████████████ 111 URL
```

## En Fazla URL'yi Etkileyen İlk 5 Sorun

| # | Sorun | Tür | Öncelik | URL | % Toplam | Potansiyel Etki |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Security: Missing Content-Security-Policy Header | Warning | Low | 47 | 94,0% | XSS ve veri enjeksiyonu riskini artırır; güven damgasını ve Core Web Vitals güven sinyallerini olumsuz etkiler. |
| 2 | H2: Multiple | Warning | Low | 21 | 95,45% | Başlık hiyerarşisi belirsizleşerek kullanıcıların tarama deneyimini ve yardımcı teknolojilerin erişilebilirliğini düşürür. |
| 3 | Canonicals: Missing | Warning | Medium | 17 | 73,91% | Yinelenen içerik varyasyonlarının Google tarafından yanlış URL'de sıralanmasına neden olabilir. |
| 4 | Canonicals: Outside `<head>` | Issue | High | 16 | 69,57% | Etiket `<head>` dışında olduğu için arama motorları canonical sinyalini tamamen yok sayabilir. |
| 5 | Content: Readability Very Difficult | Opportunity | Low | 16 | 69,57% | Karmaşık metinler; özellikle afet iletişiminde dönüşümü, bağış veya kayıt süreçlerini yavaşlatabilir. |

Bu beş sorun neredeyse tüm taranan URL'leri etkiliyor; özellikle canonical eksikliği/yanlış konumu ve güvenlik başlıklarının yokluğu indeksleme tutarlılığı ile kullanıcı güvenini tehdit ediyor.

## Yüksek Öncelikli Sorunlar ve Aksiyonlar

### Page Titles: Outside `<head>` (16 URL)
- **SF önerisi:** `<title>` etiketini HTML `<head>` bölümü içine taşıyın.
- **Ek adımlar:**
  - Şablon dosyalarını (`app/` içindeki layoutlar) kontrol ederek `head` bloğu dışında manuel eklenmiş `title` parçacıkları olup olmadığını saptayın.
  - Sunucu tarafında (örn. Blade/Vue bileşenleri) koşullu render edilen alanları inceleyip tarayıcıya gönderilen nihai DOM'un geçerli olduğundan emin olun.
  - Dağıtım öncesi HTML doğrulayıcı (W3C validator, Lighthouse) ile otomatik kontrol ekleyin.

### Response Codes: Internal Client Error (4xx) (3 URL)
- **SF önerisi:** Hatalı URL'leri 200 durum kodu döndürecek doğru sayfalara yönlendirin veya içerikleri güncelleyin.
- **Ek adımlar:**
  - 4xx veren URL'lere hangi sayfaların link verdiğini `Bulk Export > Response Codes > Internal > Client Error (4xx)` çıktısıyla eşleştirip bozulan bağlantıları düzeltin.
  - Gerçekten kaldırılmış içerikler için 410 ya da 301 ile en yakın üst kategoriye yönlendirme yapın; böylece tarama bütçesi boşa harcanmaz.
  - Rate limit (429) ya da 403 gibi sunucu bazlı hatalar görüyorsanız, CDN/firewall kurallarını ve bot kısıtlarını gözden geçirin.

### Canonicals: Outside `<head>` (16 URL)
- **SF önerisi:** Canonical link öğesini `<head>` içinde bulundurup arama motorlarına sunun.
- **Ek adımlar:**
  - Şablon motorundaki `head` bloğunu tekilleştirip canonical etiketi için merkezi bir partial kullanın.
  - Dinamik sayfalarda canonical URL'leri `absolute` formatta yazın (protokol + alan adı) ve UTM/izleme parametrelerini kaldırın.
  - AMP veya alternatif dil sürümleri varsa `rel="alternate" hreflang` ilişkilerini canonical ile eşleştirin.

## Orta Öncelikli Sorunlar ve Aksiyonlar

### Canonicals: Missing (17 URL)
- **SF önerisi:** Her URL için canonical belirtin.
- **Ek adımlar:**
  - Filtrelenmiş liste/dinamik parametre sayfalarını ana kategoriye yönlendiren canonical'lar tanımlayın.
  - CMS'in otomatik canonical üretimi varsa site yapılandırmasını gözden geçirip tüm içerik tiplerinde aktif olduğundan emin olun.
  - Yinelenen içerik bulunan URL'leri keşfetmek için Screaming Frog'un Near Duplicates raporunu çalıştırın.

### Content: Low Content Pages (7 URL)
- **SF önerisi:** Sayfa amacını daha iyi anlatacak açıklayıcı metin ekleyin.
- **Ek adımlar:**
  - Afet bilgilendirme sayfalarına sık sorulan sorular (SSS), vaka çalışmaları veya kullanıcı yorumları ekleyerek kelime sayısını artırın.
  - Anahtar kelime eşleşmesini doğal biçimde güçlendirmek için başlık, alt başlık ve görsel alt metinlerini yeniden yazın.
  - İçeriği genişletirken 200+ kelime hedefini aşacak şekilde bölüm bazlı taslak hazırlayın.

### Meta Description: Outside `<head>` (16 URL)
- **SF önerisi:** Meta açıklamaları `<head>` içinde yerleştirin.
- **Ek adımlar:**
  - Şablonlarda `<meta name="description">` çıktısını head bloğunda sabitleyin; SPA çatıları kullanılıyorsa sunucu tarafı render çıktısını doğrulayın.
  - Build pipeline'ına HTML linter ekleyerek meta etiketlerinin DOM hiyerarşisini otomatik test edin.
  - Açıklamaların benzersiz olduğundan emin olmak için Screaming Frog'un Duplicate Meta Description filtresini de kontrol edin.

### Page Titles: Over 561 Pixels (13 URL)
- **SF önerisi:** Başlıkları piksel sınırına göre kısaltın.
- **Ek adımlar:**
  - Ölçümleri Search Console performans raporundaki SERP snippet'leriyle karşılaştırıp en fazla gösterim alan URL'leri önceleyin.
  - İlk 600 piksele ana anahtar kelime + değer önerisini sığdıracak biçimde yeniden yazın.
  - Markalı son ekleri ("| Yakinimdaki Deprem") yalnızca gerekli sayfalarda kullanarak tekrarları azaltın.

### Page Titles: Over 60 Characters (13 URL)
- **SF önerisi:** Karakter sınırlarını aşmayacak şekilde sadeleştirin.
- **Ek adımlar:**
  - 60 karakterden uzun olan başlıkları piksel raporuyla çapraz kontrol ederek hangi sayfalarda gerçek SERP kesilmesi olduğunu saptayın.
  - Yinelenen kelime gruplarını kaldırın ve önemli çağrı ifadelerini başa taşıyın.
  - İç/dış link anchor'larını bu yeni başlıklara uyacak şekilde güncelleyin.

### Images: Over 100 KB (9 URL)
- **SF önerisi:** Görselleri sıkıştırın ve uygun format seçin.
- **Ek adımlar:**
  - WebP/AVIF dönüşümü ve `srcset` kullanımıyla retina cihazlarda da optimize boyut sunun.
  - Lighthouse raporundaki "Serve images in next-gen formats" ve "Defer offscreen images" maddelerini izleyerek lazy-load stratejisi uygulayın.
  - CDN katmanında otomatik yeniden boyutlandırma kuralları (ör. Cloudflare Polish) etkinleştirin.

### H1: Missing (1 URL)
- **SF önerisi:** Sayfanın ana başlığını ekleyin.
- **Ek adımlar:**
  - Şablon koşullarının H1'i gizlemediğinden emin olun; JavaScript ile sonradan yükleniyorsa SSR çıktısını güncelleyin.
  - H1 ile başlık/URL uyumunu sağlayıp breadcrumb yapısı ile destekleyin.
  - Eksik H1 için içerik editörlerine hatırlatma gönderecek CMS validasyonları ekleyin.

## Eğilimler ve Sorun Kümeleri

- **Başlık & Meta blokları:** Üç farklı başlık sorunu (head dışında, piksel, karakter) ve iki meta açıklama problemi, sayfa şablonlarının yapısal olarak gözden geçirilmesini gerektiriyor. Tek bir layout düzeltmesi, 42 URL'deki başlık/meta hatasını aynı anda giderebilir.
- **Canonical tutarlılığı:** Canonical eksikliği ve head dışındaki canonical toplam 33 URL'yi etkiliyor. Bu da çoğaltılmış içerik yönetimi için merkezi bir çözüm (örn. otomatik canonical helper) ihtiyacını gösteriyor.
- **İçerik kalitesi ve okunabilirlik:** Düşük kelime sayısı, zorlu ve çok zorlu okunabilirlik uyarıları ile birleştiğinde; özellikle kriz iletişimi yapan sayfalarda sade dil ve kapsamlı anlatı eksikliğini ortaya koyuyor.
- **Güvenlik & teknik borç:** Content-Security-Policy başlığının olmaması ve bazı 4xx kodları; güvenlik standartlarını ve kullanıcı güvenini tehdit eden yaygın eksiklikler olarak öne çıkıyor.

## Sonuç

Canonical etiketleri, başlık/meta bloklarının `<head>` hiyerarşisi ve güvenlik başlıkları üzerinde yapılacak iyileştirmeler; tarama bütçesinin korunması, SERP tutarlılığı ve kullanıcı güveni açısından en hızlı getiriyi sağlayacaktır. İçerik yoğunluğu, okunabilirlik ve görsel optimizasyonu gibi orta öncelikli çalışmalar ise özellikle deprem bilgilendirme sayfalarında kullanıcı deneyimini iyileştirip dönüşüm oranlarını artıracaktır.
