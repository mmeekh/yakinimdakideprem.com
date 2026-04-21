/*
 * Kullanici konumu modulu
 * - Geolocation API izni ister
 * - Mavi nokta + pulse animasyonu ile konumu haritada gosterir
 * - Dogruluk yariçapi (accuracy circle) cizer
 * - Semt/mahalle seviyesinde zoom yapar (~14)
 * - Nominatim (OSM) ile ters geocoding ile mahalle adini gosterir
 * - sessionStorage cache (1 saat)
 */
(function () {
  "use strict";

  const BUTTON_ID = "my-location-btn";
  const CACHE_KEY = "yd_user_location";
  const CACHE_TTL_MS = 60 * 60 * 1000; // 1 saat
  const ZOOM_NEIGHBORHOOD = 14; // ~3 km cap

  let userMarker = null;
  let accuracyCircle = null;
  let mapReadyTimer = null;

  function getMap() {
    return (window.AppState && window.AppState.map) || null;
  }

  function setButtonState(state) {
    const btn = document.getElementById(BUTTON_ID);
    if (!btn) return;
    btn.classList.toggle("is-loading", state === "loading");
    const label = btn.querySelector(".my-location-btn__label");
    if (!label) return;
    if (state === "loading") label.textContent = "Alınıyor...";
    else if (state === "located") label.textContent = "Yenile";
    else label.textContent = "Konumum";
  }

  function showToast(msg, type = "info") {
    const existing = document.querySelector(".geo-toast");
    if (existing) existing.remove();
    const toast = document.createElement("div");
    toast.className = `geo-toast geo-toast--${type}`;
    toast.innerHTML = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add("is-visible"), 20);
    setTimeout(() => {
      toast.classList.remove("is-visible");
      setTimeout(() => toast.remove(), 300);
    }, 4500);
  }

  function placeMarker(lat, lng, accuracy, locationName) {
    const map = getMap();
    if (!map || !window.L) return false;

    if (userMarker) {
      map.removeLayer(userMarker);
      userMarker = null;
    }
    if (accuracyCircle) {
      map.removeLayer(accuracyCircle);
      accuracyCircle = null;
    }

    // Mavi nokta + pulse (Google Maps tarzi)
    const blueDotIcon = L.divIcon({
      className: "user-location-marker",
      html: '<span class="user-location-marker__pulse" aria-hidden="true"></span><span class="user-location-marker__dot"></span>',
      iconSize: [22, 22],
      iconAnchor: [11, 11],
    });

    userMarker = L.marker([lat, lng], {
      icon: blueDotIcon,
      zIndexOffset: 10000,
      keyboard: false,
      interactive: true,
      title: "Mevcut konumunuz",
    }).addTo(map);

    // Dogruluk yariçapi (accuracy < 500m ise gostermeye degmez - cok kucuk)
    if (accuracy && accuracy >= 10) {
      accuracyCircle = L.circle([lat, lng], {
        radius: accuracy,
        color: "#4285f4",
        fillColor: "#4285f4",
        fillOpacity: 0.12,
        weight: 1.5,
        opacity: 0.6,
        interactive: false,
      }).addTo(map);
    }

    // Popup
    const accDisplay = accuracy < 1000 ? `±${Math.round(accuracy)}m` : `±${(accuracy / 1000).toFixed(1)}km`;
    const popupHtml = locationName
      ? `<div class="user-location-popup"><strong>📍 ${locationName}</strong><div class="accuracy">Konum doğruluğu: ${accDisplay}</div></div>`
      : `<div class="user-location-popup"><strong>📍 Konumunuz</strong><div class="accuracy">Doğruluk: ${accDisplay}</div></div>`;
    userMarker.bindPopup(popupHtml, { closeButton: true, autoClose: false });

    // Semt seviyesinde zoom
    map.setView([lat, lng], ZOOM_NEIGHBORHOOD, {
      animate: true,
      duration: 1.2,
    });
    setTimeout(() => userMarker && userMarker.openPopup(), 1000);
    return true;
  }

  function saveCache(lat, lng, accuracy, locationName) {
    try {
      sessionStorage.setItem(
        CACHE_KEY,
        JSON.stringify({ lat, lng, accuracy, locationName, ts: Date.now() })
      );
    } catch (e) { /* storage quota */ }
  }

  function loadCache() {
    try {
      const raw = sessionStorage.getItem(CACHE_KEY);
      if (!raw) return null;
      const data = JSON.parse(raw);
      if (!data.ts || Date.now() - data.ts > CACHE_TTL_MS) return null;
      return data;
    } catch (e) {
      return null;
    }
  }

  async function reverseGeocode(lat, lng) {
    try {
      const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=16&accept-language=tr&addressdetails=1`;
      const ctrl = new AbortController();
      setTimeout(() => ctrl.abort(), 5000);
      const res = await fetch(url, {
        signal: ctrl.signal,
        headers: { Accept: "application/json" },
      });
      if (!res.ok) return null;
      const data = await res.json();
      const a = data.address || {};
      const neighborhood = a.neighbourhood || a.suburb || a.quarter;
      const district = a.city_district || a.county;
      const city = a.province || a.city || a.town || a.village || a.state;
      const parts = [neighborhood, district, city].filter(Boolean);
      // Tekrarları temizle
      const uniq = [...new Set(parts)];
      return uniq.join(", ") || null;
    } catch (e) {
      return null;
    }
  }

  function onGeoSuccess(position) {
    const { latitude: lat, longitude: lng, accuracy } = position.coords;

    // Harita hazir degilse bekle
    const map = getMap();
    if (!map) {
      if (mapReadyTimer) clearTimeout(mapReadyTimer);
      mapReadyTimer = setTimeout(() => onGeoSuccess(position), 300);
      return;
    }

    setButtonState("located");

    // Once marker'ı yerlestir (hızlı tepki), sonra mahalle adını sor
    placeMarker(lat, lng, accuracy, null);

    reverseGeocode(lat, lng).then((name) => {
      if (userMarker && name) {
        const accDisplay = accuracy < 1000 ? `±${Math.round(accuracy)}m` : `±${(accuracy / 1000).toFixed(1)}km`;
        userMarker.setPopupContent(
          `<div class="user-location-popup"><strong>📍 ${name}</strong><div class="accuracy">Konum doğruluğu: ${accDisplay}</div></div>`
        );
      }
      saveCache(lat, lng, accuracy, name);
    });
  }

  function onGeoError(err) {
    setButtonState("idle");
    const messages = {
      1: "Konum izni verilmedi. Tarayıcı ayarlarından konum iznini etkinleştirebilirsiniz.",
      2: "Konum bilgisi alınamadı. GPS veya ağ bağlantınızı kontrol edin.",
      3: "Konum isteği zaman aşımına uğradı. Tekrar deneyin.",
    };
    showToast(messages[err && err.code] || "Konum alınamadı.", "error");
  }

  function requestLocation() {
    if (!navigator.geolocation) {
      showToast("Tarayıcınız konum servisini desteklemiyor.", "error");
      return;
    }

    setButtonState("loading");

    // Cache'de 1 saatlik konum varsa hemen kullan, paralel guncelleme
    const cached = loadCache();
    if (cached && cached.lat && cached.lng) {
      placeMarker(cached.lat, cached.lng, cached.accuracy || 100, cached.locationName);
      setButtonState("located");
    }

    navigator.geolocation.getCurrentPosition(onGeoSuccess, onGeoError, {
      enableHighAccuracy: true,
      timeout: 12000,
      maximumAge: 60000,
    });
  }

  function init() {
    const btn = document.getElementById(BUTTON_ID);
    if (!btn) return;
    btn.addEventListener("click", requestLocation);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
