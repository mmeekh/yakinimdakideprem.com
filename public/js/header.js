// ---- Cookie Consent (Consent Mode v2) ----
function initConsentManager() {
  try {
    window.dataLayer = window.dataLayer || [];
    if (typeof window.gtag !== 'function') {
      window.gtag = function(){ window.dataLayer.push(arguments); };
    }
    gtag('consent','default',{
      ad_storage: 'denied',
      analytics_storage: 'denied',
      functionality_storage: 'granted',
      security_storage: 'granted'
    });
    const consent = getStoredConsent();
    if (consent && consent.analytics === true) {
      grantAnalyticsConsent();
    } else {
      showCookieBanner();
    }
  } catch(e) {}
}

function getStoredConsent() {
  try {
    const raw = localStorage.getItem('cookie_consent');
    return raw ? JSON.parse(raw) : null;
  } catch(e){ return null; }
}

function storeConsent(value) {
  try {
    localStorage.setItem('cookie_consent', JSON.stringify({ analytics: !!value, ts: Date.now() }));
  } catch(e) {}
}

function grantAnalyticsConsent() {
  try {
    gtag('consent','update',{ analytics_storage: 'granted' });
    if (window.dataLayer) {
      window.dataLayer.push({ event: 'consent_update', analytics_storage: 'granted' });
    }
  } catch(e) {}
}

function denyAnalyticsConsent() {
  try {
    gtag('consent','update',{ analytics_storage: 'denied' });
    if (window.dataLayer) {
      window.dataLayer.push({ event: 'consent_update', analytics_storage: 'denied' });
    }
  } catch(e) {}
}

const GEO_ALERT_STORAGE_KEY = 'geo_alert_seen_v2';
const EDEVLET_TOPLANMA_URL = 'https://www.turkiye.gov.tr/afet-ve-acil-durum-yonetimi-acil-toplanma-alani-sorgulama';

function markGeoAlertSeen() {
  try {
    localStorage.setItem(GEO_ALERT_STORAGE_KEY, String(Date.now()));
  } catch (e) {}
}

let consentToastTimer = null;
let consentToastCleanupTimer = null;

function ensureCookieStyles() {
  const styleId = 'cookie-consent-fallback-style';
  if (document.getElementById(styleId)) return;
  const root = getComputedStyle(document.documentElement);
  const hasBgVar = root.getPropertyValue('--bg-dark').trim();
  const hasTextVar = root.getPropertyValue('--text-white').trim();
  if (hasBgVar && hasTextVar) return; // vars loaded, no need for fallback
  const style = document.createElement('style');
  style.id = styleId;
  style.textContent = `
    #cookie-consent{position:fixed;left:16px;right:16px;bottom:16px;z-index:1080;background:#161616;color:#fff;box-shadow:0 12px 32px rgba(0,0,0,.22);border-radius:16px;padding:16px;font-size:14px}
    #cookie-consent .cookie-consent__content{display:flex;flex-direction:column;gap:12px}
    #cookie-consent .cookie-consent__content p{margin:0;line-height:1.5;color:#f0f0f0}
    #cookie-consent .cookie-consent__actions{display:flex;gap:10px;justify-content:flex-end;flex-wrap:wrap}
    #cookie-consent .btn{cursor:pointer;padding:10px 16px;border-radius:10px;border:none;font-weight:700}
    #cookie-consent .btn-primary{background:#d62828;color:#fff}
    #cookie-consent .btn-ghost{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.35)}
    @media (max-width:600px){#cookie-consent{left:8px;right:8px;bottom:8px;padding:14px}}
  `;
  document.head.appendChild(style);
}

function styleCookieBanner(el) {
  if (!el) return;
  const cs = getComputedStyle(el);
  const needsBg = cs.backgroundColor === 'rgba(0, 0, 0, 0)' || cs.padding === '0px';
  if (needsBg) {
    Object.assign(el.style, {
      background: '#161616',
      color: '#fff',
      padding: '16px',
      borderRadius: '14px',
      boxShadow: '0 12px 32px rgba(0,0,0,0.22)'
    });
  }
}

