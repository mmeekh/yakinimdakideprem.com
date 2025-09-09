# 🌐 Multi-Domain Production Deployment

## 📋 Genel Bakış

Bu yapılandırma aynı VPS üzerinde 2 proje çalıştırmanızı sağlar:

1. **pdfislemleri.com** → FastAPI backend (port 8000)
2. **yakinimdakideprem.com** → FastAPI backend (port 8001)

## 🏗️ Mimari

```
VPS (Single Server)
├── Caddy (Port 80/443)
│   ├── pdfislemleri.com → pdfislemleri-api:8000
│   └── yakinimdakideprem.com → yakinimdakideprem-api:8001
├── pdfislemleri-api (Port 8000)
└── yakinimdakideprem-api (Port 8001)
```

## 📁 Dosya Yapısı

### Yakinimdakideprem.com Projesi
```
yakinimdakideprem.com/
├── docker-compose.production.yml
├── Caddyfile.production
├── deploy-multi-domain.sh
└── public/
    └── (static files)
```

### Pdfislemleri.com Projesi (Zaten Kurulu)
```
pdfislemleri.com/
├── docker-compose.production.yml
├── Caddyfile.production
└── public/
    └── (static files)
```

## 🔧 Yapılandırma Detayları

### 1. Docker Compose (yakinimdakideprem.com)

```yaml
services:
  api:
    container_name: yakinimdakideprem-api
    expose:
      - "8000"
    networks:
      - yakinimdakideprem-network

  caddy:
    container_name: yakinimdakideprem-caddy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile.production:/etc/caddy/Caddyfile
      - ./public:/srv
    networks:
      - yakinimdakideprem-network

networks:
  yakinimdakideprem-network:
    name: yakinimdakideprem-network
```

### 2. Caddyfile.production (Multi-Domain)

```caddy
# yakinimdakideprem.com domain bloğu
yakinimdakideprem.com {
    @api path /api/* /health /version
    handle @api {
        reverse_proxy yakinimdakideprem-api:8000
    }
    
    handle {
        root * /srv
        try_files {path} /index.html
        file_server
    }
}

# pdfislemleri.com domain bloğu
pdfislemleri.com {
    @api path /api/* /health /version
    handle @api {
        reverse_proxy pdfislemleri-api:8000
    }
    
    handle {
        root * /srv
        try_files {path} /index.html
        file_server
    }
}
```

## 🚀 Deployment Adımları

### 1. Yakinimdakideprem.com Kurulumu

```bash
# Proje dizinine gidin
cd yakinimdakideprem.com

# Deployment script'ini çalıştırın
chmod +x deploy-multi-domain.sh
./deploy-multi-domain.sh
```

### 2. Manuel Deployment

```bash
# Container'ları başlatın
docker-compose -f docker-compose.production.yml up -d

# Logları kontrol edin
docker-compose -f docker-compose.production.yml logs -f
```

## 🔍 Test ve Doğrulama

### 1. Domain Erişimi
```bash
# HTTPS erişimini test edin
curl -I https://yakinimdakideprem.com
curl -I https://pdfislemleri.com
```

### 2. API Endpoints
```bash
# API health check
curl https://yakinimdakideprem.com/health
curl https://pdfislemleri.com/health

# API endpoints
curl https://yakinimdakideprem.com/api/earthquakes
curl https://pdfislemleri.com/api/your-endpoint
```

### 3. SSL Sertifikaları
```bash
# SSL sertifikalarını kontrol edin
docker exec yakinimdakideprem-caddy caddy list-certificates
```

## ⚠️ Önemli Notlar

### 🔒 Güvenlik
- Her iki domain de aynı Caddy instance'ı kullanıyor
- SSL sertifikaları otomatik oluşturuluyor
- Security headers her iki domain için aktif

### 🌐 Network Yapılandırması
- Her proje kendi Docker network'üne sahip
- Container isimleri farklı (çakışma yok)
- Caddy, container isimleriyle iletişim kuruyor

### 📊 Monitoring
- Her iki proje için ayrı health check
- Ayrı log dosyaları
- Ayrı container yönetimi

## 🔧 Yönetim Komutları

### Container Yönetimi
```bash
# Yakinimdakideprem container'ları
docker-compose -f docker-compose.production.yml ps
docker-compose -f docker-compose.production.yml logs -f
docker-compose -f docker-compose.production.yml restart

# Pdfislemleri container'ları (kendi dizininde)
cd pdfislemleri.com
docker-compose -f docker-compose.production.yml ps
```

### SSL Yönetimi
```bash
# SSL sertifikalarını yenile
docker exec yakinimdakideprem-caddy caddy reload

# Sertifika durumunu kontrol et
docker exec yakinimdakideprem-caddy caddy list-certificates
```

## 🎯 Sonuç

Bu yapılandırma ile:
- ✅ 2 farklı domain aynı VPS'te çalışıyor
- ✅ Her domain kendi API'sine sahip
- ✅ Otomatik SSL sertifikaları
- ✅ Güvenlik optimizasyonları
- ✅ Kolay yönetim ve monitoring

**Multi-domain deployment başarıyla tamamlandı!** 🎉
