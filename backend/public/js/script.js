/**
 * Yakınımdaki Deprem - Ana JavaScript Modülü
 * Optimized version with better error handling and performance
 */

// Global state management
const AppState = {
  map: null,
  earthquakeData: [],
  markers: [],
  refreshInterval: null,
  timeUpdateInterval: null,
  isInitialized: false,
  lastUpdateTime: null,
  lastDataHash: null // Veri değişikliğini kontrol etmek için
};

// Configuration constants
const CONFIG = {
  REFRESH_INTERVAL: 60000, // 1 minute
  MAP_CENTER: [39.0, 35.0], // Türkiye merkezi
  MAP_ZOOM: 6, // Türkiye'yi tam gösteren zoom seviyesi
  API_TIMEOUT: 10000,
  MAX_RADIUS_KM: 5000, // Çok geniş alan
  MIN_MAGNITUDE: 1.0, // Çok düşük büyüklük
  HOURS_BACK: 168 // 1 hafta
};

// Utility functions
const Utils = {
  formatTime: (date) => date.toLocaleTimeString("tr-TR"),
  formatDateTime: (date) => date.toLocaleString("tr-TR"),
  debounce: (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }
};

// Initialize application
document.addEventListener("DOMContentLoaded", () => {
  try {
    initApp();
  } catch (error) {
    console.error("Uygulama başlatılamadı:", error);
    showErrorMessage("Uygulama başlatılırken bir hata oluştu.");
  }
});

async function initApp() {
  if (AppState.isInitialized) return;
  
  initMap();
  await fetchEarthquakeData();
  setupEventListeners();
  updateStats();
  startAutoRefresh();
  
  AppState.isInitialized = true;
}

// Map initialization
function initMap() {
  try {
    // Show loading indicator
    const mapContainer = document.getElementById("map");
    if (mapContainer) {
      mapContainer.innerHTML = '<div class="map-loading"><i class="fas fa-spinner fa-spin"></i>Harita yükleniyor...</div>';
    }

    AppState.map = L.map("map").setView(CONFIG.MAP_CENTER, CONFIG.MAP_ZOOM);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 18,
      minZoom: 4
    }).addTo(AppState.map);

    // Hide loading indicator when map is ready
    AppState.map.whenReady(() => {
      console.log("Harita başarıyla yüklendi");
      // Harita yüklendikten sonra boyutlandır
      setTimeout(() => {
        AppState.map.invalidateSize();
        console.log("Harita boyutlandırıldı");
        
        // Harita genişliğini zorla ayarla
        resizeMapContainer();
      }, 100);
    });
  } catch (error) {
    console.error("Harita başlatılamadı:", error);
    showErrorMessage("Harita yüklenirken bir hata oluştu.");
  }
}

// Fetch earthquake data from USGS API
async function fetchEarthquakeData() {
  const startTime = Date.now();
  
  try {
    const params = new URLSearchParams({
      format: "geojson",
      starttime: new Date(Date.now() - CONFIG.HOURS_BACK * 3600000).toISOString(),
      latitude: CONFIG.MAP_CENTER[0],
      longitude: CONFIG.MAP_CENTER[1],
      maxradiuskm: CONFIG.MAX_RADIUS_KM,
      minmagnitude: CONFIG.MIN_MAGNITUDE,
      orderby: "magnitude-desc",
      limit: 100
    });

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), CONFIG.API_TIMEOUT);

    const response = await fetch(
      `/api/earthquakes?${params}`,
      { signal: controller.signal }
    );

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`Backend API hata kodu: ${response.status}`);
    }

    const data = await response.json();
    
    // Veri değişikliğini kontrol et
    const currentDataHash = generateDataHash(data.data);
    const hasDataChanged = AppState.lastDataHash !== currentDataHash;
    
    if (data.success) {
      if (data.data && data.data.length > 0) {
        // Gerçek veri var
        if (hasDataChanged) {
          processEarthquakeData(data.data);
          updateLastUpdateTime(false, data.last_update_ago);
          AppState.lastDataHash = currentDataHash;
          console.log(`Yeni veri yüklendi: ${data.data.length} deprem`);
        } else {
          console.log('Veri değişmedi, sadece zaman güncelleniyor');
          updateLastUpdateTime(false, data.last_update_ago);
        }
      } else {
        // Gerçek veri yok, örnek veri göster
        console.log('Gerçek veri bulunamadı, örnek veriler gösteriliyor');
        loadSampleData();
      }
    } else {
      // Backend'den örnek veri geldi
      if (hasDataChanged) {
        processEarthquakeData(data.data);
        updateLastUpdateTime(true, data.last_update_ago);
        AppState.lastDataHash = currentDataHash;
        console.log('Backend\'den yeni örnek veriler gösteriliyor');
      } else {
        console.log('Örnek veri değişmedi, sadece zaman güncelleniyor');
        updateLastUpdateTime(true, data.last_update_ago);
      }
    }
    
    console.log(`Veri yükleme süresi: ${Date.now() - startTime}ms`);
  } catch (error) {
    console.error("Deprem verileri alınamadı:", error);
    handleDataFetchError(error);
  }
}

