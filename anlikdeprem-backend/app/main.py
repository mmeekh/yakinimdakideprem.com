import os
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

def format_time_ago(dt: datetime) -> str:
    """Zamanı 'xx dakika xx saniye önce' formatında döndür"""
    now = datetime.now()
    diff = now - dt
    
    total_seconds = int(diff.total_seconds())
    
    if total_seconds < 60:
        return f"{total_seconds} saniye önce"
    elif total_seconds < 3600:  # 1 saatten az
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        if seconds == 0:
            return f"{minutes} dakika önce"
        else:
            return f"{minutes} dakika {seconds} saniye önce"
    elif total_seconds < 86400:  # 1 günden az
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        if minutes == 0:
            return f"{hours} saat önce"
        else:
            return f"{hours} saat {minutes} dakika önce"
    else:  # 1 günden fazla
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        if hours == 0:
            return f"{days} gün önce"
        else:
            return f"{days} gün {hours} saat önce"

class EarthquakeCache:
    """Basit deprem verisi cache sınıfı"""
    
    def __init__(self, cache_duration_minutes: int = 2):
        self.cache_duration = timedelta(minutes=cache_duration_minutes)
        self.cache: Dict[str, Dict[str, Any]] = {}
    
    def get(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Cache'den veri al"""
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if datetime.now() - cached_data['timestamp'] < self.cache_duration:
                return cached_data['data']
            else:
                # Cache süresi dolmuş, sil
                del self.cache[cache_key]
        return None
    
    def set(self, cache_key: str, data: Dict[str, Any]) -> None:
        """Cache'e veri kaydet"""
        self.cache[cache_key] = {
            'data': data,
            'timestamp': datetime.now()
        }
    
    def clear(self) -> None:
        """Cache'i temizle"""
        self.cache.clear()

APP_NAME = os.getenv("APP_NAME", "anlikdeprem-api")
APP_ENV = os.getenv("APP_ENV", "dev")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")

# CORS
origins_env = os.getenv("CORS_ORIGINS", "")
ALLOWED_ORIGINS = [o.strip() for o in origins_env.split(",") if o.strip()]

app = FastAPI(title=APP_NAME, version=APP_VERSION)

# Cache instance
earthquake_cache = EarthquakeCache(cache_duration_minutes=2)

if ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Pydantic models
class EarthquakeData(BaseModel):
    id: str
    magnitude: float
    location: str
    time: datetime
    time_ago: str  # "xx dakika xx saniye önce" formatında
    coordinates: dict
    depth: float
    source: str

class EarthquakeResponse(BaseModel):
    success: bool
    data: List[EarthquakeData]
    last_update: datetime
    last_update_ago: str  # "xx dakika xx saniye önce" formatında
    total_count: int

@app.get("/health")
def health():
    return {"status": "ok", "env": APP_ENV, "service": APP_NAME}

@app.get("/version")
def version():
    return {"version": APP_VERSION}

@app.get("/api/echo")
def echo(q: str = "hello"):
    return {"echo": q}

@app.get("/api/earthquakes", response_model=EarthquakeResponse)
async def get_earthquakes(
    hours_back: int = Query(24, ge=1, le=720, description="Son kaç saatlik veriler"),  # 24 saat
    min_magnitude: float = Query(2.5, ge=0, le=10, description="Minimum büyüklük"),  # 2.5+ (USGS standardı)
    limit: int = Query(100, ge=1, le=500, description="Maksimum sonuç sayısı")
):
    """Deprem verilerini getir"""
    # Cache key oluştur
    cache_key = f"earthquakes_{hours_back}_{min_magnitude}_{limit}"
    
    # Cache'den kontrol et
    cached_data = earthquake_cache.get(cache_key)
    if cached_data:
        print(f"Cache hit for key: {cache_key}")
        return EarthquakeResponse(**cached_data)
    
    try:
        # USGS API'den veri çek - Global veri için parametreleri düzelt
        usgs_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        params = {
            "format": "geojson",
            "starttime": (datetime.now() - timedelta(hours=hours_back)).isoformat(),
            "minmagnitude": min_magnitude,
            "orderby": "time",  # Zamana göre sırala (en yeni → en eski)
            "limit": limit
        }
        
        # Global veri için koordinat ve yarıçap parametrelerini kaldır
        # USGS API global veri için bu parametreleri gerektirmez
        
        print(f"USGS API Request: {usgs_url}")
        print(f"USGS API Params: {params}")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(usgs_url, params=params)
            response.raise_for_status()
            data = response.json()
            
        print(f"USGS API Response: {len(data.get('features', []))} earthquakes found")
        
        # Verileri işle
        earthquakes = []
        for feature in data.get("features", []):
            earthquake_time = datetime.fromtimestamp(feature.get("properties", {}).get("time", 0) / 1000)
            earthquake = EarthquakeData(
                id=feature.get("id", ""),
                magnitude=feature.get("properties", {}).get("mag", 0.0),
                location=feature.get("properties", {}).get("place", "Unknown Location"),
                time=earthquake_time,
                time_ago=format_time_ago(earthquake_time),
                coordinates={
                    "lat": feature.get("geometry", {}).get("coordinates", [0, 0, 0])[1],
                    "lng": feature.get("geometry", {}).get("coordinates", [0, 0, 0])[0]
                },
                depth=feature.get("geometry", {}).get("coordinates", [0, 0, 0])[2] or 0,
                source="USGS"
            )
            earthquakes.append(earthquake)
        
        now = datetime.now()
        response_data = {
            "success": True,
            "data": earthquakes,
            "last_update": now,
            "last_update_ago": format_time_ago(now),
            "total_count": len(earthquakes)
        }
        
        # Cache'e kaydet
        earthquake_cache.set(cache_key, response_data)
        print(f"Data cached with key: {cache_key}")
        
        return EarthquakeResponse(**response_data)
        
    except Exception as e:
        # Hata durumunda örnek veri döndür
        print(f"USGS API Error: {str(e)}")
        now = datetime.now()
        sample_earthquakes = [
            EarthquakeData(
                id="sample1",
                magnitude=4.2,
                location="Ankara, Türkiye",
                time=now - timedelta(hours=1),
                time_ago=format_time_ago(now - timedelta(hours=1)),
                coordinates={"lat": 39.92, "lng": 32.85},
                depth=10.0,
                source="Sample"
            ),
            EarthquakeData(
                id="sample2",
                magnitude=3.5,
                location="İzmir, Türkiye",
                time=now - timedelta(hours=2),
                time_ago=format_time_ago(now - timedelta(hours=2)),
                coordinates={"lat": 38.42, "lng": 27.14},
                depth=8.0,
                source="Sample"
            ),
            EarthquakeData(
                id="sample3",
                magnitude=5.1,
                location="Kahramanmaraş, Türkiye",
                time=now - timedelta(hours=4),
                time_ago=format_time_ago(now - timedelta(hours=4)),
                coordinates={"lat": 37.58, "lng": 36.95},
                depth=15.0,
                source="Sample"
            )
        ]
        
        return EarthquakeResponse(
            success=False,
            data=sample_earthquakes,
            last_update=now,
            last_update_ago=format_time_ago(now),
            total_count=len(sample_earthquakes)
        )

@app.get("/api/earthquakes/stats")
async def get_earthquake_stats():
    """Deprem istatistiklerini getir"""
    try:
        # Son 24 saatlik global verileri al
        usgs_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        params = {
            "format": "geojson",
            "starttime": (datetime.now() - timedelta(hours=24)).isoformat(),
            "minmagnitude": 2.5,
            "orderby": "magnitude",
            "limit": 1000
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(usgs_url, params=params)
            response.raise_for_status()
            data = response.json()
        
        features = data.get("features", [])
        magnitudes = [f.get("properties", {}).get("mag", 0) for f in features if f.get("properties", {}).get("mag")]
        
        now = datetime.now()
        stats = {
            "total_earthquakes": len(features),
            "max_magnitude": max(magnitudes) if magnitudes else 0,
            "min_magnitude": min(magnitudes) if magnitudes else 0,
            "avg_magnitude": sum(magnitudes) / len(magnitudes) if magnitudes else 0,
            "magnitude_3_plus": len([m for m in magnitudes if m >= 3.0]),
            "magnitude_4_plus": len([m for m in magnitudes if m >= 4.0]),
            "magnitude_5_plus": len([m for m in magnitudes if m >= 5.0]),
            "last_update": now.isoformat(),
            "last_update_ago": format_time_ago(now)
        }
        
        return {"success": True, "stats": stats}
        
    except Exception as e:
        # Hata durumunda örnek istatistikler
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
                "last_update_ago": format_time_ago(now)
            }
        }
