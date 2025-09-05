document.addEventListener('DOMContentLoaded', () => {
    const hiddenHeader = document.getElementById('hidden-header');
    if (!hiddenHeader) return;
    hiddenHeader.style.top = '0';
});

document.addEventListener('keydown', (event) => {
    if (event.key === 'F5') {
        event.preventDefault();
        history.replaceState(null, '', window.location.pathname + window.location.search);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
});
