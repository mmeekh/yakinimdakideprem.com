/**
 * Header JavaScript - Optimized version
 * Handles header visibility and keyboard shortcuts
 */

// Configuration
const HEADER_CONFIG = {
    SCROLL_THRESHOLD: 100,
    HIDE_DELAY: 200,
    SHOW_DELAY: 50
};

// State management
let lastScrollTop = 0;
let isHeaderVisible = true;
let scrollTimeout = null;

// Initialize header functionality
document.addEventListener('DOMContentLoaded', () => {
    const hiddenHeader = document.getElementById('hidden-header');
    if (!hiddenHeader) return;
    
    // Set initial state
    hiddenHeader.style.top = '0';
    hiddenHeader.style.transition = 'top 0.3s ease-in-out';
    
    // Setup scroll listener
    setupScrollListener();
    
    // Setup keyboard shortcuts
    setupKeyboardShortcuts();
});

// Setup scroll listener with throttling
function setupScrollListener() {
    let ticking = false;
    
    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(handleScroll);
            ticking = true;
        }
    });
}

// Handle scroll events
function handleScroll() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const hiddenHeader = document.getElementById('hidden-header');
    
    if (!hiddenHeader) return;
    
    // Clear existing timeout
    if (scrollTimeout) {
        clearTimeout(scrollTimeout);
    }
    
    // Show/hide header based on scroll direction and position
    if (scrollTop > lastScrollTop && scrollTop > HEADER_CONFIG.SCROLL_THRESHOLD) {
        // Scrolling down - hide header
        if (isHeaderVisible) {
            hiddenHeader.style.top = '-80px';
            isHeaderVisible = false;
        }
    } else {
        // Scrolling up - show header
        if (!isHeaderVisible) {
            hiddenHeader.style.top = '0';
            isHeaderVisible = true;
        }
    }
    
    lastScrollTop = scrollTop;
    
    // Reset ticking flag
    ticking = false;
}

// Setup keyboard shortcuts
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', (event) => {
        // F5 key - refresh page and scroll to top
        if (event.key === 'F5') {
            event.preventDefault();
            refreshPage();
        }
        
        // Escape key - scroll to top
        if (event.key === 'Escape') {
            scrollToTop();
        }
    });
}

// Refresh page without full reload
function refreshPage() {
    // Update URL without reload
    history.replaceState(null, '', window.location.pathname + window.location.search);
    
    // Scroll to top
    scrollToTop();
    
    // Trigger a custom event for other scripts to listen
    window.dispatchEvent(new CustomEvent('pageRefresh'));
}

// Smooth scroll to top
function scrollToTop() {
    window.scrollTo({ 
        top: 0, 
        behavior: 'smooth' 
    });
}
