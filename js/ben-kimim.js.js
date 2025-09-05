// Global değişkenler
let map;
let earthquakeData = [];
let markers = [];
let refreshInterval;

// Sayfa yüklendiğinde çalışacak fonksiyon
document.addEventListener('DOMContentLoaded', () => {
    initMap();
    fetchEarthquakeData();
    setupEventListeners();
    updateStats();
    
    // Her 2 dakikada bir veri güncelle
    refreshInterval = setInterval(() => {
        fetchEarthquakeData();
        updateStats();
    }, 120000);
});

// Haritayı başlat
function initMap() {
    // Türkiye merkezli harita
    map = L.map('map').setView([39.0, 35.0], 6);
    
    // OpenStreetMap katmanı
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
}

// USGS API'den deprem verilerini çek
async function fetchEarthquakeData() {
    try {
        const params = new URLSearchParams({
            format: 'geojson',
            starttime: new Date(Date.now() - 86400000).toISOString(), // Son 24 saat
            latitude: 39.0,
            longitude: 35.0,
            maxradiuskm: 1000,
            minmagnitude: 2.5,
            orderby: 'magnitude-desc'
        });

        const response = await fetch(`https://earthquake.usgs.gov/fdsnws/event/1/query?${params}`);
        const data = await response.json();
        
        // Veriyi işle
        processEarthquakeData(data.features);
        
        // Son güncelleme zamanını güncelle
        const now = new Date();
        document.getElementById('last-update').textContent = 
            `Son güncelleme: ${now.toLocaleTimeString('tr-TR')}`;
        document.getElementById('last-update-time').textContent = 
            `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
            
    } catch (error) {
        console.error("Deprem verileri alınamadı:", error);
        document.getElementById('earthquake-items').innerHTML = 
            '<div class="loading">Veri alınamadı. Lütfen daha sonra tekrar deneyin.</div>';
    }
}

// Deprem verilerini işle
function processEarthquakeData(features) {
    earthquakeData = features.map(feature => ({
        id: feature.id,
        magnitude: feature.properties.mag,
        location: feature.properties.place,
        time: new Date(feature.properties.time),
        coordinates: {
            lat: feature.geometry.coordinates[1],
            lng: feature.geometry.coordinates[0]
        },
        depth: feature.geometry.coordinates[2],
        source: 'USGS'
    }));
    
    // Haritayı ve listeyi güncelle
    updateMap();
    updateEarthquakeList();
    updateStats();
}

// Haritayı güncelle
function updateMap() {
    // Eski işaretçileri temizle
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];
    
    // Yeni işaretçileri ekle
    earthquakeData.forEach(eq => {
        const intensity = Math.min(eq.magnitude / 8, 1); // 0-1 arası yoğunluk
        const radius = eq.magnitude * 15000; // Büyüklüğe göre yarıçap
        
        const marker = L.circle([eq.coordinates.lat, eq.coordinates.lng], {
            color: `rgba(255, 0, 0, ${intensity})`,
            fillColor: `rgba(255, 0, 0, ${intensity * 0.5})`,
            radius: radius,
            weight: 2
        }).addTo(map);
        
        // Popup ekle
        marker.bindPopup(`
            <div style="text-align: center; min-width: 200px;">
                <h3>${eq.location}</h3>
                <p><strong>Büyüklük:</strong> ${eq.magnitude.toFixed(1)}</p>
                <p><strong>Derinlik:</strong> ${eq.depth.toFixed(1)} km</p>
                <p><strong>Zaman:</strong> ${eq.time.toLocaleString('tr-TR')}</p>
                <p><small>Kaynak: ${eq.source}</small></p>
            </div>
        `);
        
        markers.push(marker);
    });
}

// Deprem listesini güncelle
function updateEarthquakeList() {
    const container = document.getElementById('earthquake-items');
    const filterValue = document.getElementById('magnitude-filter').value;
    
    // Filtre uygula
    let filteredData = earthquakeData;
    if (filterValue !== 'all') {
        filteredData = earthquakeData.filter(eq => eq.magnitude >= parseFloat(filterValue));
    }
    
    if (filteredData.length === 0) {
        container.innerHTML = '<div class="loading">Belirtilen kritere uygun deprem bulunamadı.</div>';
        return;
    }
    
    // Listeyi oluştur
    container.innerHTML = filteredData.map(eq => `
        <div class="earthquake-item" data-id="${eq.id}">
            <div class="magnitude" style="background-color: ${getMagnitudeColor(eq.magnitude)}">
                ${eq.magnitude.toFixed(1)}
            </div>
            <div class="details">
                <h3>${eq.location}</h3>
                <p class="time">${eq.time.toLocaleString('tr-TR')}</p>
                <p class="depth">Derinlik: ${eq.depth.toFixed(1)} km</p>
            </div>
        </div>
    `).join('');
    
    // Listeye tıklama olayı ekle
    document.querySelectorAll('.earthquake-item').forEach(item => {
        item.addEventListener('click', function() {
            const eqId = this.getAttribute('data-id');
            const eq = earthquakeData.find(e => e.id === eqId);
            if (eq) {
                map.setView([eq.coordinates.lat, eq.coordinates.lng], 8);
                markers.forEach(marker => {
                    if (marker.getLatLng().lat === eq.coordinates.lat && 
                        marker.getLatLng().lng === eq.coordinates.lng) {
                        marker.openPopup();
                    }
                });
            }
        });
    });
}

// İstatistikleri güncelle
function updateStats() {
    // Bugünkü deprem sayısı
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const todayQuakes = earthquakeData.filter(eq => {
        const eqDate = new Date(eq.time);
        eqDate.setHours(0, 0, 0, 0);
        return eqDate.getTime() === today.getTime();
    });
    
    document.getElementById('daily-quakes').textContent = todayQuakes.length;
    
    // En büyük deprem
    if (earthquakeData.length > 0) {
        const maxMag = Math.max(...earthquakeData.map(eq => eq.magnitude));
        document.getElementById('max-magnitude').textContent = maxMag.toFixed(1);
    }
}

// Büyüklüğe göre renk belirle
function getMagnitudeColor(mag) {
    if (mag >= 6) return '#d32f2f'; // Koyu kırmızı
    if (mag >= 5) return '#f44336'; // Kırmızı
    if (mag >= 4) return '#ff9800'; // Turuncu
    if (mag >= 3) return '#ffc107'; // Sarı
    return '#4caf50'; // Yeşil
}

// Olay dinleyicileri
function setupEventListeners() {
    // Yenileme butonu
    document.getElementById('refresh-btn').addEventListener('click', () => {
        // Yenileme animasyonu
        const btn = document.getElementById('refresh-btn');
        btn.querySelector('i').style.animation = 'spin 1s linear infinite';
        
        // Veriyi yeniden çek
        fetchEarthquakeData();
        
        // Animasyonu durdur
        setTimeout(() => {
            btn.querySelector('i').style.animation = '';
        }, 1000);
    });
    
    // Büyüklük filtresi
    document.getElementById('magnitude-filter').addEventListener('change', () => {
        updateEarthquakeList();
    });
    
    // Gizli header için scroll efekti
    let lastScrollTop = 0;
    const hiddenHeader = document.getElementById('hidden-header');
    
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Aşağı scroll - gizle
            hiddenHeader.style.top = '-80px';
        } else {
            // Yukarı scroll - göster
            hiddenHeader.style.top = '0';
        }
        
        lastScrollTop = scrollTop;
    });
}

// Sayfa kapatıldığında interval'i temizle
window.addEventListener('beforeunload', () => {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
});