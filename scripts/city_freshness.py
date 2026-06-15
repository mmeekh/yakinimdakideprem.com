#!/usr/bin/env python3
"""
city_freshness.py — Continuous worker.

Her 60 saniyede bir API'dan son depremleri çeker, 3.5+ büyüklükteki
depremin geçtiği şehir sayfasının statik HTML'ini günceller:

  • SSR-FRESHNESS bloğunu LiveBlogPosting schema + visible timestamp
    + "Az önce {büyüklük} deprem" passage ile doldurur (AI crawler'lar
    JS execute etmediği için bu kritik).
  • <title> ve <meta description>'ı freshness sinyali için günceller.
  • sitemap.xml'de o şehir URL'sinin lastmod'unu bumplar.
  • IndexNow API'sine ping atar (Bing/Yandex anlık).

Kullanım:
  INDEXNOW_KEY=xxx python3 scripts/city_freshness.py            # daemon
  python3 scripts/city_freshness.py --once                      # tek tur
  python3 scripts/city_freshness.py --simulate-quake istanbul   # test
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

import requests

# ----------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
ALIASES_FILE = ROOT / "scripts" / "city_aliases.json"
SITEMAP = PUBLIC / "sitemap.xml"

API_URL = os.getenv(
    "FRESHNESS_API_URL",
    "http://yakinimdakideprem-api:8000/api/earthquakes",
)
POLL_SECONDS = int(os.getenv("FRESHNESS_POLL_SECONDS", "60"))
MIN_MAGNITUDE = float(os.getenv("FRESHNESS_MIN_MAGNITUDE", "3.5"))
HOURS_BACK = int(os.getenv("FRESHNESS_HOURS_BACK", "6"))
# Bir SSR "az önce deprem" bloğu bu süreden eskiyse otomatik geri alınır
# (nötr bloğa + standart başlığa döner). Donmuş/sahte freshness'ı önler.
STALE_HOURS = float(os.getenv("FRESHNESS_STALE_HOURS", "12"))
INDEXNOW_KEY = os.getenv("INDEXNOW_KEY", "")
INDEXNOW_HOST = "yakinimdakideprem.com"
TZ_TR = timezone(timedelta(hours=3))

SSR_START = "<!-- SSR-FRESHNESS-START -->"
SSR_END = "<!-- SSR-FRESHNESS-END -->"
SD_START = "<!-- SSR-SONDAKIKA-START -->"
SD_END = "<!-- SSR-SONDAKIKA-END -->"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("freshness")


# ----------------------------------------------------------------------
def normalize(text: str) -> str:
    """Lowercase + strip Turkish diacritics (Kandilli'nin ASCII'sine eşleşir)."""
    if not text:
        return ""
    text = text.lower()
    table = str.maketrans({"ı": "i", "ş": "s", "ç": "c",
                            "ö": "o", "ü": "u", "ğ": "g", "İ": "i"})
    text = text.translate(table)
    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c))


def load_cities() -> dict:
    return json.loads(ALIASES_FILE.read_text(encoding="utf-8"))


def find_city_slug(place: str, cities: dict) -> Optional[str]:
    """Match a Kandilli place string to a city slug via alias longest-match."""
    place_norm = normalize(place)
    best = None
    best_len = 0
    for slug, info in cities.items():
        for alias in info["aliases"]:
            alias_norm = normalize(alias)
            if alias_norm and alias_norm in place_norm and len(alias_norm) > best_len:
                best = slug
                best_len = len(alias_norm)
    return best


def fetch_quakes(min_magnitude: float, hours_back: int, limit: int = 50) -> list:
    params = {"hours_back": hours_back, "min_magnitude": min_magnitude, "limit": limit}
    try:
        r = requests.get(API_URL, params=params, timeout=10)
        r.raise_for_status()
        return r.json().get("data", []) or []
    except Exception as e:
        log.error(f"API fetch failed (m{min_magnitude}/{hours_back}h): {e}")
        return []


def fetch_recent_quakes() -> list:
    return fetch_quakes(MIN_MAGNITUDE, HOURS_BACK, 50)


def parse_quake_time(raw: str) -> datetime:
    """Kandilli '2026.05.05 14:32:00' → tz-aware datetime."""
    if not raw:
        return datetime.now(TZ_TR)
    raw = raw.replace(".", "-").strip()
    try:
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=TZ_TR)
        return dt
    except ValueError:
        return datetime.now(TZ_TR)


def humanize_minutes_ago(dt: datetime) -> str:
    delta = datetime.now(TZ_TR) - dt
    minutes = int(delta.total_seconds() // 60)
    if minutes < 1:
        return "Az önce"
    if minutes < 60:
        return f"{minutes} dakika önce"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} saat önce"
    return f"{hours // 24} gün önce"


# ----------------------------------------------------------------------
def build_ssr_block(slug: str, city_name: str, quake: dict) -> str:
    mag = float(quake.get("magnitude", 0) or 0)
    place = quake.get("location") or quake.get("place") or "Bilinmeyen"
    # Derinlik fallback: boş/None değer "km" göstermesin
    depth_raw = quake.get("depth", "")
    if depth_raw in (None, "", 0, "0"):
        depth_display = "Bilinmiyor"
        depth_text = ""   # passage'da göstermez
    else:
        try:
            depth_display = f"{float(depth_raw):.1f} km"
            depth_text = f" Derinlik: {depth_display}."
        except (TypeError, ValueError):
            depth_display = str(depth_raw)
            depth_text = f" Derinlik: {depth_display}."

    qtime = parse_quake_time(quake.get("time", ""))
    iso = qtime.isoformat()
    iso_now = datetime.now(TZ_TR).isoformat()
    pretty = qtime.strftime("%d %B %Y, %H:%M") + " TSİ"
    ago = humanize_minutes_ago(qtime)

    canonical = f"https://yakinimdakideprem.com/deprem-{slug}.html"
    # liveBlogUpdate item için kalıcı anchor URL
    update_anchor = f"{canonical}#update-{qtime.strftime('%Y%m%dT%H%M%S')}"

    schema = {
        "@context": "https://schema.org",
        "@type": "LiveBlogPosting",
        "@id": f"{canonical}#liveblog",
        "headline": f"{city_name} Deprem Takibi — Canlı",
        "datePublished": iso,
        "dateModified": iso_now,
        "coverageStartTime": iso,
        "url": canonical,
        "image": f"https://yakinimdakideprem.com/images/cities/{slug}-og.webp",
        "about": {"@type": "Place", "name": city_name, "addressCountry": "TR"},
        "author": {
            "@type": "Person",
            "name": "Emin Kılıç",
            "url": "https://yakinimdakideprem.com/ben-kimim.html",
            "@id": "https://yakinimdakideprem.com/ben-kimim.html#person",
        },
        "publisher": {
            "@type": "Organization",
            "name": "Yakınımdaki Deprem",
            "@id": "https://yakinimdakideprem.com/#organization",
            "logo": {
                "@type": "ImageObject",
                "url": "https://yakinimdakideprem.com/icons/android-chrome-512x512.png",
                "width": 512,
                "height": 512,
            },
        },
        "liveBlogUpdate": [{
            "@type": "BlogPosting",
            "@id": update_anchor,
            "url": update_anchor,
            "headline": f"{city_name} {mag:.1f} büyüklüğünde deprem",
            "datePublished": iso,
            "articleBody": (
                f"{ago}, {place} bölgesinde {mag:.1f} büyüklüğünde deprem "
                f"kaydedildi.{depth_text}".strip()
            ),
        }],
    }

    return (
        f"{SSR_START}\n"
        '            <div class="ssr-freshness" itemscope '
        'itemtype="https://schema.org/Event" aria-live="polite">\n'
        f'                <p class="ssr-freshness__alert">'
        f'🔴 <strong>{ago}:</strong> '
        f'<span itemprop="name">{city_name} {mag:.1f} büyüklüğünde deprem</span> — '
        f'<span itemprop="location">{place}</span>'
        f'{f" • Derinlik: {depth_display}" if depth_text else ""}.'
        f'</p>\n'
        f'                <time class="ssr-freshness__time" '
        f'itemprop="startDate" datetime="{iso}">'
        f'Deprem zamanı: {pretty}</time>\n'
        '            </div>\n'
        '            <script type="application/ld+json">\n'
        f'            {json.dumps(schema, ensure_ascii=False, indent=2)}\n'
        '            </script>\n'
        f"            {SSR_END}"
    )


def build_quake_table_rows(quakes_for_city: list) -> str:
    """Şehir tbody'sine yerleştirilecek son 5 deprem HTML satırı."""
    if not quakes_for_city:
        return '<tr><td colspan="4">Bu şehir için kayıtlı son deprem bulunamadı.</td></tr>'

    rows = []
    for q in quakes_for_city[:5]:
        mag = float(q.get("magnitude", 0) or 0)
        place = q.get("location") or q.get("place") or "Bilinmiyor"
        depth = q.get("depth", "?")
        try:
            depth_str = f"{float(depth):.1f} km"
        except (TypeError, ValueError):
            depth_str = "—"
        qtime = parse_quake_time(q.get("time", ""))
        time_str = qtime.strftime("%d.%m.%Y %H:%M")
        rows.append(
            f'<tr><td>{time_str}</td>'
            f'<td><strong>M{mag:.1f}</strong></td>'
            f'<td>{depth_str}</td>'
            f'<td>{place}</td></tr>'
        )
    return "\n                                ".join(rows)


