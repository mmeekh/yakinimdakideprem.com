# 🌍 Yakınımdaki Deprem - Full-Stack Deprem Bilgi Platformu

[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](https://github.com/yakınımdakideprem/yakınımdakideprem)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-compose-blue.svg)](https://docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Caddy](https://img.shields.io/badge/Caddy-2.8+-blue.svg)](https://caddyserver.com/)

Türkiye'nin en kapsamlı **full-stack** deprem bilgi platformu. **FastAPI backend**, **Caddy reverse proxy** ve **modern frontend** ile gerçek zamanlı deprem verileri, interaktif harita ve hayat kurtaran güvenlik rehberleri.

## 🏗️ Proje Mimarisi

### **Backend (FastAPI + Docker)**
- **FastAPI**: Modern, hızlı Python web framework
- **USGS API Entegrasyonu**: Gerçek zamanlı deprem verileri
- **Docker Containerization**: Taşınabilir ve ölçeklenebilir deployment
- **CORS Desteği**: Cross-origin istekler için güvenli yapılandırma

### **Reverse Proxy (Caddy)**
- **Caddy Server**: Otomatik HTTPS ve modern web server
- **Static File Serving**: Frontend dosyalarını servis etme
- **API Routing**: Backend API'ye yönlendirme
- **Security Headers**: Güvenlik optimizasyonları

### **Frontend (Vanilla JavaScript + Modern CSS)**
- **Responsive Design**: Tüm cihazlarda mükemmel görünüm
- **Interactive Maps**: Leaflet.js ile harita görselleştirme
- **Real-time Updates**: 2 dakikada bir otomatik veri yenileme
- **PWA Ready**: Progressive Web App özellikleri

## 🚀 Özellikler

### 📍 Gerçek Zamanlı Deprem Haritası
- **USGS API Entegrasyonu**: En güncel deprem verileri
- **İnteraktif Leaflet Haritası**: Türkiye odaklı harita görünümü
- **Büyüklük Filtreleme**: 1.0+, 3.0+, 4.0+, 5.0+ depremleri filtreleme
- **Otomatik Güncelleme**: 2 dakikada bir otomatik veri yenileme
- **Geniş Alan Taraması**: 5000km yarıçapında kapsamlı veri

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

### 📊 Backend API Özellikleri
- **RESTful API**: Modern API tasarım prensipleri
- **Real-time Data**: USGS'den canlı veri çekme
- **Error Handling**: Kapsamlı hata yönetimi
- **Caching**: Performans optimizasyonu
- **Documentation**: Otomatik Swagger/OpenAPI dokümantasyonu

### 🤖 Sosyal Medya Entegrasyonu (Twitter Bot)
- **Otomatik Paylaşım**: 4.0 ve üzeri depremleri otomatik tweet atar
- **Görsel Oluşturma**: Deprem lokasyonu ve büyüklüğü ile dinamik görsel oluşturur
- **Akıllı Hashtag**: Lokasyona uygun hashtag (#deprem #istanbul vb.) seçimi
- **Rate Limiting**: Spam önlemek için akıllı paylaşım sıklığı yönetimi

## 🛠️ Teknik Özellikler

### Backend Teknolojileri
- **FastAPI 0.104+**: Modern Python web framework
- **Pydantic**: Veri validasyonu ve serialization
- **httpx**: Asenkron HTTP client
- **Docker**: Containerization
- **Python 3.11+**: Modern Python özellikleri

### Reverse Proxy
- **Caddy 2.8+**: Modern web server
- **Automatic HTTPS**: SSL/TLS otomatik yönetimi
- **Static File Serving**: Frontend dosya servisi
- **Security Headers**: Güvenlik optimizasyonları

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

## 📁 Proje Yapısı

```
anlikdeprem/
├── 📁 app/                         # FastAPI uygulaması
│   ├── 📄 main.py                 # Ana FastAPI uygulaması
│   └── 📁 api/                    # API modülleri
├── 📁 public/                     # Frontend dosyaları (Caddy tarafından servis edilir)
│   ├── 📄 index.html              # Ana sayfa
│   ├── 📄 deprem-aninda.html      # Deprem güvenlik rehberi
│   ├── 📄 ilk-yardim-cantasi.html # İlk yardım çantası rehberi
│   ├── 📄 ben-kimim.html          # Hakkımızda sayfası
│   ├── 📄 blog.html               # Blog ana sayfası
│   ├── 📄 blog-*.html             # Blog yazıları
│   ├── 📄 kullanim-sartlari.html  # Kullanım şartları
│   ├── 📄 gizlilik-politikasi.html # Gizlilik politikası
│   ├── 📄 cerez-politikasi.html   # Çerez politikası
│   ├── 📄 sorumluluk-reddi.html   # Sorumluluk reddi
│   ├── 📄 site.webmanifest        # PWA manifest
│   ├── 📁 css/                    # Stil dosyaları
│   │   ├── 📄 style.css           # Ana stil dosyası
│   │   ├── 📄 style-optimized.css # Optimize edilmiş stiller
│   │   ├── 📄 variables.css       # CSS değişkenleri
│   │   ├── 📄 base.css            # Temel stiller
│   │   ├── 📄 components.css      # Bileşen stilleri
│   │   ├── 📄 header.css          # Header stilleri
│   │   ├── 📄 ben-kimim.css       # Hakkımızda stilleri
│   │   ├── 📄 blog.css            # Blog stilleri
│   │   ├── 📄 deprem-aninda.css   # Deprem rehberi stilleri
│   │   └── 📄 ilk-yardim.css      # İlk yardım stilleri
│   ├── 📁 js/                     # JavaScript dosyaları
│   │   ├── 📄 script.js           # Ana JavaScript dosyası
│   │   ├── 📄 main.js             # Giriş noktası
│   │   ├── 📄 header.js           # Header işlevselliği
│   │   ├── 📄 ben-kimim.js        # Hakkımızda işlevselliği
│   │   ├── 📄 deprem-aninda.js    # Deprem rehberi işlevselliği
│   │   └── 📁 core/               # Modüler JavaScript
│   │       ├── 📄 App.js          # Ana uygulama sınıfı
│   │       ├── 📄 DataModule.js   # Veri yönetimi
│   │       ├── 📄 MapModule.js    # Harita işlevselliği
│   │       ├── 📄 StatsModule.js  # İstatistik modülü
│   │       └── 📄 UIModule.js     # UI yönetimi
│   ├── 📁 images/                 # Görsel dosyalar
│   │   ├── 📄 hero-bg.jpg         # Ana sayfa arka planı
│   │   ├── 📄 binaicindeyseniz.webp # Bina içi rehber görseli
│   │   ├── 📄 disaridayken.webp   # Dışarıda rehber görseli
│   │   ├── 📄 arackullarnirken.webp # Araç kullanım rehberi
│   │   └── 📄 depremcantasi.webp  # İlk yardım çantası görseli
│   └── 📁 icons/                  # İkon dosyaları
│       ├── 📄 logo.png            # Ana logo
│       ├── 📄 favicon-*.png       # Favicon dosyaları
│       ├── 📄 apple-touch-icon.png # iOS ikonu
│       └── 📄 android-chrome-*.png # Android ikonları
├── 📄 Dockerfile                  # Docker image tanımı
├── 📄 docker-compose.yml          # Docker Compose konfigürasyonu
├── 📄 docker-compose.production.yml # Production Docker Compose
├── 📄 Caddyfile                   # Caddy reverse proxy konfigürasyonu
├── 📄 Caddyfile.production        # Production Caddy konfigürasyonu
├── 📄 requirements.txt            # Python bağımlılıkları
├── 📄 checklist.pdf               # Proje kontrol listesi
└── 📄 README.md                   # Bu dosya
```

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler
- **Docker** >= 20.10.0
- **Docker Compose** >= 2.0.0
- **Git** (projeyi klonlamak için)

### Local Development

```bash
# Projeyi klonlayın
git clone https://github.com/yakınımdakideprem/yakınımdakideprem.git
cd yakınımdakideprem

# Docker container'ları başlatın
docker compose up -d --build

# Servislerin durumunu kontrol edin
docker compose ps

# Logları izleyin
docker compose logs -f
```

### Production Deployment (HTTPS)

```bash
# Production deployment için
docker-compose -f docker-compose.https.yml up -d

# Veya deployment script'ini kullanın (Linux/Mac)
./deploy.sh
```

### Erişim Adresleri

#### Local Development
- **Ana Sayfa**: http://localhost:8080/
- **API Dokümantasyonu**: http://localhost:8080/docs
- **API Health Check**: http://localhost:8080/health

#### Production (HTTPS)
- **Ana Sayfa**: https://yakinimdakideprem.com/
- **API Dokümantasyonu**: https://yakinimdakideprem.com/docs
- **API Health Check**: https://yakinimdakideprem.com/health
- **API Echo Test**: http://localhost:8080/api/echo?q=merhaba

### Geliştirme Modu

```bash
# Container'ları durdurun
docker compose down

# Geliştirme için yeniden başlatın
docker compose up -d --build

# Logları takip edin
docker compose logs -f api
docker compose logs -f caddy
```

## 🔒 HTTPS ve Production Hazırlık

### ✅ Hazır Özellikler
- **Otomatik SSL**: Let's Encrypt ile otomatik HTTPS
- **Security Headers**: Güvenlik optimizasyonları
- **Rate Limiting**: API koruması
- **Health Checks**: Container sağlık kontrolü
- **Domain Yönlendirme**: www subdomain'den ana domain'e yönlendirme

### 📁 Production Dosyaları
- `Caddyfile.https` - HTTPS yapılandırması
- `docker-compose.https.yml` - Production container yapılandırması
- `env.production` - Production environment variables
- `deploy.sh` - Otomatik deployment script'i

### 🌐 Domain Yapılandırması
1. **DNS Ayarları**: Domain'inizi sunucu IP'sine yönlendirin
2. **Domain Güncelleme**: `Caddyfile.https` dosyasında domain'i güncelleyin
3. **Email Ayarları**: SSL sertifika için email adresini güncelleyin
4. **Firewall**: 80 ve 443 portlarını açın

### 🚀 Production Deployment Adımları
```bash
# 1. Domain'i güncelleyin
nano Caddyfile.https

# 2. Email adresini güncelleyin
nano env.production

# 3. Production deployment'ı başlatın
docker-compose -f docker-compose.https.yml up -d

# 4. SSL sertifikasını kontrol edin
docker exec yakinimdakideprem-caddy caddy list-certificates
```

### 🔧 Production Yönetimi
```bash
# Logları görüntüle
docker-compose -f docker-compose.https.yml logs -f

# Container'ları yeniden başlat
docker-compose -f docker-compose.https.yml restart

# Container'ları durdur
docker-compose -f docker-compose.https.yml down

# SSL sertifikalarını yenile
docker exec yakinimdakideprem-caddy caddy reload
```

## 🌐 API Endpoints

### **GET /health**
Sistem sağlık durumu
```json
{
  "status": "ok",
  "env": "dev",
  "service": "yakınımdakideprem-api"
}
```

### **GET /version**
Uygulama versiyonu
```json
{
  "version": "0.1.0"
}
```

### **GET /api/echo**
Echo test endpoint'i
```json
{
  "echo": "merhaba"
}
```

### **GET /api/earthquakes**
Deprem verilerini getir

**Query Parameters:**
- `hours_back` (int): Son kaç saatlik veriler (default: 168)
- `min_magnitude` (float): Minimum büyüklük (default: 1.0)
- `max_radius` (int): Maksimum yarıçap km (default: 5000)
- `limit` (int): Maksimum sonuç sayısı (default: 200)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "usgs_id",
      "magnitude": 4.5,
      "location": "40 km W of Asadābād, Afghanistan",
      "time": "2025-09-05T17:25:51",
      "coordinates": {
        "lat": 34.8,
        "lng": 70.2
      },
      "depth": 10.0,
      "source": "USGS"
    }
  ],
  "last_update": "2025-09-05T18:00:00",
  "total_count": 25
}
```

### **GET /api/earthquakes/stats**
Deprem istatistikleri

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_earthquakes": 15,
    "max_magnitude": 5.6,
    "min_magnitude": 2.5,
    "avg_magnitude": 4.2,
    "magnitude_3_plus": 12,
    "magnitude_4_plus": 8,
    "magnitude_5_plus": 2,
    "last_update": "2025-09-05T18:00:00"
  }
}
```

