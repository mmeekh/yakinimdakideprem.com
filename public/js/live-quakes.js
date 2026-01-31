const QuakeAPI = {
  cache: null,
  async fetchData(force = false) {
    if (!force && QuakeAPI.cache) {
      return QuakeAPI.cache;
    }

    // Cache'i bypass etmek için timestamp ekle
    const ts = force ? `&_=${Date.now()}` : '';
    const params = new URLSearchParams({
      hours_back: 24, // Sadece 24 saati çekmek daha hızlı olur ama son 20 için 168 kalsın mı? API limitine bağlı.
      // Kullanıcı 168 saat (7 gün) veri istiyor olabilir analiz için.
      limit: 500 // Daha fazla veri çekelim ki filtreleyince boş kalmasın
    });

    const url = `/api/earthquakes?hours_back=168&min_magnitude=1.0&limit=500${ts}`;

    try {
      const res = await fetch(url);
      if (!res.ok) {
        throw new Error("Deprem verileri alınamadı");
      }

      const json = await res.json();
      const data = json.data || [];
      QuakeAPI.cache = data;
      return data;
    } catch (err) {
      console.error("API Hatası:", err);
      throw err;
    }
  }
};

// Tarih ayrıştırma (Daha sağlam)
function getQuakeTime(quake) {
  const raw = quake.time || quake.updated_at || quake.date;
  if (!raw) return new Date();

  // Eğer zaten Date objesiyse
  if (raw instanceof Date) return raw;

  // "2025.01.31 15:30:00" formatını düzelt
  // Kandilli genelde nokta kullanır.
  let cleanRaw = raw.toString();
  if (cleanRaw.includes('.')) {
    cleanRaw = cleanRaw.replace(/\./g, '-');
  }

  const date = new Date(cleanRaw);
  return Number.isNaN(date.getTime()) ? new Date() : date;
}

function formatShortDate(date) {
  return date.toLocaleString("tr-TR", {
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit"
  });
}

function getMagnitudeValue(quake) {
  const value = Number(quake.magnitude);
  return Number.isFinite(value) ? value : null;
}

function getMagnitudeColor(magnitude) {
  if (magnitude >= 6) return "#b71c1c"; // Koyu Kırmızı
  if (magnitude >= 5) return "#d32f2f"; // Kırmızı
  if (magnitude >= 4) return "#f44336"; // Açık Kırmızı
  if (magnitude >= 3) return "#fb8c00"; // Turuncu
  return "#43a047"; // Yeşil (Tehlikesiz)
}

function formatQuakeRowWithBadge(quake) {
  const time = getQuakeTime(quake);
  const magnitude = getMagnitudeValue(quake);
  const label = magnitude !== null ? magnitude.toFixed(1) : "-";
  const badge = magnitude !== null
    ? `<span class="magnitude-badge" style="background:${getMagnitudeColor(magnitude)}">${label}</span>`
    : "-";

  return `
    <tr class="quake-row">
      <td>${time.toLocaleString("tr-TR")}</td>
      <td>${badge}</td>
      <td>${quake.depth ? `${quake.depth} km` : "-"}</td>
      <td>${quake.place || quake.location || "Bilinmeyen"}</td>
    </tr>
  `;
}

function formatQuakeRow(quake) {
  // Şehir sayfaları vb. için badgesiz versiyon
  return formatQuakeRowWithBadge(quake); // Artık her yerde badge kullanalım, daha şık.
}