function showCookieBanner() {
  const existing = document.getElementById('cookie-consent');
  if (existing) {
    ensureCookieStyles();
    styleCookieBanner(existing);
    return;
  }
  ensureCookieStyles();
  const banner = document.createElement('div');
  banner.id = 'cookie-consent';
  banner.innerHTML = `
    <div class="cookie-consent__content">
      <p>Deneyiminizi iyileştirmek için analitik çerezleri kullanıyoruz. Zorunlu çerezler her zaman aktiftir. Analitik için onay veriyor musunuz?</p>
      <div class="cookie-consent__actions">
        <button id="cookie-reject" class="btn btn-ghost">Reddet</button>
        <button id="cookie-accept" class="btn btn-primary">Kabul Et</button>
      </div>
    </div>`;
  document.body.appendChild(banner);
  styleCookieBanner(banner);
  const accept = banner.querySelector('#cookie-accept');
  const reject = banner.querySelector('#cookie-reject');
  accept.addEventListener('click', () => {
    storeConsent(true);
    grantAnalyticsConsent();
    showConsentToast('Kabul edildi');
    banner.remove();
  });
  reject.addEventListener('click', () => {
    storeConsent(false);
    denyAnalyticsConsent();
    banner.remove();
  });
}

function showConsentToast(message) {
  const DISPLAY_DURATION = 3000;
  const FADE_DURATION = 220;
  if (consentToastTimer) {
    clearTimeout(consentToastTimer);
    consentToastTimer = null;
  }
  if (consentToastCleanupTimer) {
    clearTimeout(consentToastCleanupTimer);
    consentToastCleanupTimer = null;
  }
  const existing = document.getElementById('cookie-toast');
  if (existing) {
    existing.remove();
  }
  const toast = document.createElement('div');
  toast.id = 'cookie-toast';
  toast.textContent = message;
  toast.style.position = 'fixed';
  toast.style.zIndex = '9999';
  toast.style.padding = '10px 18px';
  toast.style.borderRadius = '12px';
  toast.style.fontWeight = '600';
  toast.style.fontSize = '14px';
  toast.style.background = 'rgba(0,0,0,0.85)';
  toast.style.color = '#fff';
  toast.style.pointerEvents = 'none';
  toast.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
  toast.style.opacity = '0';
  if (window.innerWidth <= 600) {
    toast.style.top = '16px';
    toast.style.left = '50%';
    toast.style.transform = 'translate(-50%, -8px)';
    toast.style.maxWidth = 'calc(100% - 32px)';
  } else {
    toast.style.top = '24px';
    toast.style.right = '24px';
    toast.style.transform = 'translateY(-8px)';
  }
  document.body.appendChild(toast);
  requestAnimationFrame(() => {
    toast.style.opacity = '1';
    if (window.innerWidth <= 600) {
      toast.style.transform = 'translate(-50%, 0)';
    } else {
      toast.style.transform = 'translateY(0)';
    }
  });
  consentToastTimer = setTimeout(() => {
    toast.style.opacity = '0';
    if (window.innerWidth <= 600) {
      toast.style.transform = 'translate(-50%, -8px)';
    } else {
      toast.style.transform = 'translateY(-8px)';
    }
    consentToastCleanupTimer = setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
      consentToastCleanupTimer = null;
    }, FADE_DURATION);
    consentToastTimer = null;
  }, DISPLAY_DURATION);
}

/**
 * Header JavaScript - Optimized version
 * Handles header visibility, responsive navigation, and keyboard shortcuts
 */

// Configuration
const HEADER_CONFIG = {
    SCROLL_THRESHOLD: 100,
    HIDE_DELAY: 200,
    SHOW_DELAY: 50
};

const MOBILE_BREAKPOINT = 1024;

// State management
let lastScrollTop = 0;
let isHeaderVisible = true;
let scrollTimeout = null;
let ticking = false;
let isNavOpen = false;
let isInfoOpen = false;

let headerElement = null;
let navElement = null;
let menuToggleButton = null;
let infoToggleButton = null;
let mobileOverlay = null;
let infoDropdown = null;
let infoContent = null;
let legendElement = null;
let listElement = null;
let turkeyButton = null;
let legendActionsContainer = null;
let mapWrapper = null;
let updateInfoElement = null;
let cityDropdowns = [];
const dropdownHoverTimers = new WeakMap();

