#!/usr/bin/env python3
"""
Wikipedia REST API'sinden her il için kapak görseli çeker, resize+WebP olarak
public/images/cities/{slug}.webp ve {slug}-og.webp (1200×630 OG) olarak kaydeder.

Görseller CC-BY veya Public Domain (Wikipedia summary endpoint sadece bu
lisansları döndürür). Her görsel için scripts/city_image_credits.json'a
attribution kaydedilir; ben-kimim.html veya footer'da gösterilebilir.

Kullanım:
  python3 scripts/fetch_city_images.py             # eksikleri çek
  python3 scripts/fetch_city_images.py --force     # hepsini yeniden çek
  python3 scripts/fetch_city_images.py --slug istanbul  # tek şehir
"""
from __future__ import annotations

import argparse
import json
import logging
import time
from io import BytesIO
from pathlib import Path
from urllib.parse import quote

import requests
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
ALIASES = ROOT / "scripts" / "city_aliases.json"
CITIES_DIR = PUBLIC / "images" / "cities"
CREDITS = ROOT / "scripts" / "city_image_credits.json"
USER_AGENT = "YakinimdakiDeprem/1.0 (https://yakinimdakideprem.com; contact@yakinimdakideprem.com)"

CITIES_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("img")


# Wikipedia article title overrides (default: city name in TR)
TITLE_OVERRIDES = {
    "kahramanmaras": "Kahramanmaraş",
    "afyonkarahisar": "Afyonkarahisar",
    "agri": "Ağrı",
    "aydin": "Aydın",
    "balikesir": "Balıkesir",
    "bartin": "Bartın",
    "bingol": "Bingöl",
    "bolu": "Bolu",
    "canakkale": "Çanakkale",
    "cankiri": "Çankırı",
    "corum": "Çorum",
    "elazig": "Elazığ",
    "eskisehir": "Eskişehir",
    "gumushane": "Gümüşhane",
    "hatay": "Hatay",
    "igdir": "Iğdır",
    "kirikkale": "Kırıkkale",
    "kirklareli": "Kırklareli",
    "kirsehir": "Kırşehir",
    "kutahya": "Kütahya",
    "mugla": "Muğla",
    "mus": "Muş",
    "nevsehir": "Nevşehir",
    "nigde": "Niğde",
    "osmaniye": "Osmaniye",
    "sanliurfa": "Şanlıurfa",
    "sirnak": "Şırnak",
    "tekirdag": "Tekirdağ",
    "usak": "Uşak",
    "yozgat": "Yozgat",
    "zonguldak": "Zonguldak",
    # Disambiguation override (Wikipedia genel terim olarak kullanıyor)
    "ordu": "Ordu (il)",
    "tokat": "Tokat (il)",
    "sanliurfa": "Şanlıurfa",
}


def get_summary(title: str) -> dict | None:
    url = f"https://tr.wikipedia.org/api/rest_v1/page/summary/{quote(title)}"
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
        if r.status_code == 200:
            return r.json()
        # Fallback: English Wikipedia
        url2 = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(title)}"
        r2 = requests.get(url2, headers={"User-Agent": USER_AGENT}, timeout=10)
        if r2.status_code == 200:
            return r2.json()
    except Exception as e:
        log.warning(f"summary fetch failed for {title}: {e}")
    return None


def download_image(url: str) -> Image.Image | None:
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
        r.raise_for_status()
        img = Image.open(BytesIO(r.content)).convert("RGB")
        return img
    except Exception as e:
        log.warning(f"image fetch failed: {e}")
        return None


def save_webp(img: Image.Image, path: Path, max_width: int):
    if img.width > max_width:
        ratio = max_width / img.width
        new_size = (max_width, int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)
    img.save(path, "WEBP", quality=82, method=6)


def save_og(img: Image.Image, path: Path, target=(1200, 630)):
    """OG image: cover-fit center crop to 1200×630."""
    src_ratio = img.width / img.height
    dst_ratio = target[0] / target[1]
    if src_ratio > dst_ratio:
        # source wider — crop sides
        new_w = int(img.height * dst_ratio)
        offset = (img.width - new_w) // 2
        img = img.crop((offset, 0, offset + new_w, img.height))
    else:
        new_h = int(img.width / dst_ratio)
        offset = (img.height - new_h) // 2
        img = img.crop((0, offset, img.width, offset + new_h))
    img = img.resize(target, Image.LANCZOS)
    img.save(path, "WEBP", quality=82, method=6)


def fetch_one(slug: str, name: str, force: bool, credits: dict) -> bool:
    out = CITIES_DIR / f"{slug}.webp"
    out_og = CITIES_DIR / f"{slug}-og.webp"

    if out.exists() and out_og.exists() and not force:
        return False

    title = TITLE_OVERRIDES.get(slug, name)
    summary = get_summary(title)
    if not summary:
        log.warning(f"{slug}: Wikipedia summary yok")
        return False

    img_url = (summary.get("originalimage") or {}).get("source") or \
              (summary.get("thumbnail") or {}).get("source")
    if not img_url:
        log.warning(f"{slug}: görsel yok")
        return False

    img = download_image(img_url)
    if img is None:
        return False

    # Save 800px width hero + 1200×630 OG
    save_webp(img.copy(), out, max_width=800)
    save_og(img.copy(), out_og)

    credits[slug] = {
        "title": summary.get("title", title),
        "source_url": img_url,
        "wikipedia_url": (summary.get("content_urls") or {})
            .get("desktop", {}).get("page", ""),
        "license": "Wikipedia/Wikimedia (CC-BY-SA veya kamu malı)",
    }
    log.info(f"✓ {slug:15s} → {out.name} + {out_og.name}")
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--force", action="store_true")
    p.add_argument("--slug")
    p.add_argument("--sleep", type=float, default=1.5,
                   help="Wikipedia rate-limit için bekleme (saniye)")
    args = p.parse_args()

    cities = json.loads(ALIASES.read_text(encoding="utf-8"))
    credits = {}
    if CREDITS.exists():
        credits = json.loads(CREDITS.read_text(encoding="utf-8"))

    targets = {args.slug: cities[args.slug]} if args.slug else cities
    done = skipped = failed = 0
    for slug, info in targets.items():
        try:
            if fetch_one(slug, info["name"], args.force, credits):
                done += 1
                time.sleep(args.sleep)
            else:
                skipped += 1
        except Exception as e:
            log.exception(f"{slug} failed: {e}")
            failed += 1

    CREDITS.write_text(json.dumps(credits, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    log.info(f"Done: {done}  Skipped: {skipped}  Failed: {failed}")


if __name__ == "__main__":
    main()
