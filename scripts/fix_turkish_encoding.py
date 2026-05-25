#!/usr/bin/env python3
"""
Generator cikisinda ve statik sayfalardaki ASCII Turkce kelimeleri UTF-8'e ceviren
post-processor. Idempotent: tekrar calistirmak guvenli.

Kullanim:
    python3 scripts/fix_turkish_encoding.py             # tum deprem-*.html + deprem-sehirleri
    python3 scripts/fix_turkish_encoding.py --dry-run   # degisiklikleri listele, yazma
"""
from __future__ import annotations
import argparse
import re
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "public"

# ASCII Turkce -> UTF-8 Turkce kelime donusumleri.
# ONEMLI: Bu liste KELIME bazli replace icin - word-boundary ile uygulanir.
# Case-sensitive; farkli yazim bicimleri icin ayri girdiler var.
# Self-mapping (key == value) girdileri yoktur; her giris bir donusum yapar.
WORD_MAP = {
    # Marka / site
    "Yakinimdaki": "Yakınımdaki",
    "yakinimdaki": "yakınımdaki",

    # Bolge / genel
    "Sehir": "Şehir",
    "sehir": "şehir",
    "Sehri": "Şehri",
    "sehri": "şehri",
    "Sehirleri": "Şehirleri",
    "sehirleri": "şehirleri",
    "Sehirlerin": "Şehirlerin",
    "sehirlerin": "şehirlerin",

    # Bolge (bölge) - yeni eklenenler
    "bolge": "bölge",
    "Bolge": "Bölge",
    "bolgedir": "bölgedir",
    "Bolgedir": "Bölgedir",
    "bolgede": "bölgede",
    "Bolgede": "Bölgede",
    "bolgedeki": "bölgedeki",
    "Bolgedeki": "Bölgedeki",
    "bolgenin": "bölgenin",
    "Bolgenin": "Bölgenin",
    "bolgeyi": "bölgeyi",
    "Bolgeyi": "Bölgeyi",
    "bolgesi": "bölgesi",
    "Bolgesi": "Bölgesi",
    "bolgesinde": "bölgesinde",
    "Bolgesinde": "Bölgesinde",
    "bolgesindeki": "bölgesindeki",
    "Bolgesindeki": "Bölgesindeki",
    "bolgeler": "bölgeler",
    "Bolgeler": "Bölgeler",
    "bolgelerde": "bölgelerde",
    "bolgelerdeki": "bölgelerdeki",

    # Fay hattı
    "Hatti": "Hattı",
    "hatti": "hattı",
    "Hattin": "Hattın",
    "hattin": "hattın",
    "Hattinda": "Hattında",
    "hattinda": "hattında",
    "Hattindaki": "Hattındaki",
    "hattindaki": "hattındaki",
    "Hatlari": "Hatları",
    "hatlari": "hatları",
    "Hattinin": "Hattının",
    "hattinin": "hattının",

    # Gorece
    "gorece": "görece",
    "Gorece": "Görece",

    # Sarsinti
    "sarsinti": "sarsıntı",
    "Sarsinti": "Sarsıntı",
    "sarsintilar": "sarsıntılar",
    "Sarsintilar": "Sarsıntılar",
    "sarsintisi": "sarsıntısı",
    "Sarsintisi": "Sarsıntısı",
    "sarsintilari": "sarsıntıları",
    "Sarsintilari": "Sarsıntıları",

    # Buyukluk
    "buyukluk": "büyüklük",
    "Buyukluk": "Büyüklük",
    "buyuklukte": "büyüklükte",
    "Buyuklukte": "Büyüklükte",
    "buyuklugu": "büyüklüğü",
    "Buyuklugu": "Büyüklüğü",
    "buyuklugundeki": "büyüklüğündeki",
    "buyugu": "büyüğü",

    # Buyuk / kucuk harf duyarli bolge adlari
    "Dogu": "Doğu",
    "dogu": "doğu",
    "Bati": "Batı",
    "bati": "batı",

    # Risk / hazirlik
    "yukleniyor": "yükleniyor",
    "olusturulan": "oluşturulan",
    "olusur": "oluşur",
    "olustu": "oluştu",
    "oldugu": "olduğu",
    "olasi": "olası",
    "kucuk": "küçük",
    "kucuklugunde": "küçüklüğünde",
    "yakin": "yakın",
    "Yakin": "Yakın",
    "yakininda": "yakınında",
    "Yakininda": "Yakınında",

    # Fiil / tak
    "gecmisi": "geçmişi",
    "gecen": "geçen",
    "gecmek": "geçmek",
    "gectigi": "geçtiği",
    "gecti": "geçti",
    "gorunen": "görünen",
    "gorur": "görür",
    "gorurum": "görürüm",
    "gorundugu": "göründüğü",
    "gosterir": "gösterir",
    "gosteren": "gösteren",
    "gostergeler": "göstergeler",
    "gore": "göre",
    "Gore": "Göre",
    "uzerine": "üzerine",
    "uzerinde": "üzerinde",
    "Uzerinde": "Üzerinde",
    "uzerindeki": "üzerindeki",
    "uzerinden": "üzerinden",
    "uzantisi": "uzantısı",
    "uzantilari": "uzantıları",

    # Hazirlik / icerik
    "hazirlik": "hazırlık",
    "Hazirlik": "Hazırlık",
    "hazirlayin": "hazırlayın",
    "hazirlanan": "hazırlanan",
    "ipuclari": "ipuçları",
    "Ipuclari": "İpuçları",
    "aciklama": "açıklama",
    "aciklamalar": "açıklamalar",

    # cevre / icin
    "cevresinde": "çevresinde",
    "cevresindeki": "çevresindeki",
    "cevresi": "çevresi",
    "icin": "için",
    "Icin": "İçin",
    "icinde": "içinde",
    "Icinde": "İçinde",
    "iceren": "içeren",
    "ice": "içe",

    # Kisaltmalar / anlik
    "anlik": "anlık",
    "Anlik": "Anlık",
    "anligin": "anlığın",

    # Diger yaygin
    "buyuk": "büyük",
    "Buyuk": "Büyük",
    "yogun": "yoğun",
    "Yogun": "Yoğun",
    "guclu": "güçlü",
    "Guclu": "Güçlü",
    "guvenlik": "güvenlik",
    "Guvenlik": "Güvenlik",
    "guvenli": "güvenli",
    "Guvenli": "Güvenli",
    "gunluk": "günlük",
    "gundelik": "gündelik",

    # Icindekiler / navigasyon
    "Icindekiler": "İçindekiler",
    "icindekiler": "içindekiler",

    # Cok-Kapan-Tutun
    "Cok": "Çök",
    "cok": "çök",  # tehlikeli - "cok" kelimesi "çok" mudur "çök" mu? Bagjlama bakar.
    "Cokapan": "Çökapan",
    "cokapan": "çökapan",

    # Diger
    "Turk": "Türk",
    "Turkiye": "Türkiye",
    "turkiye": "türkiye",
    "Turkiye'de": "Türkiye'de",
    "Turkiye'nin": "Türkiye'nin",
    "turkoglu": "türkoğlu",
    "Turkoglu": "Türkoğlu",
    "Nurdagi": "Nurdağı",
    "nurdagi": "nurdağı",
    "Afsin": "Afşin",
    "afsin": "afşin",
    "Goksun": "Göksun",
    "goksun": "göksun",

    # Il adlari (tekrar icin)
    "Kahramanmaras": "Kahramanmaraş",
    "kahramanmaras": "kahramanmaraş",
    "Istanbul": "İstanbul",
    "Izmir": "İzmir",
    "Agri": "Ağrı",
    "Cankiri": "Çankırı",
    "cankiri": "çankırı",
    "Canakkale": "Çanakkale",
    "canakkale": "çanakkale",
    "Corum": "Çorum",
    "Kutahya": "Kütahya",
    "kutahya": "kütahya",
    "Usak": "Uşak",
    "usak": "uşak",
    "Mugla": "Muğla",
    "mugla": "muğla",
    "Nigde": "Niğde",
    "Nevsehir": "Nevşehir",
    "Duzce": "Düzce",
    "duzce": "düzce",
    "Sanliurfa": "Şanlıurfa",
    "sanliurfa": "şanlıurfa",
    "Sirnak": "Şırnak",
    "sirnak": "şırnak",
    "Igdir": "Iğdır",
    "igdir": "ığdır",
    "Aydin": "Aydın",
    "aydin": "aydın",
    "Balikesir": "Balıkesir",
    "balikesir": "balıkesir",
    "Bartin": "Bartın",
    "bartin": "bartın",
    "Bingol": "Bingöl",
    "bingol": "bingöl",
    "Elazig": "Elazığ",
    "elazig": "elazığ",
    "Diyarbakir": "Diyarbakır",
    "diyarbakir": "diyarbakır",
    "Tekirdag": "Tekirdağ",
    "tekirdag": "tekirdağ",
    "Gumushane": "Gümüşhane",
    "gumushane": "gümüşhane",
    "Eskisehir": "Eskişehir",
    "eskisehir": "eskişehir",
    "Kirikkale": "Kırıkkale",
    "kirikkale": "kırıkkale",
    "Kirklareli": "Kırklareli",
    "kirklareli": "kırklareli",
    "Kirsehir": "Kırşehir",
    "kirsehir": "kırşehir",
    "Mus": "Muş",
    "Karabuk": "Karabük",
    "karabuk": "karabük",
    "Adiyaman": "Adıyaman",
    "adiyaman": "adıyaman",

    # Sec / bicim / ogren / vb
    "secerek": "seçerek",
    "sec": "seç",
    "Sec": "Seç",
    "surecte": "süreçte",
    "surece": "sürece",
    "sure": "süre",
    "Sure": "Süre",
    "surekli": "sürekli",

    # oneri
    "oneri": "öneri",
    "Oneri": "Öneri",
    "onerisi": "önerisi",
    "onerilen": "önerilen",
    "onerilir": "önerilir",

    # Yerellestirmeler
    "degerlendir": "değerlendir",
    "degisim": "değişim",
    "degisik": "değişik",
    "yerlesim": "yerleşim",
    "yerlesimleri": "yerleşimleri",
    "yerlesik": "yerleşik",
    "kayit": "kayıt",
    "Kayit": "Kayıt",
    "kayitlari": "kayıtları",
    "Kayitlari": "Kayıtları",

    # Ozet vb
    "ozet": "özet",
    "Ozet": "Özet",
    "ornegin": "örneğin",
    "Ornegin": "Örneğin",
    "ornek": "örnek",
    "Ornek": "Örnek",

    # Bolge-spesifik
    "Cukurova": "Çukurova",
    "cukurova": "çukurova",
    "Ozellikle": "Özellikle",
    "ozellikle": "özellikle",

    # Dogru / birlikte vb
    "dogru": "doğru",
    "Dogru": "Doğru",
    "asagidaki": "aşağıdaki",
    "Asagidaki": "Aşağıdaki",
}