## 🔧 Konfigürasyon

### Environment Variables (.env)

```bash
# Uygulama Bilgileri
APP_NAME=yakınımdakideprem-api
APP_ENV=dev
APP_VERSION=0.1.0
PORT=8001

# CORS Ayarları
CORS_ORIGINS=http://localhost:8080,http://localhost:3000

# SSL Ayarları (opsiyonel)
# DOMAIN=yourdomain.com
# ACME_EMAIL=your-email@example.com
```

### Caddy Konfigürasyonu

```caddy
{
    auto_https off  # Geliştirme için HTTP-only
}

:8080 {
    encode zstd gzip
    
    # API rotaları
    @api path /api/* /health /version
    handle @api {
        reverse_proxy api:8000
    }
    
    # API dokümantasyonu
    @apidocs path /docs* /openapi.json /redoc*
    handle @apidocs {
        reverse_proxy api:8000
    }
    
    # Frontend statik dosyalar
    handle {
        root * /srv
        try_files {path} /index.html
        file_server
    }
    
    # Güvenlik başlıkları
    header {
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Referrer-Policy "strict-origin-when-cross-origin"
        Permissions-Policy "geolocation=(), microphone=()"
        Cache-Control "public, max-age=3600"
    }
}
```

## 🐳 Docker Yapılandırması

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml
```yaml
services:
  api:
    build: .
    container_name: yakınımdakideprem-api
    env_file: .env
    environment:
      - PORT=${PORT:-8000}
    expose:
      - "8000"
    restart: unless-stopped

  caddy:
    image: caddy:2.8
    container_name: yakınımdakideprem-caddy
    depends_on:
      - api
    ports:
      - "8080:8080"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config
      - ./public:/srv
    restart: unless-stopped

volumes:
  caddy_data:
  caddy_config:
```