function normalizeText(text = "") {
  return text
    .toString()
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

// Global state for filters
let currentFilters = {
  city: "",
  minMag: 0
};

async function renderGlobalQuakes({
  highlightSelector,
  statusSelector,
  tableSelector,
  limit = 20,
  force = false,
  useBadge = true
}) {
  const btn = document.getElementById('refresh-live');
  if (force && btn) {
    btn.classList.add('btn-loading');
    btn.textContent = 'Yenileniyor...';
    btn.disabled = true;
  }

  try {
    const data = await QuakeAPI.fetchData(force);

    // Filtreleme
    const cityInput = document.getElementById('filter-city');
    const magInput = document.getElementById('filter-min-mag');

    // Eğer fonksiyona dışarıdan filtre değeri gelmediyse inputlardan oku
    // (İlk yüklemede inputlar boş olur)
    if (cityInput) currentFilters.city = normalizeText(cityInput.value);
    if (magInput) currentFilters.minMag = parseFloat(magInput.value) || 0;

    let filteredData = data.filter(quake => {
      const mag = getMagnitudeValue(quake) ?? 0;
      const place = normalizeText(quake.place || quake.location || "");

      const magCheck = mag >= currentFilters.minMag;
      const cityCheck = currentFilters.city === "" || place.includes(currentFilters.city);

      return magCheck && cityCheck;
    });

    // Özet ve Highlight kısımları FİLTRELENMEMİŞ (gerçek son dakika) veriyi kullanmalı
    // Tablo ise FİLTRELENMİŞ veriyi göstermeli.

    // --- HIGLIGHT & STATUS (Filtresiz En Son Deprem) ---
    if (data.length > 0) {
      const latest = data[0];

      if (highlightSelector) {
        const el = document.querySelector(highlightSelector);
        if (el) {
          el.innerHTML = `
              <strong>${latest.magnitude?.toFixed?.(1)} Mw</strong> - ${latest.place || "Konum paylaşılmadı"
            }
              <br><small>${formatShortDate(getQuakeTime(latest))}</small>
            `;
        }
      }

      if (statusSelector) {
        const el = document.querySelector(statusSelector);
        if (el) {
          const latestTime = getQuakeTime(latest);
          // Saniye farkını al
          const diffMs = Date.now() - latestTime.getTime();
          const minutesAgo = Math.floor(diffMs / 60000);

          if (minutesAgo < 15) { // 15 dakikaya çıkardım "az önce" algısını
            const timeText = minutesAgo < 1 ? "Az önce" : `${minutesAgo} dakika önce`;
            el.textContent = `Evet. ${timeText} ${latest.place || "bir noktada"} ${latest.magnitude?.toFixed?.(1)} büyüklüğünde deprem oldu.`;
            el.style.color = "#d32f2f";
            el.style.fontWeight = "bold";
          } else {
            const place = latest.place || latest.location || "bilinmeyen noktada";
            const mag = latest.magnitude?.toFixed?.(1) ?? latest.magnitude;
            el.textContent = `Son 15 dakika içinde önemli bir kayıt yok. Son deprem: ${mag}, ${place}.`;
            el.style.color = "#2c3e50";
            el.style.fontWeight = "normal";
          }
        }
      }
    }

    // --- TABLO (Filtrelenmiş Veri) ---
    if (tableSelector) {
      const tbody = document.querySelector(tableSelector);
      if (tbody) {
        if (filteredData.length === 0) {
          tbody.innerHTML = '<tr><td colspan="4" class="no-results">Aradığınız kriterlere uygun deprem bulunamadı.</td></tr>';
        } else {
          tbody.innerHTML = filteredData
            .slice(0, limit)
            .map((quake) => formatQuakeRowWithBadge(quake))
            .join("");
        }
      }
    }

  } catch (error) {
    console.error("Render hatası:", error);
    const tbody = document.querySelector(tableSelector);
    if (tbody) {
      tbody.innerHTML = '<tr><td colspan="4">Veri alınırken hata oluştu. Lütfen sayfayı yenileyin.</td></tr>';
    }
  } finally {
    if (force && btn) {
      setTimeout(() => {
        btn.classList.remove('btn-loading');
        btn.textContent = 'Anında Yenile';
        btn.disabled = false;
      }, 500); // Kullanıcı görsün diye minik gecikme
    }
  }
}

async function renderSonDakikaPanels({ force = false } = {}) {
  // Bu fonksiyon sadece özet panellerini günceller, tabloyu değil.
  // Tablo güncellemesi renderGlobalQuakes ile yapılır.
  // Ancak buradaki özet kartları daima FİLTRESİZ, GERÇEK veriyi baz almalı.

  const summaryElements = {
    total: document.getElementById("summary-total"),
    strongest: document.getElementById("summary-strongest"),
    strongestPlace: document.getElementById("summary-strongest-place"),
    last: document.getElementById("summary-last"),
    lastTime: document.getElementById("summary-last-time"),
    m4: document.getElementById("summary-m4"),
    updated: document.getElementById("live-updated"),
    m4Table: document.getElementById("m4plus-table")
  };

  // Eğer elementler yoksa çık
  if (!Object.values(summaryElements).some(el => el)) return;

  try {
    const data = await QuakeAPI.fetchData(force); // Cache'ten veya API'den al
    if (!data.length) return;

    const sorted = [...data].sort((a, b) => getQuakeTime(b) - getQuakeTime(a));
    const now = Date.now();

    // 24 saat ve 7 gn filtreleri
    const msPerDay = 24 * 60 * 60 * 1000;
    const last24 = sorted.filter(q => (now - getQuakeTime(q).getTime()) <= msPerDay);
    const last7 = sorted.filter(q => (now - getQuakeTime(q).getTime()) <= 7 * msPerDay);

    if (summaryElements.total) summaryElements.total.textContent = last24.length;

    if (summaryElements.m4) {
      const m4count = last7.filter(q => (getMagnitudeValue(q) ?? 0) >= 4.0).length;
      summaryElements.m4.textContent = m4count;
    }

    // En byk deprem (Son 24 saat)
    if (last24.length > 0) {
      const strongest = last24.reduce((max, q) => {
        return (getMagnitudeValue(q) ?? 0) > (getMagnitudeValue(max) ?? 0) ? q : max;
      }, last24[0]);

      if (summaryElements.strongest)
        summaryElements.strongest.textContent = `${getMagnitudeValue(strongest)?.toFixed(1)} Mw`;

      if (summaryElements.strongestPlace)
        summaryElements.strongestPlace.textContent = strongest.place || strongest.location;
    }

    // En son deprem
    const latest = sorted[0];
    if (latest) {
      if (summaryElements.last)
        summaryElements.last.textContent = `${getMagnitudeValue(latest)?.toFixed(1)} Mw`;

      if (summaryElements.lastTime)
        summaryElements.lastTime.textContent = formatShortDate(getQuakeTime(latest));

      if (summaryElements.updated)
        summaryElements.updated.textContent = formatShortDate(getQuakeTime(latest));
    }

    // 4.0+ Tablosu
    if (summaryElements.m4Table) {
      const m4list = last7.filter(q => (getMagnitudeValue(q) ?? 0) >= 4.0);
      summaryElements.m4Table.innerHTML = m4list.length
        ? m4list.slice(0, 10).map(q => formatQuakeRowWithBadge(q)).join("")
        : '<tr><td colspan="4">Son 7 gün içinde 4.0+ deprem kaydı yok.</td></tr>';
    }

  } catch (e) {
    console.error("Panel update error:", e);
  }
}

// Şehir sayfaları için wrapper (Filtreleme mantığı olmadan)
async function renderCityQuakes({
  tableSelector,
  cityKeyword,
  limit = 15,
  summarySelector
}) {
  // Burada filtre inputlarını dinlemeye gerek yok, sadece şehre özel filtre
  try {
    const data = await QuakeAPI.fetchData();
    const aliases = (window.CityKeywords && window.CityKeywords[cityKeyword]) || [cityKeyword];
    const normalizedAliases = aliases.map(a => normalizeText(a));

    const filtered = data.filter(q => {
      const place = normalizeText(q.place || q.location || "");
      return normalizedAliases.some(alias => place.includes(alias));
    });

    if (summarySelector) {
      const el = document.querySelector(summarySelector);
      if (el) {
        el.innerHTML = filtered.length > 0
          ? `<strong>Son deprem:</strong> ${filtered[0].magnitude?.toFixed(1)} Mw - ${filtered[0].place} <br> <small>${formatShortDate(getQuakeTime(filtered[0]))}</small>`
          : "Son kayıtlarda bu şehir için deprem bulunamadı.";
      }
    }

    if (tableSelector) {
      const tbody = document.querySelector(tableSelector);
      if (tbody) {
        tbody.innerHTML = filtered.length
          ? filtered.slice(0, limit).map(q => formatQuakeRowWithBadge(q)).join("")
          : `<tr><td colspan="4">${cityKeyword} için son kayıt yok.</td></tr>`;
      }
    }
  } catch (e) {
    console.error(e);
  }
}

// Filtre Event Listener'larını Sayfaya Bağlama
function setupFilters() {
  const cityInput = document.getElementById('filter-city');
  const magInput = document.getElementById('filter-min-mag');

  const triggerUpdate = () => {
    renderGlobalQuakes({
      // highlightSelector ve statusSelector'ı tekrar vermeye gerek yok filter anında, 
      // ama renderGlobalQuakes yapısı gereği versek de sorun olmaz, sadece en üstteki bilgi değişmez.
      // Biz sadece tabloyu update etmek istiyoruz aslında.
      tableSelector: '#latest-quakes-table',
      limit: 50, // Filtreleyince daha çok sonuç gerekecek
      force: false // Cache'ten oku
    });
  };

  if (cityInput) {
    cityInput.addEventListener('input', () => {
      // Debounce
      clearTimeout(window._filterDebounce);
      window._filterDebounce = setTimeout(triggerUpdate, 300);
    });
  }

  if (magInput) {
    magInput.addEventListener('change', triggerUpdate);
  }
}

// Export veya global attach
window.renderGlobalQuakes = renderGlobalQuakes;
window.renderSonDakikaPanels = renderSonDakikaPanels;
window.renderCityQuakes = renderCityQuakes;
window.setupFilters = setupFilters;