def update_city_page(slug: str, city_name: str, quake: dict,
                       quakes_for_city: list = None) -> bool:
    page = PUBLIC / f"deprem-{slug}.html"
    if not page.exists():
        return False

    html = page.read_text(encoding="utf-8")
    if SSR_START not in html:
        log.warning(f"{slug}: SSR placeholder yok, atlanıyor")
        return False

    # Replace the SSR block
    new_block = build_ssr_block(slug, city_name, quake)
    new_html = re.sub(
        re.escape(SSR_START) + r".*?" + re.escape(SSR_END),
        new_block,
        html,
        count=1,
        flags=re.DOTALL,
    )

    # SSR quake table: AI crawler'lar için tbody içine son 5 deprem inject et.
    # JS yine renderCityQuakes ile dinamik update yapar; bu sadece initial render.
    if quakes_for_city:
        rows_html = build_quake_table_rows(quakes_for_city)
        new_html = re.sub(
            r'(<tbody id="' + re.escape(slug) + r'-quakes">)\s*'
            r'(?:<tr><td colspan="4">[^<]+</td></tr>|.*?)\s*(</tbody>)',
            rf'\1\n                                {rows_html}\n                            \2',
            new_html,
            count=1,
            flags=re.DOTALL,
        )

    # Title freshness: SADECE M4.0+ depremlerde dinamik title. Aksi halde
    # standart CTR-optimize başlık. Bu, küçük (M1-2) depremlerin SERP'te
    # sayfa başlığını kötüleştirmesini önler.
    mag = float(quake.get("magnitude", 0) or 0)
    if mag >= 4.0:
        new_title = (
            f"🔴 {city_name}'da Az Önce {mag:.1f} Deprem | Anlık Deprem Takibi"
        )
    else:
        # Standart CTR-optimize başlık (deprem aktif değilse)
        new_title = default_city_title(city_name)
    new_html = re.sub(
        r"<title>[^<]+</title>",
        f"<title>{new_title}</title>",
        new_html,
        count=1,
    )

    if new_html == html:
        return False

    # Atomic write
    tmp = page.with_suffix(".html.tmp")
    tmp.write_text(new_html, encoding="utf-8")
    tmp.replace(page)
    return True


