/**
 * Main Application Entry Point - Anlık Deprem
 * Optimized modular architecture
 */

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  try {
    // Create and initialize the main application
    const app = new EarthquakeApp();
    
    // Initialize map module first
    app.modules.map.init();
    
    // Initialize the main application
    app.init();
    
    // Make app globally available for debugging
    window.app = app;
    
    console.log('Anlık Deprem application initialized successfully');
  } catch (error) {
    console.error('Failed to initialize application:', error);
    
    // Show error message to user
    const errorContainer = document.getElementById('earthquake-items');
    if (errorContainer) {
      errorContainer.innerHTML = `
        <div class="alert alert--error">
          <i class="fas fa-exclamation-triangle"></i>
          Uygulama başlatılırken bir hata oluştu. Lütfen sayfayı yenileyin.
        </div>
      `;
    }
  }
});

// Handle application events
document.addEventListener('app:initialized', () => {
  console.log('Application fully initialized');
});

document.addEventListener('app:error', (event) => {
  console.error('Application error:', event.detail);
});

document.addEventListener('data:fetched', (event) => {
  console.log('Earthquake data fetched:', event.detail.length, 'earthquakes');
});

document.addEventListener('data:error', (event) => {
  console.error('Data fetch error:', event.detail);
});

document.addEventListener('map:initialized', () => {
  console.log('Map module initialized');
});

document.addEventListener('earthquake:selected', (event) => {
  console.log('Earthquake selected:', event.detail);
});

// Handle page visibility changes for performance optimization
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    console.log('Page hidden - reducing activity');
  } else {
    console.log('Page visible - resuming activity');
  }
});

// Handle window resize for responsive behavior
window.addEventListener('resize', () => {
  if (window.app && window.app.modules.map) {
    window.app.modules.map.resizeMap();
  }
});

// Handle page unload for cleanup
window.addEventListener('beforeunload', () => {
  if (window.app) {
    window.app.cleanup();
  }
});

// Export for potential module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { EarthquakeApp };
}
