#!/bin/bash

# Production Deployment Script for Yakınımdaki Deprem
# Bu script HTTPS ile production deployment yapar

set -e

echo "🚀 Yakınımdaki Deprem Production Deployment Başlatılıyor..."

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# 1. Gerekli dosyaları kontrol et
log_info "Gerekli dosyalar kontrol ediliyor..."
if [ ! -f "Caddyfile.https" ]; then
    log_error "Caddyfile.https bulunamadı!"
    exit 1
fi

if [ ! -f "docker-compose.https.yml" ]; then
    log_error "docker-compose.https.yml bulunamadı!"
    exit 1
fi

if [ ! -f "env.production" ]; then
    log_error "env.production bulunamadı!"
    exit 1
fi

log_info "✅ Tüm gerekli dosyalar mevcut"

# 2. Domain kontrolü
log_info "Domain yapılandırması kontrol ediliyor..."
DOMAIN=$(grep "yakinimdakideprem.com" Caddyfile.https | head -1)
if [ -z "$DOMAIN" ]; then
    log_warn "Domain yapılandırması bulunamadı. Lütfen Caddyfile.https dosyasını kontrol edin."
fi

# 3. Docker ve Docker Compose kontrolü
log_info "Docker kontrol ediliyor..."
if ! command -v docker &> /dev/null; then
    log_error "Docker yüklü değil!"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    log_error "Docker Compose yüklü değil!"
    exit 1
fi

log_info "✅ Docker ve Docker Compose mevcut"

# 4. Mevcut container'ları durdur
log_info "Mevcut container'lar durduruluyor..."
docker-compose -f docker-compose.https.yml down 2>/dev/null || true

# 5. Yeni image'ları build et
log_info "Docker image'ları build ediliyor..."
docker-compose -f docker-compose.https.yml build --no-cache

# 6. Container'ları başlat
log_info "Container'lar başlatılıyor..."
docker-compose -f docker-compose.https.yml up -d

# 7. Health check
log_info "Health check yapılıyor..."
sleep 10

# API health check
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    log_info "✅ API sağlıklı"
else
    log_warn "⚠️  API health check başarısız"
fi

# 8. SSL sertifika durumu kontrol et
log_info "SSL sertifika durumu kontrol ediliyor..."
if docker exec yakinimdakideprem-caddy caddy list-certificates 2>/dev/null | grep -q "yakinimdakideprem.com"; then
    log_info "✅ SSL sertifikası mevcut"
else
    log_warn "⚠️  SSL sertifikası henüz oluşturulmamış. İlk erişimde otomatik oluşturulacak."
fi

# 9. Final kontrol
log_info "Final kontrol yapılıyor..."
if docker ps | grep -q "yakinimdakideprem"; then
    log_info "✅ Container'lar çalışıyor"
else
    log_error "❌ Container'lar çalışmıyor!"
    exit 1
fi

# 10. Başarı mesajı
echo ""
log_info "🎉 Deployment başarıyla tamamlandı!"
echo ""
echo "📋 Deployment Bilgileri:"
echo "   • Domain: https://yakinimdakideprem.com"
echo "   • API: https://yakinimdakideprem.com/api/"
echo "   • Docs: https://yakinimdakideprem.com/docs"
echo "   • Status: https://yakinimdakideprem.com/health"
echo ""
echo "🔧 Yönetim Komutları:"
echo "   • Logları görüntüle: docker-compose -f docker-compose.https.yml logs -f"
echo "   • Container'ları durdur: docker-compose -f docker-compose.https.yml down"
echo "   • Container'ları yeniden başlat: docker-compose -f docker-compose.https.yml restart"
echo ""
echo "⚠️  Önemli Notlar:"
echo "   • İlk erişimde SSL sertifikası otomatik oluşturulacak"
echo "   • Domain DNS ayarlarınızın sunucunuza yönlendirildiğinden emin olun"
echo "   • Firewall'da 80 ve 443 portlarının açık olduğundan emin olun"
echo ""
