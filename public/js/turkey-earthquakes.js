/**
 * Türkiye'deki Son 5 Deprem - Basitleştirilmiş JavaScript Modülü
 * Ana uygulamadaki verilerle senkron çalışır ve yalnızca Türkiye depremlerini gösterir.
 */

const TURKEY_BOUNDS = {
  north: 42.0,
  south: 35.8,
  east: 45.0,
  west: 25.7
};

let turkeyEarthquakes = [];

function isInTurkey(lat, lng) {
  return (
    typeof lat === 'number' &&
    typeof lng === 'number' &&
    lat >= TURKEY_BOUNDS.south &&
    lat <= TURKEY_BOUNDS.north &&
    lng >= TURKEY_BOUNDS.west &&
    lng <= TURKEY_BOUNDS.east
  );
}

function getContainer() {
  return document.querySelector('.recent-earthquakes');
}

function showLoadingState() {
  const container = getContainer();
  if (!container) return;

  container.innerHTML = `
    <div class="loading-placeholder">
      <i class="fas fa-spinner fa-spin"></i>
      <span>Veriler yükleniyor...</span>
    </div>
  `;
}

function showErrorState() {
  const container = getContainer();
  if (!container) return;

  container.innerHTML = `
    <div class="error-message">
      <i class="fas fa-exclamation-triangle"></i>
      <span>Veriler yüklenirken bir sorun oluştu</span>
    </div>
  `;
}

function updateTurkeyEarthquakesTitle() {
  const titleElement = document.querySelector('.feature-card h3');
  if (titleElement) {
    titleElement.textContent = 'Türkiye\'deki Son 5 Deprem';
  }
}

function formatTurkeyLocation(location) {
  if (!location) {
    return 'Türkiye';
  }

  const normalized = location.toLowerCase();

  if (normalized.includes('türkiye')) {
    return location.replace(/türkiye/gi, 'Türkiye');
  }

  if (normalized.includes('turkey')) {
    return location.replace(/turkey/gi, 'Türkiye');
  }

  const turkeyCities = [
    'Istanbul', 'İstanbul', 'Ankara', 'Izmir', 'İzmir', 'Bursa', 'Antalya', 'Adana',
    'Konya', 'Gaziantep', 'Mersin', 'Diyarbakir', 'Diyarbakır', 'Kayseri',
    'Eskisehir', 'Eskişehir', 'Sanliurfa', 'Şanlıurfa', 'Malatya', 'Erzurum',
    'Van', 'Batman', 'Elazig', 'Elazığ', 'Isparta', 'Trabzon', 'Ordu', 'Sivas',
    'Kahramanmaras', 'Kahramanmaraş', 'Erzincan', 'Aydin', 'Aydın', 'Denizli',
    'Manisa', 'Balikesir', 'Balıkesir', 'Sakarya'
  ];

  for (const city of turkeyCities) {
    if (normalized.includes(city.toLowerCase())) {
      return city + ', Türkiye';
    }
  }

  return location + ', Türkiye';
}

function renderTurkeyEarthquakes() {
  const container = getContainer();
  if (!container) return;

  container.innerHTML = '';

  if (!turkeyEarthquakes.length) {
    container.innerHTML = `
      <div class="no-data-message">
        <i class="fas fa-info-circle"></i>
        <span>Son 7 günde kaydedilen deprem bulunamadı</span>
      </div>
    `;
    return;
  }

  const topFive = turkeyEarthquakes.slice(0, 5);

  topFive.forEach((eq) => {
    const item = document.createElement('div');
    item.className = 'earthquake-item-small';

    const magnitude = document.createElement('span');
    magnitude.className = 'magnitude-small';
    magnitude.textContent = eq.magnitude.toFixed(1);
    if (typeof getMagnitudeColor === 'function') {
      magnitude.style.backgroundColor = getMagnitudeColor(eq.magnitude);
    }

    const location = document.createElement('span');
    location.className = 'location-small';
    location.textContent = formatTurkeyLocation(eq.location);

    item.appendChild(magnitude);
    item.appendChild(location);
    container.appendChild(item);
  });
}

function handleEarthquakeUpdate(data) {
  const sourceData = Array.isArray(data)
    ? data
    : (window.AppState && Array.isArray(window.AppState.earthquakeData)
        ? window.AppState.earthquakeData
        : []);

  turkeyEarthquakes = sourceData
    .filter((eq) => eq && eq.coordinates && isInTurkey(eq.coordinates.lat, eq.coordinates.lng))
    .sort((a, b) => b.magnitude - a.magnitude);

  renderTurkeyEarthquakes();
}

document.addEventListener('DOMContentLoaded', () => {
  updateTurkeyEarthquakesTitle();
  showLoadingState();

  if (window.AppState && Array.isArray(window.AppState.earthquakeData) && window.AppState.earthquakeData.length) {
    handleEarthquakeUpdate(window.AppState.earthquakeData);
  }
});

document.addEventListener('earthquakes:updated', (event) => {
  handleEarthquakeUpdate(event.detail);
});

document.addEventListener('earthquakes:error', () => {
  if (!turkeyEarthquakes.length) {
    showErrorState();
  }
});

window.addEventListener('pageshow', () => {
  if (window.AppState && Array.isArray(window.AppState.earthquakeData) && window.AppState.earthquakeData.length) {
    handleEarthquakeUpdate(window.AppState.earthquakeData);
  }
});

window.TurkeyEarthquakes = {
  refreshFromAppState: () => handleEarthquakeUpdate(window.AppState ? window.AppState.earthquakeData : [])
};

