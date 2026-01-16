const QuakeAPI = {
  cache: null,
  async fetchData(force = false) {
    if (!force && QuakeAPI.cache) {
      return QuakeAPI.cache;
    }

    const params = new URLSearchParams({
      hours_back: 168,
      min_magnitude: 1.5,
      limit: 250
    });

    const res = await fetch(`/api/earthquakes?${params.toString()}`);
    if (!res.ok) {
      throw new Error("Deprem verileri alınamadı");
    }

    const json = await res.json();
    const data = json.data || [];
    QuakeAPI.cache = data;
    return data;
  }
};

function getQuakeTime(quake) {
  const raw = quake.time || quake.updated_at || quake.date;
  const date = raw ? new Date(raw) : new Date();
  return Number.isNaN(date.getTime()) ? new Date() : date;
}

function formatShortDate(date) {
  return date.toLocaleString("tr-TR", {
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit"
  });
}

function getMagnitudeValue(quake) {
  const value = Number(quake.magnitude);
  return Number.isFinite(value) ? value : null;
}

function getMagnitudeColor(magnitude) {
  if (magnitude >= 6) return "#b71c1c";
  if (magnitude >= 5) return "#d32f2f";
  if (magnitude >= 4) return "#f44336";
  return "#f59e0b";
}

function formatQuakeRow(quake) {
  const time = getQuakeTime(quake);
  return `
    <tr>
      <td>${time.toLocaleString("tr-TR")}</td>
      <td><strong>${quake.magnitude?.toFixed?.(1) ?? quake.magnitude}</strong></td>
      <td>${quake.depth ? `${quake.depth} km` : "-"}</td>
      <td>${quake.place || quake.location || "Bilinmeyen"}</td>
    </tr>
  `;
}