// Handle data fetch errors
function handleDataFetchError(error) {
  if (error.name === 'AbortError') {
    showErrorMessage("Veri yükleme zaman aşımına uğradı. Lütfen tekrar deneyin.");
  } else {
    showErrorMessage("Veri yüklenirken bir hata oluştu. Örnek veriler gösteriliyor.");
    loadSampleData();
  }
}

// Load sample data when API fails
function loadSampleData() {
  const sampleFeatures = [
    {
      id: "sample1",
      properties: {
        mag: 4.2,
        place: "Ankara, Türkiye",
        time: Date.now() - 3600000,
      },
      geometry: { coordinates: [32.85, 39.92, 10] },
    },
    {
      id: "sample2",
      properties: {
        mag: 3.5,
        place: "İzmir, Türkiye",
        time: Date.now() - 7200000,
      },
      geometry: { coordinates: [27.14, 38.42, 8] },
    },
    {
      id: "sample3",
      properties: {
        mag: 5.1,
        place: "Kahramanmaraş, Türkiye",
        time: Date.now() - 14400000,
      },
      geometry: { coordinates: [36.95, 37.58, 15] },
    },
  ];

  processEarthquakeData(sampleFeatures);
  updateLastUpdateTime(true);
}

// Generate hash for data to detect changes
function generateDataHash(data) {
  if (!data || !Array.isArray(data)) return null;
  
  // Create a simple hash based on earthquake IDs and times
  const hashString = data.map(eq => `${eq.id}-${eq.time}`).join('|');
  let hash = 0;
  for (let i = 0; i < hashString.length; i++) {
    const char = hashString.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32-bit integer
  }
  return hash.toString();
}

// Format time ago in Turkish
function formatTimeAgo(date) {
  const now = new Date();
  const diff = now - date;
  const totalSeconds = Math.floor(diff / 1000);
  
  if (totalSeconds < 60) {
    if (totalSeconds === 0) {
      return "az önce";
    }
    return `${totalSeconds} saniye önce`;
  } else if (totalSeconds < 3600) { // 1 saatten az
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    if (seconds === 0) {
      return `${minutes} dakika önce`;
    } else {
      return `${minutes} dakika ${seconds} saniye önce`;
    }
  } else if (totalSeconds < 86400) { // 1 günden az
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    if (minutes === 0) {
      return `${hours} saat önce`;
    } else {
      return `${hours} saat ${minutes} dakika önce`;
    }
  } else { // 1 günden fazla
    const days = Math.floor(totalSeconds / 86400);
    const hours = Math.floor((totalSeconds % 86400) / 3600);
    if (hours === 0) {
      return `${days} gün önce`;
    } else {
      return `${days} gün ${hours} saat önce`;
    }
  }
}

