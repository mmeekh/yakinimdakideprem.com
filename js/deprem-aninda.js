/**
 * Deprem Anında Sayfası JavaScript - Optimized version
 * Handles page-specific functionality
 */

// Configuration
const PAGE_CONFIG = {
    SCROLL_THRESHOLD: 100,
    ANIMATION_DELAY: 100
};

// State management
let isInitialized = false;

// Initialize page functionality
document.addEventListener('DOMContentLoaded', () => {
    if (isInitialized) return;
    
    try {
        setupScrollEffect();
        setupEmergencyContacts();
        setupAnimations();
        isInitialized = true;
    } catch (error) {
        console.error('Sayfa başlatılamadı:', error);
    }
});

// Setup scroll effect with throttling
function setupScrollEffect() {
    let lastScrollTop = 0;
    let ticking = false;
    const hiddenHeader = document.getElementById('hidden-header');

    if (!hiddenHeader) return;

    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(() => {
                handleScroll(lastScrollTop, hiddenHeader);
                ticking = false;
            });
            ticking = true;
        }
    });
}

// Handle scroll events
function handleScroll(lastScrollTop, hiddenHeader) {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > lastScrollTop && scrollTop > PAGE_CONFIG.SCROLL_THRESHOLD) {
        // Scrolling down - hide header
        hiddenHeader.style.top = '-80px';
    } else {
        // Scrolling up - show header
        hiddenHeader.style.top = '0';
    }

    lastScrollTop = scrollTop;
}

// Setup emergency contacts functionality
function setupEmergencyContacts() {
    const contactItems = document.querySelectorAll('.contact-item');
    
    contactItems.forEach(item => {
        item.addEventListener('click', (e) => {
            // Add click animation
            item.style.transform = 'scale(0.95)';
            setTimeout(() => {
                item.style.transform = 'scale(1)';
            }, 150);
        });
    });
}

// Setup scroll animations
function setupAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animatedElements = document.querySelectorAll('.guide-card, .contact-item');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}