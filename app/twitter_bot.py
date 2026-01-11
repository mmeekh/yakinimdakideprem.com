import json
import logging
import os
import re
import time
from datetime import datetime
from io import BytesIO
from typing import List, Dict, Any, Set, Optional, Tuple

import requests
import tweepy
from PIL import Image, ImageDraw, ImageFont


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


API_URL = os.getenv("EARTHQUAKE_API_URL", "http://localhost:8000/api/earthquakes")
MIN_MAGNITUDE = float(os.getenv("TWITTER_MIN_MAGNITUDE", "4.0"))
HISTORY_FILE = os.getenv("TWITTER_HISTORY_FILE", "posted_quakes.json")
TWEET_TAGS = os.getenv("TWITTER_HASHTAGS", "#bugun #deprem #sondakika")
MAP_SERVICE_URL = os.getenv(
    "TWITTER_MAP_URL", "https://staticmap.openstreetmap.de/staticmap.php"
)
MAP_WIDTH = int(os.getenv("TWITTER_MAP_WIDTH", "1000"))
MAP_HEIGHT = int(os.getenv("TWITTER_MAP_HEIGHT", "560"))
IMAGE_WIDTH = int(os.getenv("TWITTER_IMAGE_WIDTH", "1200"))
IMAGE_HEIGHT = int(os.getenv("TWITTER_IMAGE_HEIGHT", "675"))
IMAGE_BORDER = int(os.getenv("TWITTER_IMAGE_BORDER", "12"))


def normalize_tag(tag: str) -> Optional[str]:
    """Normalize a raw tag into a hashtag, stripping invalid chars."""
    if not tag:
        return None
    cleaned = tag.strip()
    if cleaned.startswith("#"):
        cleaned = cleaned[1:]
    cleaned = re.sub(r"[^0-9A-Za-zÇĞİÖŞÜçğıöşü]+", "", cleaned)
    if not cleaned:
        return None
    return f"#{cleaned}"


def base_tags() -> List[str]:
    tags: List[str] = []
    for raw in TWEET_TAGS.split():
        tag = normalize_tag(raw)
        if tag:
            tags.append(tag)
    return tags


BASE_TAGS = base_tags()


PROVINCES = [
    "Adana",
    "Adıyaman",
    "Afyonkarahisar",
    "Ağrı",
    "Amasya",
    "Ankara",
    "Antalya",
    "Artvin",
    "Aydın",
    "Balıkesir",
    "Bilecik",
    "Bingöl",
    "Bitlis",
    "Bolu",
    "Burdur",
    "Bursa",
    "Çanakkale",
    "Çankırı",
    "Çorum",
    "Denizli",
    "Diyarbakır",
    "Edirne",
    "Elazığ",
    "Erzincan",
    "Erzurum",
    "Eskişehir",
    "Gaziantep",
    "Giresun",
    "Gümüşhane",
    "Hakkari",
    "Hatay",
    "Isparta",
    "Mersin",
    "İstanbul",
    "İzmir",
    "Kars",
    "Kastamonu",
    "Kayseri",
    "Kırklareli",
    "Kırşehir",
    "Kocaeli",
    "Konya",
    "Kütahya",
    "Malatya",
    "Manisa",
    "Kahramanmaraş",
    "Mardin",
    "Muğla",
    "Muş",
    "Nevşehir",
    "Niğde",
    "Ordu",
    "Rize",
    "Sakarya",
    "Samsun",
    "Siirt",
    "Sinop",
    "Sivas",
    "Tekirdağ",
    "Tokat",
    "Trabzon",
    "Tunceli",
    "Şanlıurfa",
    "Uşak",
    "Van",
    "Yozgat",
    "Zonguldak",
    "Aksaray",
    "Bayburt",
    "Karaman",
    "Kırıkkale",
    "Batman",
    "Şırnak",
    "Bartın",
    "Ardahan",
    "Iğdır",
    "Yalova",
    "Karabük",
    "Kilis",
    "Osmaniye",
    "Düzce",
]


def normalize_for_match(text: str) -> str:
    if not text:
        return ""
    lowered = text.casefold()
    lowered = lowered.replace("i̇", "i")
    return (
        lowered.replace("ç", "c")
        .replace("ğ", "g")
        .replace("ı", "i")
        .replace("ö", "o")
        .replace("ş", "s")
        .replace("ü", "u")
    )


PROVINCE_LOOKUP = {normalize_for_match(name): name for name in PROVINCES}
PROVINCE_LOOKUP.update(
    {
        "icel": "Mersin",
        "kahramanmaras": "Kahramanmaraş",
        "sanliurfa": "Şanlıurfa",
        "sirnak": "Şırnak",
        "duzce": "Düzce",
        "igdir": "Iğdır",
        "tekirdag": "Tekirdağ",
    }
)