def default_city_title(city_name: str) -> str:
    """Deprem aktif değilken kullanılan nötr, doğru başlık."""
    return f"Anlık Deprem {city_name} 🔴 Canlı Harita ve Son Depremler"


_BLOCK_TIME_RE = re.compile(r'itemprop="startDate"\s+datetime="([^"]+)"')


def current_block_age_hours(html: str) -> Optional[float]:
    """SSR bloğunda gösterilen depremin kaç saat önce olduğunu döndürür.
    Blok nötrse (startDate yok) veya parse edilemezse None."""
    m = re.search(re.escape(SSR_START) + r".*?" + re.escape(SSR_END),
                  html, flags=re.DOTALL)
    if not m:
        return None
    tm = _BLOCK_TIME_RE.search(m.group(0))
    if not tm:
        return None
    try:
        dt = datetime.fromisoformat(tm.group(1))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=TZ_TR)
    return (datetime.now(TZ_TR) - dt).total_seconds() / 3600.0


def build_neutral_block(city_name: str) -> str:
    """Aktif deprem yokken gösterilecek dürüst, sakin blok.
    Yanlış 'az önce deprem' iddiası içermez (E-E-A-T / YMYL güvenliği)."""
    iso_now = datetime.now(TZ_TR).isoformat()
    pretty = datetime.now(TZ_TR).strftime("%d.%m.%Y %H:%M") + " TSİ"
    return (
        f"{SSR_START}\n"
        '            <div class="ssr-freshness ssr-freshness--calm" aria-live="polite">\n'
        f'                <p class="ssr-freshness__alert">🟢 '
        f'<strong>{city_name}:</strong> Şu anda bölgede yeni bir önemli '
        f'deprem (M{MIN_MAGNITUDE:.1f}+) bildirimi yok. Tüm son depremler için '
        f'aşağıdaki canlı haritayı inceleyebilirsiniz.</p>\n'
        f'                <time class="ssr-freshness__time" datetime="{iso_now}">'
        f'Son güncelleme: {pretty}</time>\n'
        '            </div>\n'
        f"            {SSR_END}"
    )


