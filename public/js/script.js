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

if (typeof window !== 'undefined') {
  window.AppState = AppState;
}

// Configuration constants
const CONFIG = {
  REFRESH_INTERVAL: 60000, // 1 minute
  MAP_CENTER: [39.0, 35.0], // Türkiye merkezi
  MAP_ZOOM: 6, // Türkiye'yi tam gösteren zoom seviyesi
  API_TIMEOUT: 10000,
  MAX_RADIUS_KM: 5000, // Çok geniş alan
  MIN_MAGNITUDE: 1.5, // Kandilli API için optimize edildi
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
    resetExistingMap();

    // Show loading indicator
    const mapContainer = document.getElementById("map");
    if (mapContainer) {
      mapContainer.innerHTML = '<div class="map-loading"><i class="fas fa-spinner fa-spin"></i>Harita yükleniyor...</div>';
    }

    AppState.map = L.map("map").setView(CONFIG.MAP_CENTER, CONFIG.MAP_ZOOM);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 18,
      minZoom: 2
    }).addTo(AppState.map);

    // Hide loading indicator when map is ready
    AppState.map.whenReady(() => {
      // Harita yüklendikten sonra boyutlandır
      setTimeout(() => {
        AppState.map.invalidateSize();
        
        // Harita genişliğini zorla ayarla
        resizeMapContainer();
      }, 100);
    });
  } catch (error) {
    console.error("Harita başlatılamadı:", error);
    showErrorMessage("Harita yüklenirken bir hata oluştu.");
  }
}

// Remove previously created Leaflet map instance if it exists
function resetExistingMap() {
  if (AppState.map) {
    try {
      AppState.map.off();
      AppState.map.remove();
    } catch (error) {
      console.warn("Önceki harita kaldırılırken hata oluştu:", error);
    }
    AppState.map = null;
  }

  const mapContainer = document.getElementById("map");
  if (mapContainer && mapContainer._leaflet_id) {
    try {
      delete mapContainer._leaflet_id;
    } catch (error) {
      mapContainer._leaflet_id = null;
    }
  }
}

// Fetch earthquake data from USGS API
async function fetchEarthquakeData() {
  const startTime = Date.now();
  
  try {
    const params = new URLSearchParams({
      hours_back: CONFIG.HOURS_BACK,
      min_magnitude: CONFIG.MIN_MAGNITUDE,
      limit: 250
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
        } else {
          updateLastUpdateTime(false, data.last_update_ago);
        }
      } else {
        // Gerçek veri yok, örnek veri göster
        loadSampleData();
      }
    } else {
      // Backend'den örnek veri geldi
      if (hasDataChanged) {
        processEarthquakeData(data.data);
        updateLastUpdateTime(true, data.last_update_ago);
        AppState.lastDataHash = currentDataHash;
      } else {
        updateLastUpdateTime(true, data.last_update_ago);
      }
    }
    
  } catch (error) {
    console.error("Deprem verileri alınamadı:", error);
    handleDataFetchError(error);
  }
}