// Initialize header functionality
document.addEventListener('DOMContentLoaded', () => {
    try { initConsentManager(); } catch (e) {}
    headerElement = document.getElementById('hidden-header');
    if (!headerElement) return;

    headerElement.style.top = '0';
    headerElement.style.transition = 'top 0.3s ease-in-out';

    navElement = headerElement.querySelector('nav');
    mapWrapper = document.querySelector('.map-wrapper');
    legendElement = document.querySelector('.magnitude-legend');
    listElement = document.querySelector('.earthquake-list');
    turkeyButton = document.getElementById('turkey-btn');
    updateInfoElement = document.querySelector('.update-info');

    setupHeaderStructure();
    setupCityDropdowns();
    setHeaderHeightVar();
    setupScrollListener();
    setupKeyboardShortcuts();
    handleResponsivePanels();
    setupMobileWelcomeNotice();
    setupGeoAlert();

    window.addEventListener('resize', handleResize);
    document.addEventListener('click', handleDocumentClick);
    document.addEventListener('keydown', handleKeyDown);
});

// Setup scroll listener with throttling
function setupScrollListener() {
    window.addEventListener('scroll', () => {
        if (!ticking) {
            ticking = true;
            requestAnimationFrame(() => {
                handleScroll();
                ticking = false;
            });
        }
    });
}

// Handle scroll events
function handleScroll() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (!headerElement) return;

    if (isNavOpen || isInfoOpen) {
        closeNavMenu();
        closeInfoMenu();
    }

    if (scrollTimeout) {
        clearTimeout(scrollTimeout);
    }

    if (scrollTop > lastScrollTop && scrollTop > HEADER_CONFIG.SCROLL_THRESHOLD) {
        if (isHeaderVisible) {
            headerElement.style.top = '-80px';
            isHeaderVisible = false;
        }
    } else {
        if (!isHeaderVisible) {
            headerElement.style.top = '0';
            isHeaderVisible = true;
        }
    }

    lastScrollTop = scrollTop;
}

// Setup keyboard shortcuts
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', (event) => {
        if (event.key === 'F5') {
            event.preventDefault();
            refreshPage();
        }

        if (event.key === 'Escape') {
            scrollToTop();
        }
    });
}

// Refresh page without full reload
function refreshPage() {
    history.replaceState(null, '', window.location.pathname + window.location.search);
    scrollToTop();
    window.dispatchEvent(new CustomEvent('pageRefresh'));
}

// Smooth scroll to top
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// =========================
// Responsive enhancements
// =========================

function setupHeaderStructure() {
    const container = headerElement.querySelector('.container');
    if (!container) return;

    let headerActions = container.querySelector('.header-actions');
    if (!headerActions) {
        headerActions = document.createElement('div');
        headerActions.className = 'header-actions';

        infoToggleButton = document.createElement('button');
        infoToggleButton.type = 'button';
        infoToggleButton.className = 'header-btn info-toggle';
        infoToggleButton.setAttribute('aria-expanded', 'false');
        infoToggleButton.setAttribute('aria-controls', 'mobile-info-dropdown');
        infoToggleButton.setAttribute('title', 'Harita bilgileri');
        infoToggleButton.innerHTML = '<i class="fas fa-layer-group" aria-hidden="true"></i>';
        infoToggleButton.appendChild(createVisuallyHiddenSpan('Harita bilgileri panelini aç'));

        menuToggleButton = document.createElement('button');
        menuToggleButton.type = 'button';
        menuToggleButton.className = 'header-btn menu-toggle';
        menuToggleButton.setAttribute('aria-expanded', 'false');
        menuToggleButton.setAttribute('aria-controls', 'primary-navigation');
        menuToggleButton.setAttribute('title', 'Menüyü aç');
        menuToggleButton.innerHTML = '<i class="fas fa-bars" aria-hidden="true"></i>';
        menuToggleButton.appendChild(createVisuallyHiddenSpan('Menüyü aç'));

        headerActions.appendChild(infoToggleButton);
        headerActions.appendChild(menuToggleButton);
        container.appendChild(headerActions);
    } else {
        infoToggleButton = headerActions.querySelector('.info-toggle');
        menuToggleButton = headerActions.querySelector('.menu-toggle');
    }

    if (infoToggleButton && !legendElement && !listElement) {
        infoToggleButton.style.display = 'none';
    }

    if (navElement && !navElement.id) {
        navElement.id = 'primary-navigation';
    }

    setupOverlayElements();
    setupMenuToggle();
    setupInfoToggle();
    setupNavLinkHandlers();
}

