import os
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Türkiye sınırları (yaklaşık koordinatlar)
TURKEY_BOUNDS = {
    "north": 42.0,
    "south": 35.8,
    "east": 45.0,
    "west": 25.7
}

def is_in_turkey(lat: float, lng: float) -> bool:
    """Koordinatın Türkiye sınırları içinde olup olmadığını kontrol eder"""
    return (lat >= TURKEY_BOUNDS["south"] and 
            lat <= TURKEY_BOUNDS["north"] and 
            lng >= TURKEY_BOUNDS["west"] and 
            lng <= TURKEY_BOUNDS["east"])

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

async def fetch_kandilli_earthquakes(hours_back: int, min_magnitude: float) -> List[Dict[str, Any]]:
    """Kandilli Rasathanesi API'den Türkiye depremlerini çek"""
    try:
        kandilli_url = "https://api.orhanaydogdu.com.tr/deprem/kandilli/live"
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(kandilli_url)
            response.raise_for_status()
            data = response.json()
            
        # Kandilli API response formatını kontrol et
        if isinstance(data, dict) and "result" in data:
            earthquake_list = data["result"]
        else:
            earthquake_list = data
            
        # Verileri işle ve filtrele
        earthquakes = []
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        for item in earthquake_list:
            # Tarih formatını parse et
            try:
                earthquake_time = datetime.strptime(item.get("date", ""), "%Y.%m.%d %H:%M:%S")
            except ValueError:
                try:
                    earthquake_time = datetime.strptime(item.get("date_time", ""), "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue
            
            # Zaman ve büyüklük filtresi
            if earthquake_time < cutoff_time or item.get("mag", 0) < min_magnitude:
                continue
                
            # GeoJSON koordinatlarını al
            geojson = item.get("geojson", {})
            coordinates = geojson.get("coordinates", [0, 0])
            
            # Konum bilgisini al
            title = item.get("title", "Bilinmeyen Konum")
            location_properties = item.get("location_properties", {})
            closest_city = location_properties.get("closestCity", {})
            
            if closest_city:
                city_name = closest_city.get("name", "")
                if city_name:
                    location = f"{title} ({city_name})"
                else:
                    location = title
            else:
                location = title
            
            earthquake = {
                "id": item.get("earthquake_id", ""),
                "magnitude": item.get("mag", 0.0),
                "location": location,
                "time": earthquake_time,
                "coordinates": {
                    "lat": coordinates[1] if len(coordinates) > 1 else 0,
                    "lng": coordinates[0] if len(coordinates) > 0 else 0
                },
                "depth": item.get("depth", 0.0),
                "source": "Kandilli"
            }
            earthquakes.append(earthquake)
            
        return earthquakes
        
    except Exception as e:
        print(f"Kandilli API Error: {str(e)}")
        return []

async def fetch_usgs_earthquakes(hours_back: int, min_magnitude: float) -> List[Dict[str, Any]]:
    """USGS API'den dünya depremlerini çek (Türkiye dışı)"""
    try:
        usgs_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        # USGS için minimum büyüklüğü düşür (daha fazla dünya depremi için)
        usgs_min_magnitude = max(min_magnitude, 1.5)  # En az 1.5, ama parametre daha yüksekse onu kullan
        params = {
            "format": "geojson",
            "starttime": (datetime.now() - timedelta(hours=hours_back)).isoformat(),
            "minmagnitude": usgs_min_magnitude,
            "orderby": "time",
            "limit": 500  # Çok daha fazla veri al
        }
        
        print(f"USGS API Request: {usgs_url}")
        print(f"USGS API Params: {params}")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(usgs_url, params=params)
            response.raise_for_status()
            data = response.json()
            
        print(f"USGS API Response: {len(data.get('features', []))} total earthquakes found")
        
        earthquakes = []
        turkey_count = 0
        for feature in data.get("features", []):
            coordinates = feature.get("geometry", {}).get("coordinates", [0, 0, 0])
            lat, lng = coordinates[1], coordinates[0]
            
            # Sadece Türkiye dışındaki depremleri al
            if is_in_turkey(lat, lng):
                turkey_count += 1
                continue
                
            earthquake_time = datetime.fromtimestamp(feature.get("properties", {}).get("time", 0) / 1000)
            
            earthquake = {
                "id": feature.get("id", ""),
                "magnitude": feature.get("properties", {}).get("mag", 0.0),
                "location": feature.get("properties", {}).get("place", "Unknown Location"),
                "time": earthquake_time,
                "coordinates": {"lat": lat, "lng": lng},
                "depth": coordinates[2] or 0,
                "source": "USGS"
            }
            earthquakes.append(earthquake)
        
        print(f"USGS: {len(earthquakes)} non-Turkey earthquakes, {turkey_count} Turkey earthquakes filtered out")
        return earthquakes
        
    except Exception as e:
        print(f"USGS API Error: {str(e)}")
        return []

APP_NAME = os.getenv("APP_NAME", "yakınımdakideprem-api")
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

@app.get("/")
def root():
    return {
        "message": "Yakınımdaki Deprem API",
        "version": APP_VERSION,
        "environment": APP_ENV,
        "docs": "/docs",
        "health": "/health"
    }

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
    min_magnitude: float = Query(2.0, ge=0, le=10, description="Minimum büyüklük"),  # 2.0+ (Kandilli standardı)
    limit: int = Query(100, ge=1, le=2000, description="Maksimum sonuç sayısı"),
    mode: str = Query("hybrid", description="Veri modu: hybrid, turkey, global")
):
    """Deprem verilerini getir - Hibrit sistem (Türkiye: Kandilli, Dünya: USGS)"""
    # Cache key oluştur
    cache_key = f"{mode}_earthquakes_{hours_back}_{min_magnitude}_{limit}"
    
    # Cache'den kontrol et
    cached_data = earthquake_cache.get(cache_key)
    if cached_data:
        print(f"Cache hit for key: {cache_key}")
        return EarthquakeResponse(**cached_data)
    
    try:
        print(f"Fetching {mode} earthquake data...")
        
        if mode == "turkey":
            # Sadece Türkiye verileri (Kandilli)
            kandilli_earthquakes = await fetch_kandilli_earthquakes(hours_back, min_magnitude)
            usgs_earthquakes = []
        elif mode == "global":
            # Sadece dünya verileri (USGS)
            kandilli_earthquakes = []
            usgs_earthquakes = await fetch_usgs_earthquakes(hours_back, min_magnitude)
        else:
            # Hibrit sistem (varsayılan)
            kandilli_task = fetch_kandilli_earthquakes(hours_back, min_magnitude)
            usgs_task = fetch_usgs_earthquakes(hours_back, min_magnitude)
            
            kandilli_earthquakes, usgs_earthquakes = await asyncio.gather(
                kandilli_task, usgs_task, return_exceptions=True
            )
        
        # Hata kontrolü
        if isinstance(kandilli_earthquakes, Exception):
            print(f"Kandilli API failed: {kandilli_earthquakes}")
            kandilli_earthquakes = []
        if isinstance(usgs_earthquakes, Exception):
            print(f"USGS API failed: {usgs_earthquakes}")
            usgs_earthquakes = []
        
        print(f"Kandilli: {len(kandilli_earthquakes)} earthquakes")
        print(f"USGS: {len(usgs_earthquakes)} earthquakes")
        
        # Verileri birleştir ve EarthquakeData formatına çevir
        all_earthquakes = []
        
        # Kandilli verilerini ekle
        for eq in kandilli_earthquakes:
            earthquake = EarthquakeData(
                id=eq["id"],
                magnitude=eq["magnitude"],
                location=eq["location"],
                time=eq["time"],
                time_ago=format_time_ago(eq["time"]),
                coordinates=eq["coordinates"],
                depth=eq["depth"],
                source=eq["source"]
            )
            all_earthquakes.append(earthquake)
        
        # USGS verilerini ekle
        for eq in usgs_earthquakes:
            earthquake = EarthquakeData(
                id=eq["id"],
                magnitude=eq["magnitude"],
                location=eq["location"],
                time=eq["time"],
                time_ago=format_time_ago(eq["time"]),
                coordinates=eq["coordinates"],
                depth=eq["depth"],
                source=eq["source"]
            )
            all_earthquakes.append(earthquake)
        
        # Zamana göre sırala (en yeni önce)
        all_earthquakes.sort(key=lambda x: x.time, reverse=True)
        
        # Limit uygula
        all_earthquakes = all_earthquakes[:limit]
        
        now = datetime.now()
        response_data = {
            "success": True,
            "data": all_earthquakes,
            "last_update": now,
            "last_update_ago": format_time_ago(now),
            "total_count": len(all_earthquakes)
        }
        
        # Cache'e kaydet
        earthquake_cache.set(cache_key, response_data)
        print(f"{mode.title()} data cached with key: {cache_key}")
        
        return EarthquakeResponse(**response_data)
        
    except Exception as e:
        # Hata durumunda örnek veri döndür
        print(f"Hybrid API Error: {str(e)}")
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
    """Deprem istatistiklerini getir - Hibrit sistem"""
    try:
        print("Fetching hybrid earthquake stats...")
        
        # Her iki API'den paralel olarak veri çek
        kandilli_task = fetch_kandilli_earthquakes(24, 2.0)  # Son 24 saat, 2.0+
        usgs_task = fetch_usgs_earthquakes(24, 2.0)  # Son 24 saat, 2.0+ (dünya için de aynı threshold)
        
        kandilli_earthquakes, usgs_earthquakes = await asyncio.gather(
            kandilli_task, usgs_task, return_exceptions=True
        )
        
        # Hata kontrolü
        if isinstance(kandilli_earthquakes, Exception):
            print(f"Kandilli stats API failed: {kandilli_earthquakes}")
            kandilli_earthquakes = []
        if isinstance(usgs_earthquakes, Exception):
            print(f"USGS stats API failed: {usgs_earthquakes}")
            usgs_earthquakes = []
        
        # Tüm depremleri birleştir
        all_earthquakes = kandilli_earthquakes + usgs_earthquakes
        magnitudes = [eq["magnitude"] for eq in all_earthquakes if eq.get("magnitude")]
        
        now = datetime.now()
        stats = {
            "total_earthquakes": len(all_earthquakes),
            "kandilli_earthquakes": len(kandilli_earthquakes),
            "usgs_earthquakes": len(usgs_earthquakes),
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
        print(f"Hybrid stats API Error: {str(e)}")
        now = datetime.now()
        return {
            "success": False,
            "stats": {
                "total_earthquakes": 3,
                "kandilli_earthquakes": 2,
                "usgs_earthquakes": 1,
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

@app.get("/api/pdf/first-aid-checklist")
async def download_first_aid_checklist():
    """İlk yardım çantası kontrol listesi PDF'ini indir - Static dosya"""
    try:
        # Static PDF dosyasını döndür
        pdf_path = "checklist.pdf"
        
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=404, detail="PDF dosyası bulunamadı")
        
        return FileResponse(
            path=pdf_path,
            filename="ilk-yardim-cantasi-kontrol-listesi.pdf",
            media_type="application/pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF indirme hatası: {str(e)}")
