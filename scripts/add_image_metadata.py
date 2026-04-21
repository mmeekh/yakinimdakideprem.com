#!/usr/bin/env python3
"""
public/images/ altindaki tum imajlara EXIF/IPTC/XMP metadata ekler.

- Copyright, Artist, ImageDescription, WebStatement URL gomulur
- Google Images bu alanlari indexler (dogrulanmis)
- Idempotent: tekrar calistirmak guvenli (zaten varsa atlar)
- WebP, PNG, JPG destekli (exiftool uzerinden)

Kullanim:
  python3 scripts/add_image_metadata.py            # tum images/
  python3 scripts/add_image_metadata.py --force    # mevcut metadata'yi yeniden yaz
  python3 scripts/add_image_metadata.py --file X   # tek dosya
"""
from __future__ import annotations
import argparse
import subprocess
import json
from pathlib import Path

PUBLIC_IMAGES = Path(__file__).resolve().parent.parent / "public" / "images"

# Metadata sabitleri
COPYRIGHT = "© 2026 Yakınımdaki Deprem - Emin Kılıç. All rights reserved."
ARTIST = "Emin Kılıç"
CREATOR_URL = "https://yakinimdakideprem.com"
WEB_STATEMENT = "https://yakinimdakideprem.com/kullanim-sartlari.html"
LICENSE = "Yakınımdaki Deprem Tüm Hakları Saklıdır"
SOFTWARE = "Yakınımdaki Deprem (yakinimdakideprem.com)"

# Dosya adi -> aciklama map (ozel dosyalar icin)
DESCRIPTIONS = {
    "blog-son-deprem-haberleri.webp": "Son dakika deprem haberleri ve canli takip",
    "blog-deprem-cantasi.webp": "Deprem çantası hazırlama rehberi ve malzeme listesi",
    "blog-deprem-haritasi-rehberi.webp": "Türkiye deprem haritası ve risk bölgeleri",
    "blog-deprem-oncesi-hazirlik.webp": "Deprem öncesi hazırlık ve aile planı",
    "blog-deprem-sonrasi-ilk-24-saat.webp": "Deprem sonrası ilk 24 saat eylem planı",
    "blog-deprem-guvenlik-bilgileri.webp": "Deprem güvenlik bilgileri ve önlemler",
    "blog-bina-icindeyseniz.webp": "Deprem anında bina içindeyseniz yapılacaklar",
    "blog-disaridaysaniz.webp": "Deprem anında açık alandaysanız yapılacaklar",
    "blog-arac-kullanirken.webp": "Deprem anında araç kullanırken güvenlik",
    "cokapantutun.webp": "Çök - Kapan - Tutun hareketi illüstrasyonu",
    "cok.webp": "Deprem anında çökmek - hayat kurtaran ilk adım",
    "kapan.webp": "Deprem anında kapanmak - baş ve boyun koruma",
    "tutun.webp": "Deprem anında tutunmak - mobilyaya sıkı tutunma",
    "eminkilic.webp": "Emin Kılıç - Yakınımdaki Deprem kurucusu",
    "og-yakinimdakideprem.png": "Yakınımdaki Deprem - Canlı Deprem Haritası Türkiye",
    "esya-sabitleme-rehberi.webp": "Deprem için mobilya sabitleme rehberi",
    "fay-hatti-rehber.webp": "Türkiye fay hatları rehber görseli",
    "risk-hesaplayici.webp": "Deprem risk hesaplayıcı görsel",
    "widget-sitene-ekle.webp": "Deprem widget sitene ekle",
    "deprem-buyukluk-etkisi-infografik.webp": "Deprem büyüklük ölçeği ve etkileri infografik",
    "ankara-risk-haritasi.webp": "Ankara deprem risk haritası",
    "ankara-deprem-risk-haritasi-hero.webp": "Ankara deprem risk haritası hero görsel",
    "bursa-deprem-risk-haritasi.webp": "Bursa deprem risk haritası",
    "adana-deprem-risk-haritasi.webp": "Adana deprem risk haritası",
    "izmir-deprem-risk-haritasi-sema.webp": "İzmir deprem risk haritası şeması",
    "istanbul-fay-hatti.webp": "İstanbul fay hattı haritası",
    "elazig_risk.webp": "Elazığ deprem risk bölgesi",
    "kahramanmaras_risk.webp": "Kahramanmaraş deprem risk bölgesi",
    "hatay_risk.webp": "Hatay deprem risk bölgesi",
    "toplanma-alani-sorgulama.webp": "Toplanma alanı e-Devlet sorgulama rehberi",
    "DOHR.webp": "Deprem olası hasar riski",
    "deprem-haritasi.svg": "Türkiye deprem haritası",
    "deprem-aninda-cok-kapan-tutun.webp": "Deprem anında çök kapan tutun hareketi",
    "logo-placeholder.svg": "Yakınımdaki Deprem logo",
}