function setupOverlayElements() {
    mobileOverlay = document.getElementById('mobile-overlay');
    if (!mobileOverlay) {
        mobileOverlay = document.createElement('div');
        mobileOverlay.id = 'mobile-overlay';
        document.body.appendChild(mobileOverlay);
    }

    infoDropdown = document.getElementById('mobile-info-dropdown');
    if (!infoDropdown) {
        infoDropdown = document.createElement('div');
        infoDropdown.id = 'mobile-info-dropdown';
        infoDropdown.className = 'mobile-dropdown info-dropdown';
        infoContent = document.createElement('div');
        infoContent.className = 'mobile-info-content';
        infoDropdown.appendChild(infoContent);
        document.body.appendChild(infoDropdown);
    } else {
        infoContent = infoDropdown.querySelector('.mobile-info-content') || infoDropdown;
    }

    if (mobileOverlay) {
        mobileOverlay.addEventListener('click', closeAllMenus);
    }
}

function setupMenuToggle() {
    if (!menuToggleButton) return;
    menuToggleButton.addEventListener('click', (event) => {
        event.stopPropagation();
        toggleNavMenu();
    });
}

function setupInfoToggle() {
    if (!infoToggleButton) return;
    infoToggleButton.addEventListener('click', (event) => {
        event.stopPropagation();
        toggleInfoMenu();
    });
}

function setupNavLinkHandlers() {
    if (!navElement) return;
    navElement.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= MOBILE_BREAKPOINT) {
                closeNavMenu();
            }
        });
    });
}

function handleResize() {
    setHeaderHeightVar();
    handleResponsivePanels();

    if (window.innerWidth > MOBILE_BREAKPOINT) {
        resetCityDropdowns();
    }

    if (window.innerWidth > MOBILE_BREAKPOINT) {
        closeNavMenu();
        closeInfoMenu();
    }
}

function handleDocumentClick(event) {
    if (isNavOpen && navElement && !navElement.contains(event.target) && !menuToggleButton.contains(event.target)) {
        closeNavMenu();
    }

    if (isInfoOpen && infoDropdown && !infoDropdown.contains(event.target) && !infoToggleButton.contains(event.target)) {
        closeInfoMenu();
    }

    if (window.innerWidth <= MOBILE_BREAKPOINT) {
        cityDropdowns.forEach(({ wrapper, button }) => {
            if (!wrapper.contains(event.target)) {
                wrapper.classList.remove('open');
                button.setAttribute('aria-expanded', 'false');
            }
        });
    }
}

function handleKeyDown(event) {
    if (event.key === 'Escape') {
        if (isNavOpen || isInfoOpen) {
            closeAllMenus();
        }
    }
}

function toggleNavMenu(forceState) {
    if (!menuToggleButton) return;
    const nextState = typeof forceState === 'boolean' ? forceState : !isNavOpen;
    if (nextState) {
        closeInfoMenu();
    }
    isNavOpen = nextState;
    document.body.classList.toggle('nav-open', isNavOpen);
    menuToggleButton.setAttribute('aria-expanded', String(isNavOpen));
    updateOverlayState();
}

function closeNavMenu() {
    if (!isNavOpen) return;
    toggleNavMenu(false);
}

function toggleInfoMenu(forceState) {
    if (!infoToggleButton) return;
    const nextState = typeof forceState === 'boolean' ? forceState : !isInfoOpen;
    if (nextState) {
        handleResponsivePanels();
        closeNavMenu();
    }
    isInfoOpen = nextState;
    document.body.classList.toggle('info-menu-open', isInfoOpen);
    infoToggleButton.setAttribute('aria-expanded', String(isInfoOpen));
    updateOverlayState();
}

function closeInfoMenu() {
    if (!isInfoOpen) return;
    toggleInfoMenu(false);
}

function closeAllMenus() {
    closeNavMenu();
    closeInfoMenu();
}

function updateOverlayState() {
    if (!mobileOverlay) return;
    const shouldShow = isNavOpen || isInfoOpen;
    mobileOverlay.classList.toggle('visible', shouldShow);
}

function handleResponsivePanels() {
    if (!infoContent || !mapWrapper) return;
    if (!legendElement && !listElement) return;
    if (window.innerWidth <= MOBILE_BREAKPOINT) {
        moveInfoPanelsToDropdown();
        moveLegendActionsToDropdown();
    } else {
        restoreInfoPanels();
        restoreLegendActions();
    }
}

