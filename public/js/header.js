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

const MOBILE_BREAKPOINT = 768;

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
let mapWrapper = null;
let updateInfoElement = null;
let cityDropdowns = [];

// Initialize header functionality
document.addEventListener('DOMContentLoaded', () => {
    headerElement = document.getElementById('hidden-header');
    if (!headerElement) return;

    headerElement.style.top = '0';
    headerElement.style.transition = 'top 0.3s ease-in-out';

    navElement = headerElement.querySelector('nav');
    mapWrapper = document.querySelector('.map-wrapper');
    legendElement = document.querySelector('.magnitude-legend');
    listElement = document.querySelector('.earthquake-list');
    updateInfoElement = document.querySelector('.update-info');

    setupHeaderStructure();
    setupCityDropdowns();
    setHeaderHeightVar();
    setupScrollListener();
    setupKeyboardShortcuts();
    handleResponsivePanels();

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
    if (!legendElement || !listElement || !infoContent || !mapWrapper) return;
    if (window.innerWidth <= MOBILE_BREAKPOINT) {
        moveInfoPanelsToDropdown();
    } else {
        restoreInfoPanels();
    }
}

function moveInfoPanelsToDropdown() {
    if (!infoContent) return;

    if (!infoContent.contains(legendElement)) {
        legendElement.classList.add('mobile-panel');
        infoContent.appendChild(legendElement);
    }

    if (!infoContent.contains(listElement)) {
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
            const isOpen = dropdown.classList.toggle('open');
            button.setAttribute('aria-expanded', String(isOpen));
            cityDropdowns.forEach(({ wrapper, button: other }) => {
                if (wrapper !== dropdown) {
                    wrapper.classList.remove('open');
                    other.setAttribute('aria-expanded', 'false');
                }
            });
        });
        cityDropdowns.push({ wrapper: dropdown, button });
    });
}

function resetCityDropdowns() {
    cityDropdowns.forEach(({ wrapper, button }) => {
        wrapper.classList.remove('open');
        button.setAttribute('aria-expanded', 'false');
    });
}

function createVisuallyHiddenSpan(text) {
    const span = document.createElement('span');
    span.className = 'visually-hidden';
    span.textContent = text;
    return span;
}