def revert_city_page(slug: str, city_name: str) -> bool:
    """STALE_HOURS'tan eski 'az önce deprem' bloğunu nötrle + başlığı geri al.
    Donmuş/sahte freshness'ı (örn. TEST verisi, haftalarca kalan magnitude) temizler."""
    page = PUBLIC / f"deprem-{slug}.html"
    if not page.exists():
        return False
    html = page.read_text(encoding="utf-8")
    if SSR_START not in html:
        return False
    age = current_block_age_hours(html)
    if age is None or age < STALE_HOURS:
        return False  # zaten nötr veya hâlâ taze — dokunma
    new_block = build_neutral_block(city_name)
    new_html = re.sub(
        re.escape(SSR_START) + r".*?" + re.escape(SSR_END),
        lambda _: new_block,
        html, count=1, flags=re.DOTALL,
    )
    new_html = re.sub(
        r"<title>[^<]+</title>",
        lambda _: f"<title>{default_city_title(city_name)}</title>",
        new_html, count=1,
    )
    if new_html == html:
        return False
    tmp = page.with_suffix(".html.tmp")
    tmp.write_text(new_html, encoding="utf-8")
    tmp.replace(page)
    return True


def update_sitemap(slug: str) -> bool:
    if not SITEMAP.exists():
        return False
    text = SITEMAP.read_text(encoding="utf-8")
    today = datetime.now(TZ_TR).strftime("%Y-%m-%d")
    pattern = re.compile(
        r"(<loc>https://yakinimdakideprem\.com/deprem-"
        + re.escape(slug) + r"\.html</loc>\s*<lastmod>)[^<]+(</lastmod>)"
    )
    new_text, n = pattern.subn(rf"\g<1>{today}\g<2>", text)
    if n > 0 and new_text != text:
        SITEMAP.write_text(new_text, encoding="utf-8")
        return True
    return False


def ping_indexnow(slug: str):
    if not INDEXNOW_KEY:
        return
    url = f"https://yakinimdakideprem.com/deprem-{slug}.html"
    payload = {
        "host": INDEXNOW_HOST,
        "key": INDEXNOW_KEY,
        "urlList": [url, "https://yakinimdakideprem.com/"],
    }
    try:
        r = requests.post("https://api.indexnow.org/indexnow",
                          json=payload, timeout=8)
        log.info(f"IndexNow ping {slug}: HTTP {r.status_code}")
    except Exception as e:
        log.warning(f"IndexNow failed: {e}")


