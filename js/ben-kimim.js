// Sayfa yüklendiğinde çalışacak fonksiyon
document.addEventListener('DOMContentLoaded', () => {
    setupScrollEffect();
});

// Scroll efekti
function setupScrollEffect() {
    let lastScrollTop = 0;
    const hiddenHeader = document.getElementById('hidden-header');

    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Aşağı scroll - gizle
            hiddenHeader.style.top = '-80px';
        } else {
            // Yukarı scroll - göster
            hiddenHeader.style.top = '0';
        }

        lastScrollTop = scrollTop;
    });
}
