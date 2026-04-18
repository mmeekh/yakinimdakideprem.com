# Güvenlik

Yakınımdaki Deprem için uygulanan güvenlik katmanları ve sorumlu ifşa süreci.

## Uygulanan Güvenlik Katmanları

### Edge / Caddy Reverse Proxy
- **HSTS** `max-age=31536000; includeSubDomains; preload`
- **CSP (Content-Security-Policy)** — beyaz liste: sadece `self` + açıkça izin verilen 3. parti (Google Analytics, OneSignal, OpenStreetMap)
- **Cross-Origin-Opener-Policy** `same-origin`
- **Cross-Origin-Resource-Policy** `same-site`
- **X-Frame-Options** `DENY` (clickjacking koruması)
- **X-Content-Type-Options** `nosniff`
- **Referrer-Policy** `strict-origin-when-cross-origin`
- **Permissions-Policy** — kamera, mikrofon, ödeme, USB, midi, sensör vs. **kapalı**; sadece `geolocation=(self)` ve `fullscreen=(self)` açık.
- **X-Permitted-Cross-Domain-Policies** `none` (eski Flash/Silverlight için)
- **Server header'ı kaldırıldı** (teknoloji fingerprinting azaltımı)
- **Request body limit** 10 MB
- **Bloklu path'ler (404):**
  - `/docs`, `/openapi.json`, `/redoc` — production'da Swagger UI kapalı
  - `/.git*`, `/.env*`, `/.htaccess`, `/.DS_Store` — dotfile expose engeli
  - `/wp-admin*`, `/wp-login*`, `/phpmyadmin*`, `/admin*` — tarayıcı bot tuzakları
- **Cloudflare** önünde çalışıyor (DDoS + WAF + rate limit edge'de)

### Uygulama / FastAPI
- **Production'da `/docs`, `/redoc`, `/openapi.json` kapalı** (defense-in-depth)
- **TrustedHostMiddleware** — sadece `yakinimdakideprem.com`, `www.yakinimdakideprem.com`, `yakinimdakideprem-api` (container DNS) kabul edilir
- **CORSMiddleware** — `allow_origins` sadece prod domain; `allow_methods` sadece GET/HEAD/OPTIONS (read-only API)
- **Cache** — in-memory 20 sn cache ile Kandilli rate-limit'ine saygı

### Container / Docker
- **Non-root user** (uid 10001, `app`) — tüm API ve Twitter bot container'ları
- **Tini** init ile proper signal handling ve zombie reaping
- **Static server** `/srv` read-only mount (`:ro`)
- **Minimal base** `python:3.12-slim` + `apt-get upgrade` build zamanında

### Secrets / Gizli Bilgi Yönetimi
- `env.production` **git'ten tamamen çıkarıldı** (history dahil, `git-filter-repo`)
- `env.production.example` — gerçek değerler yerine `REPLACE_ME` placeholder
- `secrets/ga-sa.json` mode **600**, sadece root erişebilir
- `.gitignore`'da `env.production`, `secrets/`, `reports/`, `*.bak`
- `SECRET_KEY` 64 karakter random (`python3 -c "import secrets; print(secrets.token_urlsafe(64))"`)

### Bağımlılıklar
- FastAPI `0.115.x`, Starlette `0.46.x` (CVE-2024-47874 multipart DoS fix)
- Pillow `11.x`, Uvicorn `0.32.x`, Tweepy `4.15.x`, httpx `0.28.x`
- Build zamanında `apt-get upgrade -y` (baseline OS CVE'leri)

## Gizli Bilgi Sızıntısı Olduğunda

Eğer bir secret (API key, access token, vs.) commit'lenirse:

```bash
# 1. ANINDA Twitter/Google Developer portal'dan REVOKE et
# 2. Yeni key üret
# 3. env.production'da güncelle (LOCAL, commit etme)
# 4. git history'den tamamen temizle:
pip3 install --break-system-packages git-filter-repo
git-filter-repo --path env.production --invert-paths --force
git remote add origin git@github.com:USER/REPO.git
git push origin --force --all

# 5. GitHub admin panelde "Push protection" aktif et
```

## Raporlama

Güvenlik sorununu sorumlu şekilde bildirmek için:
**emin.kilic@clemta.com**

Public GitHub issue açmadan önce lütfen e-posta ile bildirin.

## Bilinen Kısıtlar

- **CSP `unsafe-inline`** hâlâ gerekli — Google Tag Manager, OneSignal inline script bootstrap için. Nonce-based CSP'ye geçiş gelecek sprintte.
- **Rate limiting** edge'de Cloudflare tarafında; origin Caddy'de plugin eklenmedi.
- **HSTS preload** — [hstspreload.org](https://hstspreload.org/) üzerinden submission bekleniyor (manuel).
