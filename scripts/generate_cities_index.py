#!/usr/bin/env python3
"""
/deprem-sehirleri.html - 81 ilin bolge bazinda gruplanmis index sayfasi.
generate_city_pages.py'daki PROVINCES listesini kullanir.
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from generate_city_pages import PROVINCES, REGIONS

PUBLIC_DIR = SCRIPT_DIR.parent / "public"
OUT_FILE = PUBLIC_DIR / "deprem-sehirleri.html"

REGION_ORDER = ["marmara", "ege", "akdeniz", "icanadolu", "karadeniz", "doguanadolu", "guneydoguanadolu"]
REGION_DESC = {
    "marmara": "Kuzey Anadolu Fay Hatti (KAF) etkisindeki en yuksek riskli bolge. 1999 Kocaeli ve Duzce depremlerinin merkezi.",
    "ege": "Normal fay sistemleri ve Ege Denizi genislemesinin etkisinde. 2020 Samos-Izmir depremi hatirlatici.",
    "akdeniz": "Kibris Yayi, DAF guney kolu ve Fethiye-Burdur Fay Zonu'nun etkisi altinda.",
    "icanadolu": "Tuz Golu Fay Zonu ve tali fay sistemleri; gorece sakin fakat orta siddetli depremlere acik.",
    "karadeniz": "Kuzey Anadolu Fay Hatti'nin kuzey kollari ve kiyi heyelanlarinin etkisi.",
    "doguanadolu": "Dogu Anadolu Fay Hatti (DAF) ve Kuzey Anadolu Fay Hatti'nin birlesim bolgesi; yuksek risk.",
    "guneydoguanadolu": "DAF'in guney kollari; 2023 Kahramanmaras depremlerinin etkiledigi kritik bolge.",
}

# Provinces'i bolgeye grupla
by_region = {r: [] for r in REGION_ORDER}
for p in PROVINCES:
    by_region[p["region"]].append(p)
for r in by_region:
    by_region[r].sort(key=lambda x: x["name"])

# Region cards HTML
region_sections = []
for rkey in REGION_ORDER:
    rtitle = REGIONS[rkey]["title"]
    rrisk = REGIONS[rkey]["risk_level"]
    rdesc = REGION_DESC[rkey]
    cities_html = []
    for p in by_region[rkey]:
        cities_html.append(
            f'                <li><a href="/deprem-{p["slug"]}.html">'
            f'<span class="city-dot" aria-hidden="true"></span>{p["name"]}</a></li>'
        )
    region_sections.append(f"""
    <section class="region-card">
        <header class="region-card__header">
            <h2>{rtitle}</h2>
            <span class="region-risk region-risk--{rkey}">Risk: {rrisk}</span>
        </header>
        <p class="region-card__desc">{rdesc}</p>
        <ul class="region-cities">
{chr(10).join(cities_html)}
        </ul>
    </section>""")

region_html = "\n".join(region_sections)

# FAQ Schema for cities index
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#ffffff">
    <!-- Google Tag Manager -->
    <script>(function (w, d, s, l, i) {{
            w[l] = w[l] || []; w[l].push({{
                'gtm.start':
                    new Date().getTime(), event: 'gtm.js'
            }}); var f = d.getElementsByTagName(s)[0],
                j = d.createElement(s), dl = l != 'dataLayer' ? '&l=' + l : ''; j.async = true; j.src =
                    'https://www.googletagmanager.com/gtm.js?id=' + i + dl; f.parentNode.insertBefore(j, f);
        }})(window, document, 'script', 'dataLayer', 'GTM-WQZS53QX');</script>
    <!-- End Google Tag Manager -->
    <title>81 İl Deprem Sayfaları | Türkiye Şehir Bazında Anlık Depremler</title>
    <meta name="description"
        content="81 ilin deprem sayfaları tek yerde. Şehrinizin son deprem verilerini, fay hattı bilgisini ve risk profilini bölge bazında kolayca bulun.">
    <meta name="keywords"
        content="şehir deprem sayfaları, 81 il deprem, türkiye şehir deprem, il bazında deprem, bölge deprem haritası">
    <link rel="canonical" href="https://yakinimdakideprem.com/deprem-sehirleri.html" />
    <meta property="og:type" content="website">
    <meta property="og:title" content="81 İl Deprem Sayfaları | Türkiye Şehir Bazında Anlık Depremler">
    <meta property="og:description"
        content="Türkiye'nin 81 ili için ayrı ayrı hazırlanmış deprem sayfaları. Bölge bazında risk profili, fay hattı bilgisi ve anlık veri.">
    <meta property="og:url" content="https://yakinimdakideprem.com/deprem-sehirleri.html">
    <meta property="og:site_name" content="Yakınımdaki Deprem">
    <meta property="og:image" content="https://yakinimdakideprem.com/images/og-yakinimdakideprem.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="81 İl Deprem Sayfaları | Türkiye Anlık Deprem">
    <meta name="twitter:description" content="81 ilin deprem sayfaları tek sayfada. Bölge bazında.">
    <meta name="twitter:image" content="https://yakinimdakideprem.com/images/og-yakinimdakideprem.png">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="css/blog.css?v=202601132130">
    <link rel="stylesheet" href="css/components.min.css?v=202601131900">
    <link rel="stylesheet" href="css/header.min.css?v=202601132330">
    <link rel="stylesheet" href="css/footer.css?v=202512182020">
    <link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32x32.png">
    <link rel="manifest" href="site.webmanifest">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "81 İl Deprem Sayfaları",
      "description": "Türkiye'nin 81 ili için ayrı ayrı hazırlanmış deprem sayfaları. Bölge bazında risk profili.",
      "url": "https://yakinimdakideprem.com/deprem-sehirleri.html",
      "inLanguage": "tr-TR"
    }}
    </script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type":"ListItem","position":1,"name":"Ana Sayfa","item":"https://yakinimdakideprem.com/"}},
        {{"@type":"ListItem","position":2,"name":"Tüm İller"}}
      ]
    }}
    </script>
    <style>
        nav a.nav-highlight {{ color: #d32f2f; font-weight: 700; }}
        nav a.nav-highlight:hover {{ color: #b71c1c; text-decoration: underline; }}

        .cities-hero {{
            background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%);
            color: #fff;
            padding: 48px 0 40px;
            text-align: center;
        }}
        .cities-hero h1 {{
            font-size: 2.2rem;
            margin: 0 0 12px;
            color: #fff;
        }}
        .cities-hero p {{
            max-width: 680px;
            margin: 0 auto;
            opacity: 0.95;
            font-size: 1.05rem;
            line-height: 1.5;
        }}
        .cities-main {{
            padding: 40px 0 60px;
            background: #f9fafb;
            min-height: 60vh;
        }}
        .region-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
        }}
        .region-card {{
            background: #fff;
            border-radius: 14px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
            padding: 22px 22px 18px;
        }}
        .region-card__header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
            flex-wrap: wrap;
        }}
        .region-card h2 {{
            font-size: 1.3rem;
            color: #111827;
            margin: 0;
        }}
        .region-risk {{
            font-size: 0.75rem;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 999px;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            white-space: nowrap;
        }}
        .region-risk--marmara, .region-risk--doguanadolu, .region-risk--guneydoguanadolu {{
            background: #fee2e2; color: #b91c1c;
        }}
        .region-risk--ege, .region-risk--akdeniz {{
            background: #fef3c7; color: #b45309;
        }}
        .region-risk--karadeniz {{
            background: #fef3c7; color: #92400e;
        }}
        .region-risk--icanadolu {{
            background: #dcfce7; color: #166534;
        }}
        .region-card__desc {{
            color: #4b5563;
            font-size: 0.9rem;
            line-height: 1.55;
            margin: 0 0 14px;
        }}
        .region-cities {{
            list-style: none;
            padding: 0;
            margin: 0;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
            gap: 4px 10px;
        }}
        .region-cities a {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 8px;
            color: #1f2937;
            text-decoration: none;
            border-radius: 6px;
            font-size: 0.92rem;
            transition: background .14s ease, color .14s ease;
        }}
        .region-cities a:hover {{
            background: #fef2f2;
            color: #b91c1c;
        }}
        .city-dot {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #d32f2f;
            flex-shrink: 0;
            opacity: 0.65;
        }}
        .cities-cta {{
            background: #fff;
            border-top: 1px solid #e5e7eb;
            padding: 32px 0;
            text-align: center;
        }}
        .cities-cta p {{
            color: #4b5563;
            font-size: 1rem;
        }}
        .cities-cta .highlight-link {{
            color: #d32f2f;
            font-weight: 700;
            text-decoration: none;
        }}
        .cities-cta .highlight-link:hover {{ text-decoration: underline; }}

        @media (max-width: 640px) {{
            .cities-hero h1 {{ font-size: 1.6rem; }}
            .region-cities {{ grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); }}
        }}
    </style>
</head>

<body>
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-WQZS53QX" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <header id="hidden-header">
        <div class="container">
            <a href="/" class="logo" rel="noopener noreferrer">
                <img loading="lazy" src="icons/logo.png" alt="Yakınımdaki Deprem logosu" width="60" height="60">
                <span data-text="Yakınımdaki Deprem">Yakınımdaki Deprem</span>
            </a>
            <nav>
                <a href="/" rel="noopener noreferrer">Ana Sayfa</a>
                <a href="/son-dakika-deprem.html" rel="noopener noreferrer" class="nav-highlight nav-alert">Son Dakika
                    <span class="alarm-dot" aria-hidden="true"></span></a>
                <div class="nav-dropdown nav-dropdown-guides">
                    <button class="dropdown-toggle" type="button" aria-haspopup="true" aria-expanded="false">
                        Rehberler <i class="fas fa-chevron-down"></i>
                    </button>
                    <div class="dropdown-menu">
                        <a href="/deprem-aninda.html" rel="noopener noreferrer">Deprem Anında</a>
                        <a href="/ilk-yardim-cantasi.html" rel="noopener noreferrer">İlk Yardım Çantası</a>
                        <a href="/ben-kimim.html" rel="noopener noreferrer">Ben Kimim</a>
                        <a href="/blog.html" rel="noopener noreferrer">Blog</a>
                    </div>
                </div>
                <div class="nav-dropdown">
                    <button class="dropdown-toggle" type="button" aria-haspopup="true" aria-expanded="false">
                        Şehir Depremleri <i class="fas fa-chevron-down"></i>
                    </button>
                    <div class="dropdown-menu">
                        <a href="/deprem-sehirleri.html" rel="noopener noreferrer"><strong>📍 Tüm 81 İl</strong></a>
                        <a href="/deprem-istanbul.html" rel="noopener noreferrer">İstanbul Depremi</a>
                        <a href="/deprem-izmir.html" rel="noopener noreferrer">İzmir Depremi</a>
                        <a href="/deprem-ankara.html" rel="noopener noreferrer">Ankara Depremi</a>
                        <a href="/deprem-elazig.html" rel="noopener noreferrer">Elazığ Depremi</a>
                        <a href="/deprem-bursa.html" rel="noopener noreferrer">Bursa Depremi</a>
                        <a href="/deprem-adana.html" rel="noopener noreferrer">Adana Depremi</a>
                        <a href="/deprem-kahramanmaras.html" rel="noopener noreferrer">Kahramanmaraş Depremi</a>
                    </div>
                </div>
            </nav>
        </div>
    </header>

    <section class="cities-hero">
        <div class="container">
            <h1>Türkiye'nin 81 İli İçin Deprem Sayfaları</h1>
            <p>Her il için özel hazırlanmış deprem sayfasında son depremler, fay hattı bilgisi, risk profili, toplanma alanları ve hazırlık rehberleri yer alır. Bölge bazında keşfedin.</p>
        </div>
    </section>

    <main class="cities-main">
        <div class="container">
            <div class="region-grid">
{region_html}
            </div>
        </div>
    </main>

    <section class="cities-cta">
        <div class="container">
            <p>Tüm depremleri anlık takip etmek için <a class="highlight-link" href="/">ana sayfadaki canlı haritayı</a> kullanın veya <a class="highlight-link" href="/son-dakika-deprem.html">son dakika</a> sayfasından büyük depremleri izleyin.</p>
        </div>
    </section>

    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-logo">
                    <img loading="lazy" src="icons/logo.png" alt="Yakınımdaki Deprem logosu" width="60" height="60">
                    <h3>Yakınımdaki Deprem</h3>
                    <p>Yakınımdakideprem.com bağımsız, ücretsiz ve tek kişi tarafından geliştirilen bir projedir. Resmi kurumlarla bağlantılı değildir.</p>
                </div>
                <div class="footer-links">
                    <div class="footer-column">
                        <h4>Hızlı Linkler</h4>
                        <ul>
                            <li><a href="/" rel="noopener noreferrer">Ana Sayfa</a></li>
                            <li><a href="/deprem-aninda.html" rel="noopener noreferrer">Deprem Anında</a></li>
                            <li><a href="/ilk-yardim-cantasi.html" rel="noopener noreferrer">İlk Yardım Çantası</a></li>
                            <li><a href="/ben-kimim.html" rel="noopener noreferrer">Ben Kimim</a></li>
                            <li><a href="/blog.html" rel="noopener noreferrer">Blog</a></li>
                        </ul>
                    </div>
                    <div class="footer-column">
                        <h4>Kaynaklar</h4>
                        <ul>
                            <li><a href="https://deprem.afad.gov.tr" target="_blank" rel="noopener noreferrer">AFAD</a></li>
                            <li><a href="https://koeri.boun.edu.tr" target="_blank" rel="noopener noreferrer">Kandilli Rasathanesi</a></li>
                        </ul>
                    </div>
                    <div class="footer-column">
                        <h4>İletişim</h4>
                        <ul>
                            <li><a href="https://www.linkedin.com/in/emin-k%C4%B1l%C4%B1%C3%A7-250b14210/" target="_blank" rel="noopener noreferrer">LinkedIn Profilim</a></li>
                        </ul>
                    </div>
                    <div class="footer-column">
                        <h4>Yasal</h4>
                        <ul>
                            <li><a href="/kullanim-sartlari.html" rel="noopener noreferrer">Kullanım Şartları</a></li>
                            <li><a href="/gizlilik-politikasi.html" rel="noopener noreferrer">Gizlilik Politikası</a></li>
                            <li><a href="/cerez-politikasi.html" rel="noopener noreferrer">Çerez Politikası</a></li>
                            <li><a href="/sorumluluk-reddi.html" rel="noopener noreferrer">Sorumluluk Reddi</a></li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 Yakınımdaki Deprem | Toplumu Geliştirmek İçin Çabalayan Bir Girişim</p>
            </div>
        </div>
    </footer>

    <script src="js/header.min.js?v=202602011300"></script>
</body>
</html>
"""

OUT_FILE.write_text(HTML_TEMPLATE.format(region_html=region_html), encoding="utf-8")
print(f"✓ {OUT_FILE}  ({OUT_FILE.stat().st_size} byte, {sum(len(by_region[r]) for r in REGION_ORDER)} il)")
