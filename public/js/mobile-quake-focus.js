(() => {
  const MOBILE_BREAKPOINT = 900;
  let popupAdjusting = false;

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

  function centerPopupInView(popup) {
    const map = getMap();
    if (!map || !popup || popupAdjusting) return;
    const popupEl = popup.getElement ? popup.getElement() : null;
    const mapEl = map.getContainer ? map.getContainer() : null;
    if (!popupEl || !mapEl) return;
    const popupRect = popupEl.getBoundingClientRect();
    const mapRect = mapEl.getBoundingClientRect();
    const deltaX = (popupRect.left + popupRect.width / 2) - (mapRect.left + mapRect.width / 2);
    const deltaY = (popupRect.top + popupRect.height / 2) - (mapRect.top + mapRect.height / 2);
    if (Math.abs(deltaX) < 1 && Math.abs(deltaY) < 1) return;
    popupAdjusting = true;
    map.panBy([-deltaX, -deltaY], { animate: true, duration: 0.25 });
    setTimeout(() => {
      popupAdjusting = false;
    }, 300);
  }

  function attachPopupCentering() {
    const map = getMap();
    if (!map || map._popupCenteringAttached) return;
    map._popupCenteringAttached = true;
    map.on('popupopen', (event) => {
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          centerPopupInView(event.popup);
        });
      });
    });
  }

  function focusOnQuake(item) {
    if (typeof window.ensureMapReady === 'function') {
      window.ensureMapReady();
    }
    const map = getMap();
    if (!map) return;
    const quakeId = item.getAttribute('data-id');
    if (!quakeId) return;
    const quakes = Array.isArray(window.AppState.earthquakeData) ? window.AppState.earthquakeData : [];
    const quake = quakes.find((entry) => String(entry.id) === String(quakeId));
    if (!quake || !quake.coordinates) return;
    map.setView([quake.coordinates.lat, quake.coordinates.lng], 8);
    const marker = findNearestMarker(quake);
    if (marker && marker.openPopup) {
      marker.openPopup();
    }
    setTimeout(() => {
      if (map.invalidateSize) {
        map.invalidateSize();
      }
      const activePopup = map._popup || null;
      if (activePopup) {
        centerPopupInView(activePopup);
      }
    }, 200);
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

  document.addEventListener('DOMContentLoaded', () => {
    const waitForMap = () => {
      if (getMap()) {
        attachPopupCentering();
        return;
      }
      setTimeout(waitForMap, 300);
    };
    waitForMap();
  });
})();