function moveInfoPanelsToDropdown() {
    if (!infoContent) return;

    if (listElement && !infoContent.contains(listElement)) {
        listElement.classList.add('mobile-panel');
        infoContent.appendChild(listElement);
    }
}

function restoreInfoPanels() {
    if (!mapWrapper) return;

    const referenceNode = updateInfoElement || null;

    if (legendElement && !mapWrapper.contains(legendElement)) {
        legendElement.classList.remove('mobile-panel');
        mapWrapper.insertBefore(legendElement, referenceNode);
    }

    if (listElement && !mapWrapper.contains(listElement)) {
        listElement.classList.remove('mobile-panel');
        mapWrapper.insertBefore(listElement, referenceNode);
    }
}

function ensureLegendActionsContainer() {
    if (!infoContent) return;
    if (!legendActionsContainer) {
        legendActionsContainer = document.createElement('div');
        legendActionsContainer.className = 'mobile-legend-actions';
    }
    if (!infoContent.contains(legendActionsContainer)) {
        infoContent.insertBefore(legendActionsContainer, infoContent.firstChild);
    } else if (infoContent.firstChild !== legendActionsContainer) {
        infoContent.insertBefore(legendActionsContainer, infoContent.firstChild);
    }
}

function moveLegendActionsToDropdown() {
    if (!infoContent) return;
    if (!turkeyButton) return;
    ensureLegendActionsContainer();
    if (!legendActionsContainer) return;
    if (turkeyButton && !legendActionsContainer.contains(turkeyButton)) {
        legendActionsContainer.appendChild(turkeyButton);
    }
}

function restoreLegendActions() {
    if (!legendElement) return;
    if (turkeyButton && !legendElement.contains(turkeyButton)) {
        legendElement.appendChild(turkeyButton);
    }
}

function setupMobileWelcomeNotice() {
    const welcomeModal = document.getElementById('mobile-welcome-modal');
    const menuModal = document.getElementById('mobile-menu-modal');
    if (!welcomeModal && !menuModal) return;
    if (window.innerWidth > MOBILE_BREAKPOINT) return;
    const storageKey = 'mobile_welcome_seen_v1';
    try {
        if (localStorage.getItem(storageKey)) {
            return;
        }
    } catch (e) {}

    const showModal = (modal, bodyClass) => {
        if (!modal) return;
        document.body.classList.add(bodyClass);
        modal.removeAttribute('hidden');
        modal.classList.add('is-visible');
        modal.setAttribute('aria-hidden', 'false');
    };

    const hideModal = (modal, bodyClass) => {
        if (!modal) return;
        modal.classList.remove('is-visible');
        modal.setAttribute('aria-hidden', 'true');
        modal.setAttribute('hidden', '');
        document.body.classList.remove(bodyClass);
    };

    const bindDismiss = (modal, bodyClass, onDismiss) => {
        if (!modal) return;
        const dismissTargets = modal.querySelectorAll('[data-action="dismiss"]');
        const dismiss = () => {
            hideModal(modal, bodyClass);
            if (typeof onDismiss === 'function') {
                onDismiss();
            }
        };
        dismissTargets.forEach((target) => {
            target.addEventListener('click', dismiss);
        });
    };

    const markSeen = () => {
        try {
            localStorage.setItem(storageKey, String(Date.now()));
        } catch (e) {}
    };

    const showMenuModal = () => {
        showModal(menuModal, 'nav-welcome-visible');
    };

    bindDismiss(welcomeModal, 'welcome-visible', menuModal ? showMenuModal : markSeen);
    bindDismiss(menuModal, 'nav-welcome-visible', markSeen);

    const shouldDelayWelcome = () => Boolean(document.getElementById('cookie-consent'));
    const showInitialModal = () => {
        if (welcomeModal) {
            showModal(welcomeModal, 'welcome-visible');
        } else if (menuModal) {
            showMenuModal();
        }
    };
    const queueWelcome = () => {
        if (shouldDelayWelcome()) {
            setTimeout(queueWelcome, 600);
            return;
        }
        showInitialModal();
    };
    queueWelcome();
}

