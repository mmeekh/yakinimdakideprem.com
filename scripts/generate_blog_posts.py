#!/usr/bin/env python3
"""
23 yeni deprem blog yazisi uretici.
Her blog: SEO-optimize title, meta, FAQ schema (3-4 soru), cross-link, ~700 kelime.
"""
from __future__ import annotations
import json
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "public"
TODAY = "2026-04-20"

# Blog entries: slug -> full data
BLOGS = [
    # --- Group A: High-volume evergreen ---
    {
        "slug": "blog-turkiye-fay-hatlari-haritasi",
        "title": "Türkiye Fay Hatları Haritası 2026 – KAF, DAF ve BAF",
        "desc": "Türkiye'nin üç büyük fay hattı (Kuzey, Doğu ve Batı Anadolu) nerede geçer? Hangi iller risk altında? 2026 güncel fay hattı haritası ve bilimsel veriler.",
        "keywords": "türkiye fay hatları, kuzey anadolu fay hattı, doğu anadolu fay hattı, fay haritası, KAF DAF BAF",
        "hero_img": "blog-turkiye-fay-hatlari-haritasi.webp",
        "lead": "Türkiye'nin jeolojik yapısı üç büyük fay hattı tarafından şekillendiriliyor. Bu üç hat — Kuzey Anadolu Fay Hattı (KAF), Doğu Anadolu Fay Hattı (DAF) ve Batı Anadolu Fay Hattı (BAF) — ülkenin %95'ini aktif deprem kuşağına çeviriyor.",
        "sections": [
            ("Kuzey Anadolu Fay Hattı (KAF)", "1.200 km uzunluğundaki KAF, Türkiye'nin en uzun ve en aktif fay hattıdır. Bingöl'den başlayıp Gemlik Körfezi'ne kadar uzanır. 1939 Erzincan, 1999 Gölcük ve 1999 Düzce depremleri bu hat üzerinde gerçekleşmiştir. Marmara Denizi altındaki kolu, olası İstanbul depremi senaryosunun ana odağıdır. İstanbul, Kocaeli, Sakarya, Bolu, Amasya, Tokat, Erzincan — hepsi bu hattın etki alanındadır."),
            ("Doğu Anadolu Fay Hattı (DAF)", "580 km uzunluğunda, Karlıova'dan (Bingöl) Antakya'ya uzanan DAF, 2023 Kahramanmaraş depremleri (Mw 7.8 ve 7.6) ile tarihsel olarak en büyük yıkımı yaşayan hattır. Hatay, Kahramanmaraş, Malatya, Adıyaman, Gaziantep ve Elazığ bu hattın yakınındadır. DAF, KAF ile Karlıova'da birleşir — Türkiye'nin en riskli jeolojik noktası burasıdır."),
            ("Batı Anadolu Fay Hattı (BAF) ve Ege Grabenleri", "BAF, tek bir hat olmak yerine birçok paralel grabenler (çöküntü) sistemidir. Gediz, Büyük Menderes ve Küçük Menderes grabenleri bu sisteme dahildir. İzmir, Aydın, Manisa, Denizli, Muğla, Uşak, Balıkesir — Ege'nin neredeyse tüm illeri bu yapı içindedir. 2020 İzmir-Samos depremi bu hatların aktivitesini hatırlattı."),
            ("Sizin Şehriniz Hangi Fay Hattına Yakın?", "Bizim sitemizde 81 il için ayrı ayrı fay hattı risk profilini hazırladık. <a href=\"/deprem-sehirleri.html\">Tüm şehirlerin deprem sayfasına</a> girerek şehrinizin jeolojik durumunu öğrenebilirsiniz. Risk seviyesi \"Çok yüksek\" olan illerde yaşıyorsanız DASK, <a href=\"/blog-deprem-oncesi-hazirlik.html\">deprem öncesi hazırlık</a> ve <a href=\"/blog-deprem-cantasi.html\">deprem çantası</a> bir seçenek değil, zorunluluktur."),
        ],
        "faq": [
            ("En tehlikeli fay hattı hangisi?", "Kuzey Anadolu Fay Hattı'nın Marmara segmenti ve Doğu Anadolu Fay Hattı'nın Kahramanmaraş segmenti şu anda en yüksek gerilim altındadır. Her iki hat da tarihsel olarak Mw 7.0+ depremler üretmiştir."),
            ("İstanbul depremi ne zaman bekleniyor?", "Bilim insanları 2050'den önce Marmara segmenti üzerinde Mw 7.0-7.5 arası bir deprem olasılığını %64 olarak hesaplamaktadır (2019 BU araştırması). Kesin tarih vermek mümkün değildir."),
            ("Fay hattı üzerinde yaşamak güvenli mi?", "Fay hattına 1 km'den yakın yerlerde yapılaşma yasal olarak yasaktır. Daha uzak alanlarda yapı kalitesi ve zemin güvenliği belirleyici faktördür."),
        ],
    },
    {
        "slug": "blog-evim-depreme-dayanikli-mi",
        "title": "Evim Depreme Dayanıklı mı? 7 Adımlık Test",
        "desc": "Oturduğunuz evin deprem dayanıklılığını nasıl değerlendirirsiniz? Çatlaklar, kolon yapısı, yapım yılı ve daha fazlası için 7 adımlık kontrol listesi.",
        "keywords": "evim depreme dayanıklı mı, bina deprem testi, deprem dayanıklılık, yapı güvenliği, bina kontrol",
        "hero_img": "blog-evim-depreme-dayanikli-mi.webp",
        "lead": "2023 Kahramanmaraş depremleri, Türkiye'deki bina stokunun ciddi bir kısmının deprem yönetmeliklerini karşılamadığını gösterdi. Peki siz oturduğunuz evin deprem dayanıklılığını nasıl anlarsınız? İşte profesyonel inceleme öncesi yapabileceğiniz 7 adımlık hızlı kontrol listesi.",
        "sections": [
            ("1. Yapım Yılını Kontrol Edin", "Binanızın yapım yılı, deprem yönetmeliği uyumunu belirleyen en kritik faktördür. <strong>1999 öncesi binalar</strong>: eski yönetmelikle yapılmış, risk yüksek. <strong>1999-2007 arası</strong>: 1998 yönetmeliği, orta düzey güvenlik. <strong>2007-2018 arası</strong>: 2007 yönetmeliği, iyi güvenlik. <strong>2019 sonrası</strong>: TBDY 2019, en güncel standartlarla yapılmış. Tapunuzda yapım yılı yazar veya belediyeden öğrenebilirsiniz."),
            ("2. Kolon-Duvar İlişkisini İnceleyin", "Taşıyıcı kolonlar binanızın iskeletidir. Kolonlarda <strong>X şeklinde çatlak</strong> görüyorsanız yapısal hasar var demektir. Acil statik rapor gerekli. Kolonların altı/üstü yıkılmış, sıva dökülmüş yerler varsa uzman çağırın. Bina plan görseline bakın — asimetrik kolonlar, ince kolonlar veya yumuşak katlar (ince zemin kat + kalın üst katlar) risk taşır."),
            ("3. Temel ve Zemin Bilgisini Öğrenin", "Binanızın üzerinde oturduğu zemin, yapım malzemesinden daha önemlidir. <strong>Alüvyon (çakıl, kum, kil)</strong> zeminler deprem dalgalarını güçlendirir. <strong>Kaya zemini</strong> en güvenlidir. Belediyenin jeolojik-jeoteknik etüt raporundan veya imar planından öğrenebilirsiniz. Deniz, dere yatağı veya dolgu alanda inşa edilmiş binalar özel dikkat gerektirir."),
            ("4. Yapısal Çatlaklara Bakın", "Tüm çatlaklar aynı değildir. <strong>Sıva çatlakları</strong> (ince, boya altındaki) zararsızdır. <strong>Kolon, kiriş ve taşıyıcı duvarlardaki çatlaklar</strong> — özellikle diagonal (eğik) veya X şekilli — yapısal sorunun işareti olabilir. Eğer bir çatlak binanın bir ucundan diğerine uzanıyorsa hemen uzman görüşü alın."),
            ("5. Güçlendirme Projesi Var mı?", "Binanız kentsel dönüşüm kapsamına giriyor mu veya geçmişte güçlendirme yapılmış mı? Belediyeden güçlendirme raporu isteyin. Güçlendirilmiş binalar <strong>mantolama, karbon fiber şerit, çelik kuşak</strong> gibi tekniklerle desteklenmiş olur. Görsel olarak kontrol edin: kolon etrafında çelik sargı veya kalın karbon şerit var mı?"),
            ("6. Bina Kimlik Bilgisi ve İskan Ruhsatı", "Binanızın <strong>iskan ruhsatı</strong> (yapı kullanım izni) var mı? Yoksa bu, binanın yasal inşaat denetimini tamamlamadığı anlamına gelir — deprem güvenliği ciddi soru işaretidir. Tapuda binanın yapım yılı ile iskan yılı örtüşmüyorsa (örneğin 2010 yapımı ama 2020 iskan) ek bir güvenlik sorunu olabilir."),
            ("7. Profesyonel Risk Analizi Yaptırın", "Yukarıdaki 6 adım ön kontroldür. Kesin cevap için <strong>Lisanslı Yapı Denetim Firmasına</strong> performans analizi yaptırın. Maliyet 3.000-15.000 TL arasındadır ama can güvenliğini %100 netleştirir. Kentsel dönüşüm yasası kapsamında riskli bina raporu alırsanız devlet desteği ile güçlendirme veya yıkım hakkınız doğar."),
        ],
        "faq": [
            ("Binamın depreme dayanıklılığını ücretsiz öğrenebilir miyim?", "Belediyelerin imar ve şehircilik müdürlükleri bazı ilçelerde ücretsiz ön değerlendirme yapmaktadır. AFAD'ın e-Devlet hizmetlerinden risk yapısına yakınlık sorgulanabilir. Detaylı analiz için özel yapı denetim firmaları ücretlidir."),
            ("Bina güçlendirme maliyeti nedir?", "2026 fiyatlarıyla 80-120 m² bir dairenin bulunduğu bina için güçlendirme 200.000-800.000 TL arasında değişir. Mantolama yalnızca enerji tasarrufu sağlar; taşıyıcı güçlendirme farklı bir iştir."),
            ("Riskli bina raporu çıkarsa ne olur?", "Kentsel Dönüşüm Yasası kapsamında 6306 sayılı kanun gereği 60 gün içinde bina boşaltılır. Devlet, kiracılara taşınma yardımı verir. Mülk sahipleri ya yıkıp yeniden yapar ya da müteahhite verirler."),
        ],
    },
    {
        "slug": "blog-istanbul-beklenen-deprem",
        "title": "İstanbul Beklenen Deprem Ne Zaman? Bilim İnsanları Ne Diyor?",
        "desc": "İstanbul'da beklenen büyük deprem için bilim insanlarının tahminleri, olasılık hesapları ve hazırlık önerileri. 2019-2026 araştırmalarının özeti.",
        "keywords": "istanbul beklenen deprem, istanbul depremi ne zaman, marmara depremi, KAF istanbul, beklenen büyük deprem",
        "hero_img": "blog-istanbul-beklenen-deprem.webp",
        "lead": "\"İstanbul depremi ne zaman olacak?\" sorusu son 25 yılın en çok aranan bilim sorularından biri. Kandilli Rasathanesi, Boğaziçi Üniversitesi ve TÜBİTAK'ın çalışmaları bu konuda bazı net cevaplar veriyor. İşte bilimsel veriler ışığında İstanbul depremi hakkında bilinenler.",
        "sections": [
            ("Marmara Fay Segmentinin Durumu", "Kuzey Anadolu Fay Hattı 1939'dan bu yana sistematik olarak batıya ilerledi: 1939 Erzincan, 1943 Ladik, 1944 Bolu, 1957 Abant, 1967 Adapazarı, 1999 Gölcük-Düzce. Bu zincirde <strong>tek eksik segment Marmara Denizi altındaki Kuzey Marmara Fayı'dır</strong>. Gerilim 260+ yıldır birikiyor — son büyük sarsıntı 1766 yılında oldu."),
            ("2019 Boğaziçi Araştırması — %64 Olasılık", "Boğaziçi Üniversitesi Kandilli Rasathanesi 2019'da yayınladığı çalışmada: 2050 yılına kadar Marmara segmentinde Mw 7.0 ve üzeri deprem olasılığını <strong>%64</strong> olarak hesapladı. Bu, bilim dünyasında en yüksek uzlaşı rakamıdır. Kesin bir tarih vermek imkansızdır — fay hatları saat değil, yaylar gibi çalışır."),
            ("Büyüklük Tahmini: Mw 7.0-7.6", "İstanbul depreminin büyüklüğü hakkında tahminler Mw 7.0 ile 7.6 arasında değişir. <strong>Mw 7.2</strong> senaryosuna göre: 70.000-90.000 ölü, 700.000 bina hasarı, 300 milyar TL ekonomik kayıp bekleniyor (AFAD 2024 senaryosu). Sarsıntı süresi 30-45 saniye arası olacak."),
            ("Hangi İstanbul İlçeleri En Riskli?", "<strong>Avcılar, Küçükçekmece, Bakırköy, Zeytinburnu, Fatih</strong> — deniz kıyısı + alüvyon zemin + eski bina stoku ile en riskli ilçelerdir. <strong>Ümraniye, Sarıyer, Beykoz'un sert zeminleri</strong> görece daha güvenlidir. <a href=\"/deprem-istanbul.html\">İstanbul deprem sayfamızda</a> detaylı ilçe bazında risk haritası var."),
            ("Ne Yapmalıyım?", "Belirsizlik bilmezlikle aynı şey değildir. Yapmanız gerekenler: <strong>1.</strong> Binanızın depreme dayanıklılığını test ettirin (<a href=\"/blog-evim-depreme-dayanikli-mi.html\">bu rehberimize bakın</a>). <strong>2.</strong> DASK yaptırın (<a href=\"/blog-dask-nedir.html\">DASK rehberi</a>). <strong>3.</strong> Deprem çantası hazırlayın. <strong>4.</strong> Aile toplanma planı oluşturun. <strong>5.</strong> <a href=\"/\">Anlık deprem takip sitemizi</a> kaydedin, büyük bir deprem olduğunda anında bildirim alın."),
        ],
        "faq": [
            ("İstanbul depremi 9 şiddetinde mi olacak?", "Bilim insanları Mw 7.0-7.6 arası bir büyüklük bekliyor. Bu, şiddet ölçeğinde MMI VIII-IX (Mercalli) düzeyine denk gelir — yani çok şiddetli hasar yaratan bir deprem."),
            ("Deprem kaç saniye sürecek?", "Fay segmentinin kırılma süresi 20-45 saniye arasında olacak. Sarsıntı tam İstanbul'da 30-60 saniye arası hissedilecek."),
            ("Taşınmalı mıyım?", "Deprem sadece İstanbul'u değil Türkiye'nin %95'ini etkileyen bir risk. Taşınma yerine <strong>dayanıklı bir binaya geçmek</strong> veya mevcut binayı güçlendirmek mantıklı çözümdür."),
        ],
    },
    {
        "slug": "blog-deprem-buyukluk-olcekleri",
        "title": "Deprem Büyüklük Ölçekleri: Richter, Moment ve MMI Farkı",
        "desc": "Deprem büyüklük ölçekleri nelerdir? Richter ve Moment (Mw) büyüklüğü arasındaki fark, MMI şiddet ölçeği ve hasar tahminleri hakkında detaylı rehber.",
        "keywords": "deprem büyüklük ölçekleri, richter ölçeği, moment büyüklüğü, MMI, deprem şiddeti",
        "hero_img": "blog-deprem-buyukluk-olcekleri.webp",
        "lead": "Haberlerde \"Mw 5.2 büyüklüğünde deprem\" ifadesini duyduğunuzda bu tam olarak ne anlama geliyor? Deprem ölçekleri karmaşık görünebilir ama aslında üç temel ölçek yeterli: Richter, Moment Büyüklüğü (Mw) ve MMI (Modifiye Mercalli Şiddet).",
        "sections": [
            ("Richter Ölçeği (ML) — Klasik", "1935'te Charles Richter tarafından geliştirildi. Sismograf'taki dalga genliğini logaritmik ölçekle ölçer. Her basamak artışı <strong>10 kat büyüklük, 32 kat enerji</strong> farkı yaratır. Yani Mw 6.0 bir deprem, Mw 5.0'dan 32 kat daha güçlüdür. Richter küçük-orta büyüklükteki yerel depremlerde kullanılır (Mw <6.5). Büyük depremleri olduğundan düşük gösterir."),
            ("Moment Büyüklüğü (Mw) — Modern Standart", "1970'lerde geliştirilen Mw, depremin toplam enerjisini fay yüzey alanı × yer değiştirme × sertlik formülüyle hesaplar. Richter'in aksine <strong>büyük depremlerde doygunluk yaşamaz</strong>. 1960 Şili Mw 9.5 ve 2004 Sumatra Mw 9.1 gibi devasa depremler ancak Mw ile ölçülebilir. <strong>Günümüzde AFAD ve Kandilli artık Mw kullanır</strong>. Medyada \"Richter\" denmesi eski alışkanlıktır."),
            ("MMI Şiddet Ölçeği — Hasar Bazlı", "MMI (Modifiye Mercalli), bir depremin belirli bir lokasyonda yarattığı <strong>hasarı ve hissi</strong> ölçer. Romen rakamı ile I-XII arasında gösterilir: <strong>I:</strong> hissedilmez, <strong>III:</strong> az hissedilir, <strong>V:</strong> herkes hisseder, <strong>VII:</strong> duvar çatlakları, <strong>IX:</strong> binalar yıkılır, <strong>X-XII:</strong> total yıkım. Aynı deprem, merkezine yakın yerde MMI IX, uzakta III hissedilebilir."),
            ("Büyüklük vs Şiddet — Fark Ne?", "Bu ikisi karıştırılır. <strong>Büyüklük</strong> (Richter, Mw) depremin salınan enerjisidir — sabit bir değer. <strong>Şiddet</strong> (MMI) ise belirli bir lokasyondaki etkidir — konuma göre değişir. Mw 6.5 bir deprem, merkezde MMI VIII hasar yaratır ama 100 km uzakta MMI V hissedilir. Medya genelde ikisini karıştırır: \"6 şiddetinde deprem\" ifadesi teknik olarak yanlıştır, doğru ifade \"Mw 6.0 büyüklüğünde\"dır."),
            ("Büyüklük Ne Kadar Hasar Yaratır?", "<strong>Mw <3.0:</strong> Mikro deprem, hissedilmez. <strong>Mw 3.0-3.9:</strong> Zayıf. <strong>Mw 4.0-4.9:</strong> Orta. <strong>Mw 5.0-5.9:</strong> Kuvvetli — hasarsız ama yaygın korku. <strong>Mw 6.0-6.9:</strong> Güçlü — eski binalar yıkılabilir. <strong>Mw 7.0-7.9:</strong> Büyük — önemli yıkım (1999 Gölcük Mw 7.6). <strong>Mw 8.0+:</strong> Devasa — bölgesel yıkım. <strong>Mw 9.0+:</strong> Dünya çapında tsunami (2011 Tohoku)."),
        ],
        "faq": [
            ("Neden haberlerde farklı büyüklük duyuyoruz?", "İlk açıklama genelde Mw olur ancak bazı istasyonlar Richter (ML) veya yerel büyüklük (MD) gösterir. Final değer 10-20 dakika içinde Mw olarak güncellenir."),
            ("5 büyüklüğündeki deprem tehlikeli mi?", "Mw 5.0-5.9 depremler nadiren yıkım yaratır. Eski yapılar zarar görebilir ama modern binalar için tehlike minimumdur. Mw 6.0+ ciddi risk demektir."),
            ("Bir depremin büyüklüğünü kim ve nasıl ölçer?", "Türkiye'de Kandilli Rasathanesi ve AFAD'ın sismograf ağı 700+ istasyondan gelen veriyi birleştirir. Büyüklük hesabı 2-5 dakikada otomatik yapılır."),
        ],
    },
    {
        "slug": "blog-artci-deprem-nedir",
        "title": "Artçı Deprem Nedir? Ne Kadar Sürer, Zararı Olur mu?",
        "desc": "Artçı deprem nedir, neden olur, ne kadar sürer? Ana depremden sonra gelen artçıların büyüklüğü, süresi ve güvenlik önerileri hakkında detaylı rehber.",
        "keywords": "artçı deprem nedir, artçı ne kadar sürer, artçıların büyüklüğü, deprem sonrası artçı",
        "hero_img": "blog-artci-deprem-nedir.webp",
        "lead": "Büyük bir deprem sonrası birçok daha küçük sarsıntı hissederiz. Bunlar rastgele değil — bilimsel olarak \"artçı deprem\" denilen jeolojik bir süreçtir. Peki artçılar ne kadar sürer ve ne kadar tehlikeli?",
        "sections": [
            ("Artçı Deprem Nasıl Oluşur?", "Ana deprem sırasında fay hattı boyunca büyük bir yer değiştirme olur. Ancak <strong>fay üzerindeki gerilim tek seferde tamamen boşalmaz</strong> — küçük bölgelerde gerilim kalır. Bu bölgelerdeki kırılmalar artçılardır. Her ana deprem, kendi artçı dizisini üretir — bu \"Omori yasası\" olarak bilinen bilimsel bir kuralla açıklanır."),
            ("Artçılar Ne Kadar Sürer?", "Omori yasasına göre artçı sayısı ana depremden sonra üssel olarak azalır. Pratik olarak:<br><strong>İlk 24 saat:</strong> onlarca artçı (yüzlerce küçük), büyüklük ana depremin 1 derece altında olabilir.<br><strong>İlk hafta:</strong> artçı sayısı günlük olarak azalır.<br><strong>İlk ay:</strong> önemli artçılar devam eder.<br><strong>6 ay – 2 yıl:</strong> aralıklı artçılar. 2023 Kahramanmaraş depremlerinin artçıları 2 yıl sonra bile devam ediyor."),
            ("Artçıların Büyüklüğü", "Kural olarak en büyük artçı, ana depremin 1 büyüklük altındadır (Båth yasası). Yani Mw 7.5 bir ana depremden sonra en büyük artçı yaklaşık Mw 6.5 olur. Ancak çok nadiren artçı, ana depremden daha büyük olabilir — bu durumda terminoloji değişir: ilk sarsıntı \"öncü\", sonraki \"ana\" olur. 2023'te 6 Şubat sabah 04:17'deki Mw 7.8 depremden sonra aynı gün öğlen Mw 7.6 ile ikinci bir ana deprem geldi — nadir bir örnektir."),
            ("Artçılar Neden Tehlikeli?", "Artçılar kendileri genelde yıkıcı değildir ama <strong>zaten hasarlı binaları</strong> yıkabilir. Bir Mw 7.0 ana depremden sonra gelen Mw 5.5 artçı, ana depremde hasar alan 100-200 binayı yere serer. Bu yüzden deprem uzmanları \"artçı biten kadar binaya girmeyin\" uyarısı yapar."),
            ("Artçılardan Nasıl Korunulur?", "<strong>1.</strong> Ana deprem bittikten sonra 72 saat boyunca güvenli açık alanda kalın. <strong>2.</strong> <a href=\"/deprem-sehirleri.html\">Şehrinizin deprem aktivite takibini</a> canlı yapın. <strong>3.</strong> Hasarlı binalara kesinlikle girmeyin. <strong>4.</strong> Artçılar sırasında <a href=\"/deprem-aninda.html\">çök-kapan-tutun</a> pozisyonuna geçin. <strong>5.</strong> Gaz, elektrik ve suyu kapalı tutun — artçı sırasında patlama riski yüksek."),
        ],
        "faq": [
            ("Artçılar aylarca sürer mi?", "Evet. Büyük (Mw 7.0+) bir ana depremin ardından 6-24 ay arası artçı aktivitesi gözlemlenir. 2023 Maraş depreminin artçıları 2026'da bile devam ediyor."),
            ("Artçı olmayan deprem olur mu?", "Küçük (Mw <5.0) depremlerde artçı olmayabilir veya çok az olur. Büyük depremlerde kesinlikle artçı olur."),
            ("Artçılar tahmin edilebilir mi?", "Sayısı ve ortalama büyüklüğü Omori ve Båth yasalarıyla tahmin edilir. Ancak <strong>bireysel bir artçının tam zamanı</strong> tahmin edilemez."),
        ],
    },
    {
        "slug": "blog-deprem-erken-uyari-sistemi",
        "title": "Deprem Erken Uyarı Sistemi Nasıl Çalışır?",
        "desc": "Deprem erken uyarı sistemi nedir, nasıl çalışır, Türkiye'de var mı? AFAD, ShakeAlert ve Japon sistemlerinin karşılaştırması.",
        "keywords": "deprem erken uyarı sistemi, EEW, AFAD uyarı, deprem bildirim, shakealert",
        "hero_img": "blog-deprem-erken-uyari-sistemi.webp",
        "lead": "Bir deprem olduktan saniyeler önce uyarı almak mümkün mü? Evet, deprem erken uyarı sistemleri (EEW - Earthquake Early Warning) son 20 yıldır hayat kurtarıyor. Peki nasıl çalışıyor ve Türkiye'de uygulanıyor mu?",
        "sections": [
            ("Sistemin Mantığı: P ve S Dalgaları", "Bir deprem oluştuğunda iki tür sismik dalga yayılır. <strong>P dalgası (Primer)</strong> ışık hızından yavaş ama saniyede 6 km ilerler, hasar yapmaz. <strong>S dalgası (Sekonder)</strong> 3.5 km/sn ilerler, asıl yıkıcı olan budur. EEW sistemleri P dalgasını yakalar, S dalgası varmadan 5-60 saniye önce uyarı gönderir. Mesafe uzadıkça uyarı süresi artar — merkezden 100 km uzakta ~15 saniye, 300 km uzakta ~45 saniye erken uyarı alırsınız."),
            ("Japon Sistemi — Dünyanın En Gelişmişi", "Japonya 1995 Kobe depreminden sonra dünyanın en gelişmiş EEW ağını kurdu. <strong>JMA (Japan Meteorological Agency)</strong> sistemi 2007'de aktif oldu. 1.000+ sismometre ağı, cep telefonu baz istasyonları ve TV yayın sistemleri entegre. Her Japon cep telefonuna deprem uyarısı gelir — \"Deprem! 10 saniye sonra sarsıntı!\"."),
            ("ABD ShakeAlert", "Batı sahilinde (Kaliforniya, Oregon, Washington) USGS'in ShakeAlert sistemi aktif. Google Android telefonlar otomatik bildirim gönderir. 2018'de aktif oldu. Yaklaşık 100 milyon kişiyi kapsar."),
            ("Türkiye'de AFAD Erken Uyarı", "Türkiye'de AFAD 2023'te pilot bir erken uyarı sistemi başlattı. İstanbul, İzmir ve Kahramanmaraş gibi büyük şehirlerde aktif. Sistem AFAD'ın ücretsiz uygulaması üzerinden çalışır — <strong>play.google.com'dan \"AFAD Acil\"</strong> indirerek aktif edebilirsiniz. Ancak kapsama alanı hala sınırlı — 2030 hedefiyle tüm ülke kaplanacak."),
            ("Kendi Uyarınızı Ayarlayın", "AFAD sistemine ek olarak bizim sitemizdeki <a href=\"/\">canlı deprem haritamız</a> 20 saniye aralıklarla güncellenir ve <strong>Web Push bildirimi</strong> gönderir. Ayarlardan \"4.0+ büyüklüktekilerde bildir\" seçeneğini etkinleştirebilirsiniz. <a href=\"/son-dakika-deprem.html\">Son dakika sayfamızda</a> da bölgesel bildirim ayarları var."),
        ],
        "faq": [
            ("Erken uyarı sistemi her zaman çalışır mı?", "Hayır. Çok küçük (Mw <4.0) depremlerde uyarı gönderilmez. Ayrıca epicenter'a 10 km'den yakınsanız uyarı fizikken imkansızdır — S dalgası sizinle aynı anda gelir."),
            ("Erken uyarıdan sonra ne yapmalıyım?", "Saniyeler içinde <a href=\"/deprem-aninda.html\">çök-kapan-tutun</a> pozisyonuna geçin. Asansörden inin (durdurun), gazı kapatın, camdan uzaklaşın."),
            ("Sistem hatalı uyarı verir mi?", "Nadiren. Yanlış pozitif oranı <%0.1'dir. Her uyarıyı ciddiye alın — gerçek olduğunda zamanınız yok."),
        ],
    },
    {
        "slug": "blog-mobilya-sabitleme-rehberi",
        "title": "Deprem İçin Mobilya Sabitleme – Adım Adım Rehber",
        "desc": "Depremde en büyük ölüm nedenlerinden biri devrilen mobilyadır. Dolap, kitaplık, buzdolabı gibi ağır mobilyaları duvara nasıl sabitlersiniz? Pratik rehber.",
        "keywords": "mobilya sabitleme, deprem dolap sabitleme, l-profil, devrilme önleme, kitaplık sabitleme",
        "hero_img": "blog-mobilya-sabitleme-rehberi.webp",
        "lead": "Japonya'da yapılan bir araştırmaya göre ev içi deprem ölümlerinin %40'ı devrilen mobilyalardan kaynaklanıyor. Mobilya sabitleme 30 dakika süren ama hayat kurtaran bir işlemdir.",
        "sections": [
            ("Hangi Mobilyalar Sabitlenmeli?", "<strong>Yüksekliği 90 cm'den fazla tüm mobilyalar:</strong> kitaplık, büfe, vitrin, dolap. <strong>Ağır beyaz eşyalar:</strong> buzdolabı, bulaşık makinesi, çamaşır makinesi (yan yan hareket ederek kablo ve hortumları kırabilir). <strong>TV, ekran ve monitörler:</strong> duvara takılı olmaları şart. <strong>Ağır tablo, ayna ve sanat eşyaları:</strong> özellikle yatak üzerindekiler hayati risktir."),
            ("Gerekli Malzemeler", "<strong>L-profil (L-demir):</strong> en yaygın ve en güçlü yöntem. Nalburlardan 20-60 TL arası. <strong>Emniyet kemeri (strap):</strong> esnek, yumuşak hareketi absorbe eder. <strong>Anti-deprem pedleri:</strong> mobilyanın altına sürgü gibi yerleştirilir, ön-arka kaymayı engeller. <strong>Duvar tipi dübel:</strong> betona metal dübel, alçıpan'a çift kanatlı dübel kullanın."),
            ("Kitaplık ve Yüksek Dolap Sabitleme", "1. Mobilyayı duvara dayayın. 2. Üst kısmında 2 L-profil noktası işaretleyin (köşelere yakın). 3. Duvarda matkapla delin (beton için 8 mm, alçıpan için özel ucu). 4. Dübeli yerleştirin. 5. L-profili vidalayın (mobilya tarafına ahşap vida, duvar tarafına dübel vidası). 6. Kitaplık 180 cm'den uzunsa 3 nokta kullanın."),
            ("Buzdolabı Sabitleme", "Buzdolabı genelde duvara yakın durur ama sabit değildir. <strong>Üstten strap:</strong> dolabı arkasındaki duvara L-profilli + kayış ile bağlayın. <strong>Alttan kayma önleyici:</strong> mobilya altına anti-deprem pedleri koyun. Mutfak dolaplarının içindeki ağır eşyalar (cam, porselen) için <strong>dolap kilidi</strong> kullanın — çocuk kilidi gibi, sarsıntıda kapının açılmasını engeller."),
            ("TV ve Elektronikler", "LCD/LED TV'leri mutlaka <strong>duvara VESA ayağı</strong> ile sabitleyin. Eğer sehpa üstünde ise arkasına güvenlik kayışı + sehpa üstüne anti-deprem pedi. Monitörler için 2. el satıcılarda ucuz VESA ayakları var (50-150 TL)."),
            ("Dikkat Edilecekler", "<strong>Asla duvarın derz bölgesine dübel atmayın</strong> — duvar çöker, mobilyayı tutmaz. <strong>İşinizi kontrol edin:</strong> mobilyayı elle iterek sabitlemenin tuttuğunu teyit edin. <strong>6 ayda bir tekrar kontrol</strong>: vidalar gevşeyebilir. Kiracıysanız ev sahibinizle konuşup izin alın — L-profil küçük bir iz bırakır."),
        ],
        "faq": [
            ("Sabitlemek için profesyonel çağırmam gerekir mi?", "Hayır. Temel matkap becerisi ile 2-3 saat içinde tüm evi sabitleyebilirsiniz. YouTube'da bolca Türkçe video var. Yalnız VESA TV montajı için uzman önerilir."),
            ("Kiracıyım, izin verirler mi?", "Modern ev sahipleri genelde izin verir — L-profil izi 5x5 cm civarında ve kolay kapatılır. Hasar sigorta kapsamında değildir."),
            ("Antik eşyalarımı nasıl koruyabilirim?", "Müze tipi \"museum gel\" veya yapışkan ped kullanın (ebay, aliexpress'te var). Heykel ve vazoların tabanına yapıştırılır, kaymalarını engeller."),
        ],
    },
    {
        "slug": "blog-deprem-anketi-cocuklar",
        "title": "Çocuklara Deprem Nasıl Anlatılır? Yaşlara Göre Rehber",
        "desc": "Çocuklara deprem konusunu anlatmak korkutmadan nasıl yapılır? 3-5, 6-9, 10-14 yaş gruplarına göre iletişim rehberi ve ebeveyn önerileri.",
        "keywords": "çocuklara deprem, deprem çocuklar, deprem eğitimi çocuk, çocuk afet, deprem psikolojisi çocuk",
        "hero_img": "blog-deprem-anketi-cocuklar.webp",
        "lead": "Çocuklar deprem haberlerini yetişkinlerden daha yoğun hisseder. Doğru iletişim, onları korkudan kurtarırken güvenlik bilinci kazandırır. İşte yaş gruplarına göre rehber.",
        "sections": [
            ("3-5 Yaş: Oyunla Öğret", "Küçük çocuklara \"deprem\" kelimesi soyut gelir. Onun yerine <strong>\"Ev sallandığında bu dansı yaparız!\"</strong> yaklaşımı kullanın. Çök-kapan-tutun hareketini eğlenceli bir oyuna çevirin: \"Deprem Dansı\" adında aile içi tatbikat. Çocuk sallandığında otomatik masanın altına gitmeyi oyunla öğrenir. Bu yaşta detay anlatmayın — sadece güvenli davranış refleksi kazandırın."),
            ("6-9 Yaş: Basit Bilim", "Okul çağındaki çocuklar \"neden\" sorusu sorar. Yerkabuğunu büyük taşlar, onların kaymasını deprem olarak anlatın: \"Yer taşları bazen birbirine çarparak sallanır, tıpkı çok büyük bir arabanın geçişi gibi\". Bu yaşta onlara <strong>aile toplanma planı</strong> çizmelerini isteyin — buzdolabına asın. <strong>Deprem çantalarına kendi oyuncaklarını</strong> (bir tanesi) eklesinler — aidiyet duygusu güvensizliği azaltır."),
            ("10-14 Yaş: Bilimsel Gerçekler", "Bu yaşta çocuklar magnitüd ve fay hattı gibi kavramları anlar. Onlara <a href=\"/blog-deprem-buyukluk-olcekleri.html\">büyüklük ölçeklerini</a> ve <a href=\"/blog-turkiye-fay-hatlari-haritasi.html\">fay hattı haritasını</a> gösterin. Okullarındaki <strong>deprem tatbikatlarını</strong> ciddiye almalarını sağlayın. Ama korkmasın — \"bilimsel önlem alıyoruz, güvendeyiz\" vurgusu önemli."),
            ("Korkmuş Çocuğu Nasıl Yatıştırırsınız?", "Deprem sonrası veya haber seyrederken korkan çocuk için: <strong>1.</strong> Duygularını reddetmeyin — \"korkmana gerek yok\" yerine \"korkunu anlıyorum\". <strong>2.</strong> Bedensel temas — sarılın, sıcaklık güven verir. <strong>3.</strong> Konuşmaya teşvik edin — ama zorlamayın. <strong>4.</strong> Rutinlere dönün — düzen güven verir. <strong>5.</strong> Şiddet içerikli haber görüntülerinden uzak tutun. Depremden sonra 3+ haftada uyku bozukluğu, karın ağrısı, takıntı devam ediyorsa <strong>çocuk psikoloğuna gidin</strong> — travma sonrası stres mümkündür."),
            ("Aile Hazırlık Aktivitesi", "Ayda bir aile içi <strong>deprem tatbikatı</strong> yapın: \"Deprem!\" deyince herkes güvenli pozisyona geçer. Sonra aile toplanma noktasına yürüyün. Çocuklar bunu bir oyun gibi sever. Bu tekrar, sarsıntı anında otomatik refleks sağlar — beyin düşünmeden hareket eder."),
        ],
        "faq": [
            ("Çocuk deprem sonrası uyuyamıyor, ne yapmalıyım?", "İlk 2 hafta normal. Yatakta yanında kalın, gece lambası açık bırakın. Uyku öncesi sakin bir masal anlatın. 3 haftadan uzun sürerse psikolog."),
            ("Bebek (0-3 yaş) depremden etkilenir mi?", "Evet. Bebekler ebeveynlerinin stresini emer. Sakin kalın, sarılı tutun. Rutinlerini bozmayın (uyku, mama saatleri)."),
            ("Okul tatbikatlarına çocuğum girsin mi?", "Kesinlikle evet. Tatbikat korku değil refleks geliştirir. Okul tatbikatından sonra eve gelen çocuğunuzla deneyimi paylaşın."),
        ],
    },
    {
        "slug": "blog-apartman-yoneticisi-deprem",
        "title": "Apartman Yöneticileri İçin Deprem Hazırlık Rehberi",
        "desc": "Apartman yöneticisi olarak deprem öncesi ne yapmalısınız? Ortak alanlar, yangın güvenliği, kat malikleri iletişimi ve acil durum planı rehberi.",
        "keywords": "apartman deprem, site yöneticisi deprem, ortak alanlar, kat malikleri deprem, bina güvenliği",
        "hero_img": "blog-apartman-yoneticisi-deprem.webp",
        "lead": "Apartman yöneticisi veya site sakini olarak deprem hazırlığı sadece kendi daireniz değil — tüm binanın sorumluluğudur. İşte bir yöneticinin 10 temel görevi.",
        "sections": [
            ("1. Bina Risk Durumu Öğrenin", "İlk iş: belediyeden imar bilgileri + yapı denetim raporu isteyin. Bina yapım yılı, iskan ruhsat durumu, güçlendirme geçmişi önemlidir. <a href=\"/blog-evim-depreme-dayanikli-mi.html\">Bu rehberimizdeki</a> 7 adımlık kontrolü uygulayın."),
            ("2. Ortak Alanlar Tatbikatı", "Apartman giriş ve merdiven alanlarını tahliye için düzenleyin: <strong>giriş kapısı önü boş</strong>, merdivende çelik çember veya korkuluk sağlam, asansörlerde <strong>\"deprem modu\" açık</strong> (en yakın kata gider, kapıları açık tutar)."),
            ("3. Acil İletişim Listesi", "Tüm kat malikleri ve kiracıların iletişim bilgilerini güncel tutun. <strong>WhatsApp acil grup</strong> oluşturun. Yaşlı, engelli, kronik hasta sakinleri özel listeye alın — deprem sonrası onlara öncelikli yardım gerekir."),
            ("4. Ortak Alanlarda Mobilya Sabitleme", "Lobi, koridor, ortak salon gibi ortak alanlardaki mobilyalar çoğu zaman kimsenin sabitlemediği alanlardır. Kat malikleri toplantısında <strong>sabitleme ortak giderlere ekletin</strong>. 2.000-5.000 TL maliyetle tüm ortak alan güvenli hale gelir."),
            ("5. Yangın ve Gaz Güvenliği", "Deprem sonrası %30 vaka yangınla sonuçlanır. Apartmanda: <strong>yangın söndürücü</strong> (her katta 1), <strong>duman dedektörü</strong> (koridor + dairelerde), <strong>gaz ana vana işareti</strong> (görünür, herkes bilsin), <strong>jeneratör planı</strong> (elektrik kesintisinde acil aydınlatma)."),
            ("6. Toplanma Alanı Tespiti", "Apartmanınızın resmi toplanma alanını <a href=\"/blog-toplanma-alani-sorgulama.html\">e-Devlet'ten sorgulayın</a>. Bu bilgiyi lobiye asın. Kat malikleri ile bir kez oraya yürüyün — rotayı bilsinler."),
            ("7. Deprem Sigortası Takibi", "<strong>Her dairenin DASK poliçesi olmalı</strong>. Yıllık yenileme takvimini yöneticilik olarak kontrol edin. <a href=\"/blog-dask-nedir.html\">DASK rehberimiz</a> detaylı bilgi sağlar. DASK'sız daireler deprem sonrası ortak alan onarımlarında sorun yaratır."),
            ("8. Su ve Yiyecek Deposu", "Ortak alan (bodrum, çatı) uygunsa <strong>apartman için yedek su ve battaniye deposu</strong> oluşturun. 50 kişilik bina için 1.000 litre su, 30 battaniye, konserve yemek — toplam 5.000-8.000 TL. Deprem sonrası ilk 72 saat kritik."),
            ("9. Yıllık Tatbikat", "Yılda en az 1 kez <strong>tam bina tatbikatı</strong> yapın. Bahar ayında bir Pazar sabahı \"hayali deprem\" senaryosu: herkes çök-kapan-tutun yapar, sonra tahliye, toplanma alanına yürüme, sayım. 30 dakikada biten bu aktivite gerçek bir depremde saniyeler kurtarabilir."),
            ("10. Dokümanları Güncel Tutun", "Bina dosyasında: statik proje, güçlendirme raporu, yapı denetim belgesi, iskan ruhsatı, kat malikleri kararları, sigorta poliçeleri. Bu evraklar deprem sonrası çok önemli — hasar tazminatı, kredi başvurusu, güçlendirme projesi için gereklidir."),
        ],
        "faq": [
            ("Yönetici olarak deprem sorumluluğum nedir?", "Hukuki olarak kat malikleri kurulundan aldığınız yetki dahilinde ortak alanların güvenliğinden sorumlusunuz. Bireysel dairelerden değilsiniz, ama ortak gaz-elektrik-su tesisatı ve yapısal uyarılar sizdedir."),
            ("Tatbikata katılımı nasıl artırırım?", "Kat malikleri toplantısında <strong>zorunlu hale getirin</strong> (ortak gider gibi). 2-3 yıl sonra alışkanlık olur. Çocuklu aileler öncelikle katılır."),
            ("Bina güçlendirme kararı nasıl alınır?", "Kat malikleri kurulunda 2/3 çoğunluk şarttır. Riskli bina raporu varsa Kentsel Dönüşüm Yasası gereği zaten zorunludur — bir anlamda devlet karar veriyor."),
        ],
    },
    {
        "slug": "blog-evcil-hayvanlarla-deprem",
        "title": "Evcil Hayvanlarla Deprem Planı Nasıl Yapılır?",
        "desc": "Kedi, köpek, kuş ve diğer evcil hayvanlarınızla deprem hazırlığı. Taşıma çantası, yedek mama, kimlik künyesi ve tahliye önerileri.",
        "keywords": "evcil hayvan deprem, kedi deprem, köpek deprem çantası, evcil hayvan tahliye",
        "hero_img": "blog-evcil-hayvanlarla-deprem.webp",
        "lead": "Türkiye'de 10 milyonun üzerinde evcil hayvan var. Deprem anında onları da korumak, hem onlar için hem de sizin psikolojiniz için kritik. İşte kapsamlı evcil hayvan afet planı.",
        "sections": [
            ("Taşıma Çantası Hazır Olsun", "Her evcil hayvan için bir <strong>taşıma kafesi veya çantası</strong> olmalı ve görünür yerde bulunmalı. Kedi için sert plastik kafes, küçük köpek için benzer kafes, büyük köpek için tasma + ağızlık. Panik anında hayvanlar sahiplerini tanımayabilir — ağızlık ısırık riskini azaltır."),
            ("Evcil Hayvan Deprem Çantası", "Ayrı bir çantada: <strong>3 günlük mama</strong> (konserve veya kuru, düzenli yenileme), <strong>su</strong> (hayvan başı 1 litre/gün), <strong>kaplar</strong> (katlanabilir plastik), <strong>yedek tasma ve kayış</strong>, <strong>veteriner kayıtları</strong> (aşı kartı, mikroçip numarası), <strong>kişisel fotoğraflar</strong> (kaybolursa), <strong>ağrı kesici ve sakinleştirici</strong> (veteriner önerir), <strong>kedi tuvaleti için küçük kum torbası</strong>."),
            ("Kimlik ve İletişim", "Evcil hayvanınızda mutlaka <strong>mikroçip</strong> olmalı (veterinerden, 200-400 TL). Tasmasında <strong>isim + telefon numarası</strong> yazan künye. Fotoğraflı <strong>\"beni evine götür\" kartı</strong> cüzdanınızda. Mikroçiplenmemiş hayvanlar kaybolduklarında sahip bulmak çok zor."),
            ("Deprem Anında Ne Yaparım?", "<strong>1.</strong> Kendi güvenliğinizi önce sağlayın — kendinizi kurtarmadan hayvan kurtarmaya çalışmak tehlikelidir. <strong>2.</strong> Sarsıntı sırasında hayvanınızla konuşmayın, acele tutmayın — ısırılabilir. <strong>3.</strong> Sarsıntı bitince hayvanı sakin yaklaşımla taşıma kafesine alın. <strong>4.</strong> Sert sesli çağırmak yerine sakince konuşun. <strong>5.</strong> Tahliye sırasında tasmanız kısa olsun, güvenli mesafede tutun."),
            ("Toplanma Alanında Evcil Hayvan", "Çoğu toplanma alanı evcil hayvanları kabul eder ama kural farklıdır. <strong>AFAD kayıtlı toplanma alanlarında genelde uygundur</strong> ama bağlı tutmanız gerekir. <strong>Gıda alırken tasmanızı duvara veya ağaca bağlayın</strong>. Büyük köpekler için ağızlık takmanızda fayda var — kalabalıkta stresle ısırık olabilir."),
            ("Kayıp Hayvan Prosedürü", "Deprem sonrası evcil hayvanınız kaçarsa: <strong>1.</strong> Evinizden uzaklaşmayın — çoğu hayvan 1-3 gün içinde eve döner. <strong>2.</strong> Yakındaki veterinerlere ve belediye sahipsiz hayvan birimine bilgi verin. <strong>3.</strong> Sosyal medyada paylaşın — mikroçip numarası olmadan genelde yüzlerce saat sürer."),
        ],
        "faq": [
            ("Kedi deprem öncesi sezer mi?", "Bilimsel araştırmalar net değil ama bazı hayvanlar deprem öncesi huzursuzluk gösterir. Aniden saklanmaya başlayan bir kedi dikkate alınmalı ama tek kanıt değildir."),
            ("Büyük ırk köpeğimi kafese sığdıramıyorum, ne yapayım?", "Kafes almak yerine <strong>kalın tasma + koşum + ağızlık</strong> yeterlidir. Deprem sırasında kısa tutun. Toplanma alanında sakin köşede bağlayın."),
            ("Akvaryum balığım için ne yapmalıyım?", "Akvaryum zaten küçük bir su hacmi — deprem sırasında yer değiştirebilir. Balıkları korumak zor; <strong>evden çıkarken akvaryumu yere indirin</strong>. Uzun tahliye gerekirse taze su + filtre pille çalışan sistem gerekli (zor)."),
        ],
    },
    {
        "slug": "blog-engelli-bireyler-deprem",
        "title": "Engelli Bireyler İçin Deprem Tahliye Planı",
        "desc": "Tekerlekli sandalyeli, görme engelli, işitme engelli ve hareket kısıtlı bireyler için özel deprem hazırlık ve tahliye rehberi.",
        "keywords": "engelli deprem, tekerlekli sandalye tahliye, görme engelli deprem, işitme engelli deprem",
        "hero_img": "blog-engelli-bireyler-deprem.webp",
        "lead": "Türkiye'de 8.5 milyon engelli birey yaşıyor. Standart deprem önerileri çoğu zaman onlar için yetersiz veya tehlikelidir. İşte her engel grubu için uyarlanmış rehber.",
        "sections": [
            ("Tekerlekli Sandalye Kullanıcıları", "Sarsıntı sırasında: <strong>1.</strong> Sandalyeyi durdurun, frenleri kilitleyin. <strong>2.</strong> Kolumlayla başınızı ve boynunuzu koruyun (kapan). <strong>3.</strong> Sarsıntı bitene kadar sandalyeden çıkmayın.<br>Tahliye için: <strong>güvenli kat</strong> belirleyin (asansör çalışmayacak; merdiven iniş asistanı var mı?). <strong>Yedek tekerlekli sandalye</strong> ve <strong>taşıma koltuğu</strong> araçta veya evde bulundurun."),
            ("Görme Engelli Bireyler", "<strong>Önceden mekan haritası ezberi:</strong> evdeki her odanın en güvenli noktasını bilin. Mobilya yerleri değişmesin — deprem öncesi tanıdığınız yerleşim sarsıntı sonrası navigasyona yardım eder. <strong>Baston aksesuarları:</strong> yedek baston + baston için kırmızı bez (kaybolma durumunda). <strong>Sesli uyarı cihazları:</strong> evde duman dedektörü, AFAD Acil uygulaması (sesli uyarı)."),
            ("İşitme Engelli Bireyler", "Uyarı sinyalleri sesli olduğu için ek önlem gerekir. <strong>Titreşimli uyarı cihazları:</strong> yatak altına konan titreşim pili (deprem sırasında uyandırır). <strong>Görsel alarm:</strong> yangın gibi deprem için de görsel flash alarm gerekebilir. <strong>Aile üyeleriyle özel işaret:</strong> eğer işaret dili biliyorsanız kendi deprem işaretinizi geliştirin."),
            ("Bedensel Kısıtlılığı Olan Bireyler", "Kalp yetmezliği, omurga sorunları, yaşlılık kaynaklı hareket kısıtı olanlar: <strong>Yatak yanında sağlam yer</strong> — yatak altına girmek yerine yataktan inip kenarda çök-kapan yapın. <strong>Önceden yerleştirilmiş yastık seti</strong> başınızı korumak için. <strong>Rahat kıyafetlerle uyuyun</strong> — tahliye için değiştirme süreniz yok."),
            ("Yalnız Yaşayan Engelli Bireyler İçin Sistem", "<strong>Komşu ağı:</strong> yakın komşularla özel anlaşma — deprem olursa birbirinizi kontrol edersiniz. <strong>AFAD özel kayıt:</strong> e-Devlet'ten \"özel durumu olan birey\" kaydı yapabilirsiniz. AFAD deprem sonrası sizi özel öncelikle arar. <strong>Personel alarmı:</strong> kolunuza takabileceğiniz panik butonu cihazı alın (2.000-5.000 TL)."),
            ("Tıbbi Gereksinimleri Olan Bireyler", "Oksijen tüpü, insülin pompası, diyaliz cihazı vb kullanıcılar: <strong>Her cihaz için yedek + pil</strong> hazırda tutun. <strong>30 günlük ilaç stoku</strong> çantada. <strong>Tıbbi kimlik kartı</strong> — cüzdanda ve boyun künyesinde. <strong>Hastane planı</strong> — hangi hastaneye gidileceğinizi aile bilsin."),
        ],
        "faq": [
            ("AFAD'ın engelli programı var mı?", "Evet. AFAD \"Özel İhtiyaçlı Bireyler Kayıt Sistemi\" üzerinden evinizdeki engelli kaydı yapılabilir. Deprem sonrası tahliye ekipleri bu listeye öncelikle bakar."),
            ("Apartmanda asansörsüz kaldıysam?", "Komşulara önceden bilgi verin. Apartman yöneticisine plan dahilinde sizin için <strong>merdiven tahliye koltuğu</strong> alınması için baskı yapın — 5.000-10.000 TL arası cihazlar mevcut."),
            ("İşaret dili bilmeyen acil personeli ile nasıl iletişim kurarım?", "Cüzdanınızda kart bulundurun: \"Ben işitme engelliyim. İşaret dili biliyorsanız konuşun, değilse yazılı not verin\" yazılı olsun. Veya telefonda konuşma-metin dönüşümü."),
        ],
    },
    {
        "slug": "blog-yaslilar-icin-deprem",
        "title": "Yaşlılar İçin Deprem Hazırlığı ve Güvenlik Rehberi",
        "desc": "65 yaş üstü bireylerin deprem hazırlığı: ilaç yönetimi, evde güvenli düzenleme, tahliye planı ve aile iletişimi için detaylı rehber.",
        "keywords": "yaşlı deprem, 65 yaş deprem, yaşlı bakım deprem, yaşlı tahliye planı",
        "hero_img": "blog-yaslilar-icin-deprem.webp",
        "lead": "Depremlerde ölüm ve yaralanma riski en yüksek grup 65 yaş üstü bireylerdir. 2023 Kahramanmaraş depremlerinde vefat edenlerin %31'i 60 yaş üstüdür. Yaşlı aile üyelerimiz için özel hazırlık yapmak hayat kurtarır.",
        "sections": [
            ("Neden Yaşlılar Daha Riskli?", "<strong>Hareket kısıtı:</strong> çök-kapan-tutun refleksi yavaştır. <strong>Osteoporoz:</strong> düşme durumunda kemik kırığı oranı yüksek. <strong>Bilişsel zorluk:</strong> panik anında doğru karar verme güçleşir. <strong>İlaç bağımlılığı:</strong> günlük kronik hastalık ilaçları kesilirse kriz riski. <strong>Sosyal izolasyon:</strong> yalnız yaşayan yaşlılar yardım alma konusunda dezavantajlı."),
            ("Evde Güvenli Düzenleme", "<strong>Yatak yanı:</strong> bir ayakkabı çifti + fener + gözlük + ilaçlar her zaman hazır. Deprem sonrası yatakta karanlıkta aranma olmasın. <strong>Mobilyalar sabitli:</strong> <a href=\"/blog-mobilya-sabitleme-rehberi.html\">bu rehberdeki</a> yöntemle. <strong>Banyoda tutamaklar:</strong> deprem sırasında banyoda olursanız tutunacak yeriniz olsun. <strong>Aydınlatma:</strong> gece lambası, acil ışık (pilli)."),
            ("İlaç Yönetimi", "<strong>30 günlük ilaç stoku</strong> her zaman evde + deprem çantasında. <strong>İlaç listesi yazılı ve fotoğrafı</strong> — cüzdan ve telefon. <strong>Reçete fotokopileri</strong> — eczane kayıtları bulunamayabilir. <strong>Kritik ilaçlar</strong> (kalp, diyabet, tansiyon): 3 günlük ek stok ayrı çantada. <strong>Alerji bilgisi</strong> — yazılı kart, özellikle alerjik reaksiyon geçirmişse çok önemli."),
            ("Aile İletişim Planı", "Her yaşlı aile üyesi için: <strong>Bir birincil aile sorumlusu</strong> (çocuk, akraba, komşu) belirleyin. Deprem sonrası ilk kontrol arayan o olur. <strong>WhatsApp konum paylaşımı</strong> — kronik durumu olan yaşlılar için her zaman açık. <strong>Yedek iletişim kartı</strong> — cüzdanda: isim, yaş, kan grubu, kronik hastalık, iletişim numaraları, çocuk adları."),
            ("Tahliye Planlaması", "<strong>Merdiven planı:</strong> asansör çalışmayacak, merdivenden nasıl ineceksiniz? 85 yaş üstü için bu çok zor — komşu ağı kritik. <strong>Yardımcı:</strong> apartmanda en az 2 kişi \"deprem komşusu\" olsun — deprem sonrası birbirinizin dairesini kontrol edin. <strong>Toplanma alanı yakınlığı:</strong> uzaksa yaşlı için zordur. Aile üyesi araba ile toplanma noktasına götürmelidir."),
            ("Yalnız Yaşayan Yaşlılar İçin", "<strong>Panik butonlu cihaz</strong> (boyuna takılı, 3.000-8.000 TL) — düşme sonrası yardım çağırır. <strong>AFAD özel kayıt</strong> — yaşlı ve yalnız yaşayan kaydı. <strong>Haftalık aile takibi</strong> — düzenli check-in rutini. <strong>Komşu işbirliği</strong> — anahtarı güvendiği bir komşuda olsun. <strong>Basit telefon eğitimi</strong> — WhatsApp konum, video arama, 112 arama basit tuş kombinasyonu."),
        ],
        "faq": [
            ("Alzheimer hastası annemi nasıl koruyabilirim?", "Evde mümkünse <strong>24 saat refakatçi</strong> bulundurun. <strong>Tıbbi künye bileziği</strong> (isim, adres, telefon, hastalık bilgisi) 7/24 taşısın. Kısa bilişsel açıklamalar ve görsel uyarılarla tatbikat yapın. Tahliye durumunda paniği önlemek için sakin yaklaşım ve tanıdık yüz önemli."),
            ("Yaşlılara deprem çantasında özel ne olmalı?", "Standart çantaya ek: <strong>30 günlük kronik ilaç</strong>, <strong>yedek gözlük</strong>, <strong>yedek işitme cihazı pili</strong>, <strong>yedek diş protezi</strong>, <strong>rahat ayakkabı</strong>, <strong>sıcak battaniye</strong> (yaşlı vücut soğuğa hassas)."),
            ("Yaşlı ebeveynim kentsel dönüşüm kararlı binada yaşıyor, taşınsın mı?", "Riskli bina raporu varsa yasa gereği 60 gün içinde boşaltılmalıdır. Yaşlı birey için daha da acil — düşüş riski yüksek. Aile olarak geçici çözüm (ayrı bir dairede kalma) hazırlayın."),
        ],
    },
    # --- Group C: Regional/Istanbul ---
    {
        "slug": "blog-istanbul-deprem-haritasi-ilceler",
        "title": "İstanbul Deprem Haritası – Hangi İlçeler Riskli?",
        "desc": "İstanbul'un 39 ilçesinin deprem risk haritası: Avcılar'dan Şile'ye kadar hangi bölge yüksek, hangisi orta risk taşıyor? Zemin + yapı analizi.",
        "keywords": "istanbul deprem haritası, istanbul ilçe risk, avcılar zeytinburnu deprem, istanbul riskli ilçeler",
        "hero_img": "blog-istanbul-deprem-haritasi-ilceler.webp",
        "lead": "İstanbul'un 39 ilçesi, deprem riski açısından büyük farklar gösteriyor. Zemin yapısı, fay hattına mesafe ve bina stokunun yaşı üçlüsü risk profilini belirliyor. İşte detaylı ilçe haritası.",
        "sections": [
            ("En Yüksek Risk: Marmara Sahili İlçeleri", "<strong>Avcılar, Küçükçekmece, Bakırköy, Zeytinburnu, Fatih, Beyoğlu, Beşiktaş</strong> — Marmara sahilinde, alüvyon zemin ve eski yapı stoku ile en yüksek riskli bölge. KAF'ın Marmara kolu 10-20 km yakınlıkta. 1999 Gölcük depreminde Avcılar'da 500+ bina çökmüştü. 2023 öncesi yapım binalar özellikle risk taşır."),
            ("Yüksek Risk: Avrupa Yakası Merkez", "<strong>Esenyurt, Büyükçekmece, Arnavutköy, Eyüpsultan, Bayrampaşa</strong>, Kağıthane — yoğun nüfus + orta yaşta yapı stoku + belirsiz zemin. Esenyurt özellikle plansız yapılaşma tarihi nedeniyle dikkat çekiyor."),
            ("Orta Risk: Anadolu Yakası", "<strong>Kadıköy, Üsküdar, Ümraniye, Kartal, Maltepe, Pendik, Tuzla</strong> — daha sert zemin (kuvars ve tortul) + nispeten yeni yapı stoku. Marmara fayından uzaklaşınca risk düşüyor. Yine de sarsıntı etkisi yüksek."),
            ("Görece Düşük Risk: İç ve Kuzey İlçeler", "<strong>Sarıyer, Beykoz, Çekmeköy, Sancaktepe, Şile, Silivri (kuzey)</strong> — kayaç zemin, fay hattından uzak, yapı kalitesi iyi. Yine de dikkatli olmak gerekir — İstanbul'da %100 güvenli bölge yoktur."),
            ("Zemin Etkisi Neden Önemli?", "<strong>Alüvyon zemin</strong> (sahil ve dere yatakları) deprem dalgalarını 3-5 kat güçlendirir. <strong>Kayaç zemin</strong> sarsıntıyı olduğu gibi iletir. Aynı depremi Kadıköy'de Mw 5.0, Avcılar'da Mw 6.0 gibi hissedebilirsiniz — merkez aynı olsa bile."),
            ("Kendi İlçenizin Detayını Görün", "Her İstanbul ilçesinin kendi özel dinamikleri var. <a href=\"/deprem-istanbul.html\">İstanbul deprem sayfamızda</a> detaylı ilçe haritası ve risk değerlendirmesi var. <a href=\"/blog-evim-depreme-dayanikli-mi.html\">Kendi binanızı test etmeyi</a> öğrenin — ilçe risk seviyesinden daha önemlisi sizin binanız."),
        ],
        "faq": [
            ("En güvenli İstanbul ilçesi hangisi?", "Şile, Beykoz ve Sarıyer'in yüksek kesimleri — kayaç zemin ve düşük nüfus. Ancak hiçbir ilçe \"%100 güvenli\" değildir, sadece görece daha az riskli."),
            ("Oturduğum ilçe riskli, ne yapmalıyım?", "Taşınmak yerine <strong>bina kalitesini</strong> değerlendirin. Riskli ilçede güçlü bir bina, güvenli ilçede zayıf bir binadan daha güvenlidir. Yapı denetim raporu isteyin, DASK yaptırın."),
            ("Kentsel dönüşüm hangi ilçede aktif?", "Avcılar, Küçükçekmece, Zeytinburnu, Fatih, Esenyurt, Bakırköy'de yoğun kentsel dönüşüm var. Belediyenin ilgili birimlerinden detay alabilirsiniz."),
        ],
    },
    {
        "slug": "blog-izmir-deprem-tarihi",
        "title": "İzmir Deprem Tarihi – 2020 Samos'tan Bugüne",
        "desc": "İzmir'de son 20 yılın önemli depremleri: 2020 Samos-İzmir, 1928 İzmir ve tarihi Ege sarsıntıları. Fay hattı + yapı + ders çıkarımları.",
        "keywords": "izmir deprem tarihi, 2020 izmir samos depremi, izmir fay hattı, ege depremleri",
        "hero_img": "blog-izmir-deprem-tarihi.webp",
        "lead": "İzmir, Ege'nin en büyük şehri olarak deprem tarihinde önemli bir yer tutuyor. 2020 Samos-İzmir depremi hafızalardayken, tarihsel kayıtlar çok daha fazlasını gösteriyor. İşte İzmir'in deprem hafızası.",
        "sections": [
            ("2020 Samos-İzmir Depremi", "30 Ekim 2020, 14:51'de Ege Denizi'nde Mw 6.9 büyüklüğünde deprem oldu. Merkez Samos Adası (Yunanistan) 14 km güneyi, derinlik 16 km. İzmir'de 117 kişi vefat etti, 1.035 kişi yaralandı. 11 bina tamamen çöktü — Bornova ve Bayraklı'da. Kırım alanlar <strong>alüvyon zeminde eski (1999 öncesi) binalar</strong>dı."),
            ("1928 İzmir Depremi (Tarihi)", "İzmir'in yaşadığı en büyük tarihsel deprem Haziran 1928'de gerçekleşti. Mw 6.4 tahmini, ancak sismograf ağı yeterli olmadığı için kesin veri yok. Kentte yangınlar çıktı, yüzlerce ölü. Bu deprem İzmir'in yeniden yapılanma döneminin başlangıcıydı."),
            ("İzmir'i Etkileyen Fay Sistemi", "İzmir, <strong>Gülbahçe Fayı</strong> (körfezin güneyi), <strong>Tuzla Fayı</strong> ve <strong>Izmir Fayı</strong> (kuzey) dahil birçok normal fay'ın etkisindedir. Bu fayların hepsi <strong>Batı Anadolu Grabenleri Sistemi</strong>nin parçasıdır. Gediz Grabeni (Bozdağlar'ın kuzeyinde) ve Küçük Menderes Grabeni de şehri etkiler."),
            ("Son 10 Yılda Hissedilen Sarsıntılar", "2017 Bodrum-Kos Mw 6.6 (İzmir'de hissedildi). 2019 Denizli Mw 5.7 (hafif hissedildi). 2020 Samos Mw 6.9 (yıkıcı). 2023'te birkaç Mw 4.0-4.8 sarsıntı. Ortalama <strong>her 20-30 yılda Mw 6+ bir depreme</strong> İzmir maruz kalıyor."),
            ("En Riskli İzmir İlçeleri", "<strong>Bornova, Bayraklı, Karşıyaka</strong> — 2020'de en büyük hasar buradaydı. Alüvyon zemin + yoğun bina stoku. <strong>Balçova, Narlıdere, Güzelbahçe</strong> — kıyıda, orta risk. <strong>Foça, Çeşme, Seferihisar</strong> — kıyı dalgalarının oluşturduğu tsunami riski. <strong>Buca, Konak, Karabağlar</strong> — iç bölge, görece daha güvenli. <a href=\"/deprem-izmir.html\">İzmir deprem sayfamızda</a> detaylı harita var."),
            ("Derslar ve Şimdi Ne Var?", "2020 sonrası İzmir Büyükşehir kentsel dönüşüm planlarını hızlandırdı. <strong>Bayraklı</strong> artık \"riskli bölge\" olarak işaretlendi. Binaların %30'u 2000 öncesi yapım — güçlendirme veya yeniden yapım süreci devam ediyor. Ege Üniversitesi ve İzmir Yüksek Teknoloji Enstitüsü deprem araştırma merkezlerini genişletti."),
        ],
        "faq": [
            ("2020 depremi ne kadar hasar yaptı?", "117 can kaybı, 1.035 yaralı, 11 bina tam çöküş, yüzlerce hasarlı bina, 40 milyar TL ekonomik hasar."),
            ("İzmir'de tsunami riski var mı?", "Evet, özellikle Çeşme ve Foça kıyılarında. Ege Denizi tarihsel tsunamileri kayıtlıdır. 2020'de İzmir körfezinde 1.5-2 metrelik bir mini tsunami görüldü."),
            ("İzmir'de yaşıyorsam ne yapmalıyım?", "Binanızın 2000 öncesi yapım olup olmadığını öğrenin. Eskiyse güçlendirme veya yeniden yapım düşünün. DASK mutlaka. Ege Üniversitesi'nin ücretsiz deprem eğitimlerine katılın."),
        ],
    },
    {
        "slug": "blog-marmara-depremi-1999-dersler",
        "title": "Marmara Depremi 1999 – 25 Yılda Ne Değişti?",
        "desc": "17 Ağustos 1999 Gölcük depremi sonrası Türkiye'de deprem güvenliğinde değişen 10 şey: yapı yönetmeliği, DASK, AFAD, eğitim ve daha fazlası.",
        "keywords": "1999 marmara depremi, gölcük depremi, 17 ağustos, deprem yönetmeliği, dask kuruluş",
        "hero_img": "blog-marmara-depremi-1999-dersler.webp",
        "lead": "17 Ağustos 1999 sabah 03:02. Mw 7.6 Gölcük depremi Türkiye'yi uyandırdı. 17 binden fazla can kaybı, 250 binden fazla bina hasarı. 25 yıl sonra, o depremin Türkiye'yi ne kadar değiştirdiğine bakalım.",
        "sections": [
            ("1. Deprem Yönetmeliği: 1998 → 2007 → 2019", "1998 yönetmeliği 1999 sonrası ciddi şekilde güncellendi. <strong>2007 Deprem Yönetmeliği</strong> etken tasarım, yük değerlendirmesi ve dayanım hesaplamalarını modernize etti. <strong>2019 Türkiye Bina Deprem Yönetmeliği (TBDY)</strong> ise Avrupa Eurocode 8 standartlarına yaklaştı. Yeni yapımlarda spektral değer, performans analizi zorunlu."),
            ("2. DASK: Zorunlu Deprem Sigortası Kuruldu", "27 Aralık 1999'da DASK (Doğal Afet Sigortaları Kurumu) kuruldu. 2000'den itibaren tüm tapulu konutlar için zorunlu hale geldi. 2023 Kahramanmaraş depremlerinde DASK <strong>250 milyar TL</strong> tazminat ödedi. <a href=\"/blog-dask-nedir.html\">Detaylı DASK rehberimiz burada</a>."),
            ("3. AFAD Kuruluşu (2009)", "Eski dağınık afet yönetimi (Kızılay, Sivil Savunma, Turkey Emergency) 2009'da AFAD (Afet ve Acil Durum Yönetimi Başkanlığı) adıyla birleştirildi. Bugün 81 il müdürlüğü var, 10.000+ personel, düzenli tatbikatlar ve erken uyarı sistemi kurulum süreci."),
            ("4. Kentsel Dönüşüm Yasası (2012)", "6306 sayılı kanun \"Riskli Alanların Dönüştürülmesi\" — deprem riskli yapı stoku ile başa çıkma mekanizması. Riskli bina raporu çıkarılırsa 60 gün içinde boşaltma, güçlendirme veya yıkım zorunlu. 2026 itibarıyla 3.5 milyon riskli bina dönüştürüldü."),
            ("5. Okul Eğitimi ve Tatbikatlar", "1999 sonrası tüm okullarda yıllık deprem tatbikatları zorunlu. Çocuklar çök-kapan-tutun hareketini ilkokulda öğrenir. AFAD'ın \"Sıfır Afet Okulu\" programı ile 20 milyon öğrenciye ulaşıldı."),
            ("6. Bilimsel Araştırma Yatırımı", "TÜBİTAK MAM (Marmara Araştırma Merkezi), Boğaziçi Kandilli, Gebze Teknik Üniversitesi, İstanbul Teknik Üniversitesi deprem araştırma merkezlerine büyük yatırımlar yapıldı. GPS ölçüm ağı, sismograf istasyonları 10x arttı."),
            ("7. Erken Uyarı Sistemi Başlangıcı", "Japonya modelinde erken uyarı sistemi pilot olarak İstanbul'da 2009'da başladı. 2023'te tam sistem devreye girdi — <a href=\"/blog-deprem-erken-uyari-sistemi.html\">detaylı bilgi burada</a>."),
            ("8. Kamu Binalarında Güçlendirme", "1999 sonrası tüm hastane, okul, belediye, idari binaların deprem güçlendirmesi zorunlu hale geldi. 2026 itibarıyla %90 tamamlandı. Bu, acil durum sonrası kamu hizmetlerinin süreklilik kazanmasını sağlıyor."),
            ("9. Yeni İmar Planları ve Zemin Etüdü", "1999 öncesi imar planları zemin etüdü içermezdi. Şimdi <strong>her parsel için jeolojik-jeoteknik etüt</strong> zorunlu. Alüvyon ve dere yatağı bölgelerinde yüksek kat yapılaşma yasaklandı."),
            ("10. Bireysel Farkındalık", "En önemli değişim bireysel hazırlıkta. 1999'da deprem çantası, tatbikat, toplanma alanı bilmek azdı. Bugün <strong>1 milyondan fazla</strong> Türk aile düzenli tatbikat yapıyor. <a href=\"/deprem-sehirleri.html\">Bizim 81 il sayfamız</a> gibi kaynaklarla bilinç her yıl yükseliyor."),
        ],
        "faq": [
            ("1999 depremi neden bu kadar yıkıcıydı?", "Mw 7.6 büyüklük + gece 03:02'de (herkes uyurken) + sahil alüvyon zemin + düşük yapı kalitesi + yangınlar. Hepsi birleştiğinde 17 bin can kaybına vardı."),
            ("Bugün aynı büyüklükte bir deprem olsa ne olurdu?", "Yeni binalar güvenli ama 1999 öncesi stok hala %30. Tahmini 30.000-50.000 ölü ve 300 milyar TL hasar — 1999'dan az ama hala çok yüksek."),
            ("O dönemden sonra hangi deprem unutulmaz?", "2011 Van Mw 7.2, 2020 İzmir-Samos Mw 6.9, 2023 Kahramanmaraş Mw 7.8+7.6 — her biri Türkiye deprem literatürüne önemli dersler ekledi."),
        ],
    },
    {
        "slug": "blog-kahramanmaras-6-subat-dersler",
        "title": "Kahramanmaraş 6 Şubat Depremleri – Dersler ve Sonuçlar",
        "desc": "6 Şubat 2023 Kahramanmaraş ikiz depremleri (Mw 7.8 + Mw 7.6) ne öğretti? 11 il, 50 bin kayıp ve yapı güvenliği dersleri.",
        "keywords": "6 şubat depremi, kahramanmaraş depremi, 2023 deprem, pazarcık elbistan depremi",
        "hero_img": "blog-kahramanmaras-6-subat-dersler.webp",
        "lead": "6 Şubat 2023 sabah 04:17'de yaşanan Mw 7.8 Pazarcık depremi ve 13:24'te Mw 7.6 Elbistan depremi, Türkiye tarihinin en yıkıcı afetiydi. 11 il, 50 binden fazla can kaybı. 3 yıl sonra nereye geldik?",
        "sections": [
            ("Ne Oldu?", "Doğu Anadolu Fay Hattı'nın Doğanşehir, Pazarcık ve Elbistan segmentleri kırıldı. İlk deprem Pazarcık'ta Mw 7.8, 9 saat sonra Elbistan'da Mw 7.6 — iki ayrı ana deprem. Toplam enerji 1939 Erzincan ve 1999 Gölcük'ü geride bıraktı. <strong>11 il</strong> etkilendi: Kahramanmaraş, Hatay, Gaziantep, Adıyaman, Malatya, Osmaniye, Diyarbakır, Elazığ, Şanlıurfa, Adana, Kilis."),
            ("Kayıplar ve Hasar", "<strong>50.000+ vefat, 107.000 yaralı, 3 milyon kişi evsiz</strong>. 520.000 bina hasar raporlandı, 170.000'i tamamen çöktü. Hatay, Antakya'da tarihi yapıların çoğu yok oldu. Ekonomik hasar 3.5 trilyon TL tahmini (GDP'nin %10'u)."),
            ("Neden Bu Kadar Büyük?", "<strong>1.</strong> Ana depremler Mw 7.8 + Mw 7.6 — çok büyük enerji. <strong>2.</strong> Sarsıntı süresi 45+ saniye. <strong>3.</strong> Sabahın 04:17'sinde olması (herkes uyurken). <strong>4.</strong> Yapı kalitesi zayıflığı — 2018 öncesi yönetmelik ile yapılan binaların çoğu çöktü. <strong>5.</strong> Beton kalite denetim zafiyeti — sonraki soruşturmalarda müteahhit-denetim firması bağlantıları çıktı."),
            ("Hatay'da Olağandışı Yıkım", "Antakya merkezi %80 yıkıldı. Sebep: <strong>Amik Havzası alüvyon zemini</strong> — sarsıntıyı 3-4 kat güçlendirdi. Ayrıca tarihi merkezde 1950-70 yapımı yığma binalar yoğundu — deprem yönetmeliği yoktu o dönemde."),
            ("Yapılan Değişiklikler", "2023 sonrası: <strong>1.</strong> Yapı denetim firmalarına ağır denetim ve yaptırım. <strong>2.</strong> Müteahhitler için zorunlu sorumluluk sigortası (SSK). <strong>3.</strong> \"Dirençli Kent\" programı — 11 ilde 500 milyar TL yeniden yapım. <strong>4.</strong> Beton kalite kontrol standartları sıkılaştırıldı. <strong>5.</strong> Kentsel dönüşüm hızlandırıldı — DAF boyunca tüm iller. <strong>6.</strong> DASK azami teminat 640.000 TL'ye çıkarıldı (önceki 320.000)."),
            ("Ne Öğrendik?", "<strong>1.</strong> DAF şaka değil — İstanbul depreminden önce bile büyük risk. <strong>2.</strong> Yapı denetim güvenilirliği tüm ülke için kritik. <strong>3.</strong> Kolektif psikolojik destek organizasyonu geliştirildi (AFAD Psikososyal Destek). <strong>4.</strong> Arama kurtarma AKUT+ekipleri genişletildi. <strong>5.</strong> Mobil hastaneler ve sahra hastaneleri hazırlığı yasal zorunluluk. <strong>6.</strong> <a href=\"/blog-deprem-sonrasi-ilk-24-saat.html\">72 saat kuralı</a> daha çok vurgulandı."),
        ],
        "faq": [
            ("Etkilenen 11 il hangileri?", "Kahramanmaraş, Hatay, Gaziantep, Adıyaman, Malatya, Osmaniye, Diyarbakır, Elazığ, Şanlıurfa, Adana, Kilis."),
            ("Yeniden yapım ne kadar sürecek?", "Tahminen 7-10 yıl. 2030 itibarıyla asıl hasarlı konutların yeniden yapımı beklenmektedir. Hatay merkez için 15+ yıl."),
            ("Benzer deprem bir daha olabilir mi?", "DAF hala aktif. Gerilim bölgelerde biriktiğinden 20-50 yıl arası başka bir büyük deprem olasılığı yüksek."),
        ],
    },
    {
        "slug": "blog-van-depremi-2011-dersler",
        "title": "Van Depremi 2011 – 15 Yıl Sonra Neler Öğrendik?",
        "desc": "23 Ekim 2011 Van-Erciş Mw 7.2 depremi: 600+ can kaybı, Bayram Oteli hatırası, Doğu Anadolu'da soğuk kış ve dersler.",
        "keywords": "van depremi, 2011 erciş depremi, van 23 ekim, bayram oteli van",
        "hero_img": "blog-van-depremi-2011-dersler.webp",
        "lead": "23 Ekim 2011 saat 13:41'de Van-Tabanlı'da Mw 7.2 büyüklüğünde deprem oldu. 604 kişi vefat etti. 15 yıl sonra Van'da hala izler var. Bu deprem Türkiye'ye neyi öğretti?",
        "sections": [
            ("Deprem Ne Oldu?", "23 Ekim 2011 Pazar, 13:41. Van'ın kuzeyindeki Tabanlı köyü yakınında, derinlik 7-10 km. <strong>Erciş</strong> ilçesinde en büyük hasar yaşandı — 11 bina çökmüş. Yüzlerce enkaz altında kalan oldu. Yaşanan soğuk hava (gece eksi 10°C'ye düşen sıcaklıklar) kurtarma sürecini zorlaştırdı."),
            ("9 Kasım'daki İkinci Deprem", "9 Kasım 2011'de Mw 5.6 bir artçı, asıl depremde hasar görmüş Bayram Oteli'nin tamamen çökmesine sebep oldu. Bu artçı 40+ kişinin hayatını kaybettiği bir felaket oldu. Bu olay <strong>artçıların \"küçük\" olduğunu düşünmeyin, hasarlı binaları yıkar</strong> dersini bıraktı."),
            ("Soğuk Hava ve Tahliye Zorluğu", "Ekim sonu Doğu Anadolu'da sıcaklık eksiye düşer. Enkazdan çıkarılanlar üşüdü, çadır kentler ısınamadı. Bu deneyim sonrası AFAD <strong>Kış Acil Eylem Planı</strong> geliştirdi: eksi 20'ye kadar ısıtma kapasitesi, termal battaniyeler, sıcak içecek dağıtımı."),
            ("Yapı Kalitesi Zayıflığı", "Van'daki çöken binaların %80'i <strong>kaçak</strong> inşaattı — ruhsatsız veya plan dışı. Deprem yönetmeliğine uyulmamıştı. Bu olay Türkiye'nin yapı denetim reformunu hızlandıran etmendir."),
            ("Van'ın Yeniden Yapımı", "Van Büyükşehir Belediyesi ve TOKİ ortaklığıyla 15.000+ yeni konut inşa edildi. \"Depremzede Evleri\" projesi hala örnek bir kentsel dönüşüm modeli olarak anlatılıyor. Bugün Van merkezde eski binaların %60'ı yenilenmiş durumda."),
            ("2026'da Van'da Durum", "2026 itibarıyla Van, Doğu Anadolu'nun en çok yenilenmiş şehri. <strong>Yeni binaların %100'ü 2019 yönetmeliğine göre</strong>. Yine de köy yerleşimlerinde yığma ve kerpiç yapılar dikkat gerektirir. <a href=\"/deprem-van.html\">Van deprem sayfamızda</a> detaylı bilgi var."),
        ],
        "faq": [
            ("Van depreminde kaç kişi vefat etti?", "Resmi rakam 604 (Van il merkezi + Erciş + diğer). Bayram Oteli faciasında ek 40+ kayıp."),
            ("Bayram Oteli hikayesi ne?", "İlk depremde hasar gören otel, 9 Kasım artçısında tamamen çöktü. Enkaz altında Kanada'dan gelen yardım gazeteci dahil pek çok kişi vardı."),
            ("Van'da bir daha büyük deprem olur mu?", "Van Gölü'nün doğusundaki faylar hala aktif. 50-100 yıl aralığında Mw 7+ deprem olasılığı yüksek."),
        ],
    },
    # --- Group D: Informational ---
    {
        "slug": "blog-deprem-cep-telefonu",
        "title": "Deprem ve Cep Telefonu: Doğrular ve Yanlışlar",
        "desc": "Deprem sırasında ve sonrasında cep telefonu nasıl kullanılır? SMS mi arama mı? Batarya ekonomisi, baz istasyonu çökmesi ve iletişim önerileri.",
        "keywords": "deprem cep telefonu, deprem sms, deprem baz istasyonu, deprem iletişim",
        "hero_img": "blog-deprem-cep-telefonu.webp",
        "lead": "Deprem olunca herkes ailesini aramaya çalışır. Ama işte tam burada en büyük yanlışları yapıyoruz. Deprem sonrası cep telefonu kullanımı hakkında bilmeniz gerekenler.",
        "sections": [
            ("Arama Yerine SMS Kullanın", "Deprem sonrası baz istasyonları aşırı yüklenir — aynı anda 100.000+ kişi arama yapmaya çalışır. <strong>Arama %90 başarısız olur ve şebekeyi daha da tıkar</strong>. SMS ise geçici \"kuyruk sistemi\" ile sırayla gönderilir, başarı oranı çok yüksektir. 2023 Kahramanmaraş'ta SMS gidişatı %70, arama %15 başarılıydı. <strong>Önce SMS atın, sonra arayın.</strong>"),
            ("Mesajlaşma Uygulamaları Doğru Mu?", "WhatsApp, Telegram, Signal gibi internet tabanlı uygulamalar — mobil veri çalışıyorsa — SMS'ten daha güvenilir. <strong>WhatsApp konum paylaşımı</strong> özellikle enkaz altında kalanlar için hayat kurtardı 2023'te. Canlı konum özelliğini aktif edin, aileniz sizin yerinizi gerçek zamanlı görsün."),
            ("Batarya Ekonomisi", "Deprem sonrası elektriksiz 48-72 saat geçirebilirsiniz. Bataryanızı koruyun: <strong>1.</strong> Uçak modunu aktif tutun — sadece mesaj atarken açın. <strong>2.</strong> Ekran parlaklığını minimuma al. <strong>3.</strong> Sosyal medya, YouTube, oyun kapalı. <strong>4.</strong> Bildirimleri kapatın. Bu önlemlerle 48+ saat batarya dayanabilir."),
            ("Güç Bankası Şart", "Deprem çantasında <strong>minimum 20.000 mAh güç bankası</strong> olsun. Cep telefonu 3-4 kez tam şarj edebilecek kapasite. <strong>Solar güç bankası</strong> ek bonus — elektriksiz bölgede güneş varsa işe yarar."),
            ("Baz İstasyonu Çökmesi Durumu", "Büyük depremlerde baz istasyonlarının %30-50'si çökebilir (elektrik kesintisi, yapı hasarı, kablo kopması). Böyle durumda <strong>Bluetooth Mesh networkler</strong> (Bridgefy gibi uygulamalar) internetsiz mesaj gönderir — 100 metre mesafede olan diğer telefonlara atlayarak uzağa iletilir. 2023'te enkaz altında kalanlar bu teknikle kurtarıldı."),
            ("Yararlı Uygulamalar", "<strong>AFAD Acil</strong> (Android/iOS): ücretsiz, deprem uyarısı ve yakındaki toplanma alanı. <strong>Twitter/X</strong>: hashtag (#deprem, #depremoldu) ile canlı bilgi akışı. <strong>Bridgefy</strong>: offline mesh mesajlaşma. Bizim <a href=\"/\">canlı deprem haritamız</a> ve <a href=\"/son-dakika-deprem.html\">son dakika sayfası</a> web push bildirimi gönderiyor — ayarlardan aktif edin."),
        ],
        "faq": [
            ("Deprem sırasında kameraya çekmeli miyim?", "Hayır! Sarsıntı sırasında önceliğiniz <a href=\"/deprem-aninda.html\">çök-kapan-tutun</a>. Kamera önemli değil. Sadece güvendeyseniz sarsıntı sonrası çekim yapabilirsiniz."),
            ("112'yi arayabilecek miyim?", "Acil durumlarda 112 önceliklendirilir ama hat tıkanık olabilir. Eğer 3 kez denemede bağlanmazsanız <strong>AFAD Acil uygulamasından</strong> konum paylaşımı yapın — hızlı yanıt alırsınız."),
            ("İnterneti kapatsam batarya daha mı uzun sürer?", "Uçak modu, wifi/bluetooth/mobil data'yı tamamen kapatır — batarya %40-60 daha uzun dayanır. Sadece mesaj atarken açıp kapatın."),
        ],
    },
    {
        "slug": "blog-deprem-sonrasi-psikolojik-destek",
        "title": "Deprem Sonrası Psikolojik Destek ve PTSD",
        "desc": "Deprem sonrası yetişkin ve çocuklarda travma belirtileri, PTSD nedir, ne zaman psikoloğa gidilir? Aile içi destek önerileri.",
        "keywords": "deprem travma, ptsd deprem, deprem psikolojik destek, deprem sonrası uyku",
        "hero_img": "blog-deprem-sonrasi-psikolojik-destek.webp",
        "lead": "Deprem fiziksel yıkımı görünür, psikolojik izleri ise haftalar, aylar hatta yıllar sonra ortaya çıkar. PTSD (Travma Sonrası Stres Bozukluğu) sıradan bir reaksiyon değil, klinik bir durumdur.",
        "sections": [
            ("İlk Günler: Normal Reaksiyonlar", "Deprem sonrası ilk 1-2 hafta yaşanan <strong>uyku bozukluğu, aşırı uyanıklık, ağlama krizleri, iştahsızlık, mide bulantısı</strong> — bunlar normal reaksiyonlardır. Beyin stresi işliyor. Bu dönemde aile sıcaklığı, sarılmalar, rutin aktiviteler iyileşmeyi destekler."),
            ("PTSD Belirtileri (3+ hafta)", "3 haftadan uzun süren şu belirtiler PTSD işareti: <strong>1.</strong> Deprem anını yeniden yaşama (flashback, kâbuslar). <strong>2.</strong> Aşırı tetiklenme — sert ses, sarsıntı hissi halüsinasyonları. <strong>3.</strong> Uyku bozukluğu — uyuyamama veya sık uyanma. <strong>4.</strong> Sosyal izolasyon — eski aktivitelerden kaçınma. <strong>5.</strong> Umutsuzluk, boş hissetme. <strong>6.</strong> Odaklanma güçlüğü, iş/okul performansı düşmesi. Bu belirtiler 1+ ay süren biri olmalı PSİKOLOĞA gitmeli."),
            ("Çocuklarda PTSD Belirtileri", "Çocuklar farklı şekilde gösterir: <strong>Regresyon</strong> (alt ıslatma, emzik isteme), <strong>okula gitmekten kaçınma</strong>, <strong>oyunlarda deprem temaları</strong>, <strong>karanlıktan ve sessizlikten korku</strong>, <strong>yeme-uyku bozuklukları</strong>. <a href=\"/blog-deprem-anketi-cocuklar.html\">Çocuk rehberimizde</a> detaylı bilgi var."),
            ("Kendinize Yardım Adımları", "<strong>1.</strong> Rutinleri koruyun — uyku, yemek, iş/okul aynı saatlerde. <strong>2.</strong> Haber akışını sınırlayın — saatlerce deprem haberi izlemek durumu kötüleştirir. <strong>3.</strong> Fiziksel egzersiz — yürüyüş, yoga, spor stres hormonlarını azaltır. <strong>4.</strong> Sosyalleşin — yalnız kalmayın, arkadaşlarla konuşun. <strong>5.</strong> Yazma — günlük tutma duyguları işlemeye yardım eder. <strong>6.</strong> Doğayla temas — orman yürüyüşü, deniz kıyısı iyileştirici."),
            ("Profesyonel Destek Ne Zaman?", "Şu durumlar mutlaka psikolog/psikiyatriste danışma gerektirir: <strong>1.</strong> İntihar düşünceleri. <strong>2.</strong> Günlük yaşamı etkileyen uyku bozukluğu. <strong>3.</strong> İş/okul devam edememe. <strong>4.</strong> Madde kullanımı (alkol, sakinleştirici). <strong>5.</strong> Aile ilişkilerinde ciddi bozulma. <strong>6.</strong> Ağlamayı durduramama."),
            ("Ücretsiz Kaynaklar", "<strong>AFAD Psikososyal Destek Hattı: 112</strong> (afet sonrası ücretsiz). <strong>Türkiye Psikiyatri Derneği</strong> afet sonrası ücretsiz destek grupları düzenler. <strong>Boğaziçi Üniversitesi Psikolojik Danışma</strong> (afet mağdurları için). Belediyelerin sosyal hizmet birimlerinden yönlendirme alabilirsiniz."),
        ],
        "faq": [
            ("PTSD kendiliğinden geçer mi?", "Bazı insanlarda geçici bir evre sonrasında kendiliğinden iyileşme olur ama <strong>%30-40</strong> vakada PTSD süreklidir ve tedavi gerektirir. Beklemek yerine erken destek almak iyileşme şansını artırır."),
            ("Çocuğum 1 yıl geçti hala kâbus görüyor, ne yapmalıyım?", "Mutlaka <strong>çocuk psikoloğuna</strong> götürün. Çocuk PTSD'si tedavi edilebilir ama erken müdahale kritik. Sanat terapisi, oyun terapisi çocuklarda çok etkilidir."),
            ("PTSD ilaç kullanmak zorunlu mu?", "Hayır. Hafif-orta vakalarda <strong>CBT (bilişsel davranışçı terapi), EMDR, grup terapisi</strong> yeterlidir. İlaç ağır vakalarda psikiyatrist tarafından önerilir."),
        ],
    },
    {
        "slug": "blog-tbdy-2019-nedir",
        "title": "TBDY 2019 Nedir? Deprem Yönetmeliği Değişiklikleri",
        "desc": "Türkiye Bina Deprem Yönetmeliği 2019 (TBDY) ne getirdi? 2007 yönetmeliği ile farkları, performans hedefleri ve yapı sahipleri için anlamı.",
        "keywords": "tbdy 2019, deprem yönetmeliği, türkiye bina yönetmeliği, yapı denetim",
        "hero_img": "blog-tbdy-2019-nedir.webp",
        "lead": "1 Ocak 2019'da yürürlüğe giren TBDY (Türkiye Bina Deprem Yönetmeliği) 2019, Türkiye'de yapılan tüm yeni binaları bağlıyor. 2007 yönetmeliğine göre ne değişti?",
        "sections": [
            ("TBDY 2019 Temelleri", "TBDY 2019, 2007 DBYBHY'nin genişletilmiş ve modernize edilmiş versiyonu. Avrupa Eurocode 8 standartlarıyla uyumlu. Temel fark: <strong>Performans bazlı tasarım</strong> — bir binanın 50 yıl, 475 yıl ve 2475 yıl içinde olma olasılığı olan farklı depremlere nasıl tepki vereceği hesaplanır. Önceki yönetmelikte tek deprem senaryosu kullanılırdı."),
            ("Yeni Spektral Tehlike Haritası", "Eski 1-4 deprem bölgesi haritası kaldırıldı. Yerine <strong>sürekli spektral hızlanma haritası</strong> geldi. Her koordinat için ayrı spektral değer hesaplanır. Türkiye Deprem Tehlike Haritası (TDTH) bu yönetmelikle eşlendi."),
            ("Zemin Sınıflandırması Yeni", "Eskiden 4 zemin sınıfı (A-B-C-D) vardı. TBDY 2019'da <strong>6 zemin sınıfı (ZA-ZF)</strong> var. ZA en sağlam kaya, ZF en zayıf alüvyon. Bu hassasiyet, alüvyonlu bölgelerdeki binaların daha dayanıklı tasarlanmasını sağlıyor."),
            ("Performans Hedefleri", "TBDY 2019'da 3 performans düzeyi tanımlanır: <strong>1. Kullanım Sürekliliği (KS):</strong> deprem sonrası bina hemen kullanılabilir. <strong>2. Hasar Sınırlı (HS):</strong> hasar var ama onarılabilir. <strong>3. Göçmenin Önlenmesi (GÖ):</strong> bina ayakta kalır, can kaybı yok. Her bina için hedef belirleniyor."),
            ("Yumuşak Kat ve Düzensizlikler", "Eski binalarda sıkça görülen <strong>yumuşak kat</strong> (zeminde mağaza + üstte konutlar) TBDY 2019'da özel önlem gerektiriyor. Kolon-kiriş oranları, perde duvar gereksinimleri sıkılaştırıldı. <strong>Düzensiz bina</strong> (L şekilli, T şekilli) tasarımlarda ek analizler zorunlu."),
            ("Sıkı Betonarme Kuralları", "<strong>Minimum beton sınıfı C25</strong> (eskiden C16 idi). <strong>Çelik B420c</strong> (süneklik daha yüksek). Kolonlarda etriye aralığı sıkılaştırıldı. Pas payı (betonu örten bölge) minimum 25 mm. Bu değişiklikler Kahramanmaraş sonrası 2025'te yeniden güncellendi."),
            ("Yapı Sahipleri İçin Ne Anlama Geliyor?", "<strong>2019 sonrası yapım binalar</strong> — TBDY 2019'a tam uyumlu, güvenli. <strong>2007-2018 arası binalar</strong> — orta-iyi güvenlik, güçlendirme opsiyonel. <strong>2007 öncesi binalar</strong> — risk var, güçlendirme veya yıkım düşünün. Binanızın yapım yılını belediyeden öğrenin, yapı denetim raporunu isteyin."),
        ],
        "faq": [
            ("TBDY 2019 öncesi yapılmış evim güvenli değil mi?", "Güvensiz değil ama TBDY 2019 standartlarında değil. Kiracı ise fark az; ev sahibi iseniz <a href=\"/blog-evim-depreme-dayanikli-mi.html\">ön kontrol yapın</a>, gerekirse statik rapor aldırın."),
            ("Yapı denetim firması neden önemli?", "Yapı denetim, müteahhitin inşaatta kurallara uymasını denetleyen bağımsız kuruluştur. TBDY 2019'un kağıtta değil gerçekte uygulandığını kontrol eder."),
            ("TBDY 2019 dünya standartlarının neresinde?", "Eurocode 8 (Avrupa) ve IBC (ABD) ile kıyaslanabilir düzeyde. Bazı konularda (zemin sınıflandırması) daha detaylı, bazılarında (performans sınıfları) aynı."),
        ],
    },
    {
        "slug": "blog-yapi-denetim-raporu-okuma",
        "title": "Yapı Denetim Raporu Nasıl Okunur?",
        "desc": "Binanızın yapı denetim raporu hangi bölümleri içerir, hangi değerler kritik? Rapor okuma rehberi ve kritik göstergeler.",
        "keywords": "yapı denetim raporu, bina kontrol, yapı denetim firması, statik rapor okuma",
        "hero_img": "blog-yapi-denetim-raporu-okuma.webp",
        "lead": "Yapı denetim raporu, binanızın inşaat sürecinde alınan kararları ve denetimi belgeler. Bu rapor kazılmış elmas kadar değerli — ancak çoğu kişi nasıl okunacağını bilmez.",
        "sections": [
            ("Yapı Denetim Raporu Nedir?", "4708 sayılı Yapı Denetimi Hakkında Kanun gereği tüm inşaatlar yapı denetim firmasının takibinde yapılır. Bu firma 5 aşamada rapor yazar: <strong>temel, bodrum kat, normal katlar, çatı ve bitiş</strong>. Her aşamada <strong>malzeme kalite raporları</strong>, <strong>ziyaret tutanakları</strong> ve <strong>uygunluk onayları</strong> vardır."),
            ("Nasıl Temin Edebilirim?", "Binanızın yapı denetim firması bilgisi tapuda veya belediyede kayıtlı. İlgili firmaya başvurup rapor isteyin — yasal olarak vermek zorundadırlar. Yapı sahibi değilseniz yöneticiliğe başvurun."),
            ("Beton Test Sonuçları Kritik", "Raporun en önemli bölümü <strong>beton kalite testleri</strong>'dir. 28 gün sonrası silindir testi sonuçları. Binanız için gerekli minimum: <strong>C25 (250 kgf/cm²)</strong>. Raporda C20, C16 gibi değerler varsa ciddi problem. C30+ ideal. Her bina katı için ayrı test sonuçları olmalı."),
            ("Çelik Donatı Bilgisi", "Kullanılan çelik sınıfı: <strong>B420c</strong> yeni standart, <strong>B500c</strong> ileri seviye. Donatı çapları, aralıkları kolon-kiriş detay çizimlerinde. Uzman gözle kontrol edilmeli ama raporda eksiksiz olması şart."),
            ("Uygunsuzluk Tutanakları", "Bu bölüm kritik — inşaat sırasında <strong>planı onaylanan kısımdan sapmalar</strong> kaydedilir. Örneğin plan 25 mm etriye aralığı öngördüğü halde uygulamada 30 mm atılmışsa uygunsuzluk tutanağı yazılır. Raporu incelerken bu tutanakların giderilip giderilmediğine bakın."),
            ("İskan Ruhsatı Uyumu", "Raporun son bölümünde <strong>iskan ruhsatı</strong> (yapı kullanma izni) verilmesi gerekir. Varsa bina teknik olarak tamamlanmış demektir. Yoksa inşaat yasal olarak bitmemiştir — ciddi sorun. Deprem anında hukuki problemler çıkar, DASK tazminat vermeyebilir."),
            ("Kimlere Sormalı?", "Rapor kafanızı karıştırıyorsa <strong>İnşaat Mühendisleri Odası</strong>'nın bulunduğunuz şubesine danışabilirsiniz. Bazı oda şubeleri ücretsiz ön danışma verir. Özel <strong>Sivil Yapı Değerlendirme Mühendisleri</strong> (1.500-5.000 TL) daha derinlemesine inceler."),
        ],
        "faq": [
            ("Yapı denetim firması raporu vermiyor, ne yapmalıyım?", "İl Çevre Şehircilik Müdürlüğü'ne şikayet edin. Yasal zorunluluktur — cezai yaptırımı var."),
            ("Rapor 10+ yaşında, hala geçerli mi?", "Evet, rapor bina yapım sürecini belgeler — yaşı önemli değil. Ama <strong>sonraki hasarlar</strong> (2011 Van, 2020 İzmir gibi) rapora eklenmemiş olabilir — ek gözlem gerekli."),
            ("İskan ruhsatsız evde DASK geçerli mi?", "Teknik olarak geçerli ancak <strong>tazminat ödenirken incelemede</strong> sorun çıkabilir. Kanunen ruhsatsız yapılara DASK primi alınmamalı — yine de uyarılmalısınız."),
        ],
    },
    {
        "slug": "blog-zorunlu-deprem-tatbikati",
        "title": "İşyerinde Deprem Tatbikatı Nasıl Yapılır?",
        "desc": "İşyerleri için zorunlu deprem tatbikatı düzenleme rehberi. 6331 sayılı kanun ne diyor? Tatbikat aşamaları, personel eğitimi ve belgeler.",
        "keywords": "işyeri deprem tatbikatı, iş güvenliği deprem, 6331 sayılı kanun, deprem tatbikat rehberi",
        "hero_img": "blog-zorunlu-deprem-tatbikati.webp",
        "lead": "6331 sayılı İş Sağlığı ve Güvenliği Kanunu gereği tüm işyerleri yılda en az 1 kez deprem tatbikatı yapmak zorunda. Ancak \"tatbikat\" çoğu kurumda simge kalıyor. Gerçekten hayat kurtaran bir tatbikat nasıl yapılır?",
        "sections": [
            ("Yasal Zorunluluk", "6331 sayılı kanun ve ilgili yönetmelikler gereği: <strong>Tehlike sınıfına göre</strong> yılda en az 1-2 tatbikat zorunludur. İşveren bu konuda sorumludur. Cezai yaptırım var — tatbikatsız veya usulsüz yapılan işyerlerine 30.000-300.000 TL ceza."),
            ("Ön Hazırlık", "Tatbikat tarihinden 1 hafta önce: <strong>1.</strong> Tüm personele bilgilendirme (mail/duyuru). <strong>2.</strong> İSG uzmanı eşliğinde ekip kurun: koordinatör, kat sorumluları, ilk yardımcılar. <strong>3.</strong> Toplanma alanını belirleyin. <strong>4.</strong> Kaçış rotalarını işaretleyin — panonlara talimat asın. <strong>5.</strong> Engelli personel için özel plan yapın."),
            ("Tatbikat Günü Adım Adım", "<strong>1. Siren (sabah 10:00'da ideal)</strong> — hazırlık sesi. <strong>2. Çök-Kapan-Tutun (30 saniye)</strong> — personel masanın yanına çöker, kafayı korur. <strong>3. Sarsıntı bitti anonsu</strong> — bekleyin. <strong>4. Tahliye sinyali</strong> — personel kaçış rotası üzerinden dışarı çıkar. ASANSÖR KULLANILMAZ. <strong>5. Toplanma alanı</strong> — her bölüm kendi toplanma yeri bilsin. <strong>6. Sayım</strong> — her bölüm sorumlusu personel sayımı yapar. <strong>7. Değerlendirme toplantısı</strong> — 30 dakika sonra tatbikat raporu."),
            ("Personel Eğitimi", "Tatbikat tek başına yetmez. Personele düzenli olarak: <strong>a)</strong> <a href=\"/deprem-aninda.html\">Çök-kapan-tutun eğitimi</a>. <strong>b)</strong> İlk yardım temeli (AED, KPR). <strong>c)</strong> Yangın söndürücü kullanımı. <strong>d)</strong> Kaçış rotası ezberi. <strong>e)</strong> Toplanma alanı tanımı. Yılda 1 kez 4 saatlik İSG oryantasyonu önerilir."),
            ("Engelliler ve Özel Durumlar", "Tekerlekli sandalyeli, görme engelli, işitme engelli personel için özel prosedür. <strong>Tahliye asistanı ataması</strong> — her engelli personel için bir yardımcı. <strong>Evakuasyon koltuğu</strong> (3-5 kişilik işyerlerinde 1 tane zorunlu). <strong>Görsel + sesli + titreşimli uyarı</strong> — her engel türü için uyarı yöntemi."),
            ("Değerlendirme Raporu", "Tatbikat sonrası rapor: <strong>a)</strong> Katılan personel sayısı. <strong>b)</strong> Tahliye süresi (ideali 3-5 dakika). <strong>c)</strong> Eksik veya hatalı davranışlar. <strong>d)</strong> Eksik ekipman (yangın söndürücü, aydınlatma). <strong>e)</strong> Bir sonraki tatbikat için öneriler. Raporu İSG dosyasına eklemek yasal zorunluluktur."),
        ],
        "faq": [
            ("Tatbikat olmadan İSG muayenesi geçmez mi?", "Hayır. İSG muayenesinde son tatbikat raporu istenebilir. Tatbikat eksikliği ciddi uygunsuzluk sayılır."),
            ("Küçük işyerlerinde (5 kişi) da gerekli mi?", "Evet. Yasa, 1 kişi bile olsa çalışan varsa tatbikat şartını koşuyor. Küçük işyerlerinde 15 dakikalık basit tatbikat yeterli."),
            ("Tatbikat fiilen ne kadar sürer?", "Tam kapsamlı: hazırlık + sarsıntı simülasyonu + tahliye + toplanma + değerlendirme = <strong>30-45 dakika</strong>. Büyük işyerlerinde 1 saat."),
        ],
    },
    {
        "slug": "blog-kadinlar-icin-deprem",
        "title": "Kadınlar İçin Deprem Hazırlığı ve Güvenlik",
        "desc": "Kadınlara özel deprem hazırlık rehberi: hamile, emzikli anneler ve bekar kadınlar için özel önlemler, tahliye ipuçları.",
        "keywords": "kadın deprem, hamile deprem, emzikli anne deprem, bekar kadın güvenliği",
        "hero_img": "blog-kadinlar-icin-deprem.webp",
        "lead": "Deprem hazırlığında cinsiyetsiz görünen öneriler, kadınların özel ihtiyaçlarını atlayabilir. Hamilelik, emzirme, kişisel bakım ve güvenlik için özel dikkat edilmesi gerekenler.",
        "sections": [
            ("Hamile Kadınlar İçin", "<strong>Gebelik boyunca deprem çantanızda</strong>: 10 günlük prenatal vitamin, doktor kayıtları fotokopisi, ultrason çıktıları, doğum hastanesi bilgisi. Sarsıntı sırasında: <strong>karnı koru</strong>, sırtüstü yatmayın (omurga üzerinde basınç), sol tarafa yan yatın. 3. trimesterda hızlı hareket zorsa yatakta kalın, yastıkla kaplanın."),
            ("Emzikli Anne ve Bebekle", "Bebek için: <strong>hazır mama</strong> (powder, sıcak suya ihtiyaç), <strong>biberon + yedek kapak</strong>, <strong>kundak ve bebek bezi</strong> (3 günlük), <strong>bebek bakım malzemeleri</strong> (sabun, krem, pomat). Emziren anne için: <strong>emzirme yastığı</strong> (taşınır), <strong>su</strong> (günde 3+ litre - emzirme için), <strong>hazır protein atıştırmalık</strong>. Deprem sonrası stres süt miktarını azaltabilir — panik olmayın, formül sütü yedek olarak hazır tutun."),
            ("Bekar Kadın / Yalnız Yaşayan İçin", "<strong>Komşu ağı</strong> çok önemli — apartmanda 2-3 kadınla özel WhatsApp grubu oluşturun, deprem sonrası birbirinizi kontrol edin. <strong>Panik butonu</strong> (4.000-10.000 TL) — yalnız düşme veya enkaz altında kalma durumunda yardım çağırır. <strong>Aileye uzak</strong> iseniz AFAD Özel İhtiyaç kaydı yapın."),
            ("Kişisel Bakım Malzemeleri", "<strong>Hijyen paketi</strong>: kadın tamponu (30 günlük), temizlik mendili, kişisel sabun. <strong>Yedek iç çamaşır</strong> (5 adet). <strong>Kozmetik minimum</strong> — gereksiz eşya çantayı şişirir. <strong>Doğum kontrol hapı</strong> (kullanıyorsan) 2 aylık stok — düzenli doz kaçırmak ciddi sorun."),
            ("Güvenlik Konuları", "Deprem sonrası kaotik ortamda <strong>kadın güvenliği</strong> riskleri artabilir. Çantanızda: <strong>düdük</strong> (tekrar önlem), <strong>biber spreyi</strong> (yasal olanını kontrol edin), <strong>alarm cihazı</strong>, <strong>küçük el feneri</strong>. Yalnız geceleri dışarıda kalmayın — güvenilir toplanma alanı veya refakatçi tercih edin. <strong>ÇocukAile temsilci merkezleri</strong> kadınlara öncelikli yardım sağlar."),
            ("Psikolojik Destek", "<strong>Dünya sağlık örgütü verileri</strong>: afet sonrası PTSD kadınlarda erkeklerden 2 kat daha yaygın. Özellikle aynı zamanda bakım sorumluluğu (çocuk, yaşlı) taşıyan kadınlar risk altında. <a href=\"/blog-deprem-sonrasi-psikolojik-destek.html\">Psikolojik destek rehberimiz</a> detaylı bilgi veriyor."),
        ],
        "faq": [
            ("Hamileyim, deprem sırasında ne yapmalıyım?", "Karnı koruyun — <strong>dizlerinizin üzerine değil yan yatın</strong>. Bebek pozisyonuna girin, sırtınızı sağlam bir şeye dayayın. Eller başını koru."),
            ("Doğum hastanesim deprem sonrası ulaşılmaz olursa?", "Çantanızda <strong>alternatif hastane listesi</strong> olsun — 3 hastane, telefon numarası ve adresi. AFAD Acil uygulaması size en yakın hastaneyi gösterir."),
            ("Bekar kadın olarak tek başıma güvende hissetmiyorum, ne yapmalıyım?", "Komşularla kişisel ilişki kurun, apartmanda kadın arkadaşlık grubu oluşturun. AFAD Özel İhtiyaç kaydı yapın. Panik butonlu cihaz alın."),
        ],
    },
]

