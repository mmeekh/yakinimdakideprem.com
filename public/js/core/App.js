/**
 * Core Application Module - YakÄ±nÄ±mdaki Deprem
 * Main application controller and state management
 */

class EarthquakeApp {
  constructor() {
    this.state = {
      map: null,
      earthquakeData: [],
      markers: [],
      refreshInterval: null,
      isInitialized: false,
      lastUpdateTime: null,
      isLoading: false
    };

    this.config = {
      REFRESH_INTERVAL: 120000, // 2 minutes
      MAP_CENTER: [39.0, 35.0],
      MAP_ZOOM_DESKTOP: 6,
      MAP_ZOOM_MOBILE: 5,
      API_TIMEOUT: 10000,
      MAX_RADIUS_KM: 1000,
      MIN_MAGNITUDE: 2.5,
      HOURS_BACK: 24
    };

    this.modules = {};
    this.eventListeners = new Map();
  }

  /**
   * Initialize the application
   */
  async init() {
    if (this.state.isInitialized) return;

    try {
      this.setupModules();
      await this.loadInitialData();
      this.setupEventListeners();
      this.startAutoRefresh();
      
      this.state.isInitialized = true;
      this.emit('app:initialized');
    } catch (error) {
      console.error('App initialization failed:', error);
      this.emit('app:error', error);
    }
  }

  /**
   * Setup application modules
   */
  setupModules() {
    this.modules.map = new MapModule(this);
    this.modules.data = new DataModule(this);
    this.modules.ui = new UIModule(this);
    this.modules.stats = new StatsModule(this);
  }

  /**
   * Load initial data
   */
  async loadInitialData() {
    this.state.isLoading = true;
    this.emit('app:loading:start');

    try {
      await this.modules.data.fetchEarthquakeData();
      this.modules.map.updateMap();
      this.modules.ui.updateEarthquakeList();
      this.modules.stats.updateStats();
    } finally {
      this.state.isLoading = false;
      this.emit('app:loading:end');
    }
  }

  /**
   * Setup global event listeners
   */
  setupEventListeners() {
    // Refresh button
    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) {
      this.addEventListener(refreshBtn, 'click', () => this.handleRefresh());
    }

    // Magnitude filter
    const magnitudeFilter = document.getElementById('magnitude-filter');
    if (magnitudeFilter) {
      this.addEventListener(magnitudeFilter, 'change', () => 
        this.modules.ui.updateEarthquakeList()
      );
    }

    // Window events
    this.addEventListener(window, 'resize', () => this.handleResize());
    this.addEventListener(window, 'beforeunload', () => this.cleanup());
    this.addEventListener(document, 'visibilitychange', () => this.handleVisibilityChange());
  }

  /**
   * Handle refresh action
   */
  async handleRefresh() {
    const btn = document.getElementById('refresh-btn');
    const icon = btn?.querySelector('i');
    
    if (icon) {
      icon.style.animation = 'spin 1s linear infinite';
    }

    try {
      await this.modules.data.fetchEarthquakeData();
      this.modules.map.updateMap();
      this.modules.ui.updateEarthquakeList();
      this.modules.stats.updateStats();
    } catch (error) {
      console.error('Refresh failed:', error);
    } finally {
      setTimeout(() => {
        if (icon) {
          icon.style.animation = '';
        }
      }, 1000);
    }
  }

  /**
   * Handle window resize
   */
  handleResize() {
    if (this.state.map) {
      setTimeout(() => {
        this.state.map.invalidateSize();
      }, 100);
    }
  }

  /**
   * Handle visibility change
   */
  handleVisibilityChange() {
    if (document.hidden) {
      this.stopAutoRefresh();
    } else {
      this.startAutoRefresh();
    }
  }

  /**
   * Start auto refresh
   */
  startAutoRefresh() {
    if (this.state.refreshInterval) {
      clearInterval(this.state.refreshInterval);
    }
    
    this.state.refreshInterval = setInterval(() => {
      this.modules.data.fetchEarthquakeData();
      this.modules.stats.updateStats();
    }, this.config.REFRESH_INTERVAL);
    
    // Dinamik zaman gÃ¼ncelleme iÃ§in ayrÄ± interval (her 10 saniyede)
    if (this.state.timeUpdateInterval) {
      clearInterval(this.state.timeUpdateInterval);
    }
    
    this.state.timeUpdateInterval = setInterval(() => {
      this.updateTimeDisplays();
    }, 10000); // 10 saniyede bir gÃ¼ncelle
  }

  /**
   * Update time displays dynamically
   */
  updateTimeDisplays() {
    if (this.state.lastUpdateTime) {
      const timeAgo = this.modules.data.formatTimeAgo(this.state.lastUpdateTime);
      
      const lastUpdateEl = document.getElementById('last-update');
      const lastUpdateTimeEl = document.getElementById('last-update-time');
      
      if (lastUpdateEl) {
        lastUpdateEl.textContent = `Son gÃ¼ncelleme: ${timeAgo}`;
      }
      
      if (lastUpdateTimeEl) {
        lastUpdateTimeEl.textContent = timeAgo;
      }
    }
  }

  /**
   * Stop auto refresh
   */
  stopAutoRefresh() {
    if (this.state.refreshInterval) {
      clearInterval(this.state.refreshInterval);
      this.state.refreshInterval = null;
    }
    
    if (this.state.timeUpdateInterval) {
      clearInterval(this.state.timeUpdateInterval);
      this.state.timeUpdateInterval = null;
    }
  }

  /**
   * Add event listener with cleanup tracking
   */
  addEventListener(element, event, handler) {
    element.addEventListener(event, handler);
    
    if (!this.eventListeners.has(element)) {
      this.eventListeners.set(element, []);
    }
    this.eventListeners.get(element).push({ event, handler });
  }

  /**
   * Emit custom event
   */
  emit(eventName, data) {
    const event = new CustomEvent(eventName, { detail: data });
    document.dispatchEvent(event);
  }

  /**
   * Listen for custom events
   */
  on(eventName, handler) {
    document.addEventListener(eventName, handler);
  }

  /**
   * Cleanup resources
   */
  cleanup() {
    this.stopAutoRefresh();
    
    // Remove all event listeners
    this.eventListeners.forEach((listeners, element) => {
      listeners.forEach(({ event, handler }) => {
        element.removeEventListener(event, handler);
      });
    });
    this.eventListeners.clear();
  }

  /**
   * Get application state
   */
  getState() {
    return { ...this.state };
  }

  /**
   * Update application state
   */
  setState(newState) {
    this.state = { ...this.state, ...newState };
    this.emit('app:state:changed', this.state);
  }
}

// Export for module usage
window.EarthquakeApp = EarthquakeApp;