def extract_province(location: str) -> Optional[str]:
    if not location:
        return None

    groups = re.findall(r"\(([^)]+)\)", location)
    for group in reversed(groups):
        candidate = normalize_for_match(group)
        for token in re.findall(r"[a-z0-9]+", candidate):
            province = PROVINCE_LOOKUP.get(token)
            if province:
                return province

    normalized = normalize_for_match(location)
    tokens = set(re.findall(r"[a-z0-9]+", normalized))
    for token in tokens:
        province = PROVINCE_LOOKUP.get(token)
        if province:
            return province
    return None


def build_tags_and_city(location: str) -> Tuple[List[str], Optional[str]]:
    tags: List[str] = []
    seen: Set[str] = set()
    for tag in BASE_TAGS:
        if tag not in seen:
            tags.append(tag)
            seen.add(tag)

    city = extract_province(location)
    city_tag = normalize_tag(city) if city else None
    if city_tag and city_tag not in seen:
        if "#sondakika" in seen:
            index = tags.index("#sondakika")
            tags.insert(index, city_tag)
        else:
            tags.append(city_tag)
        seen.add(city_tag)

    return tags, city


def normalize_location_key(location: str) -> Optional[str]:
    """Normalize location for grouping comparisons."""
    if not location:
        return None
    normalized = re.sub(r"\s+", " ", str(location).strip().lower())
    return normalized or None


def parse_time_bucket(quake: Dict[str, Any]) -> Optional[datetime]:
    """Bucket quake time to minute precision."""
    raw = quake.get("time")
    if not raw:
        return None
    try:
        iso = str(raw).replace("Z", "+00:00")
        dt = datetime.fromisoformat(iso)
        return dt.replace(second=0, microsecond=0)
    except Exception:
        return None


