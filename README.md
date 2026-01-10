# 🌍 Yakınımdaki Deprem - Full-Stack Deprem Bilgi Platformu

[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](https://github.com/yakınımdakideprem/yakınımdakideprem)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-compose-blue.svg)](https://docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Caddy](https://img.shields.io/badge/Caddy-2.8+-blue.svg)](https://caddyserver.com/)

Türkiye'nin en kapsamlı **full-stack** deprem bilgi platformu. **FastAPI backend**, **Caddy reverse proxy** ve **modern frontend** ile gerçek zamanlı deprem verileri, interaktif harita ve hayat kurtaran güvenlik rehberleri.

> Bu proje tek kişi tarafından geliştirilmiştir.

## 📣 Otomatik Twitter Paylaşımı
![Twitter otomatik deprem paylaşımı](public/images/twitter%20postu.jpg)

Otomatik tweet sistemi belirlenen eşik üzerindeki depremleri paylaşır; harita görseline büyüklük rozeti ve renkli çerçeve ekler.

## 🏗️ Proje Mimarisi

### **Backend (FastAPI + Docker)**
- **FastAPI**: Modern, hızlı Python web framework
- **Kandilli Rasathanesi API Entegrasyonu**: Gerçek zamanlı deprem verileri
- **Docker Containerization**: Taşınabilir ve ölçeklenebilir deployment
- **CORS Desteği**: Cross-origin istekler için güvenli yapılandırma

### **Reverse Proxy (Caddy)**
- **Caddy Server**: TLS ve modern web server
- **Static File Serving**: Frontend dosyalarını servis etme
- **API Routing**: Backend API'ye yönlendirme
- **Security Headers**: Güvenlik optimizasyonları

### **Frontend (Vanilla JavaScript + Modern CSS)**
- **Responsive Design**: Tüm cihazlarda mükemmel görünüm
- **Interactive Maps**: Leaflet.js ile harita görselleştirme
- **Real-time Updates**: 20 saniyede bir otomatik veri yenileme
- **PWA Manifest**: site.webmanifest ile ikon ve kurulum bilgisi

## 🚀 Özellikler

### 📍 Gerçek Zamanlı Deprem Haritası
- **Kandilli Rasathanesi Verileri**: En güncel deprem kayıtları
- **İnteraktif Leaflet Haritası**: Türkiye odaklı harita görünümü
- **Büyüklük Filtreleme**: 1.0+, 3.0+, 4.0+, 5.0+ depremleri filtreleme
- **Otomatik Güncelleme**: 20 saniyede bir otomatik veri yenileme

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
- **Real-time Data**: Kandilli Rasathanesi verileri
- **Error Handling**: Kapsamlı hata yönetimi
- **Caching**: Performans optimizasyonu
- **Documentation**: Otomatik Swagger/OpenAPI dokümantasyonu

### 🤖 Sosyal Medya Entegrasyonu (Twitter Bot)
- **Otomatik Paylaşım**: Eşik üzeri depremleri otomatik tweet atar
- **Harita Görseli**: Deprem lokasyonu ekran görüntüsü + büyüklüğe göre renkli çerçeve ve "M x.x" rozeti
- **Akıllı Hashtag**: #bugun #deprem #<il> #sondakika formatı
- **Geçmiş Olsun Mesajı**: Depremin olduğu il için otomatik mesaj

## 🛠️ Teknik Özellikler

### Backend Teknolojileri
- **FastAPI 0.104+**: Modern Python web framework
- **Pydantic**: Veri validasyonu ve serialization
- **httpx**: Asenkron HTTP client
- **Docker**: Containerization
- **Python 3.12+**: Modern Python özellikleri

### Reverse Proxy
- **Caddy 2.8+**: Modern web server
- **TLS Yönetimi**: HTTPS sertifika ve yönlendirme yönetimi
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
- **Lazy Loading**: Görsel yükleme optimizasyonu

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
docker compose -f docker-compose.production.yml up -d --build
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
- **API Echo Test**: https://yakinimdakideprem.com/api/echo?q=merhaba

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
- **HTTPS**: Caddy ile TLS (production'da ACME veya `tls internal`)
- **Security Headers**: Güvenlik optimizasyonları
- **Cache Headers**: HTML ve statik dosyalar için Cache-Control
- **Health Checks**: Container sağlık kontrolü
- **Domain Yönlendirme**: www subdomain'den ana domain'e yönlendirme

### 📁 Production Dosyaları
- `Caddyfile.production` - Reverse proxy yapılandırma örneği
- `yakinimdakideprem.com.Caddyfile` - Merkezi Caddy için hazır site dosyası
- `docker-compose.production.yml` - Production container yapılandırması
- `env.production` - Production environment variables

### 🌐 Domain Yapılandırması
1. **DNS Ayarları**: Domain'inizi sunucu IP'sine yönlendirin
2. **Domain Güncelleme**: `Caddyfile.production` veya `yakinimdakideprem.com.Caddyfile` içindeki domain'i güncelleyin
3. **TLS Ayarları**: Gerekirse ACME email tanımlayın veya `tls internal` kullanın
4. **Firewall**: 80 ve 443 portlarını açın

### 🚀 Production Deployment Adımları
```bash
# 1. Domain'i güncelleyin (opsiyonel)
# Merkezi Caddy kullanıyorsanız: /root/caddy/sites/yakinimdakideprem.com.Caddyfile
nano Caddyfile.production

# 2. Production deployment'ı başlatın
docker compose -f docker-compose.production.yml up -d --build
```

### 🔧 Production Yönetimi
```bash
# Logları görüntüle
docker compose -f docker-compose.production.yml logs -f

# Container'ları yeniden başlat
docker compose -f docker-compose.production.yml restart

# Container'ları durdur
docker compose -f docker-compose.production.yml down
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
- `hours_back` (int): Son kaç saatlik veriler (default: 24, min: 1, max: 720)
- `min_magnitude` (float): Minimum büyüklük (default: 2.0)
- `limit` (int): Maksimum sonuç sayısı (default: 100, max: 2000)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "eq_20260110_0713",
      "magnitude": 4.5,
      "location": "Marmara Denizi (İstanbul)",
      "time": "2026-01-10T07:13:00",
      "time_ago": "5 dakika önce",
      "coordinates": {
        "lat": 40.99,
        "lng": 28.95
      },
      "depth": 7.9,
      "source": "Kandilli"
    }
  ],
  "last_update": "2026-01-10T07:15:00",
  "last_update_ago": "2 dakika önce",
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
    "last_update": "2026-01-10T07:15:00",
    "last_update_ago": "2 dakika önce"
  }
}
```

### **GET /api/pdf/first-aid-checklist**
İlk yardım çantası kontrol listesini indirir.

## 🔧 Konfigürasyon

### Environment Variables (.env)

```bash
# API
APP_NAME=yakınımdakideprem-api
APP_ENV=dev
APP_VERSION=0.1.0
CORS_ORIGINS=http://localhost:8080

# Twitter Bot
TWITTER_MIN_MAGNITUDE=3.0
TWITTER_HASHTAGS=#bugun #deprem #sondakika
TWITTER_POLL_INTERVAL=300
TWITTER_HISTORY_FILE=/data/posted_quakes.json
TWITTER_API_KEY=your-api-key
TWITTER_API_SECRET=your-api-secret
TWITTER_ACCESS_TOKEN=your-access-token
TWITTER_ACCESS_TOKEN_SECRET=your-access-token-secret
EARTHQUAKE_API_URL=http://yakinimdakideprem-api:8000/api/earthquakes

# (Opsiyonel) Harita görsel ayarları
TWITTER_MAP_URL=https://staticmap.openstreetmap.de/staticmap.php
TWITTER_MAP_WIDTH=1000
TWITTER_MAP_HEIGHT=560
TWITTER_IMAGE_WIDTH=1200
TWITTER_IMAGE_HEIGHT=675
TWITTER_IMAGE_BORDER=12
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
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app app
COPY checklist.pdf ./

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml
```yaml
services:
  api:
    build: .
    container_name: yakınımdakideprem-api-local
    env_file: .env
    environment:
      - PORT=${PORT:-8000}
      - ENVIRONMENT=development
    ports:
      - "8000:8000"
    volumes:
      - ./:/app
    restart: unless-stopped
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  caddy:
    image: caddy:2.8
    container_name: yakınımdakideprem-caddy-local
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
- **Lazy Loading**: İhtiyaç duyulduğunda yükleme

### Ölçeklenebilirlik
- **Docker Compose**: Servisleri ayrı çalıştırma (api/static/twitter-bot)
- **Caddy Reverse Proxy**: Merkezi yönlendirme ve cache header'ları
- **In-Memory Cache**: API sonuçlarını kısa süreli önbellekleme
- **Health Checks**: API sağlık kontrolü

## 🔒 Güvenlik

### Backend Güvenliği
- **CORS Middleware**: Cross-origin istek kontrolü
- **Input Validation**: Pydantic ile veri doğrulama
- **Error Handling**: Güvenli hata yönetimi

### Frontend Güvenliği
- **HTTPS**: Güvenli bağlantı zorunluluğu
- **Security Headers**: Caddy ile güvenlik başlıkları

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

## 🚀 Deployment

### Production Deployment

1. **Environment Variables**: `env.production` içindeki Twitter anahtarlarını ve eşikleri güncelleyin.
2. **Caddy Konfigürasyonu**: `Caddyfile.production` veya `yakinimdakideprem.com.Caddyfile` içinde domain/TLS ayarlarını yapın.
3. **Deploy**:
```bash
docker compose -f docker-compose.production.yml up -d --build
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

- **Kandilli Rasathanesi**: Deprem verileri için (API kaynağı: api.orhanaydogdu.com.tr)
- **AFAD**: Acil durum bilgilendirmeleri için
- **FastAPI**: Modern Python web framework için
- **Caddy**: Modern web server için
- **Leaflet**: Harita kütüphanesi için
- **Docker**: Containerization için
- **Tüm Katkıda Bulunanlar**: Açık kaynak topluluğu

---

**⚠️ Önemli Not**: Bu platform eğitim ve bilgilendirme amaçlıdır. Acil durumlarda her zaman resmi kurumları (112, AFAD) arayın.

**🌍 Yakınımdaki Deprem** - Full-Stack Teknoloji ile Toplumu Geliştirmek İçin Çabalayan Bir Girişim