DEFAULT_DESCRIPTION = "Deprem güvenlik rehberi görseli - Yakınımdaki Deprem"


def get_existing_metadata(path: Path) -> dict:
    """exiftool ile mevcut metadata'yi oku."""
    try:
        result = subprocess.run(
            ["exiftool", "-j", "-Copyright", "-Artist", "-WebStatement", str(path)],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)
            if data:
                return data[0]
    except Exception:
        pass
    return {}


def has_metadata(path: Path) -> bool:
    """Dosya metadata'ya sahip mi?"""
    meta = get_existing_metadata(path)
    return bool(meta.get("Copyright") or meta.get("Artist"))


def add_metadata(path: Path, description: str) -> bool:
    """exiftool ile metadata ekle. Basari: True."""
    args = [
        "exiftool",
        "-overwrite_original",
        "-q", "-q",  # quiet
        f"-Copyright={COPYRIGHT}",
        f"-Artist={ARTIST}",
        f"-Creator={ARTIST}",
        f"-ImageDescription={description}",
        f"-Description={description}",
        f"-Caption-Abstract={description}",  # IPTC
        f"-XMP-dc:Creator={ARTIST}",
        f"-XMP-dc:Rights={COPYRIGHT}",
        f"-XMP-dc:Description={description}",
        f"-XMP-xmpRights:WebStatement={WEB_STATEMENT}",
        f"-XMP-xmpRights:UsageTerms={LICENSE}",
        f"-XMP-xmpRights:Marked=True",
        f"-XMP-photoshop:Credit=Yakınımdaki Deprem",
        f"-XMP-photoshop:Source={CREATOR_URL}",
        f"-Software={SOFTWARE}",
        f"-CopyrightNotice={COPYRIGHT}",
        str(path)
    ]
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except Exception as e:
        print(f"    HATA: {e}")
        return False


def process(path: Path, force: bool = False) -> str:
    """Dondurur: 'added', 'skipped', 'error'."""
    # Dosya uzantisi kontrol
    if path.suffix.lower() not in {".webp", ".jpg", ".jpeg", ".png"}:
        return "skipped (format)"

    if not force and has_metadata(path):
        return "already"

    # Aciklama sec
    desc = DESCRIPTIONS.get(path.name, DEFAULT_DESCRIPTION)

    if add_metadata(path, desc):
        return "added"
    else:
        return "error"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="Mevcut metadata'yi uzerine yaz")
    ap.add_argument("--file", help="Tek dosya isle")
    args = ap.parse_args()

    if args.file:
        paths = [Path(args.file)]
    else:
        paths = sorted(PUBLIC_IMAGES.iterdir())

    stats = {"added": 0, "already": 0, "error": 0, "skipped": 0}
    for p in paths:
        if not p.is_file():
            continue
        result = process(p, force=args.force)
        key = result.split()[0]
        stats[key] = stats.get(key, 0) + 1
        icon = {"added": "✓", "already": "-", "error": "✗", "skipped": "·"}.get(key, "?")
        print(f"  {icon} {p.name:<45} {result}")

    print(f"\nOzet: {stats.get('added', 0)} eklendi, {stats.get('already', 0)} zaten var, {stats.get('error', 0)} hata, {stats.get('skipped', 0)} atlandi")


if __name__ == "__main__":
    main()