# Pre-compiled regex (perf): tek bir alternation, en uzun key once.
# Word-boundary ile yan-kelime kirilmasi onlenir; ASCII Turkce karakter takip eden
# durumlarda da match etmez.
_SORTED_KEYS = sorted(WORD_MAP.keys(), key=len, reverse=True)
_PATTERN = re.compile(
    r'(?<![A-Za-zÇĞİÖŞÜçğıöşü0-9\-/])(' +
    '|'.join(re.escape(k) for k in _SORTED_KEYS) +
    r')(?![A-Za-zÇĞİÖŞÜçğıöşü0-9])'
)


def apply_replacements(content: str) -> tuple[str, int]:
    """Tek regex pass ile WORD_MAP'i uygular. Word-boundary sinirina dikkat eder."""
    changes = 0

    def repl(m: re.Match) -> str:
        nonlocal changes
        changes += 1
        return WORD_MAP[m.group(1)]

    new_content = _PATTERN.sub(repl, content)
    return new_content, changes


def process(path: Path, dry_run: bool = False) -> dict:
    orig = path.read_text(encoding="utf-8")
    # URL/attribute icindeki slug'lari korumak icin ask-protect:
    protected = []

    def mask(m):
        idx = len(protected)
        protected.append(m.group(0))
        return f"__PROTECTED_{idx}__"

    # 1. href/src URL leri koru
    masked = re.sub(r'(href|src|content|url)="[^"]*"', mask, orig)
    # 2. JSON-LD block'lari koru (tamamen)
    masked = re.sub(
        r'<script type="application/ld\+json">.*?</script>',
        mask,
        masked,
        flags=re.DOTALL,
    )

    # Replacement uygula
    updated, changes = apply_replacements(masked)

    # Maskelenen parcalar geri koy
    for i, segment in enumerate(protected):
        updated = updated.replace(f"__PROTECTED_{i}__", segment)

    # Meta description / title / keywords'lerdeki ASCII Turkceyi duzelt
    def fix_meta_content(match):
        attr = match.group(1)
        val = match.group(2)
        # URL ise dokunma
        if val.startswith("http") or val.startswith("/") or re.match(r"^[a-z0-9._\-]+$", val):
            return match.group(0)
        fixed, _ = apply_replacements(val)
        return f'{attr}="{fixed}"'

    updated = re.sub(
        r'(content|alt|title|placeholder|aria-label|data-text)="([^"]*)"',
        fix_meta_content,
        updated,
    )

    if updated != orig and not dry_run:
        path.write_text(updated, encoding="utf-8")

    return {
        "path": path,
        "changed": updated != orig,
        "bytes_before": len(orig),
        "bytes_after": len(updated),
        "replacements": changes,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("files", nargs="*", help="Belirli dosyalar (verilmezse tum deprem-*.html)")
    args = ap.parse_args()

    SPECIAL_SLUGS = {
        "istanbul", "izmir", "ankara", "bursa", "adana", "elazig", "kahramanmaras"
    }
    targets: list[Path] = []
    if args.files:
        targets = [Path(f) for f in args.files]
    else:
        for p in sorted(PUBLIC.glob("deprem-*.html")):
            if p.name == "deprem-aninda.html":
                continue
            slug = p.stem.replace("deprem-", "")
            if slug in SPECIAL_SLUGS:
                continue
            targets.append(p)
        targets.append(PUBLIC / "deprem-sehirleri.html")

    total = 0
    changed = 0
    for t in targets:
        r = process(t, dry_run=args.dry_run)
        tag = "[DRY]" if args.dry_run else ("[DUZELTILDI]" if r["changed"] else "[TEMIZ]")
        total += r["replacements"]
        if r["changed"]:
            changed += 1
            print(f"  {tag} {t.name}: {r['replacements']} degisiklik ({r['bytes_before']}->{r['bytes_after']} byte)")
    print(f"\nToplam: {len(targets)} dosya, {changed} degisti, {total} replacement")


if __name__ == "__main__":
    main()
