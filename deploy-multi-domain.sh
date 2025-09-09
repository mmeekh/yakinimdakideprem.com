#!/bin/bash

# Multi-Domain Production Deployment Script
# Bu script aynı VPS üzerinde 2 proje çalıştırır:
# 1. pdfislemleri.com (port 2000)
# 2. yakinimdakideprem.com (port 2001)

set -e

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonksiyonlar
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_success() {
    echo -e "${BLUE}[SUCCESS]${NC} $1"
}

echo "🚀 Multi-Domain Production Deployment Başlatılıyor..."
echo ""

# 1. Gerekli dosyaları kontrol et
log_info "Gerekli dosyalar kontrol ediliyor..."

if [ ! -f "Caddyfile.production" ]; then
    log_error "Caddyfile.production bulunamadı!"
    exit 1
fi

if [ ! -f "docker-compose.production.yml" ]; then
    log_error "docker-compose.production.yml bulunamadı!"
    exit 1
fi

log_success "✅ Tüm gerekli dosyalar mevcut"

# 2. Domain kontrolü
log_info "Domain yapılandırması kontrol ediliyor..."

YAKINIMDAKI_DOMAIN=$(grep "yakinimdakideprem.com" Caddyfile.production | head -1)
PDFISLEMLERI_DOMAIN=$(grep "pdfislemleri.com" Caddyfile.production | head -1)

if [ -z "$YAKINIMDAKI_DOMAIN" ]; then
    log_warn "yakinimdakideprem.com domain yapılandırması bulunamadı!"
fi

if [ -z "$PDFISLEMLERI_DOMAIN" ]; then
    log_warn "pdfislemleri.com domain yapılandırması bulunamadı!"
fi

# 3. Docker kontrolü
log_info "Docker kontrol ediliyor..."
if ! command -v docker &> /dev/null; then
    log_error "Docker yüklü değil!"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    log_error "Docker Compose yüklü değil!"
    exit 1
fi

log_success "✅ Docker ve Docker Compose mevcut"

# 4. Mevcut container'ları durdur
log_info "Mevcut yakinimdakideprem container'ları durduruluyor..."
docker-compose -f docker-compose.production.yml down 2>/dev/null || true

# 5. Network çakışmasını önle
log_info "Network çakışması kontrol ediliyor..."
if docker network ls | grep -q "pdfislemleri-network"; then
    log_warn "pdfislemleri-network mevcut. Çakışma olmayacak şekilde yapılandırıldı."
fi

# 6. Yeni image'ları build et
log_info "Yakinimdakideprem Docker image'ları build ediliyor..."
docker-compose -f docker-compose.production.yml build --no-cache

# 7. Container'ları başlat
log_info "Yakinimdakideprem container'ları başlatılıyor..."
docker-compose -f docker-compose.production.yml up -d

# 8. Health check
log_info "Health check yapılıyor..."
sleep 15

# API health check
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    log_success "✅ Yakinimdakideprem API sağlıklı (Port 8001)"
else
    log_warn "⚠️  Yakinimdakideprem API health check başarısız (Port 8001)"
fi

# 9. SSL sertifika durumu kontrol et
log_info "SSL sertifika durumu kontrol ediliyor..."
if docker exec yakinimdakideprem-caddy caddy list-certificates 2>/dev/null | grep -q "yakinimdakideprem.com"; then
    log_success "✅ yakinimdakideprem.com SSL sertifikası mevcut"
else
    log_warn "⚠️  yakinimdakideprem.com SSL sertifikası henüz oluşturulmamış. İlk erişimde otomatik oluşturulacak."
fi

if docker exec yakinimdakideprem-caddy caddy list-certificates 2>/dev/null | grep -q "pdfislemleri.com"; then
    log_success "✅ pdfislemleri.com SSL sertifikası mevcut"
else
    log_warn "⚠️  pdfislemleri.com SSL sertifikası henüz oluşturulmamış. İlk erişimde otomatik oluşturulacak."
fi

# 10. Final kontrol
log_info "Final kontrol yapılıyor..."
if docker ps | grep -q "yakinimdakideprem"; then
    log_success "✅ Yakinimdakideprem container'ları çalışıyor"
else
    log_error "❌ Yakinimdakideprem container'ları çalışmıyor!"
    exit 1
fi

# 11. Port kontrolü
log_info "Port kullanımı kontrol ediliyor..."
if netstat -tulpn 2>/dev/null | grep -q ":80 "; then
    log_success "✅ Port 80 (HTTP) açık"
else
    log_warn "⚠️  Port 80 kullanımda değil"
fi

if netstat -tulpn 2>/dev/null | grep -q ":443 "; then
    log_success "✅ Port 443 (HTTPS) açık"
else
    log_warn "⚠️  Port 443 kullanımda değil"
fi

# 12. Başarı mesajı
echo ""
log_success "🎉 Multi-Domain Deployment başarıyla tamamlandı!"
echo ""
echo "📋 Deployment Bilgileri:"
echo "   • yakinimdakideprem.com: https://yakinimdakideprem.com"
echo "   • pdfislemleri.com: https://pdfislemleri.com"
echo "   • API Endpoints:"
echo "     - https://yakinimdakideprem.com/api/"
echo "     - https://pdfislemleri.com/api/"
echo "   • Health Checks:"
echo "     - https://yakinimdakideprem.com/health"
echo "     - https://pdfislemleri.com/health"
echo ""
echo "🔧 Yönetim Komutları:"
echo "   • Logları görüntüle: docker-compose -f docker-compose.production.yml logs -f"
echo "   • Container'ları durdur: docker-compose -f docker-compose.production.yml down"
echo "   • Container'ları yeniden başlat: docker-compose -f docker-compose.production.yml restart"
echo ""
echo "⚠️  Önemli Notlar:"
echo "   • Her iki domain de aynı Caddy instance'ı kullanıyor"
echo "   • SSL sertifikaları otomatik oluşturulacak"
echo "   • Domain DNS ayarlarınızın sunucunuza yönlendirildiğinden emin olun"
echo "   • Firewall'da 80 ve 443 portlarının açık olduğundan emin olun"
echo ""
