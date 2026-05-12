#!/usr/bin/env python3
"""
Mevcut blog.html'den blog kartlarını parse edip blog_index.json'a yazar.
Yeni 10 bloğu da kategorisiyle ekler.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_HTML = ROOT / "public" / "blog.html"
OUT = ROOT / "scripts" / "blog_index.json"

html = BLOG_HTML.read_text(encoding="utf-8")

# Parse: <section class="blog-section" data-cat="X"> ... blog-card pattern
sections = re.split(r'<section class="blog-section"', html)[1:]

posts = []
for sec in sections:
    cat_m = re.search(r'data-cat="([^"]+)"', sec)
    if not cat_m:
        continue
    cat = cat_m.group(1)

    # All blog-card anchors in this section
    cards = re.findall(
        r'<a class="blog-card[^"]*" href="([^"]+)"[^>]*>'
        r'(?:[^<]|<(?!h3))*?<div class="blog-image">'
        r'(?:[^<]|<(?!img))*?<img[^>]+src="([^"]+)"[^>]+alt="([^"]+)"[^>]*>'
        r'(?:[^<]|<(?!h3))*?<h3>([^<]+)</h3>'
        r'(?:[^<]|<(?!p))*?<p>([^<]+)</p>',
        sec, re.DOTALL,
    )
    for href, img, alt, title, desc in cards:
        # Stop at next section
        if '<section' in sec[:sec.index(href)]:
            continue
        posts.append({
            "href": href.strip(),
            "img": img.strip(),
            "alt": alt.strip(),
            "title": title.strip(),
            "desc": desc.strip(),
            "cat": cat,
        })

# Dedup by href (keep first)
seen = set()
unique = []
for p in posts:
    if p["href"] not in seen:
        seen.add(p["href"])
        unique.append(p)

# Add 10 new blogs
new_blogs = [
    ("/blog-e-devlet-deprem-riski-sorgulama.html", "blog-e-devlet-deprem-riski-sorgulama.webp",
     "E-Devlet ile Deprem Riski Sorgulama", "E-Devlet ile Deprem Riski Sorgulama 2026",
     "AFAD verisini, kentsel dönüşüm tespitini ve DASK'ı tek noktadan e-devletten sorgulama rehberi.", "sigorta"),
    ("/blog-kentsel-donusum-vergisi-muafiyeti.html", "blog-kentsel-donusum-vergisi-muafiyeti.webp",
     "Kentsel Dönüşümde Vergi Muafiyeti", "Kentsel Dönüşümde Vergi Muafiyeti 2026",
     "6306 sayılı yasa kapsamında KDV, tapu harcı, gelir vergisi muafiyetleri 2026 güncel listesi.", "sigorta"),
    ("/blog-bina-deprem-performans-raporu-nedir.html", "blog-bina-deprem-performans-raporu-nedir.webp",
     "Bina deprem performans raporu", "Bina Deprem Performans Raporu 2026",
     "Binanızın performansını ölçen rapor: TBDY 2019, fiyat, mühendis seçimi, sonuç yorumlama.", "bilim"),
    ("/blog-kolon-kesme-cezasi-ve-hukuki-sorumluluk.html", "blog-kolon-kesme-cezasi-ve-hukuki-sorumluluk.webp",
     "Apartmanda kesilmiş taşıyıcı kolon", "Kolon Kesmenin Cezası 2026",
     "TCK ve İmar Kanunu açısından cezai yaptırım, ihbar süreci, deprem sonrası tazminat.", "sigorta"),
    ("/blog-deprem-sigortasi-prim-hesaplama.html", "blog-deprem-sigortasi-prim-hesaplama.webp",
     "DASK prim hesaplama hesap makinesi", "Deprem Sigortası Prim Hesaplama 2026",
     "DASK ve ek deprem sigortası primi: yapı türü, alan, deprem bölgesi etkisi. 2026 tarifeleri.", "sigorta"),
    ("/blog-deprem-aninda-balkon-guvenli-mi.html", "blog-deprem-aninda-balkon-guvenli-mi.webp",
     "Apartman balkonu güvenliği", "Deprem Anında Balkon Güvenli Mi?",
     "Konsol balkonların yapısal davranışı, riskler ve doğru tahliye stratejisi.", "sirasinda"),
    ("/blog-deprem-sonrasi-gida-saklama-ve-su-temini.html", "blog-deprem-sonrasi-gida-saklama-ve-su-temini.webp",
     "Afet için gıda ve su stoğu", "Deprem Sonrası Gıda ve Su Rehberi",
     "7 günlük gıda stoğu, su sterilizasyonu, raf ömrü, özel diyetler — afet beslenme planı.", "sonrasi"),
    ("/blog-eski-bina-deprem-yonetmeligi-uyum.html", "blog-eski-bina-deprem-yonetmeligi-uyum.webp",
     "Eski apartman ve yeni yapı karşılaştırması", "Eski Binalar Deprem Yönetmeliğine Uyum 2026",
     "1975-2019 arası deprem yönetmeliklerinin tarihi, eski binalarla TBDY 2019 karşılaştırması.", "bilim"),
    ("/blog-deprem-sonrasi-psikolojik-ilk-yardim.html", "blog-deprem-sonrasi-psikolojik-ilk-yardim.webp",
     "Deprem sonrası psikolojik destek", "Deprem Sonrası Psikolojik İlk Yardım",
     "DSÖ Psikolojik İlk Yardım modeli, çocuklarda ve yetişkinlerde uygulanması, uzman desteği.", "sonrasi"),
    ("/blog-komsu-binasi-deprem-riski-sikayet.html", "blog-komsu-binasi-deprem-riski-sikayet.webp",
     "Tehlikeli bina ihbar süreci", "Komşu Binası Deprem Riski Şikayet",
     "Riskli yapı ihbarı: belediye, AFAD, hukuki süreç. Komşu binası tehlikeli mi?", "sigorta"),
    # 2026-05 v2 - 10 stratejik blog (GSC content gap analizinden)
    ("/blog-canli-sismik-harita-turkiye.html", "blog-canli-sismik-harita-turkiye.webp",
     "Türkiye canlı sismik harita", "Canlı Sismik Harita Türkiye 2026",
     "Türkiye'nin anlık sismik aktivitesi: AFAD + Kandilli verisiyle 20 saniyede güncellenen canlı harita.", "bilim"),
    ("/blog-yakinimda-deprem-konum-sorgulama.html", "blog-yakinimda-deprem-konum-sorgulama.webp",
     "Yakınımda deprem sorgulama", "Yakınımda Deprem Oldu Mu? Konum Sorgulama",
     "Konum bilginizle anlık deprem sorgulama, yakın depremler ve bildirim ayarları rehberi.", "bilim"),
    ("/blog-deprem-haritasi-nasil-okunur.html", "blog-deprem-haritasi-nasil-okunur.webp",
     "Deprem haritası okuma", "Deprem Haritası Nasıl Okunur?",
     "Deprem haritalarındaki renk kodları, derinlik, magnitüd skalası ve coğrafi koordinatlar — adım adım okuma rehberi.", "bilim"),
    ("/blog-canli-fay-hatti-haritasi.html", "blog-canli-fay-hatti-haritasi.webp",
     "Türkiye fay hatları KAF DAF BAF", "Canlı Fay Hattı Haritası Türkiye",
     "Türkiye'nin 3 büyük fayı (KAF, DAF, BAF) ve son hareketleri. AFAD verisiyle aktif fay aktivitesi.", "bilim"),
    ("/blog-afad-kandilli-deprem-karsilastirma.html", "blog-afad-kandilli-deprem-karsilastirma.webp",
     "AFAD Kandilli karşılaştırma", "AFAD ve Kandilli Karşılaştırması",
     "AFAD vs Kandilli deprem verisi karşılaştırması: hız, doğruluk, magnitüd farkları ve hangisini kullanmalı.", "bilim"),
    ("/blog-az-once-deprem-mi-oldu.html", "blog-az-once-deprem-mi-oldu.webp",
     "Az önce deprem oldu mu sorgulama", "Az Önce Deprem Mi Oldu?",
     "Sarsıntı hissettiniz mi? 30 saniyede yanıt almanın 5 yolu, doğrulama yöntemleri ve panik halinde yapılacaklar.", "sirasinda"),
    ("/blog-aktif-deprem-haritasi-son-24-saat.html", "blog-aktif-deprem-haritasi-son-24-saat.webp",
     "Aktif deprem haritası son 24 saat", "Aktif Deprem Haritası — Son 24 Saat",
     "Türkiye'nin son 24 saatte gerçekleşen tüm depremleri: bölgesel dağılım, magnitüd analizi, günlük özet.", "bilim"),
    ("/blog-haritali-son-depremler.html", "blog-haritali-son-depremler.webp",
     "Haritalı son depremler liste", "Haritalı Son Depremler Türkiye",
     "AFAD + Kandilli verisiyle son depremleri hem listede hem haritada görüntüleyen kapsamlı canlı takip.", "bilim"),
    ("/blog-dunya-deprem-haritasi-canli.html", "blog-dunya-deprem-haritasi-canli.webp",
     "Dünya canlı deprem haritası", "Dünya Deprem Haritası Canlı",
     "Dünya deprem haritası canlı: küresel sismik aktivite, USGS verisi, Türkiye'nin küresel sıralamadaki yeri.", "bilim"),
    ("/blog-bugun-deprem-oldu-mu-turkiye.html", "blog-bugun-deprem-oldu-mu-turkiye.webp",
     "Türkiye bugün deprem oldu mu", "Bugün Deprem Oldu Mu Türkiye?",
     "AFAD + Kandilli verisiyle günlük tüm depremler, hissedilen olaylar, bölge özetleri ve haftalık karşılaştırma.", "bilim"),
]

new_hrefs = set()
for href, img, alt, title, desc, cat in new_blogs:
    new_hrefs.add(href)
    if href in seen:
        continue
    unique.append({
        "href": href,
        "img": f"images/{img}",
        "alt": alt,
        "title": title,
        "desc": desc,
        "cat": cat,
    })

# Sort: yeni 10 üstte, sonra eski sırasıyla
def sort_key(p):
    return (0 if p["href"] in new_hrefs else 1, p["title"])

unique.sort(key=sort_key)

OUT.write_text(json.dumps(unique, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Total: {len(unique)} blog posts. New: {len(new_hrefs)}")

# Print category counts
from collections import Counter
cat_counts = Counter(p["cat"] for p in unique)
print("Category counts:")
for cat, n in cat_counts.most_common():
    print(f"  {cat:12s} {n}")
