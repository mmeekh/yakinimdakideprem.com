# 🌍 Anlık Deprem - Gerçek Zamanlı Deprem Bilgi Platformu

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/anlikdeprem/anlikdeprem)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/node.js-%3E%3D16.0.0-brightgreen.svg)](https://nodejs.org/)
[![NPM](https://img.shields.io/badge/npm-%3E%3D8.0.0-red.svg)](https://www.npmjs.com/)

Türkiye'nin en kapsamlı gerçek zamanlı deprem bilgi platformu. USGS verileri ile güncellenen interaktif harita, hayat kurtaran güvenlik rehberleri ve kapsamlı deprem hazırlık bilgileri.

## 🚀 Özellikler

### 📍 Gerçek Zamanlı Deprem Haritası
- **USGS API Entegrasyonu**: En güncel deprem verileri
- **İnteraktif Leaflet Haritası**: Türkiye odaklı harita görünümü
- **Büyüklük Filtreleme**: 3.0+, 4.0+, 5.0+ depremleri filtreleme
- **Otomatik Güncelleme**: 2 dakikada bir otomatik veri yenileme
- **Responsive Tasarım**: Tüm cihazlarda mükemmel görünüm

### 🛡️ Deprem Güvenlik Rehberleri
- **Bina İçindeyseniz**: Çök-Kapan-Tutun hareketi rehberi
- **Dışarıdaysanız**: Açık alan güvenlik önerileri
- **Araç Kullanırken**: Araç içi güvenlik protokolleri
- **Acil İletişim**: 112, AFAD, AKUT acil numaraları

### 🎒 İlk Yardım Çantası Rehberi
- **Video Anlatım**: Uzmanlar tarafından hazırlanan detaylı video
- **Kapsamlı Malzeme Listesi**: 4 kategori altında 50+ malzeme
- **Kontrol Listesi**: PDF indirilebilir kontrol listesi
- **Kişiselleştirme**: Aile ihtiyaçlarına göre özelleştirme

### 📚 Blog ve Bilgi Merkezi
- **Uzman Yazıları**: Deprem güvenliği hakkında detaylı makaleler
- **Görsel Rehberler**: WebP formatında optimize edilmiş görseller
- **SEO Optimizasyonu**: Arama motorları için optimize edilmiş içerik

### 👤 Hakkımızda
- **Misyon ve Vizyon**: Toplumsal fayda odaklı yaklaşım
- **Değerler**: Doğruluk, yenilikçilik, iş birliği
- **İletişim**: Geri bildirim ve öneri formu

## 🛠️ Teknik Özellikler

### Frontend Teknolojileri
- **HTML5**: Semantik ve erişilebilir markup
- **CSS3**: Modern CSS özellikleri ve Grid/Flexbox
- **Vanilla JavaScript**: Framework bağımsız, performanslı kod
- **Leaflet.js**: Açık kaynak harita kütüphanesi
- **Font Awesome**: 6.4.0 ikon kütüphanesi

### Performans Optimizasyonları
- **WebP Görseller**: %30 daha küçük dosya boyutları
- **CSS Minification**: CleanCSS ile optimize edilmiş stiller
- **JavaScript Bundling**: Webpack ile modüler yapı
- **Lazy Loading**: Görsel yükleme optimizasyonu
- **Service Worker**: Offline çalışma desteği

### Responsive Tasarım
- **Mobile First**: Mobil cihazlar öncelikli tasarım
- **Breakpoints**: 576px, 768px, 1024px responsive noktaları
- **Touch Friendly**: Dokunmatik cihazlar için optimize edilmiş UI
- **PWA Ready**: Progressive Web App özellikleri

## 📁 Proje Yapısı

```
anlikdeprem/
├── 📄 index.html                 # Ana sayfa
├── 📄 deprem-aninda.html         # Deprem güvenlik rehberi
├── 📄 ilk-yardim-cantasi.html    # İlk yardım çantası rehberi
├── 📄 ben-kimim.html             # Hakkımızda sayfası
├── 📄 blog.html                  # Blog ana sayfası
├── 📄 blog-*.html                # Blog yazıları
├── 📄 kullanim-sartlari.html     # Kullanım şartları
├── 📄 gizlilik-politikasi.html   # Gizlilik politikası
├── 📄 cerez-politikasi.html      # Çerez politikası
├── 📄 sorumluluk-reddi.html      # Sorumluluk reddi
├── 📄 site.webmanifest           # PWA manifest
├── 📄 package.json               # NPM konfigürasyonu
├── 📄 webpack.config.js          # Webpack konfigürasyonu
├── 📁 css/                       # Stil dosyaları
│   ├── 📄 style.css              # Ana stil dosyası
│   ├── 📄 style-optimized.css    # Optimize edilmiş stiller
│   ├── 📄 variables.css          # CSS değişkenleri
│   ├── 📄 base.css               # Temel stiller
│   ├── 📄 components.css         # Bileşen stilleri
│   ├── 📄 header.css             # Header stilleri
│   ├── 📄 ben-kimim.css          # Hakkımızda stilleri
│   ├── 📄 blog.css               # Blog stilleri
│   ├── 📄 deprem-aninda.css      # Deprem rehberi stilleri
│   └── 📄 ilk-yardim.css         # İlk yardım stilleri
├── 📁 js/                        # JavaScript dosyaları
│   ├── 📄 script.js              # Ana JavaScript dosyası
│   ├── 📄 main.js                # Giriş noktası
│   ├── 📄 header.js              # Header işlevselliği
│   ├── 📄 ben-kimim.js           # Hakkımızda işlevselliği
│   ├── 📄 deprem-aninda.js       # Deprem rehberi işlevselliği
│   └── 📁 core/                  # Modüler JavaScript
│       ├── 📄 App.js             # Ana uygulama sınıfı
│       ├── 📄 DataModule.js      # Veri yönetimi
│       ├── 📄 MapModule.js       # Harita işlevselliği
│       ├── 📄 StatsModule.js     # İstatistik modülü
│       └── 📄 UIModule.js        # UI yönetimi
├── 📁 components/                # HTML bileşenleri
│   ├── 📄 header.html            # Header bileşeni
│   ├── 📄 footer.html            # Footer bileşeni
│   └── 📄 navigation.html        # Navigasyon bileşeni
├── 📁 images/                    # Görsel dosyalar
│   ├── 📄 hero-bg.jpg            # Ana sayfa arka planı
│   ├── 📄 binaicindeyseniz.webp  # Bina içi rehber görseli
│   ├── 📄 disaridayken.webp      # Dışarıda rehber görseli
│   ├── 📄 arackullarnirken.webp  # Araç kullanım rehberi
│   └── 📄 depremcantasi.webp     # İlk yardım çantası görseli
└── 📁 icons/                     # İkon dosyaları
    ├── 📄 logo.png               # Ana logo
    ├── 📄 favicon-*.png          # Favicon dosyaları
    ├── 📄 apple-touch-icon.png   # iOS ikonu
    └── 📄 android-chrome-*.png   # Android ikonları
```

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler
- Node.js >= 16.0.0
- NPM >= 8.0.0
- Modern web tarayıcısı

### Kurulum
```bash
# Projeyi klonlayın
git clone https://github.com/anlikdeprem/anlikdeprem.git
cd anlikdeprem

# Bağımlılıkları yükleyin
npm install

# Geliştirme sunucusunu başlatın
npm run dev

# Veya sadece build yapın
npm run build
```

### Geliştirme Komutları
```bash
# CSS minify ve optimize et
npm run css:minify

# JavaScript minify ve bundle et
npm run js:minify

# HTML minify et
npm run html:minify

# Tüm build işlemlerini çalıştır
npm run build

# Dosya değişikliklerini izle
npm run watch

# Lighthouse performans testi
npm run lighthouse

# Erişilebilirlik testi
npm run test:accessibility

# Tüm testleri çalıştır
npm run test
```

## 🌐 API Entegrasyonları

### USGS Earthquake API
- **Endpoint**: `https://earthquake.usgs.gov/fdsnws/event/1/query`
- **Veri Formatı**: GeoJSON
- **Güncelleme Sıklığı**: 2 dakika
- **Filtreleme**: Türkiye bölgesi, son 24 saat, 2.5+ büyüklük

### Güvenilir Kaynaklar
- **AFAD**: Afet ve Acil Durum Yönetimi Başkanlığı
- **USGS**: United States Geological Survey
- **KOERİ**: Kandilli Rasathanesi ve Deprem Araştırma Enstitüsü
- **American Red Cross**: Uluslararası güvenlik standartları

## 📱 PWA Özellikleri

### Web App Manifest
- **Standalone Mode**: Tam ekran uygulama deneyimi
- **Theme Color**: #d32f2f (kırmızı tema)
- **Background Color**: #f9f9f9 (açık gri)
- **Icons**: 16x16'dan 512x512'ye kadar tüm boyutlar

### Offline Desteği
- **Service Worker**: Temel offline işlevsellik
- **Cache Strategy**: Stale-while-revalidate
- **Fallback Pages**: Ağ bağlantısı olmadığında temel sayfalar

## 🎨 Tasarım Sistemi

### Renk Paleti
- **Primary**: #d32f2f (Kırmızı)
- **Secondary**: #f44336 (Açık kırmızı)
- **Dark**: #212121 (Koyu gri)
- **Light**: #f5f5f5 (Açık gri)
- **Text**: #333333 (Koyu metin)

### Tipografi
- **Font Family**: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
- **Font Sizes**: 14px - 48px arası responsive boyutlar
- **Line Height**: 1.6 (okunabilirlik için optimize)

### Spacing System
- **XS**: 5px
- **SM**: 10px
- **MD**: 15px
- **LG**: 20px
- **XL**: 30px
- **2XL**: 40px

## 🔧 Geliştirme Notları

### Modüler Mimari
- **Core Modules**: App.js, DataModule.js, MapModule.js, StatsModule.js, UIModule.js
- **Separation of Concerns**: Her modül kendi sorumluluğuna odaklanır
- **Event-Driven**: Modüller arası iletişim event sistemi ile

### Performans Optimizasyonları
- **Debounced API Calls**: Gereksiz API çağrılarını önler
- **Lazy Loading**: Görseller ihtiyaç duyulduğunda yüklenir
- **CSS Variables**: Tutarlı stil yönetimi
- **Minification**: Üretim için optimize edilmiş dosyalar

### Hata Yönetimi
- **Try-Catch Blocks**: Tüm kritik işlemler hata kontrolü ile
- **User Feedback**: Kullanıcıya anlaşılır hata mesajları
- **Fallback UI**: API hatalarında alternatif içerik

## 📊 SEO ve Erişilebilirlik

### SEO Optimizasyonları
- **Meta Tags**: Her sayfa için özel meta açıklamaları
- **Structured Data**: JSON-LD formatında yapılandırılmış veri
- **Sitemap**: Arama motorları için site haritası
- **Robots.txt**: Arama motoru yönergeleri

### Erişilebilirlik
- **ARIA Labels**: Ekran okuyucular için etiketler
- **Keyboard Navigation**: Klavye ile tam navigasyon
- **Color Contrast**: WCAG 2.1 AA standartlarına uygun kontrast
- **Alt Text**: Tüm görseller için açıklayıcı alt metinler

## 🧪 Test ve Kalite

### Otomatik Testler
- **Lighthouse**: Performans, erişilebilirlik, SEO skorları
- **Pa11y**: Erişilebilirlik testleri
- **WebPageTest**: Gerçek dünya performans testleri

### Manuel Testler
- **Cross-Browser**: Chrome, Firefox, Safari, Edge
- **Mobile Testing**: iOS Safari, Android Chrome
- **Responsive**: 320px - 1920px arası tüm boyutlar

## 📈 Performans Metrikleri

### Core Web Vitals
- **LCP (Largest Contentful Paint)**: < 2.5s
- **FID (First Input Delay)**: < 100ms
- **CLS (Cumulative Layout Shift)**: < 0.1

### Lighthouse Skorları
- **Performance**: 90+
- **Accessibility**: 95+
- **Best Practices**: 90+
- **SEO**: 95+

## 🤝 Katkıda Bulunma

### Geliştirme Süreci
1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

### Kod Standartları
- **ESLint**: JavaScript kod kalitesi
- **Prettier**: Kod formatlaması
- **Conventional Commits**: Standart commit mesajları
- **Semantic Versioning**: Sürüm numaralandırması

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📞 İletişim

- **Website**: [anlikdeprem.com](https://anlikdeprem.com)
- **Email**: info@anlikdeprem.com
- **GitHub**: [@anlikdeprem](https://github.com/anlikdeprem)

## 🙏 Teşekkürler

- **USGS**: Deprem verileri için
- **AFAD**: Türkiye deprem bilgileri için
- **Leaflet**: Harita kütüphanesi için
- **Font Awesome**: İkonlar için
- **Tüm Katkıda Bulunanlar**: Açık kaynak topluluğu

---

**⚠️ Önemli Not**: Bu platform eğitim ve bilgilendirme amaçlıdır. Acil durumlarda her zaman resmi kurumları (112, AFAD) arayın.

**🌍 Anlık Deprem** - Toplumu Geliştirmek İçin Çabalayan Bir Girişim
