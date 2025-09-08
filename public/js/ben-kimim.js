/**
 * Ben Kimim Sayfası JavaScript - Optimized version
 * Handles page-specific functionality
 */

// Configuration
const PAGE_CONFIG = {
    SCROLL_THRESHOLD: 100,
    ANIMATION_DELAY: 100
};

// State management
let isInitialized = false;
let flagAnimation = null;

// Initialize page functionality
document.addEventListener('DOMContentLoaded', () => {
    if (isInitialized) return;
    
    try {
        setupScrollEffect();
        setupContactForm();
        setupAnimations();
        setupBackendConnection();
        setupFlagAnimation();
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

    if (!hiddenHeader) {
        console.warn('hidden-header elementi bulunamadı');
        return;
    }

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

    // hiddenHeader'ın var olduğunu kontrol et
    if (hiddenHeader && hiddenHeader.style) {
        if (scrollTop > lastScrollTop && scrollTop > PAGE_CONFIG.SCROLL_THRESHOLD) {
            // Scrolling down - hide header
            hiddenHeader.style.top = '-80px';
        } else {
            // Scrolling up - show header
            hiddenHeader.style.top = '0';
        }
    }

    lastScrollTop = scrollTop;
}

// Setup contact form
function setupContactForm() {
    const contactForm = document.getElementById('contact-form');
    if (!contactForm) return;

    contactForm.addEventListener('submit', handleFormSubmit);
}

// Handle form submission
function handleFormSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const formMessage = document.getElementById('form-message');
    
    // Basic validation
    const name = formData.get('name') || document.getElementById('name')?.value;
    const email = formData.get('email') || document.getElementById('email')?.value;
    const subject = formData.get('subject') || document.getElementById('subject')?.value;
    const message = formData.get('message') || document.getElementById('message')?.value;
    
    if (!name || !email || !subject || !message) {
        showFormMessage('Lütfen tüm alanları doldurun.', 'error');
        return;
    }
    
    // Simulate form submission
    showFormMessage('Mesajınız gönderildi! En kısa sürede size dönüş yapacağız.', 'success');
    event.target.reset();
}

// Show form message
function showFormMessage(message, type) {
    const formMessage = document.getElementById('form-message');
    if (!formMessage) return;
    
    formMessage.textContent = message;
    formMessage.className = `form-message ${type}`;
    formMessage.style.display = 'block';
    
    // Hide message after 5 seconds
    setTimeout(() => {
        formMessage.style.display = 'none';
    }, 5000);
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
    const animatedElements = document.querySelectorAll('.mv-card, .value-item, .about-contact .contact-item');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Setup backend connection for earthquake data
async function setupBackendConnection() {
    try {
        // Test backend connection
        const response = await fetch('/health');
        if (response.ok) {
            console.log('Backend bağlantısı başarılı');
            
            // Fetch earthquake stats
            const statsResponse = await fetch('/api/earthquakes/stats');
            if (statsResponse.ok) {
                const statsData = await statsResponse.json();
                if (statsData.success) {
                    updatePageWithStats(statsData.stats);
                }
            }
        } else {
            console.warn('Backend bağlantısı başarısız:', response.status);
        }
    } catch (error) {
        console.warn('Backend bağlantısı hatası:', error);
        // Hata durumunda sessizce devam et
    }
}

// Update page with earthquake statistics
function updatePageWithStats(stats) {
    // Update any stats elements on the page
    const totalQuakesEl = document.getElementById('total-quakes');
    if (totalQuakesEl) {
        totalQuakesEl.textContent = stats.total_earthquakes;
    }

    const maxMagEl = document.getElementById('max-magnitude');
    if (maxMagEl) {
        maxMagEl.textContent = stats.max_magnitude.toFixed(1);
    }

    // Update last update time
    const lastUpdateEl = document.getElementById('last-update');
    if (lastUpdateEl) {
        lastUpdateEl.textContent = `Son güncelleme: ${new Date().toLocaleString('tr-TR')}`;
    }
}

// Setup flag animation
function setupFlagAnimation() {
    const flagContainer = document.getElementById('flag-container');
    if (!flagContainer) {
        console.warn('Bayrak container bulunamadı');
        return;
    }

    // Three.js yüklendiğini kontrol et
    if (typeof THREE === 'undefined') {
        console.error('Three.js yüklenemedi');
        return;
    }

    try {
        // Bayrak animasyonunu başlat
        flagAnimation = new FlagAnimation('flag-container');
        
        console.log('Bayrak animasyonu başlatıldı');
    } catch (error) {
        console.error('Bayrak animasyonu başlatılamadı:', error);
        // Hata durumunda sessizce devam et
    }
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (flagAnimation) {
        flagAnimation.destroy();
        flagAnimation = null;
    }
});