## 📊 Performans ve Ölçeklenebilirlik

### Backend Performansı
- **FastAPI**: Yüksek performanslı async framework
- **httpx**: Asenkron HTTP client
- **Pydantic**: Hızlı veri validasyonu
- **Docker**: Kaynak optimizasyonu

### Frontend Performansı
- **WebP Görseller**: %30 daha küçük dosya boyutları
- **CSS/JS Minification**: Optimize edilmiş dosyalar
- **Lazy Loading**: İhtiyaç duyulduğunda yükleme
- **Service Worker**: Offline çalışma

### Ölçeklenebilirlik
- **Docker Compose**: Kolay horizontal scaling
- **Caddy Load Balancing**: Çoklu backend instance desteği
- **Environment Variables**: Farklı ortamlar için konfigürasyon
- **Health Checks**: Otomatik sağlık kontrolü

## 🔒 Güvenlik

### Backend Güvenliği
- **CORS Middleware**: Cross-origin istek kontrolü
- **Input Validation**: Pydantic ile veri doğrulama
- **Error Handling**: Güvenli hata yönetimi
- **Rate Limiting**: API istek sınırlaması (gelecek özellik)

### Frontend Güvenliği
- **Content Security Policy**: XSS koruması
- **HTTPS Only**: Güvenli bağlantı zorunluluğu
- **Security Headers**: Caddy ile güvenlik başlıkları
- **Input Sanitization**: Kullanıcı girdisi temizleme