# ----------------------------------------------------------------------
def update_homepage(quakes: list, cities: dict) -> bool:
    """Anasayfaya son 5 önemli depremin statik listesini enjekte et.
    AI crawler'lar JS execute etmediği için bu kritik freshness sinyali."""
    page = PUBLIC / "index.html"
    if not page.exists() or not quakes:
        return False
    html = page.read_text(encoding="utf-8")
    if SSR_START not in html:
        return False

    # Top 5 by time
    items = []
    now_iso = datetime.now(TZ_TR).isoformat()
    for q in quakes[:5]:
        place = q.get("location") or q.get("place") or "Bilinmiyor"
        mag = float(q.get("magnitude", 0) or 0)
        depth = q.get("depth", "?")
        qtime = parse_quake_time(q.get("time", ""))
        ago = humanize_minutes_ago(qtime)
        slug = find_city_slug(place, cities)
        # Yurt dışı / açık deniz merkezleri için şehir sayfası yok → ölü "#" yerine
        # ulusal son-dakika akışına yönlendir (kırık link SEO/UX'i zedeliyordu).
        href = f"/deprem-{slug}.html" if slug else "/son-dakika-deprem.html"
        items.append((mag, place, depth, qtime, ago, href))

    if not items:
        return False

    latest = items[0]
    list_html = "\n".join([
        f'                <li class="hp-fresh__item">'
        f'<a href="{href}"><strong>{place}</strong></a> '
        f'— <span class="hp-fresh__mag">M{mag:.1f}</span> '
        f'<time datetime="{qt.isoformat()}">{ago}</time> '
        f'<span class="hp-fresh__depth">• {depth} km</span></li>'
        for mag, place, depth, qt, ago, href in items
    ])

    schema = {
        "@context": "https://schema.org",
        "@type": "LiveBlogPosting",
        "headline": "Türkiye Anlık Deprem Takibi — Canlı",
        "datePublished": latest[3].isoformat(),
        "dateModified": now_iso,
        "coverageStartTime": latest[3].isoformat(),
        "about": {"@type": "Place", "name": "Türkiye"},
        "author": {"@type": "Organization", "name": "Yakınımdaki Deprem"},
        "publisher": {
            "@type": "Organization",
            "name": "Yakınımdaki Deprem",
            "logo": {
                "@type": "ImageObject",
                "url": "https://yakinimdakideprem.com/icons/android-chrome-512x512.png",
            },
        },
        "liveBlogUpdate": [{
            "@type": "BlogPosting",
            "headline": f"{place} M{mag:.1f}",
            "datePublished": qt.isoformat(),
            "articleBody": f"{ago}, {place} bölgesinde {mag:.1f} büyüklüğünde "
                           f"deprem kaydedildi. Derinlik: {depth} km.",
        } for mag, place, depth, qt, ago, _ in items],
    }

    block = (
        f"{SSR_START}\n"
        '    <section class="ssr-homepage-freshness" aria-live="polite">\n'
        '        <div class="container">\n'
        '            <h2 class="hp-fresh__title">'
        '🔴 Türkiye\'de Son 5 Önemli Deprem</h2>\n'
        '            <ul class="hp-fresh__list">\n'
        f"{list_html}\n"
        '            </ul>\n'
        f'            <p class="hp-fresh__updated">Son güncelleme: '
        f'<time datetime="{now_iso}">'
        f'{datetime.now(TZ_TR).strftime("%d.%m.%Y %H:%M")} TSİ</time></p>\n'
        '        </div>\n'
        '    </section>\n'
        '    <script type="application/ld+json">\n'
        f'    {json.dumps(schema, ensure_ascii=False)}\n'
        '    </script>\n'
        f"    {SSR_END}"
    )

    new_html = re.sub(
        re.escape(SSR_START) + r".*?" + re.escape(SSR_END),
        block,
        html,
        count=1,
        flags=re.DOTALL,
    )
    if new_html == html:
        return False

    tmp = page.with_suffix(".html.tmp")
    tmp.write_text(new_html, encoding="utf-8")
    tmp.replace(page)
    return True


def _sd_table_rows(quakes: list, limit: int) -> str:
    if not quakes:
        return '<tr><td colspan="4">Şu anda görüntülenecek yeni deprem kaydı yok.</td></tr>'
    rows = []
    for q in quakes[:limit]:
        mag = float(q.get("magnitude", 0) or 0)
        place = q.get("location") or q.get("place") or "Bilinmiyor"
        depth = q.get("depth", "?")
        try:
            depth_str = f"{float(depth):.1f} km"
        except (TypeError, ValueError):
            depth_str = "—"
        qt = parse_quake_time(q.get("time", ""))
        rows.append(
            f'<tr><td>{qt.strftime("%d.%m.%Y %H:%M")}</td>'
            f'<td><strong>M{mag:.1f}</strong></td>'
            f'<td>{depth_str}</td><td>{place}</td></tr>'
        )
    return "\n                                ".join(rows)