function setupGeoAlert() {
    if (!('geolocation' in navigator)) return;
    const permissions =
        document.permissionsPolicy || document.featurePolicy || null;
    if (permissions && typeof permissions.allowsFeature === 'function') {
        try {
            if (!permissions.allowsFeature('geolocation')) {
                return;
            }
        } catch (e) {}
    }
    if (location.protocol !== 'https:' && location.hostname !== 'localhost') return;
    try {
        if (localStorage.getItem(GEO_ALERT_STORAGE_KEY)) {
            return;
        }
    } catch (e) {}

    const shouldDelayGeoAlert = () => {
        if (document.getElementById('cookie-consent')) return true;
        if (document.body.classList.contains('welcome-visible')) return true;
        if (document.body.classList.contains('nav-welcome-visible')) return true;
        return Boolean(document.querySelector('.mobile-welcome-modal.is-visible'));
    };

    const showAlert = () => {
        const alert = document.createElement('div');
        alert.id = 'geo-alert';
        alert.innerHTML = `
            <div class="geo-alert__content">
                <div class="geo-alert__title">Yakınındaki depremi kontrol edelim mi?</div>
                <div class="geo-alert__message">Konumunu paylaşman yeterli. Konumun sadece bu cihazda işlenir ve kaydedilmez.</div>
                <div class="geo-alert__actions">
                    <button class="geo-btn geo-btn-primary" data-action="geo-allow">Konumumu Paylaş</button>
                    <button class="geo-btn geo-btn-ghost" data-action="geo-later">Şimdi Değil</button>
                </div>
            </div>
        `;

        document.body.appendChild(alert);
        adjustGeoAlertOffset(alert);

        const allowBtn = alert.querySelector('[data-action="geo-allow"]');
        const laterBtn = alert.querySelector('[data-action="geo-later"]');

        const removeAlert = () => {
            if (alert && alert.parentNode) {
                alert.parentNode.removeChild(alert);
            }
        };

        const requestLocation = () => {
            markGeoAlertSeen();
            setGeoAlertState(alert, {
                title: 'Konum alınıyor...',
                message: 'Tarayıcı izni bekleniyor. Konum izni verirsen yakınındaki depremleri kontrol edeceğiz.',
                actions: []
            });

            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    checkNearbyQuakes(alert, pos.coords.latitude, pos.coords.longitude);
                },
                (error) => {
                    const code = error && error.code;
                    const isTimeout = code === 3;
                    const isDenied = code === 1;
                    const isUnavailable = code === 2;
                    const title = isDenied
                        ? 'Konum izni kapalı olabilir'
                        : isUnavailable
                            ? 'Konum bulunamadı'
                            : isTimeout
                                ? 'Konum zaman aşımına uğradı'
                                : 'Konum alınamadı';
                    const message = isDenied
                        ? 'Konum izni kapalı olabilir. Adres çubuğundaki izinlerden konumu açıp tekrar deneyebilirsin.'
                        : isUnavailable
                            ? 'Konum servisleri kapalı veya GPS sinyali zayıf olabilir. Konum ayarlarını kontrol edip tekrar deneyebilirsin.'
                            : isTimeout
                                ? 'Konum bilgisi gecikti. Tekrar deneyebilir veya e-Devlet üzerinden toplanma alanlarını sorgulayabilirsin.'
                                : 'Konum izni olmadan yakınındaki depremleri kontrol edemiyoruz. Toplanma alanlarını yine de sorgulayabilirsin.';
                    const actions = [
                        {
                            label: 'Tekrar Dene',
                            onClick: requestLocation,
                            variant: 'primary'
                        }
                    ];
                    actions.push({
                        label: 'E-Devlet Toplanma Alanı',
                        href: EDEVLET_TOPLANMA_URL,
                        variant: 'link',
                        markSeen: true
                    });
                    actions.push({ label: 'Kapat', action: 'close', markSeen: true });
                    setGeoAlertState(alert, { title, message, actions });
                },
                { enableHighAccuracy: true, timeout: 20000, maximumAge: 60000 }
            );
        };

        if (laterBtn) {
            laterBtn.addEventListener('click', () => {
                markGeoAlertSeen();
                removeAlert();
            });
        }

        if (allowBtn) {
            allowBtn.addEventListener('click', requestLocation);
        }
    };

    const queueAlert = () => {
        if (shouldDelayGeoAlert()) {
            setTimeout(queueAlert, 800);
            return;
        }
        showAlert();
    };

    queueAlert();
}