# --- HTML Template ---
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
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="Emin Kılıç">
    <link rel="canonical" href="https://yakinimdakideprem.com/{slug}.html" />
    <meta property="og:locale" content="tr_TR">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="https://yakinimdakideprem.com/{slug}.html">
    <meta property="og:site_name" content="Yakınımdaki Deprem">
    <meta property="og:image" content="https://yakinimdakideprem.com/images/{hero_img}">
    <meta property="og:image:alt" content="{title} görseli">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="https://yakinimdakideprem.com/images/{hero_img}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" media="print" onload="this.media='all'">
    <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"></noscript>
    <link rel="stylesheet" href="css/style.min.css?v=202604201000">
    <link rel="stylesheet" href="css/header.min.css?v=202604201000">
    <link rel="stylesheet" href="css/blog-detail.css?v=2026011231">
    <link rel="stylesheet" href="css/city-search.css?v=202604201000">
    <link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32x32.png">
    <link rel="manifest" href="site.webmanifest">
    <script type="application/ld+json">
{article_schema}
    </script>
    <script type="application/ld+json">
{breadcrumb_schema}
    </script>
    <script type="application/ld+json">
{faq_schema}
    </script>
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
                        <a href="/blog.html">Blog</a>
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
    <main class="blog-detail-container">
        <article>
            <div class="blog-hero" style="background-image: url('images/{hero_img}');">
                <div class="overlay"></div>
                <div class="hero-content">
                    <h1>{title}</h1>
                    <div class="meta">
                        <span><i class="far fa-calendar" aria-hidden="true"></i> {today}</span>
                        <span><i class="far fa-user" aria-hidden="true"></i> Emin Kılıç</span>
                    </div>
                </div>
            </div>
            <div class="content container">
                <p class="lead">{lead}</p>
{sections_html}

                <h2>İlgili Rehberler</h2>
                <ul>
                    <li><a href="/blog-deprem-oncesi-hazirlik.html">Deprem Öncesi Hazırlık</a></li>
                    <li><a href="/blog-deprem-cantasi.html">Deprem Çantası Listesi 2026</a></li>
                    <li><a href="/blog-dask-nedir.html">DASK Zorunlu Deprem Sigortası</a></li>
                    <li><a href="/deprem-sehirleri.html">81 İl Deprem Risk Haritası</a></li>
                    <li><a href="/blog.html">Tüm Deprem Rehberleri</a></li>
                </ul>
            </div>
        </article>
    </main>
    <footer>
        <div class="container">
            <p>&copy; 2026 Yakınımdaki Deprem. Tüm hakları saklıdır.</p>
        </div>
    </footer>
    <script src="js/header.min.js?v=202604201000" defer></script>
    <script src="js/city-keywords.js?v=202604201000" defer></script>
    <script src="js/city-search.js?v=202604201000" defer></script>