def update_son_dakika() -> bool:
    """son-dakika-deprem.html'i sunucu-render et: tablolar + canlı kutu + LiveBlogPosting.
    Sayfa %100 client-side'dı; Google boş 'Veriler yükleniyor' indeksliyordu (en yüksek
    hacimli niyet: 'son dakika / az önce deprem'). Sadece yeni deprem geldiğinde yazar."""
    global _LAST_SONDAKIKA
    page = PUBLIC / "son-dakika-deprem.html"
    if not page.exists():
        return False
    # NOT: API min_magnitude parametresini YOK SAYIYOR (M4 istesek de M2 döner),
    # bu yüzden büyüklük filtresini client-side yapıyoruz (run_once'taki şehir
    # döngüsü de aynı sebepten client-side filtreliyor).
    def _mag(q):
        try:
            return float(q.get("magnitude", 0) or 0)
        except (TypeError, ValueError):
            return 0.0
    pool = fetch_quakes(min_magnitude=0, hours_back=24 * 7, limit=100)
    if not pool:
        return False  # API boş/erişilemez → mevcut içeriği SİLME
    pool.sort(key=lambda q: q.get("time", ""), reverse=True)
    latest_list = [q for q in pool if _mag(q) >= 2.0][:20] or pool[:20]
    m4_list = [q for q in pool if _mag(q) >= 4.0][:20]

    top_id = latest_list[0].get("id") or latest_list[0].get("time")
    if top_id == _LAST_SONDAKIKA:
        return False  # yeni deprem yok, yeniden yazma (I/O + IndexNow rate limit)

    html = page.read_text(encoding="utf-8")
    orig = html
    now = datetime.now(TZ_TR)
    now_iso = now.isoformat()
    now_pretty = now.strftime("%d.%m.%Y %H:%M") + " TSİ"

    latest = latest_list[0]
    l_mag = float(latest.get("magnitude", 0) or 0)
    l_place = latest.get("location") or latest.get("place") or "Bilinmiyor"
    l_time = parse_quake_time(latest.get("time", ""))
    l_ago = humanize_minutes_ago(l_time)
    mins = (now - l_time).total_seconds() / 60

    # --- Tablolar (gerçek satırlar) ---
    html = re.sub(
        r'(<tbody id="latest-quakes-table">).*?(</tbody>)',
        lambda m: f'{m.group(1)}\n                                {_sd_table_rows(latest_list, 20)}\n                            {m.group(2)}',
        html, count=1, flags=re.DOTALL,
    )
    html = re.sub(
        r'(<tbody id="m4plus-table">).*?(</tbody>)',
        lambda m: f'{m.group(1)}\n                                {_sd_table_rows(m4_list, 20)}\n                            {m.group(2)}',
        html, count=1, flags=re.DOTALL,
    )

    # --- Canlı kutu: "Az önce deprem oldu mu?" + "Son deprem" ---
    if mins < 60:
        just_now = (f'🔴 <strong>Evet</strong>, {l_ago.lower()}, {l_place} bölgesinde '
                    f'<strong>M{l_mag:.1f}</strong> büyüklüğünde bir deprem kaydedildi.')
    else:
        just_now = (f'Son saatlerde yeni bir büyük deprem kaydedilmedi. En son: '
                    f'{l_ago.lower()}, {l_place} <strong>M{l_mag:.1f}</strong>.')
    html = re.sub(r'(<p id="just-now-info">).*?(</p>)',
                  lambda m: f'{m.group(1)}{just_now}{m.group(2)}',
                  html, count=1, flags=re.DOTALL)
    latest_txt = (f'<strong>{l_place}</strong> — M{l_mag:.1f} • '
                  f'{l_time.strftime("%d.%m.%Y %H:%M")} TSİ ({l_ago})')
    html = re.sub(r'(<p id="latest-quake">).*?(</p>)',
                  lambda m: f'{m.group(1)}{latest_txt}{m.group(2)}',
                  html, count=1, flags=re.DOTALL)
    html = re.sub(r'(<strong id="live-updated">).*?(</strong>)',
                  lambda m: f'{m.group(1)}{now_pretty}{m.group(2)}',
                  html, count=1, flags=re.DOTALL)

    # --- LiveBlogPosting schema (SSR marker arası) ---
    canonical = "https://yakinimdakideprem.com/son-dakika-deprem.html"
    updates = []
    for q in latest_list[:10]:
        mag = float(q.get("magnitude", 0) or 0)
        place = q.get("location") or q.get("place") or "Bilinmiyor"
        qt = parse_quake_time(q.get("time", ""))
        updates.append({
            "@type": "BlogPosting",
            "headline": f"{place} M{mag:.1f} deprem",
            "datePublished": qt.isoformat(),
            "articleBody": (f"{humanize_minutes_ago(qt)}, {place} bölgesinde "
                            f"{mag:.1f} büyüklüğünde deprem kaydedildi."),
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "LiveBlogPosting",
        "@id": f"{canonical}#liveblog",
        "headline": "Son Dakika Deprem — Türkiye Canlı Deprem Takibi",
        "url": canonical,
        "datePublished": l_time.isoformat(),
        "dateModified": now_iso,
        "coverageStartTime": l_time.isoformat(),
        "about": {"@type": "Place", "name": "Türkiye", "addressCountry": "TR"},
        "publisher": {
            "@type": "Organization",
            "name": "Yakınımdaki Deprem",
            "@id": "https://yakinimdakideprem.com/#organization",
            "logo": {"@type": "ImageObject",
                     "url": "https://yakinimdakideprem.com/icons/android-chrome-512x512.png"},
        },
        "liveBlogUpdate": updates,
    }
    schema_block = (
        f'{SD_START}\n'
        '    <script type="application/ld+json">\n'
        f'    {json.dumps(schema, ensure_ascii=False)}\n'
        '    </script>\n'
        f'    {SD_END}'
    )
    if SD_START in html:
        html = re.sub(re.escape(SD_START) + r".*?" + re.escape(SD_END),
                      lambda _: schema_block, html, count=1, flags=re.DOTALL)
    else:
        html = html.replace("</head>", schema_block + "\n</head>", 1)

    # --- Dinamik title (en son deprem çok taze ise) ---
    if l_mag >= 3.0 and mins < 30:
        new_title = f"🔴 {l_place} {l_mag:.1f} Deprem ({l_ago}) | Son Dakika Deprem"
    else:
        new_title = "🔴 Son Dakika Deprem | Az Önce Deprem Oldu Mu? Canlı Liste"
    html = re.sub(r"<title>[^<]*</title>",
                  lambda _: f"<title>{new_title}</title>", html, count=1)

    if html == orig:
        return False
    tmp = page.with_suffix(".html.tmp")
    tmp.write_text(html, encoding="utf-8")
    tmp.replace(page)
    _LAST_SONDAKIKA = top_id
    return True


# Deduplication state — process'in hayatı boyunca aynı (slug, quake_id) tekrar
# yazılmasın (gereksiz disk I/O + IndexNow rate limit'ten kaçın).
_LAST_WRITTEN: dict[str, str] = {}   # slug → last quake_id
_LAST_HOMEPAGE: tuple = None         # (top_quake_id, ...) tuple of latest 5 ids
_LAST_SONDAKIKA = None               # son-dakika sayfasındaki en yeni deprem id'si


def run_once(cities: dict) -> int:
    """One pass: process the most recent quake per city + update homepage.
    Deduplication: aynı deprem ID'si tekrar yazılmaz."""
    global _LAST_HOMEPAGE
    quakes = fetch_recent_quakes()
    # NOT: API boş dönse bile aşağıdaki revert-pass çalışır (bayat blokları
    # temizlemek API'ye bağlı değil), bu yüzden erken return yok.
    quakes.sort(key=lambda q: q.get("time", ""), reverse=True)

    # ----- Anasayfa: top 5'in ID-set'i değiştiyse güncelle -----
    homepage_pool = [q for q in quakes
                     if float(q.get("magnitude", 0) or 0) >= MIN_MAGNITUDE]
    top5_ids = tuple(q.get("id") for q in homepage_pool[:5])
    if top5_ids and top5_ids != _LAST_HOMEPAGE:
        if update_homepage(homepage_pool, cities):
            log.info(f"✓ Anasayfa güncellendi (son {len(top5_ids)} deprem)")
            ping_indexnow_url("https://yakinimdakideprem.com/")
            _LAST_HOMEPAGE = top5_ids

    # ----- Son dakika sayfası: yeni deprem geldiğinde SSR render -----
    # (kendi fetch'ini yapar: M2.0+/24s; quakes boş olsa da çalışır)
    try:
        if update_son_dakika():
            ping_indexnow_url("https://yakinimdakideprem.com/son-dakika-deprem.html")
            log.info("✓ son-dakika-deprem.html SSR güncellendi")
    except Exception as e:
        log.warning(f"son-dakika update: {e}")

    # ----- Şehir sayfaları: her şehir için en yeni deprem (M3.5+) -----
    # quakes_by_city: slug → en yeni 5 deprem (SSR quake table için)
    quakes_by_city: dict[str, list] = {}
    for q in quakes:
        place = q.get("location") or q.get("place") or ""
        slug = find_city_slug(place, cities)
        if slug:
            quakes_by_city.setdefault(slug, []).append(q)

    seen = set()
    updated = 0

    for q in quakes:
        try:
            mag = float(q.get("magnitude", 0) or 0)
        except (TypeError, ValueError):
            continue
        if mag < MIN_MAGNITUDE:
            continue

        place = q.get("location") or q.get("place") or ""
        slug = find_city_slug(place, cities)
        if not slug or slug in seen:
            continue
        seen.add(slug)

        qid = q.get("id") or place
        if _LAST_WRITTEN.get(slug) == qid:
            continue   # zaten bu deprem yazılı, atla

        city_name = cities[slug]["name"]
        city_quakes = quakes_by_city.get(slug, [])
        if update_city_page(slug, city_name, q, quakes_for_city=city_quakes):
            update_sitemap(slug)
            ping_indexnow(slug)
            _LAST_WRITTEN[slug] = qid
            log.info(
                f"✓ {slug:15s} M{mag:>3.1f} {place[:50]}"
            )
            updated += 1

    # ----- Revert pass: STALE_HOURS'tan eski "az önce" bloklarını nötrle -----
    # Daemon sadece yeni deprem olunca yazıyordu, asla geri almıyordu; bu yüzden
    # şehirler haftalarca "🔴 Az Önce X Deprem" başlığında donuyordu. Bu pass
    # her turda tüm şehirleri tarar, bayat olanları nötr bloğa + standart başlığa
    # döndürür. Bu turda taze yazılanlara (seen) dokunmaz.
    reverted = 0
    for r_slug, r_info in cities.items():
        if r_slug in seen:
            continue
        try:
            if revert_city_page(r_slug, r_info["name"]):
                update_sitemap(r_slug)
                _LAST_WRITTEN.pop(r_slug, None)
                reverted += 1
                log.info(f"↩ {r_slug:15s} bayat freshness nötrlendi")
        except Exception as e:
            log.warning(f"revert {r_slug}: {e}")
    if reverted:
        log.info(f"↩ Toplam {reverted} şehir nötrlendi")

    return updated


def ping_indexnow_url(url: str):
    if not INDEXNOW_KEY:
        return
    try:
        requests.post(
            "https://api.indexnow.org/indexnow",
            json={"host": INDEXNOW_HOST, "key": INDEXNOW_KEY, "urlList": [url]},
            timeout=8,
        )
    except Exception:
        pass


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--once", action="store_true", help="Tek tur, daemon değil")
    p.add_argument("--simulate-quake", metavar="SLUG",
                   help="Belirtilen şehir için sahte deprem inject et (test)")
    p.add_argument("--allow-prod-write", action="store_true",
                   help="--simulate-quake'in CANLI public/ klasörüne yazmasına izin ver (tehlikeli)")
    args = p.parse_args()

    cities = load_cities()
    log.info(f"Loaded {len(cities)} cities. API={API_URL} threshold=M{MIN_MAGNITUDE}")

    if args.simulate_quake:
        slug = args.simulate_quake
        if slug not in cities:
            log.error(f"Unknown slug: {slug}")
            sys.exit(1)
        if not args.allow_prod_write:
            log.error(
                "GÜVENLİK: --simulate-quake CANLI public/ klasörüne sahte deprem yazar. "
                "Bilerek yapıyorsanız --allow-prod-write ekleyin ve sonra mutlaka `--once` "
                "ile geri alın. (İstanbul TEST verisi bu yüzden 27 gün yayında kaldı.)"
            )
            sys.exit(2)
        fake = {
            "magnitude": 4.2,
            "place": f"TEST-{cities[slug]['name'].upper()}",
            "location": f"TEST-{cities[slug]['name'].upper()}",
            "time": datetime.now(TZ_TR).strftime("%Y-%m-%d %H:%M:%S"),
            "depth": "8.5",
            "id": "test-quake",
        }
        # SSR quake table testi için fake liste de geçir
        fake_list = [fake] * 3
        update_city_page(slug, cities[slug]["name"], fake,
                          quakes_for_city=fake_list)
        update_sitemap(slug)
        log.info(f"Simulated quake injected into deprem-{slug}.html")
        return

    if args.once:
        run_once(cities)
        return

    log.info(f"Daemon başladı, her {POLL_SECONDS}s API check.")
    while True:
        try:
            run_once(cities)
        except Exception as e:
            log.exception(f"Loop error: {e}")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