// Update last update time display
function updateLastUpdateTime(isSample = false, lastUpdateAgo = null) {
  const now = new Date();
  
  const lastUpdateEl = document.getElementById("last-update");
  const lastUpdateTimeEl = document.getElementById("last-update-time");
  
  if (lastUpdateEl) {
    if (isSample) {
      lastUpdateEl.textContent = "Son güncelleme: Örnek veriler gösteriliyor";
    } else {
      // Her zaman dinamik zaman göster (backend'den gelen veya fallback)
      const timeToShow = lastUpdateAgo || formatTimeAgo(now);
      lastUpdateEl.textContent = `Son güncelleme: ${timeToShow}`;
    }
  }
  
  if (lastUpdateTimeEl) {
    if (isSample) {
      lastUpdateTimeEl.textContent = "--:--";
    } else {
      const timeToShow = lastUpdateAgo || formatTimeAgo(now);
      lastUpdateTimeEl.textContent = timeToShow;
    }
  }
  
  AppState.lastUpdateTime = now;
}

// Process earthquake data from backend API
function processEarthquakeData(earthquakes) {
  AppState.earthquakeData = earthquakes.map((earthquake) => ({
    id: earthquake.id,
    magnitude: earthquake.magnitude || 0,
    location: earthquake.location || "Bilinmeyen Konum",
    time: new Date(earthquake.time),
    coordinates: earthquake.coordinates,
    depth: earthquake.depth || 0,
    source: earthquake.source || "Backend",
  }));

  // Update UI components
  updateMap();
  updateEarthquakeList();
  updateStats();
}

// Update map with earthquake data
function updateMap() {
  if (!AppState.map) return;
  
  // Clear existing markers
  AppState.markers.forEach((marker) => AppState.map.removeLayer(marker));
  AppState.markers = [];

  // Add new markers
  AppState.earthquakeData.forEach((eq) => {
    // Daha belirgin boyut farkları
    const radius = Math.max(eq.magnitude * 25000, 3000); // Daha büyük farklar
    
    // Yeni detaylı deprem büyüklüğü renk sistemi
    let color, fillColor;
    if (eq.magnitude >= 8.0) {
      // 8.0+ çok büyük depremler - Mor
      color = '#7b1fa2';
      fillColor = '#9c27b0';
    } else if (eq.magnitude >= 7.0) {
      // 7.0-7.9 büyük depremler - Koyu kırmızı/bordo
      color = '#d32f2f';
      fillColor = '#f44336';
    } else if (eq.magnitude >= 6.0) {
      // 6.0-6.9 kuvvetli depremler - Kırmızı
      color = '#f44336';
      fillColor = '#ff5722';
    } else if (eq.magnitude >= 5.0) {
      // 5.0-5.9 orta depremler - Koyu turuncu
      color = '#ff5722';
      fillColor = '#ff9800';
    } else if (eq.magnitude >= 4.0) {
      // 4.0-4.9 hafif depremler - Turuncu
      color = '#ff9800';
      fillColor = '#ffb74d';
    } else if (eq.magnitude >= 3.0) {
      // 3.0-3.9 küçük depremler - Sarı
      color = '#ffc107';
      fillColor = '#ffeb3b';
    } else {
      // 0-2.9 çok küçük/hissedilmez depremler - Yeşil
      color = '#4caf50';
      fillColor = '#8bc34a';
    }

    const marker = L.circle([eq.coordinates.lat, eq.coordinates.lng], {
      color: color,
      fillColor: fillColor,
      radius: radius,
      weight: 3, // Daha kalın kenar
      opacity: 0.9,
      fillOpacity: 0.4 // Daha belirgin dolgu
    }).addTo(AppState.map);

    // Add popup with earthquake details
    marker.bindPopup(`
      <div style="text-align: center; min-width: 200px; font-family: 'Segoe UI', sans-serif;">
        <h3 style="margin: 0 0 10px 0; color: #d32f2f;">${eq.location}</h3>
        <p style="margin: 5px 0;"><strong>Büyüklük:</strong> ${eq.magnitude.toFixed(1)}</p>
        <p style="margin: 5px 0;"><strong>Derinlik:</strong> ${eq.depth.toFixed(1)} km</p>
        <p style="margin: 5px 0;"><strong>Zaman:</strong> ${Utils.formatDateTime(eq.time)}</p>
        <p style="margin: 5px 0; font-size: 12px; color: #666;">Kaynak: ${eq.source}</p>
      </div>
    `);

    AppState.markers.push(marker);
  });
}

