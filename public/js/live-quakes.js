const QuakeAPI = {
  async fetchData(force = false) {
    if (!force && QuakeAPI.cache) return QuakeAPI.cache;

    const params = new URLSearchParams({
      hours_back: 168,
      min_magnitude: 1.5,
      limit: 250
    });

    const res = await fetch(`/api/earthquakes?${params.toString()}`);
    if (!res.ok) throw new Error("Deprem verileri alınamadı");
    const json = await res.json();
    const data = json.data || [];
    QuakeAPI.cache = data;
    return data;
  }
};

function formatQuakeRow(quake) {
  const time = new Date(quake.time || quake.updated_at || Date.now());
  return `
    <tr>
      <td>${time.toLocaleString("tr-TR")}</td>
      <td><strong>${quake.magnitude?.toFixed?.(1) ?? quake.magnitude}</strong></td>
      <td>${quake.depth ? `${quake.depth} km` : '-'}</td>
      <td>${quake.place || quake.location || 'Bilinmeyen'}</td>
    </tr>
  `;
}

function normalizeText(text = "") {
  return text
    .toString()
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

async function renderGlobalQuakes({
  highlightSelector,
  statusSelector,
  tableSelector,
  limit = 20,
  force = false
}) {
  try {
    const data = await QuakeAPI.fetchData(force);
    if (!data.length) throw new Error("Veri bulunamadı");

    const latest = data[0];
    if (highlightSelector) {
      const el = document.querySelector(highlightSelector);
      if (el) {
        el.innerHTML = `
          <strong>${latest.magnitude?.toFixed?.(1)} Mw</strong> - ${latest.place || "Konum paylaşılmadı"}
          <br><small>${new Date(latest.time || latest.updated_at).toLocaleString("tr-TR")}</small>
        `;
      }
    }

    if (statusSelector) {
      const el = document.querySelector(statusSelector);
      if (el) {
        const minutesAgo = Math.round(
          (Date.now() - new Date(latest.time || latest.updated_at)) / 60000
        );
        el.textContent =
          minutesAgo < 5
            ? `Evet. ${minutesAgo} dakika önce ${latest.place || "bilinmeyen noktada"} ${latest.magnitude?.toFixed?.(1)} büyüklüğünde deprem oldu.`
            : "Son 5 dakika içinde deprem kaydı yok.";
      }
    }

    if (tableSelector) {
      const tbody = document.querySelector(tableSelector);
      if (tbody) {
        tbody.innerHTML = data
          .slice(0, limit)
          .map((quake) => formatQuakeRow(quake))
          .join("");
      }
    }
  } catch (error) {
    console.error(error);
    const tbody = document.querySelector(tableSelector);
    if (tbody) {
      tbody.innerHTML = `<tr><td colspan="4">Veri alınırken hata oluştu.</td></tr>`;
    }
  }
}

async function renderCityQuakes({
  tableSelector,
  cityKeyword,
  limit = 15,
  summarySelector
}) {
  try {
    const allData = await QuakeAPI.fetchData();
    const keyword = normalizeText(cityKeyword);
    const filtered = allData.filter((quake) =>
      normalizeText(quake.place || "").includes(keyword)
    );

    if (summarySelector) {
      const el = document.querySelector(summarySelector);
      if (el) {
        el.innerHTML =
          filtered.length > 0
            ? `<strong>Son deprem:</strong> ${filtered[0].magnitude?.toFixed?.(1)} Mw - ${filtered[0].place}`
            : "Son kayıtlarda bu şehir için deprem bulunamadı.";
      }
    }

    if (tableSelector) {
      const tbody = document.querySelector(tableSelector);
      if (tbody) {
        tbody.innerHTML = filtered.length
          ? filtered.slice(0, limit).map((q) => formatQuakeRow(q)).join("")
          : `<tr><td colspan="4">${cityKeyword} için son deprem kaydı bulunamadı.</td></tr>`;
      }
    }
  } catch (error) {
    console.error(error);
    const tbody = document.querySelector(tableSelector);
    if (tbody) {
      tbody.innerHTML = `<tr><td colspan="4">Veri alınırken hata oluştu.</td></tr>`;
    }
  }
}
