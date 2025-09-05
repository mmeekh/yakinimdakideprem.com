/**
 * Anlık Deprem - Ana JavaScript Modülü
 * Optimized version with better error handling and performance
 */

// Global state management
const AppState = {
  map: null,
  earthquakeData: [],
  markers: [],
  refreshInterval: null,
  isInitialized: false,
  lastUpdateTime: null
};

// Configuration constants
const CONFIG = {
  REFRESH_INTERVAL: 120000, // 2 minutes
  MAP_CENTER: [39.0, 35.0], // Türkiye merkezi
  MAP_ZOOM: 6, // Türkiye'yi tam gösteren zoom seviyesi
  API_TIMEOUT: 10000,
  MAX_RADIUS_KM: 1000,
  MIN_MAGNITUDE: 2.5,
  HOURS_BACK: 24
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
      `https://earthquake.usgs.gov/fdsnws/event/1/query?${params}`,
      { signal: controller.signal }
    );

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`USGS API hata kodu: ${response.status}`);
    }

    const data = await response.json();
    processEarthquakeData(data.features);
    updateLastUpdateTime();
    
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

// Update last update time display
function updateLastUpdateTime(isSample = false) {
  const now = new Date();
  const timeString = Utils.formatTime(now);
  const timeDisplay = `${now.getHours().toString().padStart(2, "0")}:${now.getMinutes().toString().padStart(2, "0")}`;
  
  const lastUpdateEl = document.getElementById("last-update");
  const lastUpdateTimeEl = document.getElementById("last-update-time");
  
  if (lastUpdateEl) {
    lastUpdateEl.textContent = isSample 
      ? "Son güncelleme: Örnek veriler gösteriliyor"
      : `Son güncelleme: ${timeString}`;
  }
  
  if (lastUpdateTimeEl) {
    lastUpdateTimeEl.textContent = isSample ? "--:--" : timeDisplay;
  }
  
  AppState.lastUpdateTime = now;
}

// Process earthquake data
function processEarthquakeData(features) {
  AppState.earthquakeData = features.map((feature) => ({
    id: feature.id,
    magnitude: feature.properties.mag || 0,
    location: feature.properties.place || "Bilinmeyen Konum",
    time: new Date(feature.properties.time),
    coordinates: {
      lat: feature.geometry.coordinates[1],
      lng: feature.geometry.coordinates[0],
    },
    depth: feature.geometry.coordinates[2] || 0,
    source: "USGS",
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
    const intensity = Math.min(eq.magnitude / 8, 1);
    const radius = Math.max(eq.magnitude * 15000, 5000); // Minimum radius

    const marker = L.circle([eq.coordinates.lat, eq.coordinates.lng], {
      color: `rgba(255, 0, 0, ${intensity})`,
      fillColor: `rgba(255, 0, 0, ${intensity * 0.5})`,
      radius: radius,
      weight: 2,
      opacity: 0.8,
      fillOpacity: 0.3
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

// Get color based on magnitude
function getMagnitudeColor(mag) {
  if (mag >= 6) return "#d32f2f"; // Dark red
  if (mag >= 5) return "#f44336"; // Red
  if (mag >= 4) return "#ff9800"; // Orange
  if (mag >= 3) return "#ffc107"; // Yellow
  return "#4caf50"; // Green
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
});

// Cleanup on page visibility change
document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    if (AppState.refreshInterval) {
      clearInterval(AppState.refreshInterval);
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
