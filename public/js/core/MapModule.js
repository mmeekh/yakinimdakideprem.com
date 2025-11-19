/**
 * Map Module - Yakınımdaki Deprem
 * Handles map initialization and earthquake visualization
 */

class MapModule {
  constructor(app) {
    this.app = app;
    this.map = null;
    this.markers = [];
    this.isInitialized = false;
  }

  /**
   * Initialize the map
   */
  init() {
    if (this.isInitialized) return;

    try {
      this.showLoadingIndicator();
      this.createMap();
      this.setupMapEvents();
      this.isInitialized = true;
      this.app.emit('map:initialized');
    } catch (error) {
      console.error('Map initialization failed:', error);
      this.app.emit('map:error', error);
    }
  }

  /**
   * Show loading indicator
   */
  showLoadingIndicator() {
    const mapContainer = document.getElementById('map');
    if (mapContainer) {
      mapContainer.innerHTML = `
        <div class="loading">
          <div class="loading__spinner"></div>
          Harita yükleniyor...
        </div>
      `;
    }
  }

  /**
   * Create the map instance
   */
  createMap() {
    this.destroyExistingMap();

    const mapElement = document.getElementById('map');
    if (!mapElement) {
      throw new Error('Harita konteyneri bulunamadı');
    }

    if (mapElement._leaflet_id) {
      try {
        delete mapElement._leaflet_id;
      } catch (error) {
        mapElement._leaflet_id = null;
      }
    }

    const initialZoom = window.innerWidth <= 768
      ? this.app.config.MAP_ZOOM_MOBILE
      : this.app.config.MAP_ZOOM_DESKTOP;

    this.map = L.map('map', {
      zoomControl: false,
      attributionControl: false
    }).setView(
      this.app.config.MAP_CENTER,
      initialZoom
    );

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 18,
      minZoom: 4
    }).addTo(this.map);

    this.map.whenReady(() => {
      console.log('Map loaded successfully');
      this.resizeMap();
      this.app.setState({ map: this.map });
    });
  }

  /**
   * Setup map event listeners
   */
  setupMapEvents() {
    if (!this.map) return;

    this.map.on('zoomend', () => {
      this.app.emit('map:zoom:changed', this.map.getZoom());
    });

    this.map.on('moveend', () => {
      this.app.emit('map:move:changed', this.map.getCenter());
    });

    this.map.on('click', (e) => {
      this.app.emit('map:clicked', e.latlng);
    });
  }

  /**
   * Update map with earthquake data
   */
  updateMap() {
    if (!this.map) return;
    
    this.clearMarkers();
    this.addEarthquakeMarkers();
    this.resizeMap();
  }

  /**
   * Clear existing markers
   */
  clearMarkers() {
    this.markers.forEach(marker => this.map.removeLayer(marker));
    this.markers = [];
  }

  /**
   * Add earthquake markers to map
   */
  addEarthquakeMarkers() {
    this.app.state.earthquakeData.forEach(eq => {
      const marker = this.createEarthquakeMarker(eq);
      this.markers.push(marker);
    });
  }

  /**
   * Create earthquake marker
   */
  createEarthquakeMarker(earthquake) {
    const intensity = Math.min(earthquake.magnitude / 8, 1);
    const radius = Math.max(earthquake.magnitude * 15000, 5000);

    // Yeni detaylı deprem büyüklüğü renk sistemi
    let color, fillColor;
    if (earthquake.magnitude >= 8.0) {
      // 8.0+ çok büyük depremler - Mor
      color = '#7b1fa2';
      fillColor = '#9c27b0';
    } else if (earthquake.magnitude >= 7.0) {
      // 7.0-7.9 büyük depremler - Koyu kırmızı/bordo
      color = '#d32f2f';
      fillColor = '#f44336';
    } else if (earthquake.magnitude >= 6.0) {
      // 6.0-6.9 kuvvetli depremler - Kırmızı
      color = '#f44336';
      fillColor = '#ff5722';
    } else if (earthquake.magnitude >= 5.0) {
      // 5.0-5.9 orta depremler - Koyu turuncu
      color = '#ff5722';
      fillColor = '#ff9800';
    } else if (earthquake.magnitude >= 4.0) {
      // 4.0-4.9 hafif depremler - Turuncu
      color = '#ff9800';
      fillColor = '#ffb74d';
    } else if (earthquake.magnitude >= 3.0) {
      // 3.0-3.9 küçük depremler - Sarı
      color = '#ffc107';
      fillColor = '#ffeb3b';
    } else {
      // 0-2.9 çok küçük/hissedilmez depremler - Yeşil
      color = '#4caf50';
      fillColor = '#8bc34a';
    }

    const marker = L.circle([earthquake.coordinates.lat, earthquake.coordinates.lng], {
      color: color,
      fillColor: fillColor,
      radius: radius,
      weight: 2,
      opacity: 0.8,
      fillOpacity: 0.3
    }).addTo(this.map);

    // Add popup with earthquake details
    marker.bindPopup(this.createPopupContent(earthquake));

    // Add click event
    marker.on('click', () => {
      this.app.emit('marker:clicked', earthquake);
    });

    return marker;
  }

  /**
   * Create popup content for earthquake marker
   */
  createPopupContent(earthquake) {
    return `
      <div class="earthquake-popup">
        <h3 class="earthquake-popup__title">${earthquake.location}</h3>
        <div class="earthquake-popup__details">
          <p><strong>Büyüklük:</strong> ${earthquake.magnitude.toFixed(1)}</p>
          <p><strong>Derinlik:</strong> ${earthquake.depth.toFixed(1)} km</p>
          <p><strong>Zaman:</strong> ${earthquake.time.toLocaleString('tr-TR')}</p>
          <p class="earthquake-popup__source">Kaynak: ${earthquake.source}</p>
        </div>
        <div class="earthquake-popup__actions">
          <a class="earthquake-popup__action-btn" href="tel:112">112'yi Ara</a>
          <a class="earthquake-popup__action-btn" href="deprem-aninda.html" target="_blank" rel="noopener noreferrer">
            Deprem Anında &#128220;
          </a>
        </div>
      </div>
    `;
  }

  /**
   * Resize map container
   */
  resizeMap() {
    if (!this.map) return;

    setTimeout(() => {
      this.map.invalidateSize();
      this.adjustMapContainer();
    }, 100);
  }

  /**
   * Adjust map container dimensions
   */
  adjustMapContainer() {
    const mapContainer = document.querySelector('.map-container');
    const mapContent = document.querySelector('.map-content');
    const mapSection = document.querySelector('.map-section');

    if (mapContainer && mapContent && mapSection) {
      const parentWidth = mapContent.offsetWidth;
      
      mapContainer.style.cssText = `
        width: ${parentWidth}px !important;
        max-width: none !important;
        min-width: ${parentWidth}px !important;
        height: 385px !important;
        min-height: 385px !important;
      `;
      
      mapContent.style.cssText = `
        width: 100% !important;
        max-width: none !important;
        margin: 0 auto !important;
      `;
      
      mapSection.style.cssText = `
        width: 120% !important;
        max-width: 120% !important;
        margin: 0 auto !important;
      `;
      
      console.log(`Map container resized to ${parentWidth}px`);
    }
  }

  /**
   * Center map on earthquake
   */
  centerOnEarthquake(earthquake) {
    if (!this.map) return;

    this.map.setView([earthquake.coordinates.lat, earthquake.coordinates.lng], 8);
    
    // Find and open corresponding marker popup
    const marker = this.markers.find(m => 
      Math.abs(m.getLatLng().lat - earthquake.coordinates.lat) < 0.001 &&
      Math.abs(m.getLatLng().lng - earthquake.coordinates.lng) < 0.001
    );
    
    if (marker) {
      marker.openPopup();
    }
  }

  /**
   * Get map bounds
   */
  getBounds() {
    return this.map ? this.map.getBounds() : null;
  }

  /**
   * Get map center
   */
  getCenter() {
    return this.map ? this.map.getCenter() : null;
  }

  /**
   * Get map zoom level
   */
  getZoom() {
    return this.map ? this.map.getZoom() : null;
  }

  /**
   * Set map view
   */
  setView(center, zoom) {
    if (this.map) {
      this.map.setView(center, zoom);
    }
  }

  /**
   * Fit map to bounds
   */
  fitBounds(bounds) {
    if (this.map) {
      this.map.fitBounds(bounds);
    }
  }

  /**
   * Destroy existing Leaflet map instance if present
   */
  destroyExistingMap() {
    if (this.map) {
      try {
        this.map.off();
        this.map.remove();
      } catch (error) {
        console.warn('Mevcut harita kaldırılırken hata oluştu:', error);
      }
      this.map = null;
    }
  }
}

// Export for module usage
window.MapModule = MapModule;
