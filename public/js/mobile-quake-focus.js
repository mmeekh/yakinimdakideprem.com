(() => {
  const MOBILE_BREAKPOINT = 900;

  function closeInfoPanel() {
    if (!document.body.classList.contains('info-menu-open')) return;
    const toggleButton = document.querySelector('.info-toggle');
    if (toggleButton) {
      toggleButton.click();
      return;
    }
    document.body.classList.remove('info-menu-open');
    const overlay = document.getElementById('mobile-overlay');
    if (overlay) {
      overlay.classList.remove('visible');
    }
  }

  function scrollToMap() {
    const mapWrapper = document.querySelector('.map-wrapper');
    if (!mapWrapper) return;
    const header = document.getElementById('hidden-header');
    const headerOffset = header ? header.offsetHeight + 8 : 0;
    const targetTop = mapWrapper.getBoundingClientRect().top + window.scrollY - headerOffset;
    window.scrollTo({ top: Math.max(0, targetTop), behavior: 'smooth' });
  }

  function focusOnQuake(item) {
    if (!window.AppState || !window.AppState.map) return;
    const quakeId = item.getAttribute('data-id');
    if (!quakeId) return;
    const quakes = Array.isArray(window.AppState.earthquakeData) ? window.AppState.earthquakeData : [];
    const quake = quakes.find((entry) => String(entry.id) === String(quakeId));
    if (!quake || !quake.coordinates) return;
    window.AppState.map.setView([quake.coordinates.lat, quake.coordinates.lng], 8);
    const markers = Array.isArray(window.AppState.markers) ? window.AppState.markers : [];
    const marker = markers.find((entry) => {
      const pos = entry.getLatLng ? entry.getLatLng() : null;
      return pos
        && Math.abs(pos.lat - quake.coordinates.lat) < 0.001
        && Math.abs(pos.lng - quake.coordinates.lng) < 0.001;
    });
    if (marker && marker.openPopup) {
      marker.openPopup();
    }
    setTimeout(() => {
      if (window.AppState && window.AppState.map && window.AppState.map.invalidateSize) {
        window.AppState.map.invalidateSize();
      }
    }, 200);
  }

  document.addEventListener('click', (event) => {
    const item = event.target.closest ? event.target.closest('.earthquake-item') : null;
    if (!item) return;
    if (window.innerWidth > MOBILE_BREAKPOINT) return;
    closeInfoPanel();
    scrollToMap();
    focusOnQuake(item);
  });
})();
