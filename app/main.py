import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any

import httpx
from fastapi import FastAPI, HTTPException, Query
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


class EarthquakeCache:
    """Simple in-memory cache for earthquake responses."""

    def __init__(self, cache_duration_minutes: int = 2) -> None:
        self.cache_duration = timedelta(minutes=cache_duration_minutes)
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


async def fetch_kandilli_earthquakes(hours_back: int, min_magnitude: float) -> List[Dict[str, Any]]:
    """Fetch earthquake data from Kandilli Observatory API."""
    kandilli_url = "https://api.orhanaydogdu.com.tr/deprem/kandilli/live"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(kandilli_url)
            response.raise_for_status()
            payload = response.json()
    except Exception as exc:  # pragma: no cover - network failure
        print(f"Kandilli API Error: {exc}")
        return []

    earthquake_list = payload.get("result", payload if isinstance(payload, list) else [])
    cutoff_time = datetime.now() - timedelta(hours=hours_back)

    earthquakes: List[Dict[str, Any]] = []
    for item in earthquake_list:
        raw_time = item.get("date") or item.get("date_time") or ""
        earthquake_time: Optional[datetime] = None

        for fmt in ("%Y.%m.%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
            if earthquake_time is None:
                try:
                    earthquake_time = datetime.strptime(raw_time, fmt)
                except ValueError:
                    continue

        if earthquake_time is None or earthquake_time < cutoff_time:
            continue
        if item.get("mag", 0) < min_magnitude:
            continue

        geojson = item.get("geojson", {})
        coordinates = geojson.get("coordinates", [0, 0, 0])

        title = item.get("title", "Bilinmeyen Konum")
        location_properties = item.get("location_properties", {})
        closest_city = location_properties.get("closestCity", {}) if isinstance(location_properties, dict) else {}
        city_name = closest_city.get("name") if isinstance(closest_city, dict) else None

        location = f"{title} ({city_name})" if city_name else title

        earthquakes.append(
            {
                "id": item.get("earthquake_id", ""),
                "magnitude": float(item.get("mag", 0.0)),
                "location": location,
                "time": earthquake_time,
                "coordinates": {
                    "lat": coordinates[1] if len(coordinates) > 1 else 0.0,
                    "lng": coordinates[0] if len(coordinates) > 0 else 0.0,
                },
                "depth": float(item.get("depth", 0.0)),
                "source": "Kandilli",
            }
        )

    earthquakes.sort(key=lambda eq: eq["time"], reverse=True)
    return earthquakes


APP_NAME = os.getenv("APP_NAME", "yakınımdakideprem-api")
APP_ENV = os.getenv("APP_ENV", "dev")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")

origins_env = os.getenv("CORS_ORIGINS", "")
ALLOWED_ORIGINS = [origin.strip() for origin in origins_env.split(",") if origin.strip()]

app = FastAPI(title=APP_NAME, version=APP_VERSION)

earthquake_cache = EarthquakeCache(cache_duration_minutes=2)

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
    hours_back: int = Query(24, ge=1, le=720, description="Son kaç saatlik veriler"),
    min_magnitude: float = Query(2.0, ge=0, le=10, description="Minimum büyüklük"),
    limit: int = Query(100, ge=1, le=2000, description="Maksimum sonuç sayısı"),
) -> EarthquakeResponse:
    cache_key = f"earthquakes_{hours_back}_{min_magnitude}_{limit}"
    cached = earthquake_cache.get(cache_key)
    if cached:
        print(f"Cache hit for key: {cache_key}")
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

        return EarthquakeResponse(**response_payload)

    except Exception as exc:
        print(f"Kandilli data fetch error: {exc}")
        now = datetime.now()
        sample = [
            EarthquakeData(
                id="sample1",
                magnitude=4.2,
                location="Ankara, Türkiye",
                time=now - timedelta(hours=1),
                time_ago=format_time_ago(now - timedelta(hours=1)),
                coordinates={"lat": 39.92, "lng": 32.85},
                depth=10.0,
                source="Sample",
            ),
            EarthquakeData(
                id="sample2",
                magnitude=3.5,
                location="İzmir, Türkiye",
                time=now - timedelta(hours=2),
                time_ago=format_time_ago(now - timedelta(hours=2)),
                coordinates={"lat": 38.42, "lng": 27.14},
                depth=8.0,
                source="Sample",
            ),
            EarthquakeData(
                id="sample3",
                magnitude=5.1,
                location="Kahramanmaraş, Türkiye",
                time=now - timedelta(hours=4),
                time_ago=format_time_ago(now - timedelta(hours=4)),
                coordinates={"lat": 37.58, "lng": 36.95},
                depth=15.0,
                source="Sample",
            ),
        ]

        return EarthquakeResponse(
            success=False,
            data=sample,
            last_update=now,
            last_update_ago=format_time_ago(now),
            total_count=len(sample),
        )


@app.get("/api/earthquakes/stats")
async def get_earthquake_stats() -> Dict[str, Any]:
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

        return {"success": True, "stats": stats}

    except Exception as exc:
        print(f"Kandilli stats error: {exc}")
        now = datetime.now()
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
