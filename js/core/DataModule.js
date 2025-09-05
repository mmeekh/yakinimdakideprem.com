/**
 * Data Module - Anlık Deprem
 * Handles earthquake data fetching and processing
 */

class DataModule {
  constructor(app) {
    this.app = app;
    this.apiUrl = 'https://earthquake.usgs.gov/fdsnws/event/1/query';
  }

  /**
   * Fetch earthquake data from USGS API
   */
  async fetchEarthquakeData() {
    const startTime = Date.now();
    
    try {
      const params = new URLSearchParams({
        format: 'geojson',
        starttime: new Date(Date.now() - this.app.config.HOURS_BACK * 3600000).toISOString(),
        latitude: this.app.config.MAP_CENTER[0],
        longitude: this.app.config.MAP_CENTER[1],
        maxradiuskm: this.app.config.MAX_RADIUS_KM,
        minmagnitude: this.app.config.MIN_MAGNITUDE,
        orderby: 'magnitude-desc',
        limit: 100
      });

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), this.app.config.API_TIMEOUT);

      const response = await fetch(`${this.apiUrl}?${params}`, {
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`USGS API error: ${response.status}`);
      }

      const data = await response.json();
      this.processEarthquakeData(data.features);
      this.updateLastUpdateTime();
      
      console.log(`Data fetch completed in ${Date.now() - startTime}ms`);
      this.app.emit('data:fetched', this.app.state.earthquakeData);
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
   * Process earthquake data
   */
  processEarthquakeData(features) {
    const earthquakeData = features.map((feature) => ({
      id: feature.id,
      magnitude: feature.properties.mag || 0,
      location: feature.properties.place || 'Unknown Location',
      time: new Date(feature.properties.time),
      coordinates: {
        lat: feature.geometry.coordinates[1],
        lng: feature.geometry.coordinates[0],
      },
      depth: feature.geometry.coordinates[2] || 0,
      source: 'USGS',
    }));

    this.app.setState({ earthquakeData });
    this.app.emit('data:processed', earthquakeData);
  }

  /**
   * Update last update time display
   */
  updateLastUpdateTime(isSample = false) {
    const now = new Date();
    const timeString = now.toLocaleTimeString('tr-TR');
    const timeDisplay = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
    
    const lastUpdateEl = document.getElementById('last-update');
    const lastUpdateTimeEl = document.getElementById('last-update-time');
    
    if (lastUpdateEl) {
      lastUpdateEl.textContent = isSample 
        ? 'Son güncelleme: Örnek veriler gösteriliyor'
        : `Son güncelleme: ${timeString}`;
    }
    
    if (lastUpdateTimeEl) {
      lastUpdateTimeEl.textContent = isSample ? '--:--' : timeDisplay;
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
