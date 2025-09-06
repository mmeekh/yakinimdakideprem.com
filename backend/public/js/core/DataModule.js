/**
 * Data Module - Yakınımdaki Deprem
 * Handles earthquake data fetching and processing
 */

class DataModule {
  constructor(app) {
    this.app = app;
    this.apiUrl = '/api/earthquakes'; // Backend API endpoint'i
    this.statsUrl = '/api/earthquakes/stats'; // İstatistik endpoint'i
  }

  /**
   * Fetch earthquake data from backend API
   */
  async fetchEarthquakeData() {
    const startTime = Date.now();
    
    try {
      const params = new URLSearchParams({
        hours_back: this.app.config.HOURS_BACK,
        min_magnitude: this.app.config.MIN_MAGNITUDE,
        max_radius: this.app.config.MAX_RADIUS_KM,
        limit: 100
      });

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), this.app.config.API_TIMEOUT);

      const response = await fetch(`${this.apiUrl}?${params}`, {
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`Backend API error: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        this.processEarthquakeData(data.data);
        console.log('Backend last_update_ago:', data.last_update_ago);
        this.updateLastUpdateTime(false, data.last_update_ago);
        console.log(`Data fetch completed in ${Date.now() - startTime}ms`);
        this.app.emit('data:fetched', this.app.state.earthquakeData);
      } else {
        // Backend'den örnek veri geldi
        this.processEarthquakeData(data.data);
        console.log('Backend last_update_ago (sample):', data.last_update_ago);
        this.updateLastUpdateTime(true, data.last_update_ago);
        console.log('Using sample data from backend');
        this.app.emit('data:fetched', this.app.state.earthquakeData);
      }
    } catch (error) {
      console.error('Failed to fetch earthquake data:', error);
      this.handleDataFetchError(error);
    }
  }

  /**
   * Handle data fetch errors
   */
  handleDataFetchError(error) {
    if (error.name === 'AbortError') {
      this.app.emit('data:error', 'Data fetch timeout. Please try again.');
    } else {
      this.app.emit('data:error', 'Failed to fetch data. Loading sample data.');
      this.loadSampleData();
    }
  }

  /**
   * Load sample data when API fails
   */
  loadSampleData() {
    const sampleFeatures = [
      {
        id: 'sample1',
        properties: {
          mag: 4.2,
          place: 'Ankara, Türkiye',
          time: Date.now() - 3600000,
        },
        geometry: { coordinates: [32.85, 39.92, 10] },
      },
      {
        id: 'sample2',
        properties: {
          mag: 3.5,
          place: 'İzmir, Türkiye',
          time: Date.now() - 7200000,
        },
        geometry: { coordinates: [27.14, 38.42, 8] },
      },
      {
        id: 'sample3',
        properties: {
          mag: 5.1,
          place: 'Kahramanmaraş, Türkiye',
          time: Date.now() - 14400000,
        },
        geometry: { coordinates: [36.95, 37.58, 15] },
      },
    ];

    this.processEarthquakeData(sampleFeatures);
    this.updateLastUpdateTime(true);
  }

  /**
   * Process earthquake data from backend API
   */
  processEarthquakeData(earthquakes) {
    const earthquakeData = earthquakes.map((earthquake) => ({
      id: earthquake.id,
      magnitude: earthquake.magnitude || 0,
      location: earthquake.location || 'Unknown Location',
      time: new Date(earthquake.time),
      time_ago: earthquake.time_ago || this.formatTimeAgo(new Date(earthquake.time)),
      coordinates: earthquake.coordinates,
      depth: earthquake.depth || 0,
      source: earthquake.source || 'Backend',
    }));

    this.app.setState({ earthquakeData });
    this.app.emit('data:processed', earthquakeData);
  }

  /**
   * Format time ago in Turkish
   */
  formatTimeAgo(date) {
    const now = new Date();
    const diff = now - date;
    const totalSeconds = Math.floor(diff / 1000);
    
    if (totalSeconds < 60) {
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

  /**
   * Update last update time display
   */
  updateLastUpdateTime(isSample = false, lastUpdateAgo = null) {
    const now = new Date();
    
    console.log('updateLastUpdateTime called:', { isSample, lastUpdateAgo });
    
    const lastUpdateEl = document.getElementById('last-update');
    const lastUpdateTimeEl = document.getElementById('last-update-time');
    
    if (lastUpdateEl) {
      if (isSample) {
        lastUpdateEl.textContent = 'Son güncelleme: Örnek veriler gösteriliyor';
        console.log('Using sample data message');
      } else {
        // Her zaman dinamik zaman göster (backend'den gelen veya fallback)
        const timeToShow = lastUpdateAgo || this.formatTimeAgo(now);
        lastUpdateEl.textContent = `Son güncelleme: ${timeToShow}`;
        console.log('Using time:', timeToShow);
        
        // State'i güncelle ki dinamik güncelleme çalışsın
        this.app.setState({ lastUpdateTime: now });
      }
    }
    
    if (lastUpdateTimeEl) {
      // Zaman gösterimini de dinamik yap
      if (isSample) {
        lastUpdateTimeEl.textContent = '--:--';
      } else if (lastUpdateAgo) {
        lastUpdateTimeEl.textContent = lastUpdateAgo;
      } else {
        lastUpdateTimeEl.textContent = this.formatTimeAgo(now);
      }
    }
    
    this.app.setState({ lastUpdateTime: now });
  }

  /**
   * Get filtered earthquake data
   */
  getFilteredData(filterValue = 'all') {
    let filteredData = this.app.state.earthquakeData;
    
    if (filterValue !== 'all') {
      const minMagnitude = parseFloat(filterValue);
      filteredData = this.app.state.earthquakeData.filter(eq => eq.magnitude >= minMagnitude);
    }
    
    return filteredData;
  }

  /**
   * Get earthquake by ID
   */
  getEarthquakeById(id) {
    return this.app.state.earthquakeData.find(eq => eq.id === id);
  }

  /**
   * Get earthquakes by magnitude range
   */
  getEarthquakesByMagnitude(min, max) {
    return this.app.state.earthquakeData.filter(eq => 
      eq.magnitude >= min && eq.magnitude <= max
    );
  }

  /**
   * Get earthquakes by time range
   */
  getEarthquakesByTimeRange(startTime, endTime) {
    return this.app.state.earthquakeData.filter(eq => 
      eq.time >= startTime && eq.time <= endTime
    );
  }
}

// Export for module usage
window.DataModule = DataModule;
