import os
from copy import deepcopy
import html
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any

import httpx
from fastapi import FastAPI, HTTPException, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel


def format_time_ago(dt: datetime) -> str:
    """Return human readable time diff such as '5 dakika 12 saniye önce'."""
    now = datetime.now()
    diff = now - dt
    total_seconds = int(diff.total_seconds())

    if total_seconds < 60:
        return f"{total_seconds} saniye önce"
    if total_seconds < 3600:
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        if seconds == 0:
            return f"{minutes} dakika önce"
        return f"{minutes} dakika {seconds} saniye önce"
    if total_seconds < 86400:
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        if minutes == 0:
            return f"{hours} saat önce"
        return f"{hours} saat {minutes} dakika önce"

    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    if hours == 0:
        return f"{days} gün önce"
    return f"{days} gün {hours} saat önce"


def sanitize_text(value: str) -> str:
    """Escape text for safe HTML rendering in clients."""
    return html.escape(value or "", quote=True)


def normalize_etag_value(value: str) -> str:
    if not value:
        return ""
    value = value.strip()
    if value.startswith("W/"):
        value = value[2:].strip()
    return value.strip('"')


def etag_matches(request: Request, etag: str) -> bool:
    if not etag:
        return False
    header = request.headers.get("if-none-match")
    if not header:
        return False
    candidates = [candidate.strip() for candidate in header.split(",")]
    return any(normalize_etag_value(candidate) == etag for candidate in candidates)


def format_etag(etag: str) -> str:
    return f"\"{etag}\""


def build_earthquake_etag(items: List[Any]) -> str:
    parts: List[str] = []
    for item in items or []:
        if isinstance(item, dict):
            item_id = item.get("id")
            item_time = item.get("time")
        else:
            item_id = getattr(item, "id", None)
            item_time = getattr(item, "time", None)
        if isinstance(item_time, datetime):
            time_value = item_time.isoformat()
        else:
            time_value = str(item_time or "")
        parts.append(f"{item_id}-{time_value}")
    fingerprint = "|".join(parts)
    return hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()