function adjustGeoAlertOffset(alert) {
    if (!alert) return;
    const cookieBanner = document.getElementById('cookie-consent');
    if (cookieBanner) {
        alert.style.bottom = window.innerWidth <= 600 ? '110px' : '90px';
    }
}

function setGeoAlertState(alert, { title, message, actions }) {
    if (!alert) return;
    const content = alert.querySelector('.geo-alert__content');
    if (!content) return;
    content.innerHTML = `
        <div class="geo-alert__title">${title}</div>
        <div class="geo-alert__message">${message}</div>
        <div class="geo-alert__actions"></div>
    `;
    const actionsContainer = content.querySelector('.geo-alert__actions');
    if (!actionsContainer) return;
    actions.forEach((action) => {
        if (action.href) {
            const link = document.createElement('a');
            link.href = action.href;
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
            link.className = `geo-btn geo-btn-${action.variant || 'link'}`;
            link.textContent = action.label;
            if (action.markSeen) {
                link.addEventListener('click', () => {
                    markGeoAlertSeen();
                });
            }
            actionsContainer.appendChild(link);
            return;
        }
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = `geo-btn geo-btn-${action.variant || 'ghost'}`;
        btn.textContent = action.label;
        btn.addEventListener('click', () => {
            if (action.markSeen) {
                markGeoAlertSeen();
            }
            if (typeof action.onClick === 'function') {
                action.onClick();
                return;
            }
            if (action.action === 'close') {
                if (alert.parentNode) {
                    alert.parentNode.removeChild(alert);
                }
            }
        });
        actionsContainer.appendChild(btn);
    });
}

function checkNearbyQuakes(alert, lat, lng) {
    const NEARBY_RADIUS_KM = 120;
    const EMERGENCY_MAGNITUDE = 4.0;
    const EMERGENCY_MINUTES = 180;
    const params = new URLSearchParams({
        hours_back: 24,
        min_magnitude: 1.5,
        limit: 200
    });

    fetch(`/api/earthquakes?${params.toString()}`)
        .then((res) => res.json())
        .then((json) => {
            const data = json.data || [];
            if (!data.length) {
                setGeoAlertState(alert, {
                    title: 'Veri bulunamadı',
                    message: 'Şu anda deprem verisi alınamıyor. Toplanma alanlarını e-Devlet üzerinden sorgulayabilirsin.',
                    actions: [
                        {
                            label: 'E-Devlet Toplanma Alanı',
                            href: EDEVLET_TOPLANMA_URL,
                            variant: 'link'
                        },
                        { label: 'Kapat', action: 'close' }
                    ]
                });
                return;
            }

            const enriched = data
                .map((quake) => {
                    const coords = quake.coordinates || {};
                    const qLat = Number(coords.lat);
                    const qLng = Number(coords.lng);
                    if (!Number.isFinite(qLat) || !Number.isFinite(qLng)) return null;
                    const distance = haversineKm(lat, lng, qLat, qLng);
                    const time = new Date(quake.time || quake.updated_at || Date.now());
                    return { quake, distance, time };
                })
                .filter(Boolean)
                .sort((a, b) => a.distance - b.distance);

            const closest = enriched[0];
            const urgent = enriched.find((item) => {
                const mag = Number(item.quake.magnitude || 0);
                const minutesAgo = Math.round((Date.now() - item.time.getTime()) / 60000);
                return (
                    item.distance <= NEARBY_RADIUS_KM &&
                    mag >= EMERGENCY_MAGNITUDE &&
                    minutesAgo <= EMERGENCY_MINUTES
                );
            });

            if (urgent) {
                const mag = Number(urgent.quake.magnitude || 0).toFixed(1);
                const place = urgent.quake.place || urgent.quake.location || 'Yakın konum';
                const minutesAgo = Math.max(
                    0,
                    Math.round((Date.now() - urgent.time.getTime()) / 60000)
                );
                setGeoAlertState(alert, {
                    title: 'Yakınında deprem oldu',
                    message: `${mag} büyüklüğünde deprem ${place} bölgesinde, yaklaşık ${urgent.distance.toFixed(
                        0
                    )} km mesafede. ${minutesAgo} dakika önce kaydedildi.`,
                    actions: [
                        {
                            label: 'Toplanma Alanlarını Aç',
                            href: EDEVLET_TOPLANMA_URL,
                            variant: 'primary'
                        },
                        { label: 'Kapat', action: 'close' }
                    ]
                });
                return;
            }

            if (closest) {
                const mag = Number(closest.quake.magnitude || 0).toFixed(1);
                const place = closest.quake.place || closest.quake.location || 'Yakın konum';
                setGeoAlertState(alert, {
                    title: 'Yakınında acil deprem görünmüyor',
                    message: `En yakın deprem ${mag} büyüklüğünde, ${place} bölgesinde (yaklaşık ${closest.distance.toFixed(
                        0
                    )} km). Yine de toplanma alanlarını kontrol edebilirsin.`,
                    actions: [
                        {
                            label: 'E-Devlet Toplanma Alanı',
                            href: EDEVLET_TOPLANMA_URL,
                            variant: 'link'
                        },
                        { label: 'Kapat', action: 'close' }
                    ]
                });
            }
        })
        .catch(() => {
            setGeoAlertState(alert, {
                title: 'Veri alınamadı',
                message: 'Deprem verileri şu an yüklenemedi. Toplanma alanlarını e-Devlet üzerinden sorgulayabilirsin.',
                actions: [
                    {
                        label: 'E-Devlet Toplanma Alanı',
                        href: EDEVLET_TOPLANMA_URL,
                        variant: 'link'
                    },
                    { label: 'Kapat', action: 'close' }
                ]
            });
        });
}

