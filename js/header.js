document.addEventListener('DOMContentLoaded', () => {
    let lastScrollTop = 0;
    const hiddenHeader = document.getElementById('hidden-header');

    if (!hiddenHeader) return;

    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > lastScrollTop && scrollTop > 100) {
            hiddenHeader.style.top = '-80px';
        } else {
            hiddenHeader.style.top = '0';
        }

        lastScrollTop = scrollTop;
    });
});
