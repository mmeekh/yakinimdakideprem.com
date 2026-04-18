/*
 * Ana sayfa sehir arama kutusu.
 * window.CityData (city-keywords.js) ve /api/earthquakes verisini kullanarak,
 * kullanici yazdikca eslesen sehirleri ve o sehirlerdeki son deprem bilgisini gosterir.
 */
(function () {
  "use strict";

  const MAX_RESULTS = 7;
  const DEFAULT_RESULTS = 5; // Input bossken en populer 5 ili goster
  // Baslangic seed'i (SEO verilerine ve tarihsel arama hacmine gore en populer 5 il)
  const TOP_POPULAR_SLUGS = ["istanbul", "izmir", "ankara", "kahramanmaras", "hatay"];
  const CLICK_STORAGE_KEY = "citySearchClicks_v1";
  const API_URL = "/api/earthquakes?hours_back=168&min_magnitude=1.0&limit=500";

  const state = {
    quakes: null, // Array (cache)
    quakesPromise: null,
    latestByCity: {}, // slug -> quake object
    activeIndex: -1,
  };

  function normalize(str) {
    return (str || "")
      .toString()
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      // Turkce-ozgu donusumler (NFD bunlari kapsamiyor)
      .replace(/ı/g, "i")
      .replace(/ş/g, "s")
      .replace(/ğ/g, "g")
      .replace(/ç/g, "c")
      .replace(/ö/g, "o")
      .replace(/ü/g, "u");
  }

  function fetchQuakes() {
    if (state.quakes) return Promise.resolve(state.quakes);
    if (state.quakesPromise) return state.quakesPromise;

    state.quakesPromise = fetch(API_URL)
      .then((res) => (res.ok ? res.json() : Promise.reject(new Error("api"))))
      .then((json) => {
        const data = Array.isArray(json.data) ? json.data : [];
        state.quakes = data;
        buildLatestIndex(data);
        return data;
      })
      .catch(() => {
        state.quakes = [];
        return [];
      });
    return state.quakesPromise;
  }

  function buildLatestIndex(quakes) {
    if (!window.CityData || !Array.isArray(window.CityData)) return;

    // Quakes'i zamana gore sirala (en yeni once)
    const sorted = [...quakes].sort((a, b) => {
      const ta = new Date((a.time || "").replace(/\./g, "-")).getTime() || 0;
      const tb = new Date((b.time || "").replace(/\./g, "-")).getTime() || 0;
      return tb - ta;
    });

    window.CityData.forEach((city) => {
      const aliases = city.keywords.map(normalize);
      const match = sorted.find((q) => {
        const place = normalize(q.place || q.location || "");
        return aliases.some((a) => place.includes(a));
      });
      if (match) state.latestByCity[city.slug] = match;
    });
  }

  function parseQuakeTime(quake) {
    const raw = quake.time || quake.date || "";
    const clean = raw.toString().replace(/\./g, "-");
    const d = new Date(clean);
    return isNaN(d.getTime()) ? null : d;
  }

  function formatAgo(date) {
    if (!date) return "";
    const diff = Math.floor((Date.now() - date.getTime()) / 1000);
    if (diff < 60) return `${diff} sn once`;
    const min = Math.floor(diff / 60);
    if (min < 60) return `${min} dk once`;
    const hr = Math.floor(min / 60);
    if (hr < 48) return `${hr} saat once`;
    const day = Math.floor(hr / 24);
    return `${day} gun once`;
  }

  function magnitudeColor(mag) {
    const v = Number(mag);
    if (!Number.isFinite(v)) return "#6b7280";
    if (v >= 5) return "#b71c1c";
    if (v >= 4) return "#ef4444";
    if (v >= 3) return "#f59e0b";
    return "#16a34a";
  }

  function getClickCounts() {
    try {
      const raw = localStorage.getItem(CLICK_STORAGE_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      return {};
    }
  }

  function recordClick(slug) {
    if (!slug) return;
    try {
      const counts = getClickCounts();
      counts[slug] = (counts[slug] || 0) + 1;
      localStorage.setItem(CLICK_STORAGE_KEY, JSON.stringify(counts));
    } catch (e) {
      /* quota vs. - sessizce gec */
    }
  }

  function searchCities(query) {
    const cities = window.CityData || [];
    if (!query) {
      // Kullanicinin kendi tiklama gecmisi + curated populer listesini birlestir
      const counts = getClickCounts();
      const userTop = Object.entries(counts)
        .sort((a, b) => b[1] - a[1])
        .map(([slug]) => slug);
      // Once kullanicinin en cok tikladigi, sonra populer default'lar (tekrar edenler atlanir)
      const mergedOrder = [...userTop, ...TOP_POPULAR_SLUGS];
      const seen = new Set();
      const result = [];
      for (const slug of mergedOrder) {
        if (seen.has(slug)) continue;
        seen.add(slug);
        const city = cities.find((c) => c.slug === slug);
        if (city) result.push(city);
        if (result.length >= DEFAULT_RESULTS) break;
      }
      return result;
    }
    const q = normalize(query);
    const prefix = [];
    const contains = [];
    cities.forEach((city) => {
      const nName = normalize(city.name);
      const nSlug = normalize(city.slug);
      const nRegion = normalize(city.region);
      if (nName.startsWith(q) || nSlug.startsWith(q)) {
        prefix.push(city);
      } else if (nName.includes(q) || nSlug.includes(q) || nRegion.includes(q)) {
        contains.push(city);
      } else if (city.keywords.some((k) => normalize(k).startsWith(q))) {
        contains.push(city);
      }
    });
    return [...prefix, ...contains].slice(0, MAX_RESULTS);
  }

  function renderResults(results, resultsEl) {
    if (!results.length) {
      resultsEl.innerHTML = '<li class="city-search-empty">Sehir bulunamadi</li>';
      resultsEl.hidden = false;
      state.activeIndex = -1;
      return;
    }

    resultsEl.innerHTML = results
      .map((city, i) => {
        const latest = state.latestByCity[city.slug];
        let quakeHtml;
        if (latest) {
          const mag = Number(latest.magnitude);
          const magText = Number.isFinite(mag) ? mag.toFixed(1) : "?";
          const date = parseQuakeTime(latest);
          const ago = formatAgo(date);
          quakeHtml = `
            <span class="city-search-quake">
              <span class="city-search-mag" style="background:${magnitudeColor(mag)}">${magText}</span>
              <span class="city-search-ago">${ago}</span>
            </span>`;
        } else if (state.quakes === null) {
          quakeHtml = '<span class="city-search-quake city-search-quake--loading">...</span>';
        } else {
          quakeHtml = '<span class="city-search-quake city-search-quake--none">Son kayit yok</span>';
        }

        return `
          <li role="option" data-index="${i}">
            <a href="/deprem-${city.slug}.html" class="city-search-item${i === state.activeIndex ? " is-active" : ""}">
              <span class="city-search-city">
                <i class="fas fa-map-marker-alt" aria-hidden="true"></i>
                <span>
                  <strong>${city.name}</strong>
                  <small>${city.region}</small>
                </span>
              </span>
              ${quakeHtml}
            </a>
          </li>`;
      })
      .join("");
    resultsEl.hidden = false;
  }

  function navigateActive(delta, resultsEl) {
    const items = resultsEl.querySelectorAll("li[data-index]");
    if (!items.length) return;
    state.activeIndex = (state.activeIndex + delta + items.length) % items.length;
    items.forEach((li) => li.querySelector(".city-search-item")?.classList.remove("is-active"));
    const cur = items[state.activeIndex];
    cur.querySelector(".city-search-item")?.classList.add("is-active");
    cur.scrollIntoView({ block: "nearest" });
  }

  function slugFromHref(href) {
    const m = (href || "").match(/deprem-([^./]+)\.html/);
    return m ? m[1] : null;
  }

  function openActive(resultsEl) {
    const items = resultsEl.querySelectorAll(".city-search-item");
    const target = items[state.activeIndex] || items[0];
    if (target) {
      recordClick(slugFromHref(target.getAttribute("href")));
      window.location.href = target.getAttribute("href");
    }
  }

  function setup() {
    const container = document.getElementById("city-search");
    if (!container) return;
    const input = container.querySelector("#city-search-input");
    const clearBtn = container.querySelector("#city-search-clear");
    const resultsEl = container.querySelector("#city-search-results");
    if (!input || !resultsEl) return;

    // API fetch baslat, sonuclar gelince mevcut render'i yenile
    fetchQuakes().then(() => {
      if (!resultsEl.hidden) render();
    });

    function render() {
      const q = input.value.trim();
      const results = searchCities(q);
      renderResults(results, resultsEl);
      state.activeIndex = -1;
    }

    input.addEventListener("focus", render);
    input.addEventListener("input", () => {
      clearBtn.hidden = !input.value;
      render();
    });

    input.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        navigateActive(1, resultsEl);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        navigateActive(-1, resultsEl);
      } else if (e.key === "Enter") {
        e.preventDefault();
        openActive(resultsEl);
      } else if (e.key === "Escape") {
        resultsEl.hidden = true;
        input.blur();
      }
    });

    clearBtn.addEventListener("click", () => {
      input.value = "";
      clearBtn.hidden = true;
      resultsEl.hidden = true;
      state.activeIndex = -1;
      input.focus();
    });

    // Container disinda tiklama -> dropdown kapat
    document.addEventListener("click", (e) => {
      if (!container.contains(e.target)) resultsEl.hidden = true;
    });

    // Sonuc uzerine tiklayinca (fare/dokunmatik) secimi localStorage'a yaz
    resultsEl.addEventListener(
      "click",
      (e) => {
        const item = e.target.closest(".city-search-item");
        if (item) recordClick(slugFromHref(item.getAttribute("href")));
      },
      true // capture - navigate'ten once calisir
    );

    // Herhangi bir header menusu/dropdown'i acildiginda arama sonuclarini kapat
    const closeOnMenuOpen = (e) => {
      const t = e.target.closest(".menu-toggle, .info-toggle, .nav-dropdown .dropdown-toggle");
      if (t) resultsEl.hidden = true;
    };
    document.addEventListener("click", closeOnMenuOpen, true); // capture fazi - diger handlerlardan once

    // body'deki nav-open / info-menu-open siniflarini izle (header.js bunlari toggle ediyor)
    const bodyObserver = new MutationObserver(() => {
      if (
        document.body.classList.contains("nav-open") ||
        document.body.classList.contains("info-menu-open")
      ) {
        resultsEl.hidden = true;
      }
    });
    bodyObserver.observe(document.body, { attributes: true, attributeFilter: ["class"] });

    // Sayfa scroll edildiginde de kapat (mobilde UX temizligi)
    let lastScrollY = window.scrollY;
    window.addEventListener(
      "scroll",
      () => {
        if (Math.abs(window.scrollY - lastScrollY) > 40) {
          resultsEl.hidden = true;
          lastScrollY = window.scrollY;
        }
      },
      { passive: true }
    );
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setup);
  } else {
    setup();
  }
})();