function haversineKm(lat1, lon1, lat2, lon2) {
    const toRad = (value) => (value * Math.PI) / 180;
    const R = 6371;
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(toRad(lat1)) *
            Math.cos(toRad(lat2)) *
            Math.sin(dLon / 2) *
            Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
}

function setHeaderHeightVar() {
    if (!headerElement) return;
    const height = headerElement.offsetHeight;
    document.documentElement.style.setProperty('--header-height', height + 'px');
}

function setupCityDropdowns() {
    if (!headerElement) return;
    cityDropdowns = [];
    const dropdowns = headerElement.querySelectorAll('.nav-dropdown');
    dropdowns.forEach((dropdown) => {
        const button = dropdown.querySelector('.dropdown-toggle');
        if (!button) return;
        button.setAttribute('aria-expanded', 'false');
        button.addEventListener('click', (event) => {
            if (window.innerWidth > MOBILE_BREAKPOINT) return;
            event.preventDefault();
            clearHoverTimer(dropdown);
            const isOpen = dropdown.classList.toggle('open');
            button.setAttribute('aria-expanded', String(isOpen));
            cityDropdowns.forEach(({ wrapper, button: other }) => {
                if (wrapper !== dropdown) {
                    clearHoverTimer(wrapper);
                    wrapper.classList.remove('open');
                    other.setAttribute('aria-expanded', 'false');
                }
            });
        });
        setupDesktopHoverDropdown(dropdown, button);
        cityDropdowns.push({ wrapper: dropdown, button });
    });
}

function resetCityDropdowns() {
    cityDropdowns.forEach(({ wrapper, button }) => {
        clearHoverTimer(wrapper);
        wrapper.classList.remove('open');
        button.setAttribute('aria-expanded', 'false');
    });
}

function setupDesktopHoverDropdown(dropdown, button) {
    dropdown.addEventListener('mouseenter', () => {
        if (window.innerWidth <= MOBILE_BREAKPOINT) return;
        clearHoverTimer(dropdown);
        dropdown.classList.add('open');
        button.setAttribute('aria-expanded', 'true');
    });

    dropdown.addEventListener('mouseleave', () => {
        if (window.innerWidth <= MOBILE_BREAKPOINT) return;
        scheduleHoverClose(dropdown, button);
    });
}

function scheduleHoverClose(dropdown, button) {
    clearHoverTimer(dropdown);
    const timer = setTimeout(() => {
        dropdown.classList.remove('open');
        button.setAttribute('aria-expanded', 'false');
    }, 200);
    dropdownHoverTimers.set(dropdown, timer);
}

function clearHoverTimer(dropdown) {
    const timer = dropdownHoverTimers.get(dropdown);
    if (timer) {
        clearTimeout(timer);
        dropdownHoverTimers.delete(dropdown);
    }
}

function createVisuallyHiddenSpan(text) {
    const span = document.createElement('span');
    span.className = 'visually-hidden';
    span.textContent = text;
    return span;
}
