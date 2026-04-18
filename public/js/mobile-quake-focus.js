(() => {
  const MOBILE_BREAKPOINT = 900;
  let recentering = false;

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

  function getMap() {
    return window.AppState && window.AppState.map ? window.AppState.map : null;
  }

  function getQuakeById(quakeId) {
    const quakes = Array.isArray(window.AppState?.earthquakeData) ? window.AppState.earthquakeData : [];
    return quakes.find((entry) => String(entry.id) === String(quakeId)) || null;
  }

  function findNearestMarker(quake) {
    const markers = Array.isArray(window.AppState?.markers) ? window.AppState.markers : [];
    if (!markers.length) return null;
    let bestMarker = null;
    let bestScore = Infinity;
    markers.forEach((marker) => {
      const pos = marker.getLatLng ? marker.getLatLng() : null;
      if (!pos) return;
      const score = Math.abs(pos.lat - quake.coordinates.lat) + Math.abs(pos.lng - quake.coordinates.lng);
      if (score < bestScore) {
        bestScore = score;
        bestMarker = marker;
      }
    });
    return bestMarker;
  }

  function openPopupWithoutAutoPan(marker) {
    if (!marker || !marker.openPopup) return;
    const popup = marker.getPopup ? marker.getPopup() : marker._popup;
    let previousAutoPan = null;
    if (popup && popup.options && typeof popup.options.autoPan === 'boolean') {
      previousAutoPan = popup.options.autoPan;
      popup.options.autoPan = false;
    }
    marker.openPopup();
    if (popup && popup.options && previousAutoPan !== null) {
      popup.options.autoPan = previousAutoPan;
    }
  }

  function recenterMap(coords) {
    const map = getMap();
    if (!map || !coords || recentering) return;
    recentering = true;
    try {
      if (map.invalidateSize) {
        map.invalidateSize();
      }
    } catch (e) {}
    map.panTo([coords.lat, coords.lng], { animate: false });
    setTimeout(() => {
      recentering = false;
    }, 80);
  }

  function focusOnQuakeById(quakeId) {
    if (!quakeId) return;
    if (typeof window.ensureMapReady === 'function') {
      window.ensureMapReady();
    }
    const map = getMap();
    if (!map) return;
    const quake = getQuakeById(quakeId);
    if (!quake || !quake.coordinates) return;

    const target = [quake.coordinates.lat, quake.coordinates.lng];
    const targetZoom = 8;
    let handled = false;

    const finalize = () => {
      if (handled) return;
      handled = true;
      const marker = findNearestMarker(quake);
      openPopupWithoutAutoPan(marker);
      requestAnimationFrame(() => {
        recenterMap(quake.coordinates);
      });
    };

    map.once('moveend', finalize);
    map.setView(target, targetZoom, { animate: true, duration: 0.35 });
    setTimeout(finalize, 500);
  }

  function focusOnQuake(item) {
    const quakeId = item.getAttribute('data-id');
    focusOnQuakeById(quakeId);
  }

  document.addEventListener('click', (event) => {
    const item = event.target.closest ? event.target.closest('.earthquake-item') : null;
    if (!item) return;
    if (window.innerWidth <= MOBILE_BREAKPOINT) {
      closeInfoPanel();
      scrollToMap();
    }
    setTimeout(() => {
      focusOnQuake(item);
    }, 50);
  });

  window.focusEarthquakeById = focusOnQuakeById;
})();