def pick_strongest_per_location_minute(
    quakes: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    For quakes sharing the same normalized location within the same minute,
    keep only the strongest magnitude entry.
    """
    buckets: Dict[Tuple[str, datetime], Dict[str, Any]] = {}
    order: List[Tuple[str, datetime]] = []

    for quake in quakes:
        loc_key = normalize_location_key(quake.get("location"))
        bucket = parse_time_bucket(quake)
        if not loc_key or not bucket:
            continue

        try:
            mag = float(quake.get("magnitude", 0))
        except Exception:
            mag = 0

        key = (loc_key, bucket)
        existing = buckets.get(key)
        if not existing:
            buckets[key] = quake
            order.append(key)
        else:
            try:
                existing_mag = float(existing.get("magnitude", 0))
            except Exception:
                existing_mag = 0
            if mag > existing_mag:
                buckets[key] = quake

    # Return in chronological order based on bucket
    ordered_quakes: List[Dict[str, Any]] = []
    for key in sorted(order, key=lambda k: k[1]):
        ordered_quakes.append(buckets[key])
    return ordered_quakes


def make_clients() -> Tuple[Optional[tweepy.Client], Optional[tweepy.API]]:
    """Create Twitter v2 client + v1.1 API (media upload); return None if missing creds."""
    required = {
        "TWITTER_API_KEY": os.getenv("TWITTER_API_KEY"),
        "TWITTER_API_SECRET": os.getenv("TWITTER_API_SECRET"),
        "TWITTER_ACCESS_TOKEN": os.getenv("TWITTER_ACCESS_TOKEN"),
        "TWITTER_ACCESS_TOKEN_SECRET": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        logging.error("Eksik Twitter anahtarları: %s", ", ".join(missing))
        return None, None
    client = tweepy.Client(
        consumer_key=required["TWITTER_API_KEY"],
        consumer_secret=required["TWITTER_API_SECRET"],
        access_token=required["TWITTER_ACCESS_TOKEN"],
        access_token_secret=required["TWITTER_ACCESS_TOKEN_SECRET"],
    )
    auth = tweepy.OAuth1UserHandler(
        required["TWITTER_API_KEY"],
        required["TWITTER_API_SECRET"],
        required["TWITTER_ACCESS_TOKEN"],
        required["TWITTER_ACCESS_TOKEN_SECRET"],
    )
    api = tweepy.API(auth)
    return client, api


def load_history() -> Set[str]:
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                return set(json.load(f))
    except Exception as exc:
        logging.warning("Geçmiş okunamadı: %s", exc)
    return set()


def save_history(history: Set[str]) -> None:
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(list(history), f)
    except Exception as exc:
        logging.error("Geçmiş yazılamadı: %s", exc)


def fetch_quakes() -> List[Dict[str, Any]]:
    try:
        resp = requests.get(
            API_URL, params={"limit": 20, "min_magnitude": MIN_MAGNITUDE}, timeout=15
        )
        if resp.status_code != 200:
            logging.error("API hatası: %s", resp.status_code)
            return []
        data = resp.json()
        if isinstance(data, list):
            logging.info("API deprem sayısı: %s", len(data))
            return data
        if isinstance(data, dict):
            if data.get("success") is False:
                logging.warning("API başarısız yanıt döndü.")
                return []
            if "earthquakes" in data:
                logging.info("API deprem sayısı: %s", len(data["earthquakes"]))
                return data["earthquakes"]
            if "data" in data:
                logging.info("API deprem sayısı: %s", len(data["data"]))
                return data["data"]
        logging.error("Beklenmeyen API yanıtı: %s", type(data))
        return []
    except Exception as exc:
        logging.error("API bağlantı hatası: %s", exc)
        return []


def format_time(iso_str: str) -> str:
    try:
        iso = iso_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(iso)
        return dt.strftime("%d.%m.%Y %H:%M")
    except Exception:
        return iso_str


def magnitude_color(magnitude: float) -> str:
    if magnitude >= 8.0:
        return "#7b1fa2"
    if magnitude >= 7.0:
        return "#b71c1c"
    if magnitude >= 6.0:
        return "#d32f2f"
    if magnitude >= 5.0:
        return "#f44336"
    if magnitude >= 4.0:
        return "#ff9800"
    if magnitude >= 3.0:
        return "#ffc107"
    return "#4caf50"


def hex_to_rgb(value: str) -> Tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def adjust_color(rgb: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
    return tuple(max(0, min(255, int(channel * factor))) for channel in rgb)


def load_badge_font(size: int) -> ImageFont.ImageFont:
    for font_path in ("DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(font_path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def pick_text_color(rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
    luminance = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
    return (15, 23, 42) if luminance > 165 else (255, 255, 255)


def draw_magnitude_badge(canvas: Image.Image, magnitude: float, border_hex: str) -> None:
    text = f"M {magnitude:.1f}"
    font_size = max(22, int(IMAGE_HEIGHT * 0.06))
    font = load_badge_font(font_size)

    draw = ImageDraw.Draw(canvas)
    if hasattr(draw, "textbbox"):
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
    else:
        text_w, text_h = draw.textsize(text, font=font)

    padding_x = max(14, int(text_h * 0.8))
    padding_y = max(8, int(text_h * 0.5))
    badge_w = text_w + padding_x * 2
    badge_h = text_h + padding_y * 2

    x0 = IMAGE_BORDER + 18
    y0 = IMAGE_BORDER + 18
    x1 = x0 + badge_w
    y1 = y0 + badge_h

    bg_rgb = hex_to_rgb(border_hex)
    outline = adjust_color(bg_rgb, 0.85)
    radius = min(badge_h // 2, 24)

    if hasattr(draw, "rounded_rectangle"):
        draw.rounded_rectangle((x0, y0, x1, y1), radius=radius, fill=bg_rgb, outline=outline, width=2)
    else:
        draw.rectangle((x0, y0, x1, y1), fill=bg_rgb, outline=outline, width=2)

    text_color = pick_text_color(bg_rgb)
    shadow = (0, 0, 0) if text_color == (255, 255, 255) else (255, 255, 255)
    text_x = x0 + (badge_w - text_w) / 2
    text_y = y0 + (badge_h - text_h) / 2
    draw.text((text_x + 1, text_y + 1), text, font=font, fill=shadow)
    draw.text((text_x, text_y), text, font=font, fill=text_color)


def map_zoom_for_magnitude(magnitude: float) -> int:
    if magnitude >= 7.0:
        return 6
    if magnitude >= 5.0:
        return 7
    if magnitude >= 3.0:
        return 8
    return 9


def fetch_static_map(lat: float, lng: float, zoom: int) -> Optional[Image.Image]:
    params = {
        "center": f"{lat},{lng}",
        "zoom": str(zoom),
        "size": f"{MAP_WIDTH}x{MAP_HEIGHT}",
        "maptype": "mapnik",
        "markers": f"{lat},{lng},red-pushpin",
    }
    try:
        resp = requests.get(MAP_SERVICE_URL, params=params, timeout=12)
        resp.raise_for_status()
        return Image.open(BytesIO(resp.content)).convert("RGB")
    except Exception as exc:
        logging.error("Harita görseli alınamadı: %s", exc)
        return None


def build_quake_image(quake: Dict[str, Any]) -> Optional[str]:
    coords = quake.get("coordinates") or {}
    try:
        lat = float(coords.get("lat"))
        lng = float(coords.get("lng"))
    except (TypeError, ValueError):
        return None

    try:
        magnitude = float(quake.get("magnitude", 0))
    except (TypeError, ValueError):
        magnitude = 0.0

    border_color = magnitude_color(magnitude)
    zoom = map_zoom_for_magnitude(magnitude)
    map_image = fetch_static_map(lat, lng, zoom) or Image.new(
        "RGB", (MAP_WIDTH, MAP_HEIGHT), "#f8fafc"
    )

    canvas = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), border_color)
    target_size = (IMAGE_WIDTH - 2 * IMAGE_BORDER, IMAGE_HEIGHT - 2 * IMAGE_BORDER)
    map_image = map_image.resize(target_size, Image.LANCZOS)
    canvas.paste(map_image, (IMAGE_BORDER, IMAGE_BORDER))

    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    center = (IMAGE_WIDTH // 2, IMAGE_HEIGHT // 2)
    radius = int(32 + max(0.0, magnitude) * 12)
    color = hex_to_rgb(border_color)
    draw.ellipse(
        (
            center[0] - radius,
            center[1] - radius,
            center[0] + radius,
            center[1] + radius,
        ),
        fill=(*color, 60),
        outline=(*color, 200),
        width=5,
    )
    draw.ellipse(
        (
            center[0] - 7,
            center[1] - 7,
            center[0] + 7,
            center[1] + 7,
        ),
        fill=(*color, 255),
    )
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    draw_magnitude_badge(canvas, magnitude, border_color)

    quake_id = re.sub(r"[^a-zA-Z0-9_-]+", "", str(quake.get("id", "quake")))
    output_path = f"/tmp/quake_{quake_id or 'quake'}.jpg"
    canvas.save(output_path, format="JPEG", quality=90, optimize=True)
    return output_path


def format_tweet(quake: Dict[str, Any]) -> str:
    mag = quake.get("magnitude")
    location = quake.get("location", "Bilinmiyor")
    depth = quake.get("depth", "?")
    ts = format_time(str(quake.get("time", "")))
    tags, city = build_tags_and_city(location)
    tags_section = f"{' '.join(tags)}\n\n" if tags else ""
    logging.debug(
        "Tweet formatı: location=%s mag=%s city=%s tags=%s",
        location,
        mag,
        city,
        tags,
    )
    body = (
        "🚨 DEPREM UYARISI\n\n"
        f"📍 Yer: {location}\n"
        f"📉 Büyüklük: {mag}\n"
        f"⏱️ Tarih: {ts}\n"
        f"⬇️ Derinlik: {depth} km\n\n"
        "Detaylar ve Harita: https://yakinimdakideprem.com\n\n"
    )
    if tags_section:
        body += tags_section
    if city:
        body += f"🙏 Geçmiş olsun {city}."
    else:
        body += "🙏 Geçmiş olsun."
    return body


def run_once() -> None:
    client, media_api = make_clients()
    if not client:
        return

    raw_quakes = fetch_quakes()
    quakes = pick_strongest_per_location_minute(raw_quakes)
    if raw_quakes:
        logging.info(
            "Deprem filtreleme: gelen=%s, gruplanan=%s (konum+dakika)",
            len(raw_quakes),
            len(quakes),
        )
    if not quakes:
        logging.info("Paylaşılacak deprem yok.")
        return

    posted = load_history()
    updated = set(posted)
    logging.info(
        "Twitter bot çalışıyor. Min büyüklük=%.1f, geçmiş kayıt=%s",
        MIN_MAGNITUDE,
        len(posted),
    )

    # Oldest first to preserve order
    for quake in quakes:
        quake_id = quake.get("id")
        try:
            mag = float(quake.get("magnitude", 0))
        except Exception:
            logging.warning("Geçersiz büyüklük: %s", quake.get("magnitude"))
            continue
        if not quake_id:
            logging.warning("Deprem ID eksik, atlandı: %s", quake)
            continue
        if quake_id in posted:
            logging.info("Daha önce atıldı, atlandı: %s", quake_id)
            continue
        if mag < MIN_MAGNITUDE:
            logging.info(
                "Eşik altında, atlandı: %s (%.1f < %.1f)",
                quake.get("location"),
                mag,
                MIN_MAGNITUDE,
            )
            continue

        tweet_text = format_tweet(quake)
        media_ids: Optional[List[str]] = None
        image_path = build_quake_image(quake)
        if image_path and media_api:
            try:
                media = media_api.media_upload(image_path)
                media_ids = [media.media_id_string]
            except Exception as exc:
                logging.error("Görsel yüklenemedi: %s", exc)
            finally:
                try:
                    os.remove(image_path)
                except OSError:
                    pass
        try:
            if media_ids:
                client.create_tweet(text=tweet_text, media_ids=media_ids)
            else:
                client.create_tweet(text=tweet_text)
            logging.info("Tweet atıldı: %s - %.1f", quake.get("location"), mag)
            updated.add(quake_id)
            time.sleep(2)
        except Exception as exc:
            logging.error("Tweet hatası: %s", exc)

    if updated != posted:
        save_history(updated)


if __name__ == "__main__":
    run_once()