def build_stats_etag(stats: Dict[str, Any]) -> str:
    payload = json.dumps(stats, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class EarthquakeCache:
    """Simple in-memory cache for earthquake responses."""

    def __init__(self, cache_duration_seconds: int = 20) -> None:
        self.cache_duration = timedelta(seconds=cache_duration_seconds)
        self.cache: Dict[str, Dict[str, Any]] = {}

    def get(self, cache_key: str) -> Optional[Dict[str, Any]]:
        if cache_key not in self.cache:
            return None
        cached = self.cache[cache_key]
        if datetime.now() - cached["timestamp"] < self.cache_duration:
            return cached["data"]
        del self.cache[cache_key]
        return None

    def set(self, cache_key: str, data: Dict[str, Any]) -> None:
        self.cache[cache_key] = {"data": data, "timestamp": datetime.now()}

    def clear(self) -> None:
        self.cache.clear()


KANDILLI_CACHE_TTL = timedelta(seconds=20)
_kandilli_cache_data: Optional[List[Dict[str, Any]]] = None
_kandilli_cache_timestamp: Optional[datetime] = None

KANDILLI_API_URL = os.getenv(
    "KANDILLI_API_URL", "https://api.orhanaydogdu.com.tr/deprem/kandilli/live"
)
AFAD_API_URL = os.getenv(
    "AFAD_API_URL", "https://api.orhanaydogdu.com.tr/deprem/afad/live"
)
DATA_SOURCES = [
    ("Kandilli", KANDILLI_API_URL),
    ("AFAD", AFAD_API_URL),
]


def parse_earthquake_time(raw_time: str) -> Optional[datetime]:
    if not raw_time:
        return None
    raw_time = str(raw_time)
    try:
        parsed = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
        if parsed.tzinfo:
            return parsed.astimezone().replace(tzinfo=None)
        return parsed
    except ValueError:
        pass
    for fmt in ("%Y.%m.%d %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(raw_time, fmt)
        except ValueError:
            continue
    return None


def extract_coordinates(item: Dict[str, Any]) -> Dict[str, float]:
    coordinates = []
    geojson = item.get("geojson")
    if isinstance(geojson, dict):
        coordinates = geojson.get("coordinates") or []
    if not coordinates:
        geometry = item.get("geometry")
        if isinstance(geometry, dict):
            coordinates = geometry.get("coordinates") or []
    if not coordinates:
        coords_raw = item.get("coordinates")
        if isinstance(coords_raw, list):
            coordinates = coords_raw

    lat = None
    lng = None
    if len(coordinates) >= 2:
        lng = coordinates[0]
        lat = coordinates[1]

    properties = item.get("properties") if isinstance(item.get("properties"), dict) else {}
    if lat is None:
        lat = item.get("lat") or item.get("latitude") or properties.get("lat") or properties.get("latitude")
    if lng is None:
        lng = item.get("lng") or item.get("longitude") or item.get("lon") or properties.get("lng") or properties.get("longitude") or properties.get("lon")

    try:
        lat = float(lat)
    except (TypeError, ValueError):
        lat = 0.0
    try:
        lng = float(lng)
    except (TypeError, ValueError):
        lng = 0.0

    return {"lat": lat, "lng": lng}


def extract_depth(item: Dict[str, Any]) -> float:
    depth = item.get("depth")
    properties = item.get("properties") if isinstance(item.get("properties"), dict) else {}
    if depth is None and properties:
        depth = properties.get("depth")
    if depth is None:
        geojson = item.get("geojson")
        if isinstance(geojson, dict):
            coords = geojson.get("coordinates") or []
            if len(coords) >= 3:
                depth = coords[2]
        geometry = item.get("geometry")
        if depth is None and isinstance(geometry, dict):
            coords = geometry.get("coordinates") or []
            if len(coords) >= 3:
                depth = coords[2]
    try:
        return float(depth) if depth is not None else 0.0
    except (TypeError, ValueError):
        return 0.0


def extract_location(item: Dict[str, Any]) -> str:
    properties = item.get("properties") if isinstance(item.get("properties"), dict) else {}
    title = (
        item.get("title")
        or properties.get("title")
        or item.get("location")
        or properties.get("location")
        or item.get("place")
        or properties.get("place")
        or item.get("region")
        or properties.get("region")
        or "Bilinmeyen Konum"
    )
    location_properties = item.get("location_properties") or properties.get("location_properties") or {}
    closest_city = location_properties.get("closestCity", {}) if isinstance(location_properties, dict) else {}
    city_name = closest_city.get("name") if isinstance(closest_city, dict) else None
    if not city_name:
        for key in ("city", "province", "il", "ilce", "district"):
            if item.get(key):
                city_name = item.get(key)
                break
        if not city_name and properties:
            for key in ("city", "province", "il", "ilce", "district"):
                if properties.get(key):
                    city_name = properties.get(key)
                    break
    location = f"{title} ({city_name})" if city_name else title
    return sanitize_text(location)


async def fetch_kandilli_earthquakes(hours_back: int, min_magnitude: float) -> List[Dict[str, Any]]:
    """Fetch earthquake data from configured sources with fallback."""
    global _kandilli_cache_data, _kandilli_cache_timestamp
    now = datetime.now()

    if (
        _kandilli_cache_data is not None
        and _kandilli_cache_timestamp
        and now - _kandilli_cache_timestamp < KANDILLI_CACHE_TTL
    ):
        return deepcopy(_kandilli_cache_data)

    cutoff_time = now - timedelta(hours=hours_back)
    last_error: Optional[Exception] = None

    async with httpx.AsyncClient(timeout=10.0) as client:
        for source_name, source_url in DATA_SOURCES:
            if not source_url:
                continue
            try:
                response = await client.get(source_url)
                response.raise_for_status()
                payload = response.json()
            except Exception as exc:  # pragma: no cover - network failure
                print(f"{source_name} API Error: {exc}")
                last_error = exc
                continue

            if isinstance(payload, dict):
                earthquake_list = payload.get("result") or payload.get("data") or payload.get("features") or []
            elif isinstance(payload, list):
                earthquake_list = payload
            else:
                earthquake_list = []

            earthquakes: List[Dict[str, Any]] = []
            for item in earthquake_list:
                properties = item.get("properties") if isinstance(item, dict) else {}
                raw_time = (
                    item.get("date")
                    or item.get("date_time")
                    or item.get("time")
                    or item.get("datetime")
                    or item.get("event_time")
                    or properties.get("time")
                    or properties.get("date")
                    or ""
                )

                earthquake_time: Optional[datetime] = None
                if isinstance(raw_time, (int, float)):
                    timestamp = float(raw_time)
                    if timestamp > 1_000_000_000_000:
                        timestamp /= 1000.0
                    earthquake_time = datetime.fromtimestamp(timestamp)
                else:
                    earthquake_time = parse_earthquake_time(raw_time)

                if earthquake_time is None or earthquake_time < cutoff_time:
                    continue

                magnitude = (
                    item.get("mag")
                    or item.get("magnitude")
                    or item.get("md")
                    or item.get("ml")
                    or item.get("mw")
                    or (properties.get("mag") if isinstance(properties, dict) else None)
                    or (properties.get("magnitude") if isinstance(properties, dict) else None)
                )
                try:
                    magnitude = float(magnitude) if magnitude is not None else 0.0
                except (TypeError, ValueError):
                    magnitude = 0.0
                if magnitude < min_magnitude:
                    continue

                coordinates = extract_coordinates(item)
                depth = extract_depth(item)
                location = extract_location(item)

                quake_id = (
                    item.get("earthquake_id")
                    or item.get("id")
                    or item.get("_id")
                    or item.get("event_id")
                    or (properties.get("id") if isinstance(properties, dict) else None)
                )
                if not quake_id:
                    quake_id = (
                        f"{source_name.lower()}-{earthquake_time.isoformat()}-"
                        f"{coordinates['lat']:.3f}-{coordinates['lng']:.3f}-{magnitude:.1f}"
                    )

                earthquakes.append(
                    {
                        "id": str(quake_id),
                        "magnitude": magnitude,
                        "location": location,
                        "time": earthquake_time,
                        "coordinates": coordinates,
                        "depth": depth,
                        "source": source_name,
                    }
                )

            if earthquakes:
                earthquakes.sort(key=lambda eq: eq["time"], reverse=True)
                _kandilli_cache_data = deepcopy(earthquakes)
                _kandilli_cache_timestamp = datetime.now()
                return earthquakes

    if last_error:
        print(f"All sources failed. Last error: {last_error}")
    if _kandilli_cache_data:
        return deepcopy(_kandilli_cache_data)
    return []


APP_NAME = os.getenv("APP_NAME", "yakınımdakideprem-api")
APP_ENV = os.getenv("APP_ENV", "dev")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")

origins_env = os.getenv("CORS_ORIGINS", "")
ALLOWED_ORIGINS = [origin.strip() for origin in origins_env.split(",") if origin.strip()]

app = FastAPI(title=APP_NAME, version=APP_VERSION)

earthquake_cache = EarthquakeCache(cache_duration_seconds=20)

if ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


class EarthquakeData(BaseModel):
    id: str
    magnitude: float
    location: str
    time: datetime
    time_ago: str
    coordinates: Dict[str, float]
    depth: float
    source: str


class EarthquakeResponse(BaseModel):
    success: bool
    data: List[EarthquakeData]
    last_update: datetime
    last_update_ago: str
    total_count: int


@app.get("/")
def root() -> Dict[str, Any]:
    return {
        "message": "Yakınımdaki Deprem API",
        "version": APP_VERSION,
        "environment": APP_ENV,
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "env": APP_ENV, "service": APP_NAME}


@app.get("/api/health")
def api_health() -> Dict[str, Any]:
    return {"status": "ok", "env": APP_ENV, "service": APP_NAME}


@app.get("/version")
def version() -> Dict[str, str]:
    return {"version": APP_VERSION}


@app.get("/api/echo")
def echo(q: str = "hello") -> Dict[str, str]:
    return {"echo": q}


@app.get("/api/earthquakes", response_model=EarthquakeResponse)
async def get_earthquakes(
    request: Request,
    response: Response,
    hours_back: int = Query(24, ge=1, le=720, description="Son kaç saatlik veriler"),
    min_magnitude: float = Query(2.0, ge=0, le=10, description="Minimum büyüklük"),
    limit: int = Query(100, ge=1, le=2000, description="Maksimum sonuç sayısı"),
) -> EarthquakeResponse:
    cache_key = f"earthquakes_{hours_back}_{min_magnitude}_{limit}"
    cached = earthquake_cache.get(cache_key)
    if cached:
        print(f"Cache hit for key: {cache_key}")
        etag = build_earthquake_etag(cached.get("data", []))
        cache_control = "public, max-age=10, stale-while-revalidate=20"
        if etag_matches(request, etag):
            return Response(
                status_code=304,
                headers={"ETag": format_etag(etag), "Cache-Control": cache_control},
            )
        response.headers["ETag"] = format_etag(etag)
        response.headers["Cache-Control"] = cache_control
        return EarthquakeResponse(**cached)

    try:
        earthquakes = await fetch_kandilli_earthquakes(hours_back, min_magnitude)
        earthquakes = earthquakes[:limit]

        now = datetime.now()
        response_payload = {
            "success": True,
            "data": [
                EarthquakeData(
                    id=eq["id"],
                    magnitude=eq["magnitude"],
                    location=eq["location"],
                    time=eq["time"],
                    time_ago=format_time_ago(eq["time"]),
                    coordinates=eq["coordinates"],
                    depth=eq["depth"],
                    source=eq["source"],
                )
                for eq in earthquakes
            ],
            "last_update": now,
            "last_update_ago": format_time_ago(now),
            "total_count": len(earthquakes),
        }

        earthquake_cache.set(cache_key, response_payload)
        print(f"Kandilli data cached with key: {cache_key}")

        etag = build_earthquake_etag(response_payload.get("data", []))
        cache_control = "public, max-age=10, stale-while-revalidate=20"
        if etag_matches(request, etag):
            return Response(
                status_code=304,
                headers={"ETag": format_etag(etag), "Cache-Control": cache_control},
            )
        response.headers["ETag"] = format_etag(etag)
        response.headers["Cache-Control"] = cache_control
        return EarthquakeResponse(**response_payload)

    except Exception as exc:
        print(f"Kandilli data fetch error: {exc}")
        now = datetime.now()
        sample = [
            EarthquakeData(
                id="sample1",
                magnitude=4.2,
                location=sanitize_text("Ankara, Türkiye"),
                time=now - timedelta(hours=1),
                time_ago=format_time_ago(now - timedelta(hours=1)),
                coordinates={"lat": 39.92, "lng": 32.85},
                depth=10.0,
                source="Sample",
            ),
            EarthquakeData(
                id="sample2",
                magnitude=3.5,
                location=sanitize_text("İzmir, Türkiye"),
                time=now - timedelta(hours=2),
                time_ago=format_time_ago(now - timedelta(hours=2)),
                coordinates={"lat": 38.42, "lng": 27.14},
                depth=8.0,
                source="Sample",
            ),
            EarthquakeData(
                id="sample3",
                magnitude=5.1,
                location=sanitize_text("Kahramanmaraş, Türkiye"),
                time=now - timedelta(hours=4),
                time_ago=format_time_ago(now - timedelta(hours=4)),
                coordinates={"lat": 37.58, "lng": 36.95},
                depth=15.0,
                source="Sample",
            ),
        ]

        response.headers["Cache-Control"] = "no-store"
        return EarthquakeResponse(
            success=False,
            data=sample,
            last_update=now,
            last_update_ago=format_time_ago(now),
            total_count=len(sample),
        )


@app.get("/api/earthquakes/stats")
async def get_earthquake_stats(request: Request, response: Response) -> Dict[str, Any]:
    try:
        earthquakes = await fetch_kandilli_earthquakes(24, 2.0)
        magnitudes = [eq["magnitude"] for eq in earthquakes if eq.get("magnitude")]
        now = datetime.now()

        stats = {
            "total_earthquakes": len(earthquakes),
            "max_magnitude": max(magnitudes) if magnitudes else 0,
            "min_magnitude": min(magnitudes) if magnitudes else 0,
            "avg_magnitude": sum(magnitudes) / len(magnitudes) if magnitudes else 0,
            "magnitude_3_plus": len([m for m in magnitudes if m >= 3.0]),
            "magnitude_4_plus": len([m for m in magnitudes if m >= 4.0]),
            "magnitude_5_plus": len([m for m in magnitudes if m >= 5.0]),
            "last_update": now.isoformat(),
            "last_update_ago": format_time_ago(now),
        }

        etag = build_stats_etag(stats)
        cache_control = "public, max-age=20, stale-while-revalidate=40"
        if etag_matches(request, etag):
            return Response(
                status_code=304,
                headers={"ETag": format_etag(etag), "Cache-Control": cache_control},
            )
        response.headers["ETag"] = format_etag(etag)
        response.headers["Cache-Control"] = cache_control
        return {"success": True, "stats": stats}

    except Exception as exc:
        print(f"Kandilli stats error: {exc}")
        now = datetime.now()
        response.headers["Cache-Control"] = "no-store"
        return {
            "success": False,
            "stats": {
                "total_earthquakes": 3,
                "max_magnitude": 5.1,
                "min_magnitude": 3.5,
                "avg_magnitude": 4.3,
                "magnitude_3_plus": 3,
                "magnitude_4_plus": 2,
                "magnitude_5_plus": 1,
                "last_update": now.isoformat(),
                "last_update_ago": format_time_ago(now),
            },
        }


@app.get("/api/pdf/first-aid-checklist")
async def download_first_aid_checklist() -> FileResponse:
    pdf_path = "checklist.pdf"

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF dosyası bulunamadı")

    return FileResponse(
        path=pdf_path,
        filename="ilk-yardim-cantasi-kontrol-listesi.pdf",
        media_type="application/pdf",
    )