// Handle data fetch errors
function handleDataFetchError(error) {
  document.dispatchEvent(new CustomEvent('earthquakes:error', { detail: error }));

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

  const latestData = Array.isArray(AppState.earthquakeData) ? AppState.earthquakeData : [];
  document.dispatchEvent(new CustomEvent('earthquakes:updated', {
    detail: latestData.map(eq => ({ ...eq }))
  }));
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

    // Override popup with accessible classes for better contrast
    try {
      marker.setPopupContent(`
        <div class="earthquake-popup">
          <h3 class="earthquake-popup__title">${eq.location}</h3>
          <div class="earthquake-popup__details">
            <p><strong>Büyüklük:</strong> ${eq.magnitude.toFixed(1)}</p>
            <p><strong>Derinlik:</strong> ${eq.depth.toFixed(1)} km</p>
            <p><strong>Zaman:</strong> ${Utils.formatDateTime(eq.time)}</p>
          </div>
          <div class="earthquake-popup__source">Kaynak: ${eq.source}</div>
        </div>
      `);
    } catch (e) {}

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

  // Update recent earthquakes section (now handled by turkey-earthquakes.js)
  // updateRecentEarthquakes();

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

  // Turkey button
  const turkeyBtn = document.getElementById("turkey-btn");
  if (turkeyBtn) {
    turkeyBtn.addEventListener("click", goToTurkey);
  }

  // Night mode button
  const nightModeBtn = document.getElementById("night-mode-btn");
  if (nightModeBtn) {
    nightModeBtn.addEventListener("click", toggleNightMode);
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

// Go to Turkey on map
function goToTurkey() {
  if (AppState.map) {
    // Türkiye koordinatları ve zoom seviyesi
    const turkeyCenter = [39.0, 35.0]; // Türkiye merkezi
    const turkeyZoom = 6; // Türkiye'yi tam gösteren zoom seviyesi
    
    // Haritayı Türkiye'ye odakla
    AppState.map.setView(turkeyCenter, turkeyZoom);
    
    // Buton animasyonu
    const btn = document.getElementById("turkey-btn");
    if (btn) {
      btn.style.transform = "scale(0.95)";
      setTimeout(() => {
        btn.style.transform = "";
      }, 150);
    }
    
  }
}

// Toggle night mode
function toggleNightMode() {
  const body = document.body;
  const nightModeBtn = document.getElementById("night-mode-btn");
  const icon = nightModeBtn?.querySelector("i");
  
  // Toggle night mode class
  body.classList.toggle("night-mode");
  
  // Update button state and icon
  if (body.classList.contains("night-mode")) {
    nightModeBtn.classList.add("active");
    if (icon) {
      icon.className = "fas fa-sun";
    }
    nightModeBtn.innerHTML = '<i class="fas fa-sun"></i> Gündüz Modu';
    
    // Apply dark filter to existing map
    const mapElement = document.getElementById('map');
    if (mapElement) {
      mapElement.style.filter = 'invert(1) hue-rotate(180deg) brightness(0.8) contrast(1.2)';
    }
    
  } else {
    nightModeBtn.classList.remove("active");
    if (icon) {
      icon.className = "fas fa-moon";
    }
    nightModeBtn.innerHTML = '<i class="fas fa-moon"></i> Gece Modu';
    
    // Remove dark filter from map
    const mapElement = document.getElementById('map');
    if (mapElement) {
      mapElement.style.filter = '';
    }
    
  }
  
  // Buton animasyonu
  if (nightModeBtn) {
    nightModeBtn.style.transform = "scale(0.95)";
    setTimeout(() => {
      nightModeBtn.style.transform = "";
    }, 150);
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

// Update recent earthquakes section with real data
function updateRecentEarthquakes() {
  const recentEarthquakesContainer = document.querySelector('.recent-earthquakes');
  if (!recentEarthquakesContainer || !AppState.earthquakeData.length) return;

  // Get top 5 earthquakes by magnitude
  const top5Earthquakes = AppState.earthquakeData
    .sort((a, b) => b.magnitude - a.magnitude)
    .slice(0, 5);

  // Clear existing content
  recentEarthquakesContainer.innerHTML = '';

  // Add new earthquake items
  top5Earthquakes.forEach((eq, index) => {
    const earthquakeItem = document.createElement('div');
    earthquakeItem.className = 'earthquake-item-small';
    
    const magnitude = document.createElement('span');
    magnitude.className = 'magnitude-small';
    magnitude.textContent = eq.magnitude.toFixed(1);
    
    const location = document.createElement('span');
    location.className = 'location-small';
    location.textContent = eq.location || 'Bilinmeyen Konum';
    
    earthquakeItem.appendChild(magnitude);
    earthquakeItem.appendChild(location);
    recentEarthquakesContainer.appendChild(earthquakeItem);
  });
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

// Handle pageshow events (e.g. browser back/forward cache)
window.addEventListener("pageshow", async (event) => {
  const navigationEntries = typeof performance !== "undefined" && typeof performance.getEntriesByType === "function"
    ? performance.getEntriesByType("navigation")
    : [];

  const hasBackForwardEntry = Array.isArray(navigationEntries)
    ? navigationEntries.some((entry) => entry && entry.type === "back_forward")
    : false;

  const hasActivationStart = Array.isArray(navigationEntries)
    ? navigationEntries.some((entry) => entry && typeof entry.activationStart === "number" && entry.activationStart > 0)
    : false;

  const legacyNavigation = typeof performance !== "undefined" && performance.navigation
    ? performance.navigation
    : null;

  const legacyBackForward = legacyNavigation && typeof legacyNavigation.type === "number" && typeof legacyNavigation.TYPE_BACK_FORWARD === "number"
    ? legacyNavigation.type === legacyNavigation.TYPE_BACK_FORWARD
    : false;

  const isBackForwardNavigation = Boolean(
    event.persisted ||
    hasBackForwardEntry ||
    hasActivationStart ||
    legacyBackForward
  );

  if (!isBackForwardNavigation) {
    return;
  }

  if (!AppState.isInitialized) {
    await initApp();
    return;
  }

  // BFCache geri dönüşlerinde Leaflet haritasını tamamen yeniden oluştur
  resetExistingMap();
  initMap();

  if (!AppState.earthquakeData || AppState.earthquakeData.length === 0) {
    await fetchEarthquakeData();
  } else {
    updateMap();
    updateEarthquakeList();
    updateStats();
  }

  startAutoRefresh();
  updateTimeDisplays();
  resizeMapContainer();

  const latestData = Array.isArray(AppState.earthquakeData) ? AppState.earthquakeData : [];
  document.dispatchEvent(new CustomEvent('earthquakes:updated', {
    detail: latestData.map(eq => ({ ...eq }))
  }));
});

// --- Map recovery helpers to avoid black map on return/navigation ---
function ensureMapReady() {
  const mapEl = document.getElementById('map');
  if (!AppState.map || !mapEl || mapEl.offsetWidth === 0 || mapEl.offsetHeight === 0) {
    resetExistingMap();
    initMap();
    return;
  }
  requestAnimationFrame(() => {
    try { AppState.map.invalidateSize(true); } catch (e) {}
    resizeMapContainer();
  });
}

// When tab becomes visible again
document.addEventListener('visibilitychange', () => {
  if (!document.hidden) {
    ensureMapReady();
  }
});

// When window regains focus
window.addEventListener('focus', () => {
  ensureMapReady();
});