// Update earthquake list
function updateEarthquakeList() {
  const container = document.getElementById("earthquake-items");
  const filterValue = document.getElementById("magnitude-filter")?.value || "all";

  if (!container) return;

  // Apply filter
  let filteredData = AppState.earthquakeData;
  if (filterValue !== "all") {
    const minMagnitude = parseFloat(filterValue);
    filteredData = AppState.earthquakeData.filter(eq => eq.magnitude >= minMagnitude);
  }

  if (filteredData.length === 0) {
    container.innerHTML = '<div class="loading">Belirtilen kritere uygun deprem bulunamadı.</div>';
    return;
  }

  // Create list HTML
  container.innerHTML = filteredData
    .map(eq => `
      <div class="earthquake-item" data-id="${eq.id}">
        <div class="magnitude" style="background-color: ${getMagnitudeColor(eq.magnitude)}">
          ${eq.magnitude.toFixed(1)}
        </div>
        <div class="details">
          <h3>${eq.location}</h3>
          <p class="time">${Utils.formatDateTime(eq.time)}</p>
          <p class="depth">Derinlik: ${eq.depth.toFixed(1)} km</p>
        </div>
      </div>
    `)
    .join("");

  // Add click events to list items
  container.querySelectorAll(".earthquake-item").forEach((item) => {
    item.addEventListener("click", function () {
      const eqId = this.getAttribute("data-id");
      const eq = AppState.earthquakeData.find(e => e.id === eqId);
      if (eq && AppState.map) {
        AppState.map.setView([eq.coordinates.lat, eq.coordinates.lng], 8);
        // Find and open corresponding marker popup
        const marker = AppState.markers.find(m => 
          Math.abs(m.getLatLng().lat - eq.coordinates.lat) < 0.001 &&
          Math.abs(m.getLatLng().lng - eq.coordinates.lng) < 0.001
        );
        if (marker) marker.openPopup();
      }
    });
  });
}

// Update statistics
function updateStats() {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  // Count today's earthquakes
  const todayQuakes = AppState.earthquakeData.filter(eq => {
    const eqDate = new Date(eq.time);
    eqDate.setHours(0, 0, 0, 0);
    return eqDate.getTime() === today.getTime();
  });

  // Update daily count
  const dailyQuakesEl = document.getElementById("daily-quakes");
  if (dailyQuakesEl) {
    dailyQuakesEl.textContent = todayQuakes.length;
  }

  // Find maximum magnitude
  if (AppState.earthquakeData.length > 0) {
    const maxMag = Math.max(...AppState.earthquakeData.map(eq => eq.magnitude));
    const maxMagnitudeEl = document.getElementById("max-magnitude");
    if (maxMagnitudeEl) {
      maxMagnitudeEl.textContent = maxMag.toFixed(1);
    }
  }
}

// Get color based on magnitude - Yeni detaylı renk sistemi
function getMagnitudeColor(mag) {
  if (mag >= 8.0) return "#7b1fa2"; // Mor - 8.0+ (çok büyük)
  if (mag >= 7.0) return "#d32f2f"; // Koyu kırmızı/bordo - 7.0-7.9 (büyük)
  if (mag >= 6.0) return "#f44336"; // Kırmızı - 6.0-6.9 (kuvvetli)
  if (mag >= 5.0) return "#ff5722"; // Koyu turuncu - 5.0-5.9 (orta)
  if (mag >= 4.0) return "#ff9800"; // Turuncu - 4.0-4.9 (hafif)
  if (mag >= 3.0) return "#ffc107"; // Sarı - 3.0-3.9 (küçük)
  return "#4caf50"; // Yeşil - 0-2.9 (çok küçük/hissedilmez)
}

