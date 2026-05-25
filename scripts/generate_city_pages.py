#!/usr/bin/env python3
"""
81 il için deprem sayfasi generator'u.

Kullanim:
    python3 scripts/generate_city_pages.py            # eksik illeri olustur
    python3 scripts/generate_city_pages.py --force    # hepsini yeniden yaz (mevcut özel sayfalar dahil)
    python3 scripts/generate_city_pages.py --dry-run  # sadece listele

Varsayilan davranis: mevcut deprem-<slug>.html dosyalarini korur (ozenle yazilmis 7 şehir kaybolmaz).
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

# Build-time tarih (her sayfa üretiminde güncel)
BUILD_DATE_ISO = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+03:00")

PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"

# --- Region templates ------------------------------------------------------
# Her bölge için fay hattı ozeti ve hazırlık ipuçları tabani.
REGIONS = {
    "marmara": {
        "title": "Marmara Bölgesi",
        "fault_summary": (
            "Kuzey Anadolu Fay Hattı'nın (KAF) Marmara Denizi altından geçen kolu, "
            "bölgenin en önemli sismik kaynağıdır. 1999 Gölcük ve Düzce depremleri bu hattın "
            "ne kadar aktif olduğunu göstermiştir. Marmara illeri olası büyük İstanbul depremi "
            "senaryosunda doğrudan etkilenir."
        ),
        "risk_level": "Çok yüksek",
        "common_tips": [
            "Eski yapı stoku yoğun olduğundan, bulunduğunuz binanın kentsel dönüşüm kapsamına girip girmediğini sorgulayın.",
            "Deniz kıyısındaki ilçelerde tsunami tahliye rotalarını öğrenin ve yüksek kotlu toplanma alanlarını not edin.",
            "Deprem çantanızda yedek şarj cihazı, düdük ve 72 saatlik su bulundurun.",
        ],
    },
    "ege": {
        "title": "Ege Bölgesi",
        "fault_summary": (
            "Ege Bölgesi, kuzey-güney yönlü normal faylar ve Ege Denizi'nin genişlemesiyle "
            "şekillenir. 2020 Samos-İzmir depremi, bölgenin büyük yıkımlara açık olduğunu hatırlattı. "
            "Denizli, Muğla ve Aydın hattında da tarihsel kayıtlarda önemli sarsıntılar vardır."
        ),
        "risk_level": "Yüksek",
        "common_tips": [
            "Zemin sıvılaşması riski bulunan kıyı kesimlerinde jeoteknik raporları inceletin.",
            "Turistik yoğunluğun yüksek olduğu mevsimlerde otel ve pansiyonların tahliye planına ulaşın.",
            "Tarım işçilerinin sığındığı barakalarda, hafif çelik profil destekli iyileştirmeler yapın.",
        ],
    },
    "akdeniz": {
        "title": "Akdeniz Bölgesi",
        "fault_summary": (
            "Akdeniz bölgesi, Doğu Anadolu Fay Hattı'nın güney uzantıları ile Kıbrıs Yayı'nın "
            "etkisi altındadır. Fethiye-Burdur hattı ile Çukurova ovası özellikle dikkat gerektirir. "
            "6 Şubat 2023 Kahramanmaraş depremleri bölgenin risklerini açıkça ortaya koydu."
        ),
        "risk_level": "Yüksek",
        "common_tips": [
            "Sera ve tarım yapılarında hafif çatılar kullanın, ağır betonarme çıkıntıların düşmesini engelleyin.",
            "Tsunami uyarı sistemleri konusunda AFAD ve belediye anonslarını takip edin.",
            "Turistik tesislerde çok dilli tahliye yönlendirmeleri talep edin.",
        ],
    },
    "icanadolu": {
        "title": "İç Anadolu Bölgesi",
        "fault_summary": (
            "İç Anadolu, Tuz Gölü Fay Zonu ve Kuzey Anadolu Fay Hattı'nın güney kolları arasında "
            "kalan, görece sakin fakat orta büyüklükte depremlere açık bir bölgedir. Konya Ovası'nın "
            "kuzeyindeki fay sistemleri ile Yozgat-Sivas hattında zaman zaman orta şiddetli sarsıntılar olur."
        ),
        "risk_level": "Orta",
        "common_tips": [
            "Kırsal mahallelerde kerpiç ve yığma yapıları güçlendirmek için yerel belediyelerden rehber isteyin.",
            "Kış aylarında soğuk sebebiyle tahliye süresini uzatacak battaniye, termal eldiven bulundurun.",
            "Tarım makinelerinin park yerini, acil durumda toplanma alanına erişimi engellemeyecek şekilde düzenleyin.",
        ],
    },
    "karadeniz": {
        "title": "Karadeniz Bölgesi",
        "fault_summary": (
            "Karadeniz bölgesi, Kuzey Anadolu Fay Hattı'nın kuzey kolları ve kıyı doğrultulu "
            "tali fayların etkisi altındadır. 1939 Erzincan, 1942 Niksar-Erbaa ve 1943 Ladik "
            "depremleri, hattın batı Karadeniz'e doğru uzanan aktivitesine örnektir."
        ),
        "risk_level": "Orta-Yüksek",
        "common_tips": [
            "Eğim dik vadi yerleşimlerinde heyelan ve kaya düşmesi riskini deprem sonrası değerlendirmek için plan yapın.",
            "Çay, fındık ve tütün işletmelerinde rafların yüksek koteden montajından kaçının.",
            "Kırsal yaylalarda jeneratörlü iletişim noktalarını muhtarlıkla birlikte belirleyin.",
        ],
    },
    "doguanadolu": {
        "title": "Doğu Anadolu Bölgesi",
        "fault_summary": (
            "Doğu Anadolu Fay Hattı (DAF) boyunca uzanan bölge, Türkiye'nin en aktif sismik "
            "kuşaklarından biridir. 1939 Erzincan, 2003 Bingöl, 2011 Van ve 2020 Elazığ-Sivrice "
            "depremleri bölgenin tarihini şekillendirdi. Yüksek rakım ve sert kış şartları "
            "tahliye sürecini zorlaştırır."
        ),
        "risk_level": "Çok yüksek",
        "common_tips": [
            "Kış şartlarında uzun süreli tahliye için termal yelek, kuru gıda ve kar kürekleri hazır bulundurun.",
            "Kırsal köylerde yığma ve taş yapıları takviye etmek için İl AFAD birimlerinden destek isteyin.",
            "Hidroelektrik ve baraj alanlarındaki yerleşim yerlerinde tahliye rotaları önceden belirlensin.",
        ],
    },
    "guneydoguanadolu": {
        "title": "Güneydoğu Anadolu Bölgesi",
        "fault_summary": (
            "Güneydoğu Anadolu, Doğu Anadolu Fay Hattı'nın Antakya-Kahramanmaraş-Adıyaman-Gölbaşı "
            "hattındaki güney kollarıyla yüksek risk altındadır. 6 Şubat 2023 depremleri bölgedeki "
            "şehirlerde geniş yıkıma neden oldu ve yeni yapılaşma standartlarını zorunlu kıldı."
        ),
        "risk_level": "Çok yüksek",
        "common_tips": [
            "2023 sonrası yapılan denetimlerde kırmızı veya sarı etiket alan binalardan uzak durun.",
            "Konteyner kent ve geçici barınma alanlarının tahliye eğitimlerine katılın.",
            "Bölgedeki tarihi yapılar için Vakıflar Genel Müdürlüğü sismik raporlarını inceleyin.",
        ],
    },
}

# --- Il verileri ----------------------------------------------------------
# slug: URL'de kullanilacak ASCII formu (mevcut 7 şehir bu format)
# name: H1, title'da kullanilacak (Turkce karakterli)
# keywords: place string'inde eslestirilecek kelimeler (normalize edilmis hali zaten arama yapacak)
# fault: il için kisa fay/risk notu
# lat/lon: schema.org GeoCoordinates
PROVINCES = [
    # --- Akdeniz ---
    {"slug": "adana", "name": "Adana", "region": "akdeniz", "keywords": ["adana", "ceyhan", "yumurtalik", "imamoglu", "pozanti", "kozan", "karatas"], "fault": "Doğu Anadolu Fay Hattı'nın Çukurova uzantısı ve Misis-Andirin fay zonu bölgede etkilidir.", "lat": 37.0000, "lon": 35.3213, "exists": True},
    {"slug": "antalya", "name": "Antalya", "region": "akdeniz", "keywords": ["antalya", "manavgat", "alanya", "serik", "kas", "finike", "kumluca", "elmali", "korkuteli", "kemer"], "fault": "Kibris Yayi'nin kuzey kolu ve Fethiye-Burdur fay zonu Antalya korfezini etkiler.", "lat": 36.8969, "lon": 30.7133},
    {"slug": "burdur", "name": "Burdur", "region": "akdeniz", "keywords": ["burdur", "bucak", "tefenni", "golhisar", "aglasun"], "fault": "Fethiye-Burdur Fay Zonu ve Burdur Golu civarindaki aktif faylar bölge riskini yukseltir.", "lat": 37.7203, "lon": 30.2908},
    {"slug": "hatay", "name": "Hatay", "region": "akdeniz", "keywords": ["hatay", "antakya", "iskenderun", "samandag", "kirikhan", "reyhanli", "dortyol", "belen"], "fault": "Doğu Anadolu Fay Hattı'nın en guney ucu (Amik-Olu Deniz Fayi) ve Kibris Yayi birlesimindedir. 2023 Maras depremlerinde agir hasar gördü.", "lat": 36.2025, "lon": 36.1606},
    {"slug": "isparta", "name": "Isparta", "region": "akdeniz", "keywords": ["isparta", "yalvac", "egirdir", "senirkent", "sutculer", "keciborlu"], "fault": "Isparta Buklumu olarak anilan fay sistemleri ve Egirdir-Kovada Fay Zonu aktiftir.", "lat": 37.7626, "lon": 30.5537},
    {"slug": "kahramanmaras", "name": "Kahramanmaras", "region": "guneydoguanadolu", "keywords": ["kahramanmaras", "maras", "elbistan", "pazarcik", "turkoglu", "afsin", "goksun", "nurdagi"], "fault": "6 Subat 2023 Pazarcik (Mw 7.8) ve Elbistan (Mw 7.6) depremlerinin merkezi. DAF üzerindeki en kritik illerden.", "lat": 37.5753, "lon": 36.9228, "exists": True},
    {"slug": "mersin", "name": "Mersin", "region": "akdeniz", "keywords": ["mersin", "tarsus", "erdemli", "silifke", "anamur", "bozyazi", "mut", "gulnar"], "fault": "Ecemis Fay Zonu ve Kibris Yayi'nin kuzey kesimi Mersin kiyilarini etkiler.", "lat": 36.8121, "lon": 34.6415},
    {"slug": "osmaniye", "name": "Osmaniye", "region": "akdeniz", "keywords": ["osmaniye", "kadirli", "duzici", "bahce", "toprakkale"], "fault": "Doğu Anadolu Fay Hattı'nın Karatas-Osmaniye kolu aktif olup 2023 depremlerinde etkilenmistir.", "lat": 37.2130, "lon": 36.1763},

    # --- Doğu Anadolu ---
    {"slug": "agri", "name": "Agri", "region": "doguanadolu", "keywords": ["agri", "dogubeyazit", "patnos", "diyadin", "tutak", "eleskirt"], "fault": "Kuzey Anadolu Fay Hattı'nın doğu ucu ile Tutak-Agri fay zonu bölge aktivitesini belirler.", "lat": 39.7191, "lon": 43.0503},
    {"slug": "ardahan", "name": "Ardahan", "region": "doguanadolu", "keywords": ["ardahan", "posof", "cildir", "gole", "hanak", "damal"], "fault": "Kuzeydogu Anadolu Fay Zonu boyunca yerel sarsintilara açık, yüksek rakimli bir ildir.", "lat": 41.1105, "lon": 42.7022},
    {"slug": "bingol", "name": "Bingol", "region": "doguanadolu", "keywords": ["bingol", "karliova", "genc", "solhan", "kigi"], "fault": "Kuzey ve Doğu Anadolu fay hatlarinin birlestigi Karliova ucgeninde bulunur; 2003 Mw 6.4 depremi büyük hasar yapti.", "lat": 38.8855, "lon": 40.4966},
    {"slug": "bitlis", "name": "Bitlis", "region": "doguanadolu", "keywords": ["bitlis", "tatvan", "ahlat", "adilcevaz", "mutki", "hizan", "guroymak"], "fault": "Bitlis Bindirme Kusagi ve Van Golu'nun batisindaki faylar aktif risk olusturur.", "lat": 38.4006, "lon": 42.1095},
    {"slug": "elazig", "name": "Elazig", "region": "doguanadolu", "keywords": ["elazig", "karakocan", "palu", "sivrice", "keban", "pertek", "maden", "kovancilar"], "fault": "Doğu Anadolu Fay Hattı üzerinde 2020 Sivrice (Mw 6.8) depreminin merkezi.", "lat": 38.6810, "lon": 39.2264, "exists": True},
    {"slug": "erzincan", "name": "Erzincan", "region": "doguanadolu", "keywords": ["erzincan", "tercan", "cayirli", "uzumlu", "kemaliye", "refahiye"], "fault": "Kuzey Anadolu Fay Hattı'nın en tehlikeli segmentlerinden biri. 1939 depremi 30 binin üzerinde can kaybina neden oldu.", "lat": 39.7500, "lon": 39.5000},
    {"slug": "erzurum", "name": "Erzurum", "region": "doguanadolu", "keywords": ["erzurum", "pasinler", "aziziye", "oltu", "horasan", "narman", "tortum", "ispir"], "fault": "Kuzey Anadolu Fay Hattı'nın Erzurum segmenti ve Tortum civarindaki yerel faylar etkilidir.", "lat": 39.9055, "lon": 41.2658},
    {"slug": "hakkari", "name": "Hakkari", "region": "doguanadolu", "keywords": ["hakkari", "yuksekova", "semdinli", "cukurca"], "fault": "Bitlis-Zagros Bindirme Kusagi üzerinde bulunan, yerel aktiviteye açık bir bölgedir.", "lat": 37.5744, "lon": 43.7408},
    {"slug": "igdir", "name": "Igdir", "region": "doguanadolu", "keywords": ["igdir", "aralik", "tuzluca", "karakoyunlu"], "fault": "Doğu Anadolu Yüksek Platosu'nda, Ağrı Dağı'na yakın konumu nedeniyle tektonik aktiviteye açık.", "lat": 39.9237, "lon": 44.0450},
    {"slug": "kars", "name": "Kars", "region": "doguanadolu", "keywords": ["kars", "sarikamis", "kagizman", "digor", "selim", "susuz", "arpacay"], "fault": "Kuzeydogu Anadolu Fay Zonu ve Kagizman faylari etkisi altindadir.", "lat": 40.6013, "lon": 43.0975},
    {"slug": "malatya", "name": "Malatya", "region": "doguanadolu", "keywords": ["malatya", "battalgazi", "yesilyurt", "dogansehir", "puturge", "akcadag", "hekimhan"], "fault": "Doğu Anadolu Fay Hattı'nın Puturge-Dogansehir segmenti; 2023 depremlerinde büyük hasar aldi.", "lat": 38.3552, "lon": 38.3095},
    {"slug": "mus", "name": "Mus", "region": "doguanadolu", "keywords": ["mus", "bulanik", "malazgirt", "varto", "korkut", "haskoy"], "fault": "Varto Fayi ve Muş havzasinin kuzey kenari yerel sismik aktivite uretir.", "lat": 38.7432, "lon": 41.5060},
    {"slug": "tunceli", "name": "Tunceli", "region": "doguanadolu", "keywords": ["tunceli", "pertek", "mazgirt", "ovacik", "cemisgezek", "pulumur", "hozat", "nazimiye"], "fault": "Kuzey Anadolu ve Doğu Anadolu fay hatlarinin birlesimine yakın, orta-yuksek aktivite bölgesi.", "lat": 39.1079, "lon": 39.5401},
    {"slug": "van", "name": "Van", "region": "doguanadolu", "keywords": ["van", "ercis", "edremit", "ipekyolu", "tusba", "ozalp", "muradiye", "baskale"], "fault": "2011 Van (Mw 7.2) ve Ercis depremlerinin merkezi; Van Golu'nun dogusundaki faylar aktiftir.", "lat": 38.4942, "lon": 43.3833},

    # --- Ege ---
    {"slug": "afyonkarahisar", "name": "Afyonkarahisar", "region": "ege", "keywords": ["afyon", "afyonkarahisar", "sandikli", "dinar", "sultandagi", "bolvadin", "sinanpasa"], "fault": "Sultandagi, Dinar ve Aksehir fay zonlari Afyon'un guneyinde aktiftir.", "lat": 38.7638, "lon": 30.5403},
    {"slug": "aydin", "name": "Aydin", "region": "ege", "keywords": ["aydin", "soke", "nazilli", "kusadasi", "didim", "germencik", "cine", "kocarli"], "fault": "Büyük Menderes Grabeni ve normal faylar sik sarsintilara neden olur.", "lat": 37.8560, "lon": 27.8416},
    {"slug": "balikesir", "name": "Balikesir", "region": "marmara", "keywords": ["balikesir", "bandirma", "edremit", "erdek", "ayvalik", "gonen", "sindirgi", "bigadic", "havran"], "fault": "Kuzey Anadolu Fay Hattı'nın guney kollari ve Edremit korfezindeki normal faylar etkilidir.", "lat": 39.6484, "lon": 27.8826},
    {"slug": "canakkale", "name": "Canakkale", "region": "marmara", "keywords": ["canakkale", "biga", "bayramic", "ezine", "gelibolu", "ayvacik", "yenice", "lapseki"], "fault": "Kuzey Anadolu Fay Hattı'nın Saros korfezi kolu ve Yenice-Gonen Fayi aktiftir.", "lat": 40.1553, "lon": 26.4142},
    {"slug": "denizli", "name": "Denizli", "region": "ege", "keywords": ["denizli", "pamukkale", "saraykoy", "buldan", "acipayam", "tavas", "honaz", "civril"], "fault": "Denizli Grabeni ve Büyük Menderes Grabeni bölgenin sismik karakterini belirler.", "lat": 37.7765, "lon": 29.0864},
    {"slug": "izmir", "name": "Izmir", "region": "ege", "keywords": ["izmir", "seferihisar", "foca", "cesme", "urla", "torbali", "gaziemir", "bayindir", "bornova", "karsiyaka", "menderes"], "fault": "Gulbahce, Tuzla ve İzmir korfezi faylari aktiftir; 2020 Samos-Izmir depremi hafizalarda.", "lat": 38.4237, "lon": 27.1428, "exists": True},
    {"slug": "kutahya", "name": "Kutahya", "region": "ege", "keywords": ["kutahya", "tavsanli", "gediz", "simav", "emet", "hisarcik", "domanic"], "fault": "Simav Fayi ve Kütahya Grabeni zaman zaman orta şiddetli depremler uretir.", "lat": 39.4167, "lon": 29.9833},
    {"slug": "manisa", "name": "Manisa", "region": "ege", "keywords": ["manisa", "akhisar", "salihli", "turgutlu", "saruhanli", "soma", "demirci", "kula", "golmarmara"], "fault": "Gediz Grabeni ve normal faylar; 1969 Alasehir ile 2020 Akhisar depremleri bölge hafizasinda.", "lat": 38.6191, "lon": 27.4289},
    {"slug": "mugla", "name": "Mugla", "region": "ege", "keywords": ["mugla", "bodrum", "marmaris", "fethiye", "milas", "dalaman", "koycegiz", "datca", "ula", "seydikemer"], "fault": "Fethiye-Burdur Fay Zonu ve Ege'nin normal fay sistemleri etkindir; 2017 Bodrum-Kos depremi yasandi.", "lat": 37.2153, "lon": 28.3636},
    {"slug": "usak", "name": "Usak", "region": "ege", "keywords": ["usak", "banaz", "esme", "sivasli", "karahalli", "ulubey"], "fault": "Simav ve Gediz Grabenleri'nin doğu ucuna yakindir.", "lat": 38.6823, "lon": 29.4082},

    # --- Güneydoğu Anadolu ---
    {"slug": "adiyaman", "name": "Adiyaman", "region": "guneydoguanadolu", "keywords": ["adiyaman", "kahta", "besni", "gerger", "golbasi", "samsat", "sincik"], "fault": "Doğu Anadolu Fay Hattı'nın Golbasi-Celikhan kolu aktiftir; 2023 depremlerinde büyük hasar aldi.", "lat": 37.7648, "lon": 38.2786},
    {"slug": "batman", "name": "Batman", "region": "guneydoguanadolu", "keywords": ["batman", "kozluk", "sason", "besiri", "hasankeyf", "gercus"], "fault": "Bitlis-Zagros Bindirme Kusagi'nin guneyinde bulunan, orta riskli bir bölgedir.", "lat": 37.8812, "lon": 41.1351},
    {"slug": "diyarbakir", "name": "Diyarbakir", "region": "guneydoguanadolu", "keywords": ["diyarbakir", "bismil", "cermik", "cinar", "ergani", "silvan", "kulp", "hazro"], "fault": "Bitlis Bindirme Kusagi ve Doğu Anadolu Fay Hattı'nın guney kollari etkisi altindadir.", "lat": 37.9144, "lon": 40.2306},
    {"slug": "gaziantep", "name": "Gaziantep", "region": "guneydoguanadolu", "keywords": ["gaziantep", "antep", "nizip", "islahiye", "nurdagi", "sahinbey", "sehitkamil", "oguzeli"], "fault": "Doğu Anadolu Fay Hattı'nın Islahiye-Nurdagi segmenti aktiftir; 2023 depremlerinden dogrudan etkilendi.", "lat": 37.0660, "lon": 37.3833},
    {"slug": "kilis", "name": "Kilis", "region": "guneydoguanadolu", "keywords": ["kilis", "elbeyli", "musabeyli", "polateli"], "fault": "DAF'in guney ucundaki tali faylarin etkisi altinda, sınır hattı boyunca yerel sarsıntılar yasar.", "lat": 36.7184, "lon": 37.1212},
    {"slug": "mardin", "name": "Mardin", "region": "guneydoguanadolu", "keywords": ["mardin", "kiziltepe", "midyat", "nusaybin", "derik", "savur", "mazidagi"], "fault": "Bitlis-Zagros Bindirme Kusagi'nin guney eteklerinde, görece orta riskli bolgededir.", "lat": 37.3120, "lon": 40.7350},
    {"slug": "sanliurfa", "name": "Sanliurfa", "region": "guneydoguanadolu", "keywords": ["sanliurfa", "urfa", "siverek", "birecik", "viransehir", "suruc", "harran", "akcakale", "bozova"], "fault": "DAF'in guney kollari ile Karacadağ volkanik yapisinin civarindaki faylar etkilidir.", "lat": 37.1591, "lon": 38.7969},
    {"slug": "siirt", "name": "Siirt", "region": "guneydoguanadolu", "keywords": ["siirt", "pervari", "eruh", "kurtalan", "baykan", "sirvan", "tillo"], "fault": "Bitlis-Zagros Bindirme Kusagi bölgede orta seviyede risk yaratir.", "lat": 37.9333, "lon": 41.9500},
    {"slug": "sirnak", "name": "Sirnak", "region": "guneydoguanadolu", "keywords": ["sirnak", "cizre", "silopi", "idil", "uludere", "beytussebap", "guclukonak"], "fault": "Bitlis-Zagros Bindirme Kusagi ve Iran sinirindaki aktif faylar etkilidir.", "lat": 37.4187, "lon": 42.4918},

    # --- İç Anadolu ---
    {"slug": "aksaray", "name": "Aksaray", "region": "icanadolu", "keywords": ["aksaray", "ortakoy", "eskil", "guzelyurt", "gulagac", "sariyahsi"], "fault": "Tuz Golu Fay Zonu ve Hasandag volkanik kompleksinin civarindaki faylar bölgeyi etkiler.", "lat": 38.3687, "lon": 34.0370},
    {"slug": "ankara", "name": "Ankara", "region": "icanadolu", "keywords": ["ankara", "kirikkale", "polatli", "cankiri", "beypazari", "kizilcahamam", "cubuk", "etimesgut", "sincan", "golbasi", "kahramankazan", "elmadag"], "fault": "Ezinepazari-Sungurlu Fayi, Tuz Golu Fay Zonu ve Kuzey Anadolu Fay Hattı'nın guney uzantıları etkilidir.", "lat": 39.9334, "lon": 32.8597, "exists": True},
    {"slug": "cankiri", "name": "Cankiri", "region": "icanadolu", "keywords": ["cankiri", "cerkes", "ilgaz", "korgun", "sabanozu", "atkaracalar", "kizilirmak", "yapraklik"], "fault": "Kuzey Anadolu Fay Hattı'nın Cerkes-Kursunlu segmentine yakın konumdadir.", "lat": 40.6013, "lon": 33.6134},
    {"slug": "eskisehir", "name": "Eskisehir", "region": "icanadolu", "keywords": ["eskisehir", "odunpazari", "tepebasi", "sivrihisar", "mahmudiye", "cifteler", "alpu", "beylikova", "inonu"], "fault": "Eskişehir Fay Zonu ve Inonu-Dodurga fay sistemi orta riskli aktiviteye sahiptir.", "lat": 39.7767, "lon": 30.5206},
    {"slug": "karaman", "name": "Karaman", "region": "icanadolu", "keywords": ["karaman", "ermenek", "ayranci", "kazimkarabekir", "sariveliler", "basyayla"], "fault": "Ecemis Fay Zonu'nun kuzey ucunda, orta seviyede risk altindadir.", "lat": 37.1759, "lon": 33.2287},
    {"slug": "kayseri", "name": "Kayseri", "region": "icanadolu", "keywords": ["kayseri", "bunyan", "develi", "incesu", "melikgazi", "kocasinan", "pinarbasi", "sarioglan", "yahyali", "yesilhisar", "tomarza"], "fault": "Ecemis Fay Zonu ve Erciyes volkanik kompleksinin civarindaki faylar etkilidir.", "lat": 38.7312, "lon": 35.4787},
    {"slug": "kirikkale", "name": "Kirikkale", "region": "icanadolu", "keywords": ["kirikkale", "keskin", "delice", "sulakyurt", "baliseyh", "karakecili", "yahsihan"], "fault": "Kuzey Anadolu Fay Hattı'nın Kırıkkale-Delice kolu yakınında, orta risk bolgesindedir.", "lat": 39.8468, "lon": 33.5153},
    {"slug": "kirsehir", "name": "Kirsehir", "region": "icanadolu", "keywords": ["kirsehir", "kaman", "mucur", "akpinar", "akcakent", "cicekdagi", "boztepe"], "fault": "Kırşehir Masifi üzerinde yer alir; yerel faylar orta seviyede sarsıntı uretir.", "lat": 39.1425, "lon": 34.1709},
    {"slug": "konya", "name": "Konya", "region": "icanadolu", "keywords": ["konya", "aksehir", "beysehir", "cumra", "eregli", "ilgin", "karatay", "meram", "seydisehir", "selcuklu", "kulu", "bozkir"], "fault": "Aksehir-Afyon Grabeni ve Beysehir Golu fay zonu bölgede etkindir.", "lat": 37.8714, "lon": 32.4846},
    {"slug": "nevsehir", "name": "Nevsehir", "region": "icanadolu", "keywords": ["nevsehir", "urgup", "avanos", "derinkuyu", "kozakli", "acigol", "hacibektas", "gulsehir"], "fault": "Kapadokya volkanik platosunun civarindaki faylar ve Tuz Golu Fay Zonu etkilidir.", "lat": 38.6939, "lon": 34.6857},
    {"slug": "nigde", "name": "Nigde", "region": "icanadolu", "keywords": ["nigde", "bor", "camardi", "ulukisla", "altunhisar", "ciftlik"], "fault": "Ecemis Fay Zonu ve Niğde masifinin kuzey kenari etkilidir.", "lat": 37.9667, "lon": 34.6833},
    {"slug": "sivas", "name": "Sivas", "region": "icanadolu", "keywords": ["sivas", "kangal", "divrigi", "susehri", "zara", "gurun", "hafik", "yildizeli", "imranli"], "fault": "Kuzey Anadolu Fay Hattı'nın Susehri-Koyulhisar kolu Sivas'in kuzeyinde aktiftir.", "lat": 39.7477, "lon": 37.0179},
    {"slug": "yozgat", "name": "Yozgat", "region": "icanadolu", "keywords": ["yozgat", "sorgun", "akdagmadeni", "bogazliyan", "sarikaya", "yerkoy", "cekerek", "kadisehri"], "fault": "Ezinepazari-Sungurlu Fayi ve Kuzey Anadolu Fay Hattı'nın guney kollari etkisindedir.", "lat": 39.8181, "lon": 34.8147},

    # --- Karadeniz ---
    {"slug": "amasya", "name": "Amasya", "region": "karadeniz", "keywords": ["amasya", "merzifon", "suluova", "tasova", "gumushacikoy", "goynucek", "hamamozu"], "fault": "Kuzey Anadolu Fay Hattı'nın Tasova-Erbaa segmenti etkilidir.", "lat": 40.6499, "lon": 35.8353},
    {"slug": "artvin", "name": "Artvin", "region": "karadeniz", "keywords": ["artvin", "hopa", "arhavi", "borcka", "savsat", "ardanuc", "yusufeli", "kemalpasa"], "fault": "Doğu Karadeniz Daglari civarindaki yerel faylar orta risk uretir.", "lat": 41.1828, "lon": 41.8183},
    {"slug": "bartin", "name": "Bartin", "region": "karadeniz", "keywords": ["bartin", "amasra", "ulus", "kurucasile"], "fault": "Kuzey Anadolu Fay Hattı'nın kuzey kollari ve kiyi heyelan riskleri dikkate alinmalidir.", "lat": 41.6344, "lon": 32.3375},
    {"slug": "bayburt", "name": "Bayburt", "region": "karadeniz", "keywords": ["bayburt", "aydintepe", "demirozu"], "fault": "Kuzey Anadolu Fay Hattı'nın Refahiye-Erzincan kolu yakinindadir.", "lat": 40.2552, "lon": 40.2249},
    {"slug": "bolu", "name": "Bolu", "region": "karadeniz", "keywords": ["bolu", "mudurnu", "gerede", "goynuk", "mengen", "seben", "yenicaga", "dortdivan"], "fault": "1944 Bolu-Gerede ve 1999 Düzce depremlerinin ucgeni. Kuzey Anadolu Fay Hattı merkez üzerinden gecer.", "lat": 40.7398, "lon": 31.6110},
    {"slug": "corum", "name": "Corum", "region": "karadeniz", "keywords": ["corum", "osmancik", "iskilip", "sungurlu", "alaca", "bayat", "mecitozu", "ortakoy corum"], "fault": "Kuzey Anadolu Fay Hattı'nın Sungurlu-Osmancik kolu aktiftir.", "lat": 40.5506, "lon": 34.9556},
    {"slug": "duzce", "name": "Duzce", "region": "karadeniz", "keywords": ["duzce", "akcakoca", "kaynasli", "yigilca", "golyaka", "cumayeri", "cilimli"], "fault": "1999 Mw 7.2 Düzce depreminin merkezi; Kuzey Anadolu Fay Hattı burada ciftlesir.", "lat": 40.8438, "lon": 31.1565},
    {"slug": "giresun", "name": "Giresun", "region": "karadeniz", "keywords": ["giresun", "bulancak", "espiye", "tirebolu", "gorele", "dereli", "sebinkarahisar", "alucra"], "fault": "Kuzey Anadolu Fay Hattı'nın Kuzey kollari ve kiyi heyelan faylari etkilidir.", "lat": 40.9128, "lon": 38.3895},
    {"slug": "gumushane", "name": "Gumushane", "region": "karadeniz", "keywords": ["gumushane", "kelkit", "siran", "kose", "torul", "kurtun"], "fault": "Kuzey Anadolu Fay Hattı'nın Kelkit vadisindeki segmenti etkilidir.", "lat": 40.4609, "lon": 39.4814},
    {"slug": "karabuk", "name": "Karabuk", "region": "karadeniz", "keywords": ["karabuk", "safranbolu", "eskipazar", "ovacik karabuk", "eflani", "yenice karabuk"], "fault": "Kuzey Anadolu Fay Hattı'nın Eskipazar segmenti yakinindadir.", "lat": 41.2061, "lon": 32.6204},
    {"slug": "kastamonu", "name": "Kastamonu", "region": "karadeniz", "keywords": ["kastamonu", "tosya", "taskopru", "cide", "inebolu", "bozkurt", "arac", "abana", "devrekani"], "fault": "Kuzey Anadolu Fay Hattı'nın Tosya segmenti; heyelan ve deprem etkilesimi yuksektir.", "lat": 41.3887, "lon": 33.7827},
    {"slug": "ordu", "name": "Ordu", "region": "karadeniz", "keywords": ["ordu", "unye", "fatsa", "perşembe", "korgan", "kumru", "mesudiye", "ulubey ordu", "aybasti"], "fault": "Kuzey Anadolu Fay Hattı'nın kuzey kiyi kolu etkilidir.", "lat": 40.9839, "lon": 37.8764},
    {"slug": "rize", "name": "Rize", "region": "karadeniz", "keywords": ["rize", "ardesen", "cayeli", "pazar", "findikli", "ikizdere", "camlihemsin", "guneysu"], "fault": "Doğu Karadeniz'in yerel faylari ve heyelan kaynakli sarsıntılar etkilidir.", "lat": 41.0201, "lon": 40.5234},
    {"slug": "samsun", "name": "Samsun", "region": "karadeniz", "keywords": ["samsun", "bafra", "carsamba", "vezirkopru", "havza", "terme", "ladik", "19 mayis", "ayvacik samsun", "alacam"], "fault": "Kuzey Anadolu Fay Hattı'nın Ladik-Havza segmenti etkilidir.", "lat": 41.2867, "lon": 36.3300},
    {"slug": "sinop", "name": "Sinop", "region": "karadeniz", "keywords": ["sinop", "boyabat", "gerze", "ayancik", "turkeli", "dikmen", "erfelek", "duragan", "saraydüzü"], "fault": "Kuzey Anadolu Fay Hattı'nın Boyabat-Duragan kolu aktiftir.", "lat": 42.0265, "lon": 35.1550},
    {"slug": "tokat", "name": "Tokat", "region": "karadeniz", "keywords": ["tokat", "niksar", "erbaa", "turhal", "zile", "resadiye", "almus", "artova"], "fault": "1942 ve 1943 Niksar-Erbaa depremlerinin hatirlattigi Kuzey Anadolu Fay Hattı aktiftir.", "lat": 40.3167, "lon": 36.5500},
    {"slug": "trabzon", "name": "Trabzon", "region": "karadeniz", "keywords": ["trabzon", "akcaabat", "arakli", "yomra", "of", "vakfikebir", "macka", "surmene", "besikduzu"], "fault": "Doğu Karadeniz kiyi faylari ve heyelanlarla birlesik sismik riskler vardir.", "lat": 41.0015, "lon": 39.7178},
    {"slug": "zonguldak", "name": "Zonguldak", "region": "karadeniz", "keywords": ["zonguldak", "eregli", "karadeniz eregli", "caycuma", "devrek", "alapli", "kilimli", "kozlu", "gokcebey"], "fault": "Kuzey Anadolu Fay Hattı'nın batı Karadeniz kolu ve maden zemini tetiklemeleri etkilidir.", "lat": 41.4564, "lon": 31.7987},

    # --- Marmara ---
    {"slug": "bilecik", "name": "Bilecik", "region": "marmara", "keywords": ["bilecik", "bozuyuk", "sogut", "golpazari", "osmaneli", "pazaryeri", "inhisar", "yenipazar bilecik"], "fault": "Kuzey Anadolu Fay Hattı'nın Geyve-Bozuyuk kolu etkilidir.", "lat": 40.1456, "lon": 29.9793},
    {"slug": "bursa", "name": "Bursa", "region": "marmara", "keywords": ["bursa", "gemlik", "mudanya", "inegol", "orhangazi", "iznik", "yenisehir", "karacabey", "mustafakemalpasa", "osmangazi", "nilufer", "yildirim"], "fault": "Gemlik Fayi ve Yenisehir Fay Zonu ile Kuzey Anadolu Fay Hattı'nın guney kollari etkilidir.", "lat": 40.1826, "lon": 29.0665, "exists": True},
    {"slug": "edirne", "name": "Edirne", "region": "marmara", "keywords": ["edirne", "kesan", "uzunkopru", "ipsala", "havsa", "enez", "lalapasa", "suloglu", "meric"], "fault": "Kuzey Anadolu Fay Hattı'nın Saros kolu ve Ganos Fayi etkisindedir.", "lat": 41.6771, "lon": 26.5557},
    {"slug": "istanbul", "name": "Istanbul", "region": "marmara", "keywords": ["istanbul", "marmara", "marmara denizi", "silivri", "adalar", "yalova", "kocaeli", "cinarcik", "bogaz", "besiktas", "kadikoy", "bakirkoy", "avcilar", "tuzla", "sariyer"], "fault": "Kuzey Anadolu Fay Hattı'nın Marmara Denizi altindaki kolu, olası büyük İstanbul depremi senaryosunun kaynagidir.", "lat": 41.0082, "lon": 28.9784, "exists": True},
    {"slug": "kirklareli", "name": "Kirklareli", "region": "marmara", "keywords": ["kirklareli", "luleburgaz", "babaeski", "pinarhisar", "vize", "demirkoy", "pehlivankoy", "kofcaz"], "fault": "Kuzey Anadolu Fay Hattı'nın Saros ve Istranca kollari civarindadir.", "lat": 41.7351, "lon": 27.2246},
    {"slug": "kocaeli", "name": "Kocaeli", "region": "marmara", "keywords": ["kocaeli", "izmit", "gebze", "derince", "korfez", "golcuk", "karamursel", "dilovasi", "kandira", "basiskele", "darica", "cayirova"], "fault": "1999 Mw 7.6 Izmit depreminin merkezi; Kuzey Anadolu Fay Hattı'nın Marmara kolu uzerindedir.", "lat": 40.8533, "lon": 29.8815},
    {"slug": "sakarya", "name": "Sakarya", "region": "marmara", "keywords": ["sakarya", "adapazari", "akyazi", "hendek", "karasu", "geyve", "pamukova", "sapanca", "ferizli", "karapurcek", "kaynarca"], "fault": "Kuzey Anadolu Fay Hattı'nın Sapanca-Akyazi kolu aktiftir; 1999'da büyük hasar aldi.", "lat": 40.7889, "lon": 30.4060},
    {"slug": "tekirdag", "name": "Tekirdag", "region": "marmara", "keywords": ["tekirdag", "corlu", "cerkezkoy", "malkara", "saray", "muratli", "hayrabolu", "kapakli", "suleymanpasa", "marmara ereglisi"], "fault": "Kuzey Anadolu Fay Hattı'nın Marmara-Saros kolu ve Ganos Fayi kiyi boyunca aktif.", "lat": 40.9780, "lon": 27.5110},
    {"slug": "yalova", "name": "Yalova", "region": "marmara", "keywords": ["yalova", "cinarcik", "termal", "altinova", "armutlu", "cifltikkoy"], "fault": "Kuzey Anadolu Fay Hattı'nın Marmara Denizi ici kolu Yalova'yi dogrudan etkiler; 1999 depreminde çök agir hasar aldi.", "lat": 40.6500, "lon": 29.2667},
]


REGION_FOOTER_TIP = (
    "AFAD'in resmi ariza ve toplanma alanı uygulamalarini yukleyin; okul ve isyeri tahliye "
    "tatbikatlarina katılın. Bilgi ve veri için Kandilli Rasathanesi ile AFAD siteleri en güncel "
    "resmi kaynaklardir."
)


# --- Template -------------------------------------------------------------
TEMPLATE = """<!DOCTYPE html>
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
    <title>{name} Deprem – Anlık Deprem Haritası ve Son Depremler</title>
    <meta name="description"
        content="{name} anlık deprem haritası: son {name} depremleri, fay hattı bilgisi, risk profili ve hazırlık rehberi. Kandilli + AFAD canlı veri.">
    <meta name="keywords"
        content="{name_lower} deprem, son deprem {name_lower}, {name_lower} deprem haritası, anlık {name_lower} deprem, {region_title_lower} depremi, afad {name_lower}, kandilli {name_lower}">
    <link rel="canonical" href="https://yakinimdakideprem.com/deprem-{slug}.html" />
    <meta property="og:locale" content="tr_TR">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{name} Depremi - {region_title} Deprem Bilgileri">
    <meta property="og:description"
        content="{name} ve {region_title} için son deprem kayitlarini, fay hattı bilgisini ve hazırlık rehberlerini goruntuleyin.">
    <meta property="og:url" content="https://yakinimdakideprem.com/deprem-{slug}.html">
    <meta property="og:site_name" content="Yakınımdaki Deprem">
    <meta property="og:image" content="https://yakinimdakideprem.com/images/og-yakinimdakideprem.webp">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{name} Depremi - {region_title} Deprem Bilgileri">
    <meta name="twitter:description"
        content="{name} için güncel deprem tablosu, toplanma alanları ve hazırlık ipuçları.">
    <meta name="twitter:image" content="https://yakinimdakideprem.com/images/og-yakinimdakideprem.webp">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" media="print" onload="this.media='all'">
    <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"></noscript>
    <link rel="stylesheet" href="css/blog.css?v=202601132130">
    <link rel="stylesheet" href="css/components.min.css?v=202601131900">
    <link rel="stylesheet" href="css/header.min.css?v=202604182300">
    <link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="icons/favicon-16x16.png">
    <link rel="manifest" href="site.webmanifest">
    <link rel="mask-icon" href="/icons/safari-pinned-tab.svg" color="#5bbad5">
    <script type="application/ld+json">
{article_schema}
    </script>
    <script type="application/ld+json">
{place_schema}
    </script>
    <link rel="stylesheet" href="css/footer.css?v=202512182020">
    <link rel="stylesheet" href="css/city-search.css?v=202604182300">
    <script type="application/ld+json">
{breadcrumb_schema}
    </script>
    <style>
        nav a.nav-highlight {{
            color: #d32f2f;
            font-weight: 700;
        }}
        nav a.nav-highlight:hover {{
            color: #b71c1c;
            text-decoration: underline;
        }}
        .city-summary-card {{
            background: #fff;
            border: 1px solid #e5e7eb;
            border-left: 5px solid #d32f2f;
            border-radius: 12px;
            padding: 20px 22px;
            margin: 18px 0 28px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px 24px;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
        }}
        .city-summary-card dt {{
            font-size: 0.85rem;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}
        .city-summary-card dd {{
            margin: 0 0 10px;
            font-weight: 600;
            color: #111827;
        }}
        @media (max-width: 640px) {{
            .city-summary-card {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
    <!-- Microsoft Clarity -->
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){{
            c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        }})(window, document, "clarity", "script", "wdt4zn01kt");
    </script>
</head>

<body>
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-WQZS53QX" height="0" width="0"
            style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->
    <header id="hidden-header">
        <div class="container">
            <a href="/" class="logo" rel="noopener noreferrer">
                <img loading="lazy" src="icons/logo.png" alt="Yak&#305;n&#305;mdaki Deprem logosu" width="60" height="60">
                <span data-text="Yak&#305;n&#305;mdaki Deprem">Yak&#305;n&#305;mdaki Deprem</span>
            </a>

            <div id="city-search" class="city-search" role="search">
                <div class="city-search__bar">
                    <i class="fas fa-search city-search__icon" aria-hidden="true"></i>
                    <label for="city-search-input" class="sr-only">Şehir ara</label>
                    <input type="text" id="city-search-input"
                        placeholder="Şehir Ara"
                        autocomplete="off"
                        aria-autocomplete="list"
                        aria-controls="city-search-results">
                    <button type="button" id="city-search-clear" aria-label="Temizle" hidden>
                        <i class="fas fa-times" aria-hidden="true"></i>
                    </button>
                </div>
                <ul id="city-search-results" class="city-search__results" role="listbox" hidden></ul>
            </div>

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
                        <a href="/ilk-yardim-cantasi.html" rel="noopener noreferrer">İlk Yardım Cantasi</a>
                        <a href="/ben-kimim.html" rel="noopener noreferrer">Ben Kimim</a>
                        <a href="/blog.html" rel="noopener noreferrer">Blog</a>
                    </div>
                </div>
                <div class="nav-dropdown">
                    <button class="dropdown-toggle" type="button" aria-haspopup="true" aria-expanded="false">
                        Şehir Depremleri <i class="fas fa-chevron-down"></i>
                    </button>
                    <div class="dropdown-menu">
                        <a href="/deprem-sehirleri.html" rel="noopener noreferrer"><strong>Tüm 81 Il</strong></a>
                        <a href="/deprem-istanbul.html" rel="noopener noreferrer">Istanbul Depremi</a>
                        <a href="/deprem-izmir.html" rel="noopener noreferrer">Izmir Depremi</a>
                        <a href="/deprem-ankara.html" rel="noopener noreferrer">Ankara Depremi</a>
                        <a href="/deprem-elazig.html" rel="noopener noreferrer">Elazig Depremi</a>
                        <a href="/deprem-bursa.html" rel="noopener noreferrer">Bursa Depremi</a>
                        <a href="/deprem-adana.html" rel="noopener noreferrer">Adana Depremi</a>
                        <a href="/deprem-kahramanmaras.html" rel="noopener noreferrer">Kahramanmaras Depremi</a>
                    </div>
                </div>
            </nav>
        </div>
    </header>

    <header class="page-header">
        <div class="container">
            <h1>{name} Depremi</h1>
            <p>{name} ve {region_title} için son deprem verileri, fay hattı bilgisi, toplanma alanları ve hazırlık önerileri.</p>
        </div>
    </header>

    <main class="container">
        <article class="blog-post">
            <div class="post-content city-quake-content">
                <nav class="toc" aria-label="İçindekiler">
                    <strong>İçindekiler</strong>
                    <ul></ul>
                </nav>

                <section>
                    <h2>{name}'da Az Önce Deprem Oldu mu?</h2>
                    <p id="city-summary">Veriler yükleniyor...</p>
                    <dl class="city-summary-card" aria-label="{name} özet bilgi karti">
                        <dt>Bölge</dt>
                        <dd>{region_title}</dd>
                        <dt>Risk Seviyesi</dt>
                        <dd>{risk_level}</dd>
                        <dt>Aktif Fay</dt>
                        <dd>{fault_short}</dd>
                        <dt>Resmi Kaynaklar</dt>
                        <dd><a href="https://deprem.afad.gov.tr" target="_blank" rel="noopener noreferrer">AFAD</a> - <a href="https://koeri.boun.edu.tr" target="_blank" rel="noopener noreferrer">Kandilli</a></dd>
                    </dl>
                </section>

                <section>
                    <h2>Son {name} Depremleri</h2>
                    <div class="table-wrapper">
                        <table class="quake-table">
                            <thead>
                                <tr>
                                    <th>Tarih/Saat</th>
                                    <th>Büyüklük</th>
                                    <th>Derinlik</th>
                                    <th>Konum</th>
                                </tr>
                            </thead>
                            <tbody id="city-quakes">
                                <tr>
                                    <td colspan="4">Kayitlar yükleniyor...</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </section>

                <section class="city-context">
                    <h2>{name} Fay Hatları ve Bölge Risk Profili</h2>
                    <p>{fault_detail}</p>
                    <p>{region_summary}</p>
                </section>

                <section>
                    <h2>Deprem Anında Üç Adım: Çök, Kapan, Tutun</h2>
                    <div class="safety-steps safety-steps--grid">
                        <figure class="safety-steps__item">
                            <img src="images/cok.webp" alt="Deprem sirasinda cokmek" loading="lazy" width="1024" height="448">
                            <figcaption><strong>1 - Çök:</strong> Dizlerinizin üzerine çökerek yere mumkun oldugunca yaklasin.</figcaption>
                        </figure>
                        <figure class="safety-steps__item">
                            <img src="images/kapan.webp" alt="Deprem sirasinda kapanmak" loading="lazy" width="1024" height="448">
                            <figcaption><strong>2 - Kapan:</strong> Başınızı ve boynunuzu ellerinizle koruyun.</figcaption>
                        </figure>
                        <figure class="safety-steps__item">
                            <img src="images/tutun.webp" alt="Deprem sirasinda tutunmak" loading="lazy" width="1024" height="448">
                            <figcaption><strong>3 - Tutun:</strong> Güvenli bir mobilyaya tutunarak sarsinti bitene kadar bekleyin.</figcaption>
                        </figure>
                    </div>
                </section>

                <section>
                    <h2>{name} Toplanma Alanları</h2>
                    <p>AFAD toplanma alanlarını <a class="highlight-link" href="https://www.türkiye.gov.tr/afet-ve-acil-durum-yonetimi-acil-toplanma-alani-sorgulama?bölge=Secimi" target="_blank" rel="noopener noreferrer">e-Devlet</a> üzerinden {name} seçerek kontrol edin. Mahallenizin en yakın toplanma alanını aile üyeleriyle bir kez birlikte yürümeniz, panik anındaki reflekslerinizi güçlendirir.</p>
                </section>

                <section>
                    <h2>{name} Deprem Hazırlık İpuçları</h2>
                    <ul>
{tips_html}
                        <li>{closing_tip}</li>
                    </ul>
                </section>

                <section>
                    <h2>{region_title} Diğer İller</h2>
                    <p>Bolgedeki komsu illerin deprem sayfalarini da inceleyebilirsiniz:</p>
                    <ul class="region-neighbors">
{neighbors_html}
                    </ul>
                    <p><a class="highlight-link" href="/deprem-sehirleri.html" rel="noopener noreferrer">Tüm 81 ilin deprem sayfasini goruntule &rarr;</a></p>
                </section>

                <section>
                    <h2>{name} İçin Deprem Rehberleri</h2>
                    <p>{name}'da deprem hazırlığı için incelemeniz gereken rehberler:</p>
                    <ul>
                        <li><a href="/blog-deprem-oncesi-hazirlik.html" rel="noopener noreferrer">Deprem Öncesi Hazırlık: Ev ve Aile Planı</a></li>
                        <li><a href="/blog-deprem-cantasi.html" rel="noopener noreferrer">Deprem Çantası Listesi 2026</a></li>
                        <li><a href="/blog-bina-icindeyseniz.html" rel="noopener noreferrer">Bina İçindeyseniz: Çök-Kapan-Tutun</a></li>
                        <li><a href="/blog-disaridaysaniz.html" rel="noopener noreferrer">Açık Alandayken: Güvenli Davranış</a></li>
                        <li><a href="/blog-deprem-sonrasi-ilk-24-saat.html" rel="noopener noreferrer">Deprem Sonrası İlk 24 Saat</a></li>
                        <li><a href="/blog-dask-nedir.html" rel="noopener noreferrer">DASK Zorunlu Deprem Sigortası</a></li>
                        <li><a href="/blog-toplanma-alani-sorgulama.html" rel="noopener noreferrer">Toplanma Alanı E-Devlet Sorgulama</a></li>
                    </ul>
                </section>

                <section>
                    <h2>İlgili Sayfalar</h2>
                    <ul>
                        <li><a href="/son-dakika-deprem.html" rel="noopener noreferrer">Deprem Mi Oldu? Anlık Takip</a></li>
                        <li><a href="/" rel="noopener noreferrer">Anlık Deprem Haritası Türkiye</a></li>
                        <li><a href="/deprem-aninda.html" rel="noopener noreferrer">Deprem Anında Yapılacaklar</a></li>
                        <li><a href="/ilk-yardim-cantasi.html" rel="noopener noreferrer">İlk Yardım Çantası</a></li>
                        <li><a href="/turkiye-deprem-rehberi-fay-hatlari.html" rel="noopener noreferrer">Türkiye Fay Hatları Rehberi</a></li>
                        <li><a href="/blog.html" rel="noopener noreferrer">Tüm Deprem Rehberleri</a></li>
                    </ul>
                </section>
            </div>
        </article>
    </main>

    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-logo">
                    <img loading="lazy" src="icons/logo.png" alt="Yakınımdaki Deprem logosu" width="60" height="60">
                    <h3>Yakınımdaki Deprem</h3>
                    <p>Yakınımdakideprem.com bağımsız, ücretsiz ve tek kişi tarafından geliştirilen bir projedir. Resmi kurumlarla bağlantılı degildir.</p>
                </div>
                <div class="footer-links">
                    <div class="footer-column">
                        <h3>Hızlı Linkler</h3>
                        <ul>
                            <li><a href="/" rel="noopener noreferrer">Ana Sayfa</a></li>
                            <li><a href="/deprem-aninda.html" rel="noopener noreferrer">Deprem Anında</a></li>
                            <li><a href="/ilk-yardim-cantasi.html" rel="noopener noreferrer">İlk Yardım Cantasi</a></li>
                            <li><a href="/ben-kimim.html" rel="noopener noreferrer">Ben Kimim</a></li>
                            <li><a href="/blog.html" rel="noopener noreferrer">Blog</a></li>
                        </ul>
                    </div>
                    <div class="footer-column">
                        <h3>Kaynaklar</h3>
                        <ul>
                            <li><a href="https://deprem.afad.gov.tr" target="_blank" rel="noopener noreferrer">AFAD</a></li>
                            <li><a href="https://koeri.boun.edu.tr" target="_blank" rel="noopener noreferrer">Kandilli Rasathanesi</a></li>
                        </ul>
                    </div>
                    <div class="footer-column">
                        <h3>Iletisim</h3>
                        <ul>
                            <li><a href="https://www.linkedin.com/in/emin-k%C4%B1l%C4%B1%C3%A7-250b14210/" target="_blank" rel="noopener noreferrer">LinkedIn Profilim</a></li>
                        </ul>
                    </div>
                    <div class="footer-column">
                        <h3>Yasal</h3>
                        <ul>
                            <li><a href="/kullanim-sartlari.html" rel="noopener noreferrer">Kullanim Sartlari</a></li>
                            <li><a href="/gizlilik-politikasi.html" rel="noopener noreferrer">Gizlilik Politikasi</a></li>
                            <li><a href="/cerez-politikasi.html" rel="noopener noreferrer">Cerez Politikasi</a></li>
                            <li><a href="/sorumluluk-reddi.html" rel="noopener noreferrer">Sorumluluk Reddi</a></li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 Yakınımdaki Deprem | Toplumu Geliştirmek İçin Çabalayan Bir Girişim</p>
                <p class="footer-api-source">Deprem API verileri <a href="https://github.com/orhanayd/kandilli-rasathanesi-api" target="_blank" rel="noopener noreferrer">github.com/orhanayd/kandilli-rasathanesi-api</a> kaynagindan cekilmektedir.</p>
            </div>
        </div>
    </footer>

    <script src="js/header.min.js?v=202604182300"></script>
    <script src="js/toc.js?v=202512182020"></script>
    <script src="js/city-keywords.js?v=202604182300"></script>
    <script src="js/city-search.js?v=202604182300" defer></script>
    <script src="js/live-quakes.js?v=202601132330"></script>
    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            renderCityQuakes({{
                tableSelector: '#city-quakes',
                cityKeyword: '{slug}',
                limit: 20,
                summarySelector: '#city-summary'
            }});
        }});
    </script>
