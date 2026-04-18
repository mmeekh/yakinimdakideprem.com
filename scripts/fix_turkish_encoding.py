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
WORD_MAP = {
    # Marka / site
    "Yakinimdaki": "Yakınımdaki",
    "yakinimdaki": "yakınımdaki",
    "YAKINIMDAKI": "YAKINIMDAKI",  # uppercase zaten gecerli

    # Bolge / genel
    "Sehir": "Şehir",
    "sehir": "şehir",
    "Sehri": "Şehri",
    "sehri": "şehri",
    "Sehirleri": "Şehirleri",
    "sehirleri": "şehirleri",
    "Sehirlerin": "Şehirlerin",
    "sehirlerin": "şehirlerin",

    # Fay hattı
    "Hatti": "Hattı",
    "hatti": "hattı",
    "Hatlari": "Hatları",
    "hatlari": "hatları",
    "Hattinin": "Hattının",
    "hattinin": "hattının",
    "Hattindaki": "Hattındaki",

    # Buyuk / kucuk harf duyarli bolge adlari
    "Dogu": "Doğu",
    "dogu": "doğu",
    "Bati": "Batı",
    "bati": "batı",
    "Anadolu'da": "Anadolu'da",
    "Anadolu'nun": "Anadolu'nun",
    "Anadolu'ya": "Anadolu'ya",

    # Risk / hazirlik
    "yukleniyor": "yükleniyor",
    "olusturulan": "oluşturulan",
    "olusur": "oluşur",
    "olustu": "oluştu",
    "oldugu": "olduğu",
    "olan": "olan",  # zaten dogru (no change, keep for idempotency check)
    "olasi": "olası",
    "buyukluk": "büyüklük",
    "Buyukluk": "Büyüklük",
    "buyuklugu": "büyüklüğü",
    "buyuklugundeki": "büyüklüğündeki",
    "buyugu": "büyüğü",
    "kucuk": "küçük",
    "kucuklugunde": "küçüklüğünde",
    "derinlik": "derinlik",  # zaten dogru
    "Derinlik": "Derinlik",  # zaten dogru
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
    "gorusm": "görüşm",  # "gorusme" stem
    "gorunen": "görünen",
    "gorur": "görür",
    "gorurum": "görürüm",
    "gorundugu": "göründüğü",
    "gosterir": "gösterir",
    "gosteren": "gösteren",
    "gostergeler": "göstergeler",
    "gosterir.": "gösterir.",
    "goster": "göster",  # stem
    "gore": "göre",
    "Gore": "Göre",
    "uzerine": "üzerine",
    "uzerinde": "üzerinde",
    "Uzerinde": "Üzerinde",
    "uzerindeki": "üzerindeki",
    "uzerinden": "üzerinden",
    "uzanan": "uzanan",  # zaten
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
    "acil": "acil",  # zaten
    "Acil": "Acil",

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
    "gun": "gün",
    "Gun": "Gün",  # baslangicta ama "Gun" tek basina nadirdir
    "gece": "gece",  # zaten
    "gundelik": "gündelik",
    "Sondakika": "Sondakika",  # zaten
    "son": "son",  # zaten

    # Icindekiler / navigasyon
    "Icindekiler": "İçindekiler",
    "icindekiler": "içindekiler",

    # Cok-Kapan-Tutun
    "Cok": "Çök",
    "cok": "çök",  # tehlikeli - "cok" kelimesi "çok" mudur "çök" mu? Bagjlama bakar.
    "Cokapan": "Çökapan",
    "cokapan": "çökapan",
    "Kapan": "Kapan",  # zaten
    "Tutun": "Tutun",  # zaten

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
    "goster": "göster",

    # Il adlari (tekrar icin)
    "Kahramanmaras": "Kahramanmaraş",
    "kahramanmaras": "kahramanmaraş",
    "Istanbul": "İstanbul",
    "istanbul": "istanbul",  # keep as-is in URLs; word boundary gerekli
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

    # Diger parcali kelimeler
    "Hafifletici": "Hafifletici",  # zaten
    "Koru": "Koru",  # zaten
    "koruyun": "koruyun",  # zaten
    "Koruyun": "Koruyun",

    # Sec / bicim / ogren / vb
    "secerek": "seçerek",
    "sec": "seç",
    "Sec": "Seç",
    "surecte": "süreçte",
    "surece": "sürece",
    "sure": "süre",
    "Sure": "Süre",
    "surekli": "sürekli",

    # "devrilm" vb icin
    "devrilme": "devrilme",  # zaten
    "oneri": "öneri",
    "Oneri": "Öneri",
    "onerisi": "önerisi",
    "onerilen": "önerilen",
    "onerilir": "önerilir",

    # Yerellestirmeler
    "degerlendir": "değerlendir",
    "degisim": "değişim",
    "degisik": "değişik",
    "detay": "detay",  # zaten
    "Detay": "Detay",
    "sergilemektedir": "sergilemektedir",
    "sendeleme": "sendeleme",
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
    "birlikte": "birlikte",  # zaten
    "asagidaki": "aşağıdaki",
    "Asagidaki": "Aşağıdaki",

    # Aktif vb
    "tektonik": "tektonik",  # zaten
    "Tektonik": "Tektonik",

    # Bilgi
    "bilgisi": "bilgisi",  # zaten
    "bilgi": "bilgi",  # zaten

    # Verim
    "resmi": "resmi",  # zaten
    "Resmi": "Resmi",

    # Afad / Kandilli zaten ascii ok
}


