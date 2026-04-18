/*
 * 81 il icin Kandilli/AFAD konum (place) alaninda eslesecek anahtar kelimeler.
 * renderCityQuakes(cityKeyword: <slug>) tarafindan kullanilir.
 * Ayrica index.html'deki sehir arama kutusu da bu listeyi kullanir.
 *
 * Anahtar tasarim notu: Kandilli place stringi genelde "SEHIR ILCE (IL)" gibi
 * ASCII karakterlerle gelir (ör. "SIVRICE-ELAZIG"), bu yuzden alias'lari
 * ASCII normalize etmek yeterli. Turkce karakterli varyasyonlar da eklenmistir.
 */
(function () {
  const cityData = [
    { slug: "adana", name: "Adana", region: "Akdeniz", lat: 37.0000, lon: 35.3213, keywords: ["adana", "ceyhan", "yumurtalik", "imamoglu", "pozanti", "kozan", "karatas"] },
    { slug: "adiyaman", name: "Adıyaman", region: "Güneydoğu Anadolu", lat: 37.7648, lon: 38.2786, keywords: ["adiyaman", "adıyaman", "kahta", "besni", "gerger", "golbasi adiyaman", "samsat", "sincik"] },
    { slug: "afyonkarahisar", name: "Afyonkarahisar", region: "Ege", lat: 38.7638, lon: 30.5403, keywords: ["afyon", "afyonkarahisar", "sandikli", "sandıklı", "dinar", "sultandagi", "sultandağı", "bolvadin", "sinanpasa", "sinanpaşa"] },
    { slug: "agri", name: "Ağrı", region: "Doğu Anadolu", lat: 39.7191, lon: 43.0503, keywords: ["agri", "ağrı", "dogubeyazit", "doğubeyazıt", "patnos", "diyadin", "tutak", "eleskirt", "eleşkirt"] },
    { slug: "aksaray", name: "Aksaray", region: "İç Anadolu", lat: 38.3687, lon: 34.0370, keywords: ["aksaray", "ortakoy aksaray", "eskil", "guzelyurt", "güzelyurt", "gulagac", "gülağaç", "sariyahsi", "sarıyahşi"] },
    { slug: "amasya", name: "Amasya", region: "Karadeniz", lat: 40.6499, lon: 35.8353, keywords: ["amasya", "merzifon", "suluova", "tasova", "taşova", "gumushacikoy", "gümüşhacıköy", "goynucek", "göynücek", "hamamozu", "hamamözü"] },
    { slug: "ankara", name: "Ankara", region: "İç Anadolu", lat: 39.9334, lon: 32.8597, keywords: ["ankara", "kirikkale", "kırıkkale", "polatli", "polatlı", "cankiri", "çankırı", "beypazari", "beypazarı", "kizilcahamam", "kızılcahamam", "cubuk", "çubuk", "etimesgut", "sincan", "golbasi ankara", "gölbaşı", "kahramankazan", "elmadag", "elmadağ"] },
    { slug: "antalya", name: "Antalya", region: "Akdeniz", lat: 36.8969, lon: 30.7133, keywords: ["antalya", "manavgat", "alanya", "serik", "kas", "kaş", "finike", "kumluca", "elmali", "elmalı", "korkuteli", "kemer", "demre"] },
    { slug: "ardahan", name: "Ardahan", region: "Doğu Anadolu", lat: 41.1105, lon: 42.7022, keywords: ["ardahan", "posof", "cildir", "çıldır", "gole", "göle", "hanak", "damal"] },
    { slug: "artvin", name: "Artvin", region: "Karadeniz", lat: 41.1828, lon: 41.8183, keywords: ["artvin", "hopa", "arhavi", "borcka", "borçka", "savsat", "şavşat", "ardanuc", "ardanuç", "yusufeli", "kemalpasa artvin", "kemalpaşa"] },
    { slug: "aydin", name: "Aydın", region: "Ege", lat: 37.8560, lon: 27.8416, keywords: ["aydin", "aydın", "soke", "söke", "nazilli", "kusadasi", "kuşadası", "didim", "germencik", "cine", "çine", "kocarli", "koçarlı"] },
    { slug: "balikesir", name: "Balıkesir", region: "Marmara", lat: 39.6484, lon: 27.8826, keywords: ["balikesir", "balıkesir", "bandirma", "bandırma", "edremit", "erdek", "ayvalik", "ayvalık", "gonen", "gönen", "sindirgi", "sındırgı", "bigadic", "bigadiç", "havran"] },
    { slug: "bartin", name: "Bartın", region: "Karadeniz", lat: 41.6344, lon: 32.3375, keywords: ["bartin", "bartın", "amasra", "ulus", "kurucasile", "kurucaşile"] },
    { slug: "batman", name: "Batman", region: "Güneydoğu Anadolu", lat: 37.8812, lon: 41.1351, keywords: ["batman", "kozluk", "sason", "sason batman", "besiri", "beşiri", "hasankeyf", "gercus", "gerçüş"] },
    { slug: "bayburt", name: "Bayburt", region: "Karadeniz", lat: 40.2552, lon: 40.2249, keywords: ["bayburt", "aydintepe", "aydıntepe", "demirozu", "demirözü"] },
    { slug: "bilecik", name: "Bilecik", region: "Marmara", lat: 40.1456, lon: 29.9793, keywords: ["bilecik", "bozuyuk", "bozüyük", "sogut", "söğüt", "golpazari", "gölpazarı", "osmaneli", "pazaryeri", "inhisar", "yenipazar bilecik"] },
    { slug: "bingol", name: "Bingöl", region: "Doğu Anadolu", lat: 38.8855, lon: 40.4966, keywords: ["bingol", "bingöl", "karliova", "karlıova", "genc bingol", "genç", "solhan", "kigi", "kiğı"] },
    { slug: "bitlis", name: "Bitlis", region: "Doğu Anadolu", lat: 38.4006, lon: 42.1095, keywords: ["bitlis", "tatvan", "ahlat", "adilcevaz", "mutki", "hizan", "guroymak", "güroymak"] },
    { slug: "bolu", name: "Bolu", region: "Karadeniz", lat: 40.7398, lon: 31.6110, keywords: ["bolu", "mudurnu", "gerede", "goynuk bolu", "göynük", "mengen", "seben", "yenicaga", "yeniçağa", "dortdivan", "dörtdivan"] },
    { slug: "burdur", name: "Burdur", region: "Akdeniz", lat: 37.7203, lon: 30.2908, keywords: ["burdur", "bucak", "tefenni", "golhisar", "gölhisar", "aglasun", "ağlasun"] },
    { slug: "bursa", name: "Bursa", region: "Marmara", lat: 40.1826, lon: 29.0665, keywords: ["bursa", "gemlik", "mudanya", "inegol", "inegöl", "orhangazi", "iznik", "yenisehir bursa", "yenişehir", "karacabey", "mustafakemalpasa", "mustafakemalpaşa", "osmangazi", "nilufer", "nilüfer", "yildirim", "yıldırım"] },
    { slug: "canakkale", name: "Çanakkale", region: "Marmara", lat: 40.1553, lon: 26.4142, keywords: ["canakkale", "çanakkale", "biga", "bayramic", "bayramiç", "ezine", "gelibolu", "ayvacik", "ayvacık", "yenice canakkale", "lapseki"] },
    { slug: "cankiri", name: "Çankırı", region: "İç Anadolu", lat: 40.6013, lon: 33.6134, keywords: ["cankiri", "çankırı", "cerkes", "çerkeş", "ilgaz", "korgun", "sabanozu", "şabanözü", "atkaracalar", "kizilirmak", "kızılırmak", "yapraklik", "yapraklı"] },
    { slug: "corum", name: "Çorum", region: "Karadeniz", lat: 40.5506, lon: 34.9556, keywords: ["corum", "çorum", "osmancik", "osmancık", "iskilip", "sungurlu", "alaca", "bayat corum", "mecitozu", "mecitözü", "ortakoy corum"] },
    { slug: "denizli", name: "Denizli", region: "Ege", lat: 37.7765, lon: 29.0864, keywords: ["denizli", "pamukkale", "saraykoy", "sarayköy", "buldan", "acipayam", "acıpayam", "tavas", "honaz", "civril", "çivril"] },
    { slug: "diyarbakir", name: "Diyarbakır", region: "Güneydoğu Anadolu", lat: 37.9144, lon: 40.2306, keywords: ["diyarbakir", "diyarbakır", "bismil", "cermik", "çermik", "cinar diyarbakir", "çınar", "ergani", "silvan", "kulp", "hazro"] },
    { slug: "duzce", name: "Düzce", region: "Karadeniz", lat: 40.8438, lon: 31.1565, keywords: ["duzce", "düzce", "akcakoca", "akçakoca", "kaynasli", "kaynaşlı", "yigilca", "yığılca", "golyaka", "gölyaka", "cumayeri", "cilimli", "çilimli"] },
    { slug: "edirne", name: "Edirne", region: "Marmara", lat: 41.6771, lon: 26.5557, keywords: ["edirne", "kesan", "keşan", "uzunkopru", "uzunköprü", "ipsala", "havsa", "enez", "lalapasa", "lalapaşa", "suloglu", "süloğlu", "meric", "meriç"] },
    { slug: "elazig", name: "Elazığ", region: "Doğu Anadolu", lat: 38.6810, lon: 39.2264, keywords: ["elazig", "elazığ", "karakocan", "karakoçan", "palu", "sivrice", "keban", "pertek", "maden", "kovancilar", "kovancılar"] },
    { slug: "erzincan", name: "Erzincan", region: "Doğu Anadolu", lat: 39.7500, lon: 39.5000, keywords: ["erzincan", "tercan", "cayirli", "çayırlı", "uzumlu", "üzümlü", "kemaliye", "refahiye"] },
    { slug: "erzurum", name: "Erzurum", region: "Doğu Anadolu", lat: 39.9055, lon: 41.2658, keywords: ["erzurum", "pasinler", "aziziye", "oltu", "horasan", "narman", "tortum", "ispir", "ispir erzurum"] },
    { slug: "eskisehir", name: "Eskişehir", region: "İç Anadolu", lat: 39.7767, lon: 30.5206, keywords: ["eskisehir", "eskişehir", "odunpazari", "odunpazarı", "tepebasi", "tepebaşı", "sivrihisar", "mahmudiye", "cifteler", "çifteler", "alpu", "beylikova", "inonu eskisehir", "inönü"] },
    { slug: "gaziantep", name: "Gaziantep", region: "Güneydoğu Anadolu", lat: 37.0660, lon: 37.3833, keywords: ["gaziantep", "antep", "nizip", "islahiye", "nurdagi", "nurdağı", "sahinbey", "şahinbey", "sehitkamil", "şehitkamil", "oguzeli", "oğuzeli"] },
    { slug: "giresun", name: "Giresun", region: "Karadeniz", lat: 40.9128, lon: 38.3895, keywords: ["giresun", "bulancak", "espiye", "tirebolu", "görele", "gorele", "dereli", "sebinkarahisar", "şebinkarahisar", "alucra"] },
    { slug: "gumushane", name: "Gümüşhane", region: "Karadeniz", lat: 40.4609, lon: 39.4814, keywords: ["gumushane", "gümüşhane", "kelkit", "siran", "şiran", "kose", "köse", "torul", "kurtun", "kürtün"] },
    { slug: "hakkari", name: "Hakkari", region: "Doğu Anadolu", lat: 37.5744, lon: 43.7408, keywords: ["hakkari", "yuksekova", "yüksekova", "semdinli", "şemdinli", "cukurca", "çukurca"] },
    { slug: "hatay", name: "Hatay", region: "Akdeniz", lat: 36.2025, lon: 36.1606, keywords: ["hatay", "antakya", "iskenderun", "samandag", "samandağ", "kirikhan", "kırıkhan", "reyhanli", "reyhanlı", "dortyol", "dörtyol", "belen", "erzin", "arsuz"] },
    { slug: "igdir", name: "Iğdır", region: "Doğu Anadolu", lat: 39.9237, lon: 44.0450, keywords: ["igdir", "ığdır", "aralik", "aralık", "tuzluca", "karakoyunlu"] },
    { slug: "isparta", name: "Isparta", region: "Akdeniz", lat: 37.7626, lon: 30.5537, keywords: ["isparta", "yalvac", "yalvaç", "egirdir", "eğirdir", "senirkent", "sutculer", "sütçüler", "keciborlu", "keçiborlu"] },
    { slug: "istanbul", name: "İstanbul", region: "Marmara", lat: 41.0082, lon: 28.9784, keywords: ["istanbul", "marmara", "marmara denizi", "silivri", "adalar", "yalova", "kocaeli", "cinarcik", "çınarcık", "bogaz", "boğaz", "besiktas", "beşiktaş", "kadikoy", "kadıköy", "bakirkoy", "bakırköy", "avcilar", "avcılar", "tuzla", "sariyer", "sarıyer", "pendik", "kartal", "maltepe", "tekirdag", "tekirdağ"] },
    { slug: "izmir", name: "İzmir", region: "Ege", lat: 38.4237, lon: 27.1428, keywords: ["izmir", "izmir korfezi", "izmir körfezi", "ege denizi", "seferihisar", "foca", "foça", "cesme", "çeşme", "urla", "manisa", "torbali", "torbalı", "gaziemir", "bayindir", "bayındır", "bornova", "karsiyaka", "karşıyaka", "menderes izmir"] },
    { slug: "kahramanmaras", name: "Kahramanmaraş", region: "Güneydoğu Anadolu", lat: 37.5753, lon: 36.9228, keywords: ["kahramanmaras", "kahramanmaraş", "maras", "maraş", "elbistan", "pazarcik", "pazarcık", "turkoglu", "türkoğlu", "nurdagi", "nurdağı", "afsin", "afşin", "goksun", "göksun", "osmaniye", "antep", "gaziantep", "hatay"] },
    { slug: "karabuk", name: "Karabük", region: "Karadeniz", lat: 41.2061, lon: 32.6204, keywords: ["karabuk", "karabük", "safranbolu", "eskipazar", "ovacik karabuk", "ovacık", "eflani", "yenice karabuk"] },
    { slug: "karaman", name: "Karaman", region: "İç Anadolu", lat: 37.1759, lon: 33.2287, keywords: ["karaman", "ermenek", "ayranci", "ayrancı", "kazimkarabekir", "kazımkarabekir", "sariveliler", "sarıveliler", "basyayla", "başyayla"] },
    { slug: "kars", name: "Kars", region: "Doğu Anadolu", lat: 40.6013, lon: 43.0975, keywords: ["kars", "sarikamis", "sarıkamış", "kagizman", "kağızman", "digor", "digör", "selim kars", "susuz", "arpacay", "arpaçay"] },
    { slug: "kastamonu", name: "Kastamonu", region: "Karadeniz", lat: 41.3887, lon: 33.7827, keywords: ["kastamonu", "tosya", "taskopru", "taşköprü", "cide", "inebolu", "bozkurt", "arac", "araç", "abana", "devrekani"] },
    { slug: "kayseri", name: "Kayseri", region: "İç Anadolu", lat: 38.7312, lon: 35.4787, keywords: ["kayseri", "bunyan", "bünyan", "develi", "incesu", "melikgazi", "kocasinan", "pinarbasi", "pınarbaşı", "sarioglan", "sarıoğlan", "yahyali", "yahyalı", "yesilhisar", "yeşilhisar", "tomarza"] },
    { slug: "kilis", name: "Kilis", region: "Güneydoğu Anadolu", lat: 36.7184, lon: 37.1212, keywords: ["kilis", "elbeyli", "musabeyli", "polateli"] },
    { slug: "kirikkale", name: "Kırıkkale", region: "İç Anadolu", lat: 39.8468, lon: 33.5153, keywords: ["kirikkale", "kırıkkale", "keskin", "delice", "sulakyurt", "baliseyh", "balışeyh", "karakecili", "karakeçili", "yahsihan", "yahşihan"] },
    { slug: "kirklareli", name: "Kırklareli", region: "Marmara", lat: 41.7351, lon: 27.2246, keywords: ["kirklareli", "kırklareli", "luleburgaz", "lüleburgaz", "babaeski", "pinarhisar", "pınarhisar", "vize", "demirkoy", "demirköy", "pehlivankoy", "pehlivanköy", "kofcaz", "kofçaz"] },
    { slug: "kirsehir", name: "Kırşehir", region: "İç Anadolu", lat: 39.1425, lon: 34.1709, keywords: ["kirsehir", "kırşehir", "kaman", "mucur", "akpinar", "akpınar", "akcakent", "akçakent", "cicekdagi", "çiçekdağı", "boztepe"] },
    { slug: "kocaeli", name: "Kocaeli", region: "Marmara", lat: 40.8533, lon: 29.8815, keywords: ["kocaeli", "izmit", "gebze", "derince", "korfez", "körfez", "golcuk", "gölcük", "karamursel", "karamürsel", "dilovasi", "dilovası", "kandira", "kandıra", "basiskele", "başiskele", "darica", "darıca", "cayirova", "çayırova"] },
    { slug: "konya", name: "Konya", region: "İç Anadolu", lat: 37.8714, lon: 32.4846, keywords: ["konya", "aksehir", "akşehir", "beysehir", "beyşehir", "cumra", "çumra", "eregli konya", "ereğli", "ilgin", "ilgın", "karatay", "meram", "seydisehir", "seydişehir", "selcuklu", "selçuklu", "kulu", "bozkir", "bozkır"] },
    { slug: "kutahya", name: "Kütahya", region: "Ege", lat: 39.4167, lon: 29.9833, keywords: ["kutahya", "kütahya", "tavsanli", "tavşanlı", "gediz", "simav", "emet", "hisarcik", "hisarcık", "domanic", "domaniç"] },
    { slug: "malatya", name: "Malatya", region: "Doğu Anadolu", lat: 38.3552, lon: 38.3095, keywords: ["malatya", "battalgazi", "yesilyurt", "yeşilyurt", "dogansehir", "doğanşehir", "puturge", "pütürge", "akcadag", "akçadağ", "hekimhan", "darende"] },
    { slug: "manisa", name: "Manisa", region: "Ege", lat: 38.6191, lon: 27.4289, keywords: ["manisa", "akhisar", "salihli", "turgutlu", "saruhanli", "saruhanlı", "soma", "demirci", "kula", "golmarmara", "gölmarmara", "alasehir", "alaşehir"] },
    { slug: "mardin", name: "Mardin", region: "Güneydoğu Anadolu", lat: 37.3120, lon: 40.7350, keywords: ["mardin", "kiziltepe", "kızıltepe", "midyat", "nusaybin", "derik", "savur", "mazidagi", "mazıdağı"] },
    { slug: "mersin", name: "Mersin", region: "Akdeniz", lat: 36.8121, lon: 34.6415, keywords: ["mersin", "tarsus", "erdemli", "silifke", "anamur", "bozyazi", "bozyazı", "mut", "gulnar", "gülnar", "icel", "içel"] },
    { slug: "mugla", name: "Muğla", region: "Ege", lat: 37.2153, lon: 28.3636, keywords: ["mugla", "muğla", "bodrum", "marmaris", "fethiye", "milas", "dalaman", "koycegiz", "köyceğiz", "datca", "datça", "ula", "seydikemer"] },
    { slug: "mus", name: "Muş", region: "Doğu Anadolu", lat: 38.7432, lon: 41.5060, keywords: ["mus", "muş", "bulanik", "bulanık", "malazgirt", "varto", "korkut", "haskoy", "hasköy"] },
    { slug: "nevsehir", name: "Nevşehir", region: "İç Anadolu", lat: 38.6939, lon: 34.6857, keywords: ["nevsehir", "nevşehir", "urgup", "ürgüp", "avanos", "derinkuyu", "kozakli", "kozaklı", "acigol", "acıgöl", "hacibektas", "hacıbektaş", "gulsehir", "gülşehir"] },
    { slug: "nigde", name: "Niğde", region: "İç Anadolu", lat: 37.9667, lon: 34.6833, keywords: ["nigde", "niğde", "bor nigde", "camardi", "çamardı", "ulukisla", "ulukışla", "altunhisar", "ciftlik", "çiftlik"] },
    { slug: "ordu", name: "Ordu", region: "Karadeniz", lat: 40.9839, lon: 37.8764, keywords: ["ordu", "unye", "ünye", "fatsa", "persembe", "perşembe", "korgan", "kumru", "mesudiye", "ulubey ordu", "aybasti", "aybastı"] },
    { slug: "osmaniye", name: "Osmaniye", region: "Akdeniz", lat: 37.2130, lon: 36.1763, keywords: ["osmaniye", "kadirli", "duzici", "düziçi", "bahce osmaniye", "bahçe", "toprakkale"] },
    { slug: "rize", name: "Rize", region: "Karadeniz", lat: 41.0201, lon: 40.5234, keywords: ["rize", "ardesen", "ardeşen", "cayeli", "çayeli", "pazar rize", "findikli", "fındıklı", "ikizdere", "camlihemsin", "çamlıhemşin", "guneysu", "güneysu"] },
    { slug: "sakarya", name: "Sakarya", region: "Marmara", lat: 40.7889, lon: 30.4060, keywords: ["sakarya", "adapazari", "adapazarı", "akyazi", "akyazı", "hendek", "karasu", "geyve", "pamukova", "sapanca", "ferizli", "karapurcek", "karapürçek", "kaynarca"] },
    { slug: "samsun", name: "Samsun", region: "Karadeniz", lat: 41.2867, lon: 36.3300, keywords: ["samsun", "bafra", "carsamba samsun", "çarşamba", "vezirkopru", "vezirköprü", "havza", "terme", "ladik", "19 mayis", "ayvacik samsun", "alacam", "alaçam"] },
    { slug: "sanliurfa", name: "Şanlıurfa", region: "Güneydoğu Anadolu", lat: 37.1591, lon: 38.7969, keywords: ["sanliurfa", "şanlıurfa", "urfa", "siverek", "birecik", "viransehir", "viranşehir", "suruc", "suruç", "harran", "akcakale", "akçakale", "bozova", "halfeti"] },
    { slug: "siirt", name: "Siirt", region: "Güneydoğu Anadolu", lat: 37.9333, lon: 41.9500, keywords: ["siirt", "pervari", "eruh", "kurtalan", "baykan", "sirvan", "şirvan", "tillo"] },
    { slug: "sinop", name: "Sinop", region: "Karadeniz", lat: 42.0265, lon: 35.1550, keywords: ["sinop", "boyabat", "gerze", "ayancik", "ayancık", "turkeli", "türkeli", "dikmen", "erfelek", "duragan", "durağan", "saraydüzü", "saraydonu"] },
    { slug: "sirnak", name: "Şırnak", region: "Güneydoğu Anadolu", lat: 37.4187, lon: 42.4918, keywords: ["sirnak", "şırnak", "cizre", "silopi", "idil", "uludere", "beytussebap", "beytüşşebap", "guclukonak", "güçlükonak"] },
    { slug: "sivas", name: "Sivas", region: "İç Anadolu", lat: 39.7477, lon: 37.0179, keywords: ["sivas", "kangal", "divrigi", "divriği", "susehri", "suşehri", "zara", "gurun", "gürün", "hafik", "yildizeli", "yıldızeli", "imranli", "imranlı"] },
    { slug: "tekirdag", name: "Tekirdağ", region: "Marmara", lat: 40.9780, lon: 27.5110, keywords: ["tekirdag", "tekirdağ", "corlu", "çorlu", "cerkezkoy", "çerkezköy", "malkara", "saray tekirdag", "muratli", "muratlı", "hayrabolu", "kapakli", "kapaklı", "suleymanpasa", "süleymanpaşa", "marmara ereglisi"] },
    { slug: "tokat", name: "Tokat", region: "Karadeniz", lat: 40.3167, lon: 36.5500, keywords: ["tokat", "niksar", "erbaa", "turhal", "zile", "resadiye", "reşadiye", "almus", "artova"] },
    { slug: "trabzon", name: "Trabzon", region: "Karadeniz", lat: 41.0015, lon: 39.7178, keywords: ["trabzon", "akcaabat", "akçaabat", "arakli", "araklı", "yomra", "of trabzon", "vakfikebir", "macka", "maçka", "surmene", "sürmene", "besikduzu", "beşikdüzü"] },
    { slug: "tunceli", name: "Tunceli", region: "Doğu Anadolu", lat: 39.1079, lon: 39.5401, keywords: ["tunceli", "pertek", "mazgirt", "ovacik tunceli", "ovacık", "cemisgezek", "çemişgezek", "pulumur", "pülümür", "hozat", "nazimiye", "nazımiye"] },
    { slug: "usak", name: "Uşak", region: "Ege", lat: 38.6823, lon: 29.4082, keywords: ["usak", "uşak", "banaz", "esme", "eşme", "sivasli", "sivaslı", "karahalli", "karahallı", "ulubey usak", "ulubey"] },
    { slug: "van", name: "Van", region: "Doğu Anadolu", lat: 38.4942, lon: 43.3833, keywords: ["van", "ercis", "erciş", "edremit van", "ipekyolu", "tusba", "tuşba", "ozalp", "özalp", "muradiye", "baskale", "başkale", "gevas", "gevaş"] },
    { slug: "yalova", name: "Yalova", region: "Marmara", lat: 40.6500, lon: 29.2667, keywords: ["yalova", "cinarcik", "çınarcık", "termal", "altinova", "altınova", "armutlu", "cifltikkoy", "çiftlikköy"] },
    { slug: "yozgat", name: "Yozgat", region: "İç Anadolu", lat: 39.8181, lon: 34.8147, keywords: ["yozgat", "sorgun", "akdagmadeni", "akdağmadeni", "bogazliyan", "boğazlıyan", "sarikaya", "sarıkaya", "yerkoy", "yerköy", "cekerek", "çekerek", "kadisehri", "kadışehri"] },
    { slug: "zonguldak", name: "Zonguldak", region: "Karadeniz", lat: 41.4564, lon: 31.7987, keywords: ["zonguldak", "eregli zonguldak", "ereğli", "karadeniz eregli", "caycuma", "çaycuma", "devrek", "alapli", "alaplı", "kilimli", "kozlu", "gokcebey", "gökçebey"] }
  ];

  const cityKeywords = {};
  cityData.forEach((c) => {
    cityKeywords[c.slug] = c.keywords;
  });

  // Eski takma adlar (onceki surumle uyumluluk)
  const aliasMap = {
    "elazığ": "elazig",
    "kahramanmaraş": "kahramanmaras"
  };
  Object.keys(aliasMap).forEach((alias) => {
    const canonical = aliasMap[alias];
    cityKeywords[alias] = cityKeywords[canonical] || [];
  });

  window.CityKeywords = cityKeywords;
  window.CityData = cityData; // index.html arama kutusu icin
})();