## 🧪 Test ve Kalite

### Backend Testleri
```bash
# API testleri
curl http://localhost:8080/health
curl http://localhost:8080/api/echo?q=test
curl http://localhost:8080/api/earthquakes

# Container logları
docker compose logs api
```

### Frontend Testleri
- **Lighthouse**: Performans, erişilebilirlik, SEO
- **Cross-browser**: Chrome, Firefox, Safari, Edge
- **Mobile Testing**: iOS Safari, Android Chrome
- **Responsive**: 320px - 1920px arası tüm boyutlar

## 📈 Monitoring ve Logging

### Container Monitoring
```bash
# Container durumu
docker compose ps

# Resource kullanımı
docker stats

# Log takibi
docker compose logs -f
```

### API Monitoring
- **Health Endpoint**: `/health` ile sistem durumu
- **Version Endpoint**: `/version` ile uygulama versiyonu
- **Error Logging**: Console ve Docker logları
- **Performance Metrics**: Response time ve throughput

## 🚀 Deployment

### Production Deployment

1. **Environment Variables**:
```bash
APP_ENV=production
CORS_ORIGINS=https://yourdomain.com
DOMAIN=yourdomain.com
ACME_EMAIL=your-email@example.com
```

2. **SSL Configuration**:
```caddy
yourdomain.com {
    encode zstd gzip
    
    @api path /api/* /health /version
    handle @api {
        reverse_proxy api:8000
    }
    
    @apidocs path /docs* /openapi.json /redoc*
    handle @apidocs {
        reverse_proxy api:8000
    }
    
    handle {
        root * /srv
        try_files {path} /index.html
        file_server
    }
}
```

3. **Deploy**:
```bash
docker compose up -d --build
```

### Cloud Deployment

- **AWS ECS**: Container orchestration
- **Google Cloud Run**: Serverless containers
- **Azure Container Instances**: Managed containers
- **DigitalOcean App Platform**: Simple deployment

## 🤝 Katkıda Bulunma

### Geliştirme Süreci
1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

### Kod Standartları
- **Python**: PEP 8, Black formatter
- **JavaScript**: ESLint, Prettier
- **Docker**: Multi-stage builds, security best practices
- **Git**: Conventional commits, semantic versioning

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📞 İletişim

- **Website**: [yakınımdakideprem.com](https://yakınımdakideprem.com)
- **Email**: info@yakınımdakideprem.com
- **GitHub**: [@yakınımdakideprem](https://github.com/yakınımdakideprem)

## 🙏 Teşekkürler

- **USGS**: Deprem verileri için
- **AFAD**: Türkiye deprem bilgileri için
- **FastAPI**: Modern Python web framework için
- **Caddy**: Modern web server için
- **Leaflet**: Harita kütüphanesi için
- **Docker**: Containerization için
- **Tüm Katkıda Bulunanlar**: Açık kaynak topluluğu

---

**⚠️ Önemli Not**: Bu platform eğitim ve bilgilendirme amaçlıdır. Acil durumlarda her zaman resmi kurumları (112, AFAD) arayın.

**🌍 Yakınımdaki Deprem** - Full-Stack Teknoloji ile Toplumu Geliştirmek İçin Çabalayan Bir Girişim