import json
import logging
import os
import re
import time
from datetime import datetime
from typing import List, Dict, Any, Set, Optional, Tuple

import requests
import tweepy


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


API_URL = os.getenv("EARTHQUAKE_API_URL", "http://localhost:8000/api/earthquakes")
MIN_MAGNITUDE = float(os.getenv("TWITTER_MIN_MAGNITUDE", "4.0"))
HISTORY_FILE = os.getenv("TWITTER_HISTORY_FILE", "posted_quakes.json")
TWEET_TAGS = os.getenv("TWITTER_HASHTAGS", "#deprem #sondakika #turkiye")


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


def make_client() -> Optional[tweepy.Client]:
    """Create Twitter client from environment; return None if missing creds."""
    required = {
        "TWITTER_API_KEY": os.getenv("TWITTER_API_KEY"),
        "TWITTER_API_SECRET": os.getenv("TWITTER_API_SECRET"),
        "TWITTER_ACCESS_TOKEN": os.getenv("TWITTER_ACCESS_TOKEN"),
        "TWITTER_ACCESS_TOKEN_SECRET": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        logging.error("Eksik Twitter anahtarları: %s", ", ".join(missing))
        return None
    return tweepy.Client(
        consumer_key=required["TWITTER_API_KEY"],
        consumer_secret=required["TWITTER_API_SECRET"],
        access_token=required["TWITTER_ACCESS_TOKEN"],
        access_token_secret=required["TWITTER_ACCESS_TOKEN_SECRET"],
    )


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
            return data
        if isinstance(data, dict):
            if data.get("success") is False:
                return []
            if "earthquakes" in data:
                return data["earthquakes"]
            if "data" in data:
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


def extract_location_tags(location: str) -> List[str]:
    candidates: Set[str] = set()
    if not location:
        return []

    # Parentheses often carry province info, keep those pieces.
    for part in re.findall(r"\(([^)]+)\)", location):
        part = part.strip()
        if len(part) > 1:
            candidates.add(part)

    # Also try splitting the leading portion on "-" and "/" to catch district names.
    prefix = location.split("(")[0]
    for piece in re.split(r"[-/]", prefix):
        piece = piece.strip()
        if len(piece) > 2:
            candidates.add(piece)

    tags: List[str] = []
    for candidate in candidates:
        tag = normalize_tag(candidate)
        if tag:
            tags.append(tag)

    return sorted(set(tags))


def format_tweet(quake: Dict[str, Any]) -> str:
    mag = quake.get("magnitude")
    location = quake.get("location", "Bilinmiyor")
    depth = quake.get("depth", "?")
    ts = format_time(str(quake.get("time", "")))
    tags = []

    # Base hashtags + city/province tags
    seen: Set[str] = set()
    for tag in BASE_TAGS + extract_location_tags(location):
        if tag not in seen:
            seen.add(tag)
            tags.append(tag)

    tags_section = f"{' '.join(tags)}\n\n" if tags else ""
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
    body += "🙏 Geçmiş olsun."
    return body


def run_once() -> None:
    client = make_client()
    if not client:
        return

    quakes = pick_strongest_per_location_minute(fetch_quakes())
    if not quakes:
        logging.info("Paylaşılacak deprem yok.")
        return

    posted = load_history()
    updated = set(posted)

    # Oldest first to preserve order
    for quake in quakes:
        quake_id = quake.get("id")
        try:
            mag = float(quake.get("magnitude", 0))
        except Exception:
            continue
        if not quake_id or quake_id in posted or mag < MIN_MAGNITUDE:
            continue

        tweet_text = format_tweet(quake)
        try:
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