</body>
</html>
"""


def get_image_dimensions(filename):
    """Gorsel boyutlarini Pillow ile oku."""
    from PIL import Image
    path = PUBLIC / "images" / filename
    if path.exists():
        try:
            with Image.open(path) as im:
                return im.size
        except Exception:
            pass
    return (1200, 630)  # fallback OG standart


def build_image_object(filename, description):
    """Rich ImageObject - Google Image SEO icin tum alanlari doldurur."""
    width, height = get_image_dimensions(filename)
    return {
        "@type": "ImageObject",
        "url": f"https://yakinimdakideprem.com/images/{filename}",
        "width": width,
        "height": height,
        "caption": description,
        "description": description,
        "creditText": "Yakınımdaki Deprem",
        "copyrightNotice": "© 2026 Yakınımdaki Deprem - Emin Kılıç",
        "license": "https://yakinimdakideprem.com/kullanim-sartlari.html",
        "acquireLicensePage": "https://yakinimdakideprem.com/iletisim.html",
        "creator": {"@type": "Person", "name": "Emin Kılıç", "url": "https://yakinimdakideprem.com/ben-kimim.html"},
        "copyrightHolder": {"@type": "Organization", "name": "Yakınımdaki Deprem"},
    }


def build_article_schema(data):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": data["title"],
        "description": data["desc"],
        "image": build_image_object(data["hero_img"], data["title"]),
        "author": {"@type": "Person", "name": "Emin Kılıç", "url": "https://yakinimdakideprem.com/ben-kimim.html"},
        "publisher": {
            "@type": "Organization", "name": "Yakınımdaki Deprem",
            "url": "https://yakinimdakideprem.com",
            "logo": {"@type": "ImageObject", "url": "https://yakinimdakideprem.com/icons/android-chrome-512x512.png", "width": 512, "height": 512}
        },
        "datePublished": TODAY,
        "dateModified": TODAY,
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://yakinimdakideprem.com/{data['slug']}.html"},
        "inLanguage": "tr-TR",
        "copyrightYear": 2026,
        "copyrightHolder": {"@type": "Organization", "name": "Yakınımdaki Deprem"},
    }, ensure_ascii=False, indent=2)


def build_breadcrumb_schema(data):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": "https://yakinimdakideprem.com/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://yakinimdakideprem.com/blog.html"},
            {"@type": "ListItem", "position": 3, "name": data["title"]},
        ]
    }, ensure_ascii=False, indent=2)


def build_faq_schema(faq_list):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq_list
        ]
    }, ensure_ascii=False, indent=2)


def build_sections_html(sections):
    out = []
    for heading, body in sections:
        out.append(f"                <h2>{heading}</h2>\n                <p>{body}</p>")
    return "\n".join(out)


def render_blog(data):
    return TEMPLATE.format(
        slug=data["slug"],
        title=data["title"],
        desc=data["desc"],
        keywords=data["keywords"],
        hero_img=data["hero_img"],
        today=TODAY,
        lead=data["lead"],
        sections_html=build_sections_html(data["sections"]),
        article_schema=build_article_schema(data),
        breadcrumb_schema=build_breadcrumb_schema(data),
        faq_schema=build_faq_schema(data["faq"]),
    )


def main():
    written = 0
    for data in BLOGS:
        target = PUBLIC / f"{data['slug']}.html"
        html = render_blog(data)
        target.write_text(html, encoding="utf-8")
        # Word count
        import re
        words = len(re.findall(r"\b\w+\b", re.sub(r"<[^>]+>", " ", html)))
        print(f"  ✓ {data['slug']:<42} {words:>4} kelime, {len(html)//1024}KB")
        written += 1
    print(f"\n{written} blog yazisi uretildi.")


if __name__ == "__main__":
    main()

# ── 10 YENİ BLOG (Nisan 2026 ek) ────────────────────────────────────────
NEW_BLOGS_APRIL = [
]