</body>

</html>
"""


# --- Helpers --------------------------------------------------------------
def normalize_name_for_keywords(value: str) -> str:
    """Turkce karakterleri ASCII'ye cevirir ve lower yapar."""
    mapping = str.maketrans({
        "ç": "c", "Ç": "c", "ğ": "g", "Ğ": "g", "ı": "i", "İ": "i",
        "ö": "o", "Ö": "o", "ş": "s", "Ş": "s", "ü": "u", "Ü": "u",
        "â": "a", "Â": "a", "î": "i", "Î": "i", "û": "u", "Û": "u",
    })
    return value.translate(mapping).lower()


def build_schema(province: dict) -> tuple[str, str, str]:
    name = province["name"]
    slug = province["slug"]
    region_title = REGIONS[province["region"]]["title"]
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"{name} Depremi - {region_title} Deprem Bilgileri",
        "description": f"{name} deprem sayfasi: {region_title} için son deprem tablosu, fay hattı bilgisi, tahliye plani önerileri ve toplanma alanı baglantilari.",
        "author": {
            "@type": "Person",
            "name": "Emin Kilic",
            "url": "https://yakinimdakideprem.com/ben-kimim.html",
            "image": {
                "@type": "ImageObject",
                "url": "https://yakinimdakideprem.com/images/eminkilic.jpg",
                "width": 1664,
                "height": 1876,
            },
        },
        "publisher": {
            "@type": "Organization",
            "name": "Yakınımdaki Deprem",
            "logo": {
                "@type": "ImageObject",
                "url": "https://yakinimdakideprem.com/icons/android-chrome-192x192.png",
                "width": 192,
                "height": 192,
            },
        },
        "url": f"https://yakinimdakideprem.com/deprem-{slug}.html",
        "image": {
            "@type": "ImageObject",
            "url": "https://yakinimdakideprem.com/images/og-yakinimdakideprem.webp",
            "width": 1200,
            "height": 630,
            "caption": f"{name} deprem haritası ve son depremler",
            "creditText": "Yakınımdaki Deprem",
            "copyrightNotice": "© 2026 Yakınımdaki Deprem",
            "license": "https://yakinimdakideprem.com/kullanim-sartlari.html",
            "creator": {"@type": "Person", "name": "Emin Kılıç", "url": "https://yakinimdakideprem.com/ben-kimim.html"},
        },
        "datePublished": "2026-04-17T09:00:00+03:00",
        "dateModified": BUILD_DATE_ISO,
        "inLanguage": "tr-TR",
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"https://yakinimdakideprem.com/deprem-{slug}.html",
        },
    }
    place = {
        "@context": "https://schema.org",
        "@type": "Place",
        "name": name,
        "url": f"https://yakinimdakideprem.com/deprem-{slug}.html",
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": province["lat"],
            "longitude": province["lon"],
        },
        "containedInPlace": {"@type": "Country", "name": "Türkiye"},
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": "https://yakinimdakideprem.com/"},
            {"@type": "ListItem", "position": 2, "name": "Şehir Depremleri", "item": "https://yakinimdakideprem.com/"},
            {"@type": "ListItem", "position": 3, "name": f"{name} Depremi"},
        ],
    }
    return (
        json.dumps(article, ensure_ascii=False, indent=2),
        json.dumps(place, ensure_ascii=False, indent=2),
        json.dumps(breadcrumb, ensure_ascii=False, indent=2),
    )