function formatQuakeRowWithBadge(quake) {
  const time = getQuakeTime(quake);
  const magnitude = getMagnitudeValue(quake);
  const label = magnitude !== null ? magnitude.toFixed(1) : "-";
  const badge = magnitude !== null
    ? `<span class="magnitude-badge" style="background:${getMagnitudeColor(magnitude)}">${label}</span>`
    : "-";

  return `
    <tr>
      <td>${time.toLocaleString("tr-TR")}</td>
      <td>${badge}</td>
      <td>${quake.depth ? `${quake.depth} km` : "-"}</td>
      <td>${quake.place || quake.location || "Bilinmeyen"}</td>
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
  force = false,
  useBadge = false
}) {
  try {
    const data = await QuakeAPI.fetchData(force);
    if (!data.length) throw new Error("Veri bulunamadı");

    const latest = data[0];
    if (highlightSelector) {
      const el = document.querySelector(highlightSelector);
      if (el) {
        el.innerHTML = `
          <strong>${latest.magnitude?.toFixed?.(1)} Mw</strong> - ${
            latest.place || "Konum paylaşılmadı"
          }
          <br><small>${new Date(latest.time || latest.updated_at).toLocaleString(
            "tr-TR"
          )}</small>
        `;
      }
    }

    if (statusSelector) {
      const el = document.querySelector(statusSelector);
      if (el) {
        const latestTime = getQuakeTime(latest);
        const minutesAgo = Math.max(
          0,
          Math.round((Date.now() - latestTime.getTime()) / 60000)
        );
        if (minutesAgo < 5) {
          el.textContent = `Evet. ${minutesAgo} dakika önce ${
            latest.place || "bilinmeyen noktada"
          } ${latest.magnitude?.toFixed?.(1)} büyüklüğünde deprem oldu.`;
        } else {
          const place = latest.place || latest.location || "bilinmeyen noktada";
          const mag = latest.magnitude?.toFixed?.(1) ?? latest.magnitude;
          el.textContent = `Son 5 dakika içinde deprem kaydı yok. Son deprem: ${mag} büyüklüğünde, ${place}.`;
        }
      }
    }

    if (tableSelector) {
      const tbody = document.querySelector(tableSelector);
      if (tbody) {
        tbody.innerHTML = data
          .slice(0, limit)
          .map((quake) =>
            useBadge ? formatQuakeRowWithBadge(quake) : formatQuakeRow(quake)
          )
          .join("");
      }
    }
  } catch (error) {
    console.error(error);
    const tbody = document.querySelector(tableSelector);
    if (tbody) {
      tbody.innerHTML =
        '<tr><td colspan="4">Veri alınırken hata oluştu.</td></tr>';
    }
  }
}

async function renderSonDakikaPanels({ force = false } = {}) {
  try {
    const summaryTotal = document.getElementById("summary-total");
    const summaryStrongest = document.getElementById("summary-strongest");
    const summaryStrongestPlace = document.getElementById(
      "summary-strongest-place"
    );
    const summaryLast = document.getElementById("summary-last");
    const summaryLastTime = document.getElementById("summary-last-time");
    const summaryM4 = document.getElementById("summary-m4");
    const summaryUpdated = document.getElementById("live-updated");
    const m4Table = document.getElementById("m4plus-table");

    if (
      !summaryTotal &&
      !summaryStrongest &&
      !summaryStrongestPlace &&
      !summaryLast &&
      !summaryLastTime &&
      !summaryM4 &&
      !m4Table
    ) {
      return;
    }

    const data = await QuakeAPI.fetchData(force);
    if (!data.length) {
      return;
    }

    const sorted = [...data].sort(
      (a, b) => getQuakeTime(b) - getQuakeTime(a)
    );
    const now = Date.now();
    const last24 = sorted.filter(
      (quake) => now - getQuakeTime(quake).getTime() <= 24 * 60 * 60 * 1000
    );
    const last7 = sorted.filter(
      (quake) => now - getQuakeTime(quake).getTime() <= 7 * 24 * 60 * 60 * 1000
    );

    if (summaryTotal) {
      summaryTotal.textContent = String(last24.length);
    }

    if (summaryM4) {
      const m4count = last7.filter((q) => (getMagnitudeValue(q) ?? 0) >= 4)
        .length;
      summaryM4.textContent = String(m4count);
    }

    const strongest = last24.reduce((max, quake) => {
      const value = getMagnitudeValue(quake) ?? -1;
      const maxValue = getMagnitudeValue(max) ?? -1;
      return value > maxValue ? quake : max;
    }, last24[0] || sorted[0]);

    if (strongest && summaryStrongest) {
      const strongestValue = getMagnitudeValue(strongest);
      summaryStrongest.textContent =
        strongestValue !== null ? `${strongestValue.toFixed(1)} Mw` : "-";
    }

    if (strongest && summaryStrongestPlace) {
      summaryStrongestPlace.textContent =
        strongest.place || strongest.location || "Bilinmeyen lokasyon";
    }

    const latest = sorted[0];
    if (latest && summaryLast) {
      const latestValue = getMagnitudeValue(latest);
      summaryLast.textContent =
        latestValue !== null
          ? `${latestValue.toFixed(1)} Mw ${latest.place || ""}`.trim()
          : latest.place || "Son deprem";
    }

    if (latest && summaryLastTime) {
      summaryLastTime.textContent = formatShortDate(getQuakeTime(latest));
    }

    if (latest && summaryUpdated) {
      summaryUpdated.textContent = formatShortDate(getQuakeTime(latest));
    }

    if (m4Table) {
      const m4list = last7.filter((q) => (getMagnitudeValue(q) ?? 0) >= 4);
      m4Table.innerHTML = m4list.length
        ? m4list.slice(0, 20).map((q) => formatQuakeRowWithBadge(q)).join("")
        : '<tr><td colspan="4">Son 7 gün içinde 4.0+ deprem kaydı yok.</td></tr>';
    }
  } catch (error) {
    console.error(error);
    const m4Table = document.getElementById("m4plus-table");
    if (m4Table) {
      m4Table.innerHTML =
        '<tr><td colspan="4">Veri alınırken hata oluştu.</td></tr>';
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
    const aliases =
      (window.CityKeywords && window.CityKeywords[cityKeyword]) || [
        cityKeyword
      ];
    const normalizedAliases = aliases.map((alias) => normalizeText(alias));
    const filtered = allData.filter((quake) => {
      const place = normalizeText(quake.place || quake.location || "");
      return normalizedAliases.some((alias) => place.includes(alias));
    });

    if (summarySelector) {
      const el = document.querySelector(summarySelector);
      if (el) {
        el.innerHTML =
          filtered.length > 0
            ? `<strong>Son deprem:</strong> ${filtered[0].magnitude?.toFixed?.(
                1
              )} Mw - ${filtered[0].place}`
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
      tbody.innerHTML =
        '<tr><td colspan="4">Veri alınırken hata oluştu.</td></tr>';
    }
  }
}
