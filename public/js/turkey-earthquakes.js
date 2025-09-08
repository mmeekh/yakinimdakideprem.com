/**
 * Türkiye'deki Son 5 Deprem - Özel JavaScript Modülü
 * Sadece Türkiye sınırları içindeki depremleri gösterir
 */

// Türkiye sınırları (yaklaşık koordinatlar)
const TURKEY_BOUNDS = {
  north: 42.0,
  south: 35.8,
  east: 45.0,
  west: 25.7
};

// Türkiye deprem verilerini saklamak için
let turkeyEarthquakes = [];

/**
 * Koordinatın Türkiye sınırları içinde olup olmadığını kontrol eder
 */
function isInTurkey(lat, lng) {
  return lat >= TURKEY_BOUNDS.south && 
         lat <= TURKEY_BOUNDS.north && 
         lng >= TURKEY_BOUNDS.west && 
         lng <= TURKEY_BOUNDS.east;
}

/**
 * Türkiye deprem verilerini API'den çeker
 */
async function fetchTurkeyEarthquakes() {
  try {
    const response = await fetch('/api/earthquakes?hours_back=168&min_magnitude=1.5&limit=500');
    const data = await response.json();
    
    if (data.success && data.data) {
      // Türkiye sınırları içindeki depremleri filtrele
      turkeyEarthquakes = data.data.filter(eq => 
        isInTurkey(eq.coordinates.lat, eq.coordinates.lng)
      );
      
      // Büyüklüğe göre sırala (en büyük önce)
      turkeyEarthquakes.sort((a, b) => b.magnitude - a.magnitude);
      
      updateTurkeyEarthquakesDisplay();
    }
  } catch (error) {
    console.error('Türkiye deprem verileri alınamadı:', error);
    showTurkeyEarthquakesError();
  }
}

/**
 * Türkiye deprem listesini günceller
 */
function updateTurkeyEarthquakesDisplay() {
  const container = document.querySelector('.recent-earthquakes');
  if (!container) return;

  // Loading placeholder'ı kaldır
  const loadingPlaceholder = container.querySelector('.loading-placeholder');
  if (loadingPlaceholder) {
    loadingPlaceholder.remove();
  }

  // Mevcut içeriği temizle
  container.innerHTML = '';

  if (turkeyEarthquakes.length === 0) {
    // Türkiye'de deprem yoksa
    const noDataMessage = document.createElement('div');
    noDataMessage.className = 'no-data-message';
    noDataMessage.innerHTML = `
      <i class="fas fa-info-circle"></i>
      <span>Son 7 günde Türkiye'de deprem kaydedilmedi</span>
    `;
    container.appendChild(noDataMessage);
    return;
  }

  // En büyük 5 depremi göster
  const top5Earthquakes = turkeyEarthquakes.slice(0, 5);

  top5Earthquakes.forEach((eq, index) => {
    const earthquakeItem = document.createElement('div');
    earthquakeItem.className = 'earthquake-item-small';
    
    // Büyüklük
    const magnitude = document.createElement('span');
    magnitude.className = 'magnitude-small';
    magnitude.textContent = eq.magnitude.toFixed(1);
    
    // Büyüklüğe göre renk ataması (legend ile uyumlu)
    magnitude.style.backgroundColor = getMagnitudeColor(eq.magnitude);
    
    // Konum (Türkçe format)
    const location = document.createElement('span');
    location.className = 'location-small';
    location.textContent = formatTurkeyLocation(eq.location);
    
    earthquakeItem.appendChild(magnitude);
    earthquakeItem.appendChild(location);
    container.appendChild(earthquakeItem);
  });
}

/**
 * Deprem büyüklüğüne göre renk döndürür (legend ile uyumlu)
 */
function getMagnitudeColor(magnitude) {
  if (magnitude >= 8.0) {
    return '#7b1fa2'; // 8.0+ - Mor
  } else if (magnitude >= 7.0) {
    return '#d32f2f'; // 7.0 - 7.9 - Koyu Kırmızı
  } else if (magnitude >= 6.0) {
    return '#f44336'; // 6.0 - 6.9 - Kırmızı
  } else if (magnitude >= 5.0) {
    return '#ff5722'; // 5.0 - 5.9 - Turuncu-Kırmızı
  } else if (magnitude >= 4.0) {
    return '#ff9800'; // 4.0 - 4.9 - Turuncu
  } else if (magnitude >= 3.0) {
    return '#ffc107'; // 3.0 - 3.9 - Sarı
  } else {
    return '#4caf50'; // 0 - 2.9 - Yeşil
  }
}

/**
 * Konum bilgisini Türkçe formatına çevirir
 */
function formatTurkeyLocation(location) {
  if (!location || location === 'Unknown Location') {
    return 'Türkiye';
  }

  // Yaygın Türkiye şehir isimlerini kontrol et
  const turkeyCities = [
    'Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Antalya', 'Adana', 'Konya', 'Gaziantep',
    'Mersin', 'Diyarbakir', 'Kayseri', 'Eskisehir', 'Urfa', 'Malatya', 'Erzurum',
    'Van', 'Batman', 'Elazig', 'Isparta', 'Trabzon', 'Ordu', 'Sivas', 'Kahramanmaras',
    'Erzincan', 'Aydin', 'Denizli', 'Manisa', 'Balikesir', 'Kahramanmaras', 'Sakarya'
  ];

  // Türkiye şehir isimlerini kontrol et
  for (const city of turkeyCities) {
    if (location.toLowerCase().includes(city.toLowerCase())) {
      return city + ', Türkiye';
    }
  }

  // Türkiye kelimesi varsa
  if (location.toLowerCase().includes('turkey') || location.toLowerCase().includes('türkiye')) {
    return location.replace(/turkey/gi, 'Türkiye');
  }

  // Diğer durumlarda sadece "Türkiye" yaz
  return 'Türkiye';
}

/**
 * Hata durumunda gösterilecek mesaj
 */
function showTurkeyEarthquakesError() {
  const container = document.querySelector('.recent-earthquakes');
  if (!container) return;

  container.innerHTML = `
    <div class="error-message">
      <i class="fas fa-exclamation-triangle"></i>
      <span>Veriler yüklenirken hata oluştu</span>
    </div>
  `;
}

/**
 * Sayfa yüklendiğinde çalışır
 */
document.addEventListener('DOMContentLoaded', () => {
  // Sayfa yüklendikten sonra kısa bir gecikme ile veri çek
  setTimeout(() => {
    fetchTurkeyEarthquakes();
  }, 1000);

  // Her 5 dakikada bir güncelle
  setInterval(() => {
    fetchTurkeyEarthquakes();
  }, 300000); // 5 dakika
});

// Global olarak erişilebilir yap
window.TurkeyEarthquakes = {
  fetch: fetchTurkeyEarthquakes,
  update: updateTurkeyEarthquakesDisplay
};
