# Yakınımdaki Deprem

Türkiye için gerçek zamanlı deprem haritası ve güvenlik rehberleri. FastAPI API + statik frontend + Docker ile çalışır.

> Bu proje tek kişi tarafından geliştirilmiştir.

## Öne çıkanlar
- Kandilli/AFAD verileriyle canlı deprem listesi ve harita
- Büyüklük filtreleri, son depremler, istatistikler
- Deprem güvenlik rehberleri ve blog içerikleri
- Otomatik X (Twitter) botu: harita görseli + etiket + geçmiş olsun mesajı

## Mimari
- `app/`: FastAPI backend
- `public/`: statik frontend (Caddy tarafından servis edilir)
- `docker-compose.production.yml`: production kurulum
- `Caddyfile.production`: reverse proxy + statik içerik

## Hızlı kurulum (Docker)
```bash
docker compose up -d --build
```

## Production
```bash
docker compose -f docker-compose.production.yml up -d --build
```

## Sitemap maintenance
Keep `public/sitemap.xml` `lastmod` values aligned with real file updates:
```bash
./scripts/update-sitemap-lastmod.sh
```

## Erişim
- Site: `https://yakinimdakideprem.com/`
- API Docs: `/docs`
- Health: `/health`

## Twitter Bot (özet)
`.env` veya `env.production` içinde:
- `TWITTER_MIN_MAGNITUDE`
- `TWITTER_HASHTAGS`
- `TWITTER_POLL_INTERVAL`
- `TWITTER_*` anahtarları
