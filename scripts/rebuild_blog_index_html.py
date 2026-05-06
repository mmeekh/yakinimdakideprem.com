#!/usr/bin/env python3
"""
blog.html'i yeniden inşa eder:
- Mevcut head bölümünü korur
- Yeni body: kategori filtre + posts grid + pagination (JS-driven)
- blog_index.json'dan tüm posts'u yükler
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
INDEX = ROOT / "scripts" / "blog_index.json"

posts = json.loads(INDEX.read_text(encoding="utf-8"))

CATEGORIES = [
    ("all",       "📚 Tümü",            "#d32f2f"),
    ("hazirlik",  "🎒 Hazırlık",        "#d32f2f"),
    ("sirasinda", "⚡ Deprem Anında",    "#ff6b35"),
    ("sonrasi",   "🆘 Deprem Sonrası",   "#c62828"),
    ("bilim",     "🧪 Bilim ve Teknik",  "#1565c0"),
    ("sehir",     "🏙 Şehir ve Tarih",   "#6a1b9a"),
    ("sigorta",   "📰 Sigorta & Hukuk",  "#2e7d32"),
]

# Build category counts dynamically
from collections import Counter
counts = Counter(p["cat"] for p in posts)
counts["all"] = len(posts)

# JSON for inline JS
posts_js = json.dumps(posts, ensure_ascii=False)

# Build category buttons HTML
cat_buttons = []
for slug, label, color in CATEGORIES:
    n = counts.get(slug, 0)
    cls = "cat-btn is-active" if slug == "all" else "cat-btn"
    cat_buttons.append(
        f'                <button class="{cls}" data-cat="{slug}" type="button" '
        f'style="--cat-color: {color};">{label} <small>({n})</small></button>'
    )
buttons_html = "\n".join(cat_buttons)

# Generate ALL cards as static HTML (SEO-friendly: all 58 cards in source).
# JS pagination will hide/show based on cat + page.
cards_html_parts = []
for p in posts:
    cat_class = f' data-cat="{p["cat"]}"'
    cards_html_parts.append(
        f'                <a class="blog-card"{cat_class} href="{p["href"]}" rel="noopener noreferrer">\n'
        f'                    <div class="blog-image"><img loading="lazy" src="{p["img"]}" '
        f'alt="{p["alt"]}" width="1200" height="675"></div>\n'
        f'                    <h3>{p["title"]}</h3>\n'
        f'                    <p>{p["desc"]}</p>\n'
        f'                </a>'
    )
cards_html = "\n".join(cards_html_parts)

# Total posts and pages calculation
PAGE_SIZE = 12
total_pages = (len(posts) + PAGE_SIZE - 1) // PAGE_SIZE

# Read existing blog.html, extract <head> until </head>
src = (PUBLIC / "blog.html").read_text(encoding="utf-8")
head_end = src.index("</head>") + len("</head>")
head_section = src[:head_end]

# Update <title> and <meta description> for current count
import re
head_section = re.sub(
    r'<title>[^<]+</title>',
    f'<title>Deprem Blogu — {len(posts)} Rehber | Yakınımdaki Deprem</title>',
    head_section, count=1)
head_section = re.sub(
    r'(<meta name="description"\s+content=)"[^"]+"',
    rf'\1"Türkiye\'nin {len(posts)} kapsamlı deprem rehberi: çanta, hazırlık, anında davranış, sonrası toparlanma, DASK, kentsel dönüşüm ve daha fazlası."',
    head_section, count=1)

# Append pagination CSS to head's <style> block
pagination_css = """
        /* Pagination & filter */
        .blog-grid-container { padding: 16px 0 40px; }
        .blog-card.is-hidden { display: none; }
        .pagination-controls { display: flex; gap: 12px; justify-content: center; align-items: center; padding: 32px 0; flex-wrap: wrap; }
        .page-btn { background: #fff; border: 2px solid #e5e7eb; color: #1f2937; padding: 10px 16px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.18s ease; font-family: inherit; min-width: 44px; }
        .page-btn:hover:not(:disabled) { border-color: #d32f2f; color: #d32f2f; }
        .page-btn.is-active { background: #d32f2f; border-color: #d32f2f; color: #fff; }
        .page-btn:disabled { opacity: 0.4; cursor: not-allowed; }
        .page-info { font-size: 0.95rem; color: #555; }
        .empty-state { text-align: center; padding: 60px 20px; color: #888; font-size: 1.05rem; }
"""
head_section = head_section.replace("</style>", pagination_css + "    </style>", 1)

# Build new body
body = f"""<body>
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-WQZS53QX" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <header id="hidden-header">
        <div class="container">
            <a href="/" class="logo"><img src="icons/logo.png" alt="Yakınımdaki Deprem" width="50" height="50"><span data-text="Yakınımdaki Deprem">Yakınımdaki Deprem</span></a>
            <div id="city-search" class="city-search" role="search">
                <div class="city-search__bar">
                    <i class="fas fa-search city-search__icon" aria-hidden="true"></i>
                    <label for="city-search-input" class="sr-only">Şehir ara</label>
                    <input type="text" id="city-search-input" placeholder="Şehir Ara 🏙️" autocomplete="off" aria-autocomplete="list" aria-controls="city-search-results">
                    <button type="button" id="city-search-clear" aria-label="Temizle" hidden><i class="fas fa-times" aria-hidden="true"></i></button>
                </div>
                <ul id="city-search-results" class="city-search__results" role="listbox" hidden></ul>
            </div>
            <nav>
                <a href="/">Ana Sayfa</a>
                <a href="/son-dakika-deprem.html" class="nav-highlight nav-alert">Son Dakika <span class="alarm-dot" aria-hidden="true"></span></a>
                <div class="nav-dropdown nav-dropdown-guides">
                    <button class="dropdown-toggle" type="button" aria-haspopup="true" aria-expanded="false">Rehberler <i class="fas fa-chevron-down"></i></button>
                    <div class="dropdown-menu">
                        <a href="/deprem-aninda.html">Deprem Anında</a>
                        <a href="/ilk-yardim-cantasi.html">İlk Yardım Çantası</a>
                        <a href="/blog.html"><strong>Blog</strong></a>
                    </div>
                </div>
                <div class="nav-dropdown">
                    <button class="dropdown-toggle" type="button" aria-haspopup="true" aria-expanded="false">Şehir Depremleri <i class="fas fa-chevron-down"></i></button>
                    <div class="dropdown-menu">
                        <a href="/deprem-sehirleri.html"><strong>📍 Tüm 81 İl</strong></a>
                        <a href="/deprem-istanbul.html">İstanbul</a>
                        <a href="/deprem-izmir.html">İzmir</a>
                        <a href="/deprem-ankara.html">Ankara</a>
                    </div>
                </div>
            </nav>
        </div>
    </header>

    <header class="page-header">
        <div class="container">
            <h1>Deprem Blogu</h1>
            <p>{len(posts)} kapsamlı rehber: deprem öncesi hazırlık, anında davranış, sonrası toparlanma, DASK, kentsel dönüşüm, hukuki haklar ve şehir bazlı analizler.</p>
        </div>
    </header>

    <main class="container">
        <!-- Kategori Filtresi -->
        <nav class="blog-categories" aria-label="Blog kategorileri">
{buttons_html}
        </nav>

        <!-- Bloglar — JS pagination + filter -->
        <section class="blog-grid-container">
            <div class="blog-grid" id="posts-grid">
{cards_html}
            </div>
            <div class="empty-state" id="empty-state" hidden>Bu kategoride yazı bulunamadı.</div>
        </section>

        <!-- Pagination -->
        <nav class="pagination-controls" id="pagination" aria-label="Sayfa gezinme">
            <button class="page-btn" id="prev-btn" type="button" aria-label="Önceki sayfa">←</button>
            <span class="page-info" id="page-info">Sayfa 1 / {total_pages}</span>
            <button class="page-btn" id="next-btn" type="button" aria-label="Sonraki sayfa">→</button>
        </nav>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2026 Yakınımdaki Deprem. Tüm hakları saklıdır.</p>
        </div>
    </footer>

    <script src="js/header.min.js?v=202605051900" defer></script>
    <script src="js/city-keywords.js?v=202604202200" defer></script>
    <script src="js/city-search.js?v=202604202200" defer></script>

    <script>
    (function () {{
        const PAGE_SIZE = {PAGE_SIZE};
        const grid = document.getElementById('posts-grid');
        const empty = document.getElementById('empty-state');
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        const pageInfo = document.getElementById('page-info');
        const catBtns = document.querySelectorAll('.cat-btn');
        const allCards = Array.from(grid.querySelectorAll('.blog-card'));

        let currentCat = 'all';
        let currentPage = 1;

        function getFilteredCards() {{
            return currentCat === 'all'
                ? allCards
                : allCards.filter(c => c.dataset.cat === currentCat);
        }}

        function render() {{
            const filtered = getFilteredCards();
            const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
            if (currentPage > totalPages) currentPage = totalPages;

            const start = (currentPage - 1) * PAGE_SIZE;
            const end = start + PAGE_SIZE;
            const visibleSet = new Set(filtered.slice(start, end));

            allCards.forEach(c => {{
                if (visibleSet.has(c)) c.classList.remove('is-hidden');
                else c.classList.add('is-hidden');
            }});

            empty.hidden = filtered.length > 0;
            pageInfo.textContent = `Sayfa ${{currentPage}} / ${{totalPages}}`;
            prevBtn.disabled = currentPage === 1;
            nextBtn.disabled = currentPage === totalPages;

            // Update URL hash for shareability
            const params = new URLSearchParams();
            if (currentCat !== 'all') params.set('cat', currentCat);
            if (currentPage > 1) params.set('page', String(currentPage));
            const url = new URL(window.location);
            url.search = params.toString();
            window.history.replaceState(null, '', url);
        }}

        catBtns.forEach(btn => {{
            btn.addEventListener('click', () => {{
                catBtns.forEach(b => b.classList.remove('is-active'));
                btn.classList.add('is-active');
                currentCat = btn.dataset.cat;
                currentPage = 1;
                render();
                grid.scrollIntoView({{behavior: 'smooth', block: 'start'}});
            }});
        }});

        prevBtn.addEventListener('click', () => {{
            if (currentPage > 1) {{
                currentPage--;
                render();
                grid.scrollIntoView({{behavior: 'smooth', block: 'start'}});
            }}
        }});

        nextBtn.addEventListener('click', () => {{
            const filtered = getFilteredCards();
            const totalPages = Math.ceil(filtered.length / PAGE_SIZE);
            if (currentPage < totalPages) {{
                currentPage++;
                render();
                grid.scrollIntoView({{behavior: 'smooth', block: 'start'}});
            }}
        }});

        // Initial state from URL
        const urlParams = new URLSearchParams(window.location.search);
        const urlCat = urlParams.get('cat');
        const urlPage = parseInt(urlParams.get('page'), 10);
        if (urlCat) {{
            const matchBtn = document.querySelector(`.cat-btn[data-cat="${{urlCat}}"]`);
            if (matchBtn) {{
                catBtns.forEach(b => b.classList.remove('is-active'));
                matchBtn.classList.add('is-active');
                currentCat = urlCat;
            }}
        }}
        if (urlPage && urlPage > 0) currentPage = urlPage;

        render();
    }})();
    </script>
</body>
</html>
"""

new_html = head_section + "\n" + body
(PUBLIC / "blog.html").write_text(new_html, encoding="utf-8")
print(f"Wrote new blog.html with {len(posts)} posts, {total_pages} pages.")