// Setup event listeners
function setupEventListeners() {
  // Refresh button
  const refreshBtn = document.getElementById("refresh-btn");
  if (refreshBtn) {
    refreshBtn.addEventListener("click", handleRefresh);
  }

  // Magnitude filter
  const magnitudeFilter = document.getElementById("magnitude-filter");
  if (magnitudeFilter) {
    magnitudeFilter.addEventListener("change", Utils.debounce(updateEarthquakeList, 300));
  }
}

// Handle refresh button click
async function handleRefresh() {
  const btn = document.getElementById("refresh-btn");
  const icon = btn?.querySelector("i");
  
  if (icon) {
    icon.style.animation = "spin 1s linear infinite";
  }

  try {
    await fetchEarthquakeData();
  } catch (error) {
    console.error("Yenileme hatası:", error);
  } finally {
    setTimeout(() => {
      if (icon) {
        icon.style.animation = "";
      }
    }, 1000);
  }
}

// Start auto refresh
function startAutoRefresh() {
  if (AppState.refreshInterval) {
    clearInterval(AppState.refreshInterval);
  }
  
  AppState.refreshInterval = setInterval(() => {
    fetchEarthquakeData();
    updateStats();
  }, CONFIG.REFRESH_INTERVAL);
  
  // Dinamik zaman güncelleme için ayrı interval (her 10 saniyede)
  if (AppState.timeUpdateInterval) {
    clearInterval(AppState.timeUpdateInterval);
  }
  
  AppState.timeUpdateInterval = setInterval(() => {
    updateTimeDisplays();
  }, 1000); // 1 saniyede bir güncelle
}

// Update time displays dynamically
function updateTimeDisplays() {
  if (AppState.lastUpdateTime) {
    const timeAgo = formatTimeAgo(AppState.lastUpdateTime);
    
    const lastUpdateEl = document.getElementById('last-update');
    const lastUpdateTimeEl = document.getElementById('last-update-time');
    
    if (lastUpdateEl) {
      lastUpdateEl.textContent = `Son güncelleme: ${timeAgo}`;
    }
    
    if (lastUpdateTimeEl) {
      lastUpdateTimeEl.textContent = timeAgo;
    }
  }
}

// Resize map container to proper width
function resizeMapContainer() {
  const header = document.getElementById('hidden-header');
  const mapWrapper = document.querySelector('.map-wrapper');
  const mapEl = document.getElementById('map');
  const headerHeight = header ? header.offsetHeight : 0;

  if (mapWrapper) {
    mapWrapper.style.marginTop = `${headerHeight}px`;
  }

  if (mapEl) {
    mapEl.style.height = `${(window.innerHeight - headerHeight) * 0.8}px`;
  }

  if (AppState.map) {
    setTimeout(() => {
      AppState.map.invalidateSize();
    }, 100);
  }
}

// Show error message
function showErrorMessage(message) {
  console.error(message);
  // You can add a toast notification here if needed
}

// Cleanup on page unload
window.addEventListener("beforeunload", () => {
  if (AppState.refreshInterval) {
    clearInterval(AppState.refreshInterval);
  }
  if (AppState.timeUpdateInterval) {
    clearInterval(AppState.timeUpdateInterval);
  }
});

// Cleanup on page visibility change
document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    if (AppState.refreshInterval) {
      clearInterval(AppState.refreshInterval);
    }
    if (AppState.timeUpdateInterval) {
      clearInterval(AppState.timeUpdateInterval);
    }
  } else {
    startAutoRefresh();
  }
});

// Resize map on window resize
window.addEventListener("resize", () => {
  if (AppState.isInitialized) {
    resizeMapContainer();
  }
});