# Ozel regex yaklasim: "cok" -> "çok" yaklasimini bagjlama gore yap
# "cok" cogunlukla "çok" demek (adverb) - surekli kullanimi kontrol
# Fakat "Cok, Kapan, Tutun" -> "Çök, Kapan, Tutun"
# Bu yuzden word-based basit mapping iyi isler.


def apply_replacements(content: str) -> tuple[str, int]:
    """Metin icinde WORD_MAP'i uygular. Word-boundary sinirina dikkat eder."""
    changes = 0
    # En uzun keyleri once islemek icin sort (so that "Hattindaki" before "Hatti")
    keys = sorted(WORD_MAP.keys(), key=lambda k: -len(k))
    for key in keys:
        val = WORD_MAP[key]
        if key == val:
            continue
        # URL icinde (href="/deprem-izmir.html" gibi) DOKUNMAMAK icin
        # "izmir" ve "istanbul" gibi slug-gerekli kelimeleri ozel isleriz.
        # Genel durum: ASCII alfanumerik sonrasinda/oncesinde olmayan yerlerde degistir.
        # Yani (?<![A-Za-z0-9\-_/])KEY(?![A-Za-z0-9_])
        # Ama url icinde /deprem-izmir.html olursa "izmir" kismini yakalamak istemeyiz.
        # Cozum: URL pattern olanlari once maskele, sonra replace, sonra geri ac.

        # Ilk pass: URL'lerde kullanilan slug'lari koru
        # /deprem-XXX.html seklindeki pattern'in icini dokunmadan birak.
        # Genel regex ile yap:
        pattern = re.compile(rf"(?<![A-Za-zÇĞİÖŞÜçğıöşü0-9\-/]){re.escape(key)}(?![A-Za-zÇĞİÖŞÜçğıöşü0-9])")

        def replacer(m):
            nonlocal changes
            changes += 1
            return val

        content = pattern.sub(replacer, content)
    return content, changes


def process(path: Path, dry_run: bool = False) -> dict:
    orig = path.read_text(encoding="utf-8")
    # URL/attribute icindeki slug'lari korumak icin ask-protect:
    # data-text, alt, title, content (meta), > <text ... orderinge gore isleriz.
    # Basit yaklasim: URL (/deprem-xxx.html) ve canonical url'leri maskele
    protected = []

    def mask(m):
        idx = len(protected)
        protected.append(m.group(0))
        return f"__PROTECTED_{idx}__"

    # 1. href/src URL leri koru
    masked = re.sub(r'(href|src|content|url)="[^"]*"', mask, orig)
    # 2. JSON-LD block'lari koru (tamamen) - basit yaklasim: application/ld+json scriptlerini koru
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

    # JSON-LD ve meta icindeki text'leri DE bir sonraki passta duzelt
    # (sadece content="..." icindeki gercek cumleleri, URL'leri degil)
    # Meta description / title / keywords'lerdeki ASCII Turkceyi duzelt
    # Bu nispeten dar scope, dikkatli yapmak lazim.

    def fix_meta_content(match):
        attr = match.group(1)
        val = match.group(2)
        # URL ise dokunma
        if val.startswith("http") or val.startswith("/") or re.match(r"^[a-z0-9._\-]+$", val):
            return match.group(0)
        # Aksi halde uygula
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
    args = ap.parse_args()

    # Hedefler: generator ciktisi 74 sehir sayfasi (istanbul/izmir/ankara/bursa/adana/elazig/kahramanmaras hariç zaten Turkce)
    # + deprem-sehirleri.html
    SPECIAL_SLUGS = {
        "istanbul", "izmir", "ankara", "bursa", "adana", "elazig", "kahramanmaras"
    }
    targets = []
    for p in sorted(PUBLIC.glob("deprem-*.html")):
        # deprem-aninda.html statik rehber - Turkce zaten OK, atla
        if p.name == "deprem-aninda.html":
            continue
        slug = p.stem.replace("deprem-", "")
        if slug in SPECIAL_SLUGS:
            continue  # bunlar zaten Turkce, dokunma
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