def build_neighbors_html(province: dict) -> str:
    """Ayni bolgedeki diğer illeri rasgele degil, alfabetik siralayip 8 tanesini seç."""
    same_region = [p for p in PROVINCES if p["region"] == province["region"] and p["slug"] != province["slug"]]
    same_region.sort(key=lambda p: p["name"])
    # En fazla 8 komsu
    selected = same_region[:8]
    lines = []
    for n in selected:
        lines.append(
            f'                        <li><a href="/deprem-{n["slug"]}.html" rel="noopener noreferrer">{n["name"]} Depremi</a></li>'
        )
    return "\n".join(lines)


def render_page(province: dict) -> str:
    region = REGIONS[province["region"]]
    article_schema, place_schema, breadcrumb_schema = build_schema(province)

    tips_html_lines = []
    for tip in region["common_tips"]:
        tips_html_lines.append(f"                        <li>{tip}</li>")
    tips_html = "\n".join(tips_html_lines)

    # Kisa fay ozeti (karta goster) - ilk cumle
    fault_short = province["fault"].split(".")[0] + "."

    return TEMPLATE.format(
        slug=province["slug"],
        name=province["name"],
        name_lower=normalize_name_for_keywords(province["name"]),
        region_title=region["title"],
        region_title_lower=normalize_name_for_keywords(region["title"]),
        region_summary=region["fault_summary"],
        risk_level=region["risk_level"],
        fault_short=fault_short,
        fault_detail=province["fault"],
        tips_html=tips_html,
        closing_tip=REGION_FOOTER_TIP,
        neighbors_html=build_neighbors_html(province),
        article_schema=article_schema,
        place_schema=place_schema,
        breadcrumb_schema=breadcrumb_schema,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Mevcut sayfalari da yeniden yaz")
    parser.add_argument("--dry-run", action="store_true", help="Yazmadan yalnizca listele")
    args = parser.parse_args()

    # Slug tekrari kontrolü
    slugs = [p["slug"] for p in PROVINCES]
    if len(slugs) != len(set(slugs)):
        duplicates = {s for s in slugs if slugs.count(s) > 1}
        raise SystemExit(f"Slug tekrari: {duplicates}")

    written = 0
    skipped = 0
    total = len(PROVINCES)
    for province in PROVINCES:
        target = PUBLIC_DIR / f"deprem-{province['slug']}.html"

        # exists:True olan 7 özel sayfa ASLA yazilmaz (--force'ta bile)
        if province.get("exists"):
            print(f"[korundu] {target.name} (özel tasarim, --force'ta bile atlanir)")
            skipped += 1
            continue

        if target.exists() and not args.force:
            print(f"[atlandi]  {target.name} (mevcut korundu)")
            skipped += 1
            continue

        rendered = render_page(province)
        if args.dry_run:
            print(f"[dry-run]  {target.name} olusturulacakti ({len(rendered)} byte)")
        else:
            target.write_text(rendered, encoding="utf-8")
            print(f"[yazildi]  {target.name}")
        written += 1

    print(f"\nOzet: toplam {total} il, yazildi {written}, atlandi {skipped}")


if __name__ == "__main__":
    main()
