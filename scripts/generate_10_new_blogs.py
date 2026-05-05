#!/usr/bin/env python3
"""10 yeni blog yazisi - Mayis 2026 eki. Mevcut 34 blogla sifir keyword çakismasi."""
from __future__ import annotations
import json
from pathlib import Path
from PIL import Image

PUBLIC = Path(__file__).resolve().parent.parent / "public"
TODAY = "2026-04-27"

NEW_BLOGS = [
    {
        "slug": "blog-konut-sigortasi-vs-dask",
        "title": "Konut Sigortası mı DASK mi? Fark ve Birlikte Almanın Önemi",
        "desc": "Konut sigortası ile DASK arasındaki fark nedir? Hangisi hangi hasarı karşılar? 2026 fiyat karşılaştırması ve birlikte alma rehberi.",
        "keywords": "konut sigortası, konut sigortası ve dask, konut sigortası nedir, dask farkı, ev sigortası deprem",
        "hero_img": "blog-konut-sigortasi-vs-dask.webp",
        "lead": "DASK yaptırdım, evim sigortalı — düşünce doğru, ama eksik. Çoğu kişi DASK'ın eşyaları, yangını veya su baskınını kapsamadığını deprem olduktan sonra öğreniyor. İşte iki sigortanın tam karşılaştırması.",
        "sections": [
            ("DASK Neyi Karşılar, Neyi Karşılamaz?", "DASK (Zorunlu Deprem Sigortası) sadece binanın <strong>yapısal elemanlarını</strong> kapsar: temel, duvarlar, çatı, merdivenler, asansörler. <strong>Kesinlikle kapsamadıkları:</strong> mobilya, elektronik, giysi, mutfak eşyası — yani \"ev içindeki her şey\". Ayrıca deprem sonrası yangın, su baskını, hırsızlık ve kira kaybı da DASK dışındadır. 2026 azami teminatı 640.000 TL."),
            ("Konut Sigortası Ne Kapsar?", "Konut sigortası <strong>isteğe bağlı</strong> olup bina + eşya hasarlarını aynı anda karşılar. Tipik bir konut sigortası poliçesi: <strong>Yangın, infilak, su baskını, fırtına, deprem (ek teminat), hırsızlık, cam kırılması, elektronik cihaz</strong> — hepsi tek poliçede. Yıllık ortalama 2.000-8.000 TL arasında değişir (konutun m² ve konumuna göre)."),
            ("Deprem Ek Teminatı Aldatmacası", "Dikkat: Konut sigortasına 'deprem ek teminatı' ekletseniz bile bu DASK'ın yerini tutmaz. Konut sigortası deprem teminatı <strong>genelde eşya ve iç dekorasyon hasarlarını</strong> kapsar; binanın yapısal hasarını değil. Bina hasarı için DASK zorunlu olmaya devam eder."),
            ("2026 Fiyat Karşılaştırması", "<strong>DASK (100 m², 1. bölge):</strong> yaklaşık 300-500 TL/yıl. <strong>Konut sigortası (100 m², İstanbul):</strong> yaklaşık 2.500-6.000 TL/yıl. <strong>İkisini birden almanın maliyeti:</strong> yılda 3.000-7.000 TL. Bu maliyet, bir deprem sonrasında 50.000+ TL eşya hasarını veya 200.000+ TL bina hasarını karşılamasının karşısında son derece mantıklı. <a href='/blog-dask-nedir.html'>DASK detayları için tıklayın</a>."),
            ("Hangi Durumda Ne İşe Yarar?", "Senaryolar: <strong>Depremde bina çöktü →</strong> DASK bina tazminatı öder, konut sigortası eşya tazminatı öder. <strong>Komşu dairenin borusu patladı →</strong> DASK ödemez, konut sigortası su hasarı öder. <strong>Hırsız girdi →</strong> DASK ödemez, konut sigortası hırsızlık teminatı öder. <strong>Deprem sırasında yangın çıktı →</strong> Her ikisi de öder (bina hasarı DASK, eşya hasarı konut). Yani ikisi birbirinin rakibi değil, tamamlayıcısıdır."),
            ("Nasıl Yaptırılır?", "Her iki sigortayı da aynı sigorta acentesinden yaptırabilirsiniz. Aynı firmadan alırsanız genellikle %10-15 indirim uygulanır. Online olarak <a href='https://dask.gov.tr' target='_blank' rel='noopener noreferrer'>dask.gov.tr</a> üzerinden DASK, herhangi bir yetkili sigorta şirketinin sitesinden konut sigortası alabilirsiniz. <a href='/deprem-sehirleri.html'>Şehrinizin deprem risk profilini</a> öğrenerek ihtiyacınıza uygun teminat seviyesini belirleyin."),
        ],
        "faq": [
            ("DASK olmadan konut sigortası yaptırabilir miyim?", "Evet, konut sigortasında DASK zorunluluğu yoktur. Ancak tapu işlemleri, elektrik/su aboneliği için DASK zorunludur. İkisini ayrı ayrı yaptırabilirsiniz."),
            ("Kiracı olarak konut sigortası yaptırmalı mıyım?", "Kiracı olarak binanın yapısal hasarından sorumlu değilsiniz (o ev sahibinin yükümlülüğü). Ancak eşya hasarı, sorumluluk (komşu zararı) için konut sigortası almanız önerilir."),
            ("Deprem sonrası konut sigortası geçerli mi?", "Evet, poliçe başlangıcından önce gerçekleşen olaylar kapsam dışında olsa da mevcut poliçeniz deprem sırasında geçerliyse tazminat hakkınız doğar."),
        ],
    },
    {
        "slug": "blog-deprem-sonrasi-kiracilarin-haklari",
        "title": "Deprem Sonrası Kiracıların Hakları – Hukuki Rehber 2026",
        "desc": "Deprem sonrası kiracılar kira öder mi? Tahliye zorla yapılabilir mi? Hasar tazminatı kime ödenir? 2026 güncel kira hukuku rehberi.",
        "keywords": "deprem sonrası kiracı hakları, deprem kira, deprem sonrası tahliye, kiracı deprem tazminat, hasar kira",
        "hero_img": "blog-deprem-sonrasi-kiracilarin-haklari.webp",
        "lead": "Deprem sonrası binalar hasar görünce binlerce kişinin aklına aynı soru geliyor: Kira ödemek zorunda mıyım? Ev sahibi beni çıkarabilir mi? Tazminat bana mı ona mı ödenecek? İşte hukuki gerçekler.",
        "sections": [
            ("Hasar Gören Evde Kira Ödemek Zorunda mısınız?", "Türk Borçlar Kanunu'na göre kiralanan taşınmaz <strong>kullanılamaz hale gelirse</strong> (kırmızı/sarı etiket), kiracının kira ödeme yükümlülüğü sona erer. Ancak bina oturulabilir durumdaysa (yeşil etiket, hafif hasar) kira ödemesi devam eder. Hasar tespiti için belediye veya AFAD'a başvurmanız gerekir."),
            ("Ev Sahibi Sizi Tahliye Edebilir mi?", "Deprem hasarı gerekçesiyle <strong>yasal tahliye süresi 60 gündür</strong> (6306 sayılı kanun kapsamında riskli yapı ilan edildiyse). Ev sahibi bu süreyi zorla kısaltamaz, mahkeme kararı olmadan tahliye gerçekleştiremez. Güvenceniz: <strong>Noterden hasar tespiti belgesi</strong> alın ve tüm yazışmalar kayıt altına alın."),
            ("Tazminat Ev Sahibine mi Kiracıya mı?", "DASK tazminatı her zaman <strong>poliçe sahibine</strong>, yani ev sahibine ödenir. Kiracının eşya hasarı için <strong>kendi konut sigortasını</strong> yaptırmış olması gerekir. DASK kiracıyı korumaz. Önemli istisna: Kiracının ev sahibine karşı bir talep hakkı olabilir (örneğin bina bakımsızlığı depreme katkıda bulunduysa)."),
            ("Taşınma Yardımı Var mı?", "6306 sayılı Kentsel Dönüşüm Kanunu kapsamındaki riskli binalarda kiracılara <strong>taşınma yardımı</strong> verilir (2026 itibarıyla yaklaşık 4.000 TL/ay, 18 ay). AFAD üzerinden başvuru yapılır. Belediyenin kira yardım programlarından da yararlanabilirsiniz."),
            ("Depozitonuzu Geri Alabilir misiniz?", "Kira sözleşmesi deprem nedeniyle sona erdiğinde <strong>depozito iade edilmek zorundadır</strong> (kiracıdan kaynaklı hasar yoksa). İki ay içinde iade edilmezse noter aracılığıyla talep edin. Ev sahibi iade etmezse <strong>sulh hukuk mahkemesine</strong> başvurabilirsiniz."),
            ("Pratik Adımlar", "<strong>1.</strong> Belediyeden resmi hasar tespiti belgesi alın. <strong>2.</strong> Ev sahibine noterden bildirim gönderin (kira ödeyip ödemeyeceğinizi yazılı bildirin). <strong>3.</strong> Tüm hasar fotoğraflarını tarihlendirerek saklayın. <strong>4.</strong> AFAD, belediye ve kiracı yardım hatlarına başvurun. <strong>5.</strong> Hukuki danışmanlık için Barolar'ın ücretsiz adli yardım birimlerine başvurabilirsiniz."),
        ],
        "faq": [
            ("Hasar gören evde oturmaya devam etmek zorunda mıyım?", "Hayır. Yapı riskli ise güvenliğiniz için derhal ayrılabilirsiniz. Kira ödeme yükümlülüğünüz de sona erer. Ev sahibini bilgilendirin."),
            ("Ev sahibi deprem nedeniyle kirayı artırabilir mi?", "Deprem, kira artışı için yasal bir gerekçe değildir. Mevcut kira artış sınırları geçerliliğini korur."),
            ("Kira sözleşmem bitmeden çıkmak istesem tazminat öder miyim?", "Binanın oturulmaz hale gelmesi durumunda sözleşmeden erken çıkış tazminat gerektirmez. Durum mahkemede ispatlanabilir."),
        ],
    },
    {
        "slug": "blog-zemin-etudu-nedir",
        "title": "Zemin Etüdü Nedir? Deprem ve Yapı Güvenliğindeki Önemi",
        "desc": "Zemin etüdü nedir, nasıl yapılır, raporu nasıl okunur? Depremde zeminin yapıyı nasıl etkilediği ve zemin analizi rehberi.",
        "keywords": "zemin etüdü nedir, zemin analizi, zemin araştırması, deprem zemin, jeoteknik etüt, zemin sıvılaşması",
        "hero_img": "blog-zemin-etudu-nedir.webp",
        "lead": "2023 Kahramanmaraş depremlerinde en fazla hasarın alüvyon zemin üzerindeki binalarda görülmesi tesadüf değil. Zeminin türü, bir binanın depremde nasıl davranacağını büyük ölçüde belirler. İşte zemin etüdü ve neden bu kadar önemli olduğu.",
        "sections": [
            ("Zemin Etüdü Nedir?", "Zemin etüdü (jeoteknik etüt), bir arazi parçasının fiziksel ve mekanik özelliklerini belirlemek için yapılan bilimsel incelemedir. <strong>Amaç:</strong> o zeminde inşa edilecek yapının güvenli olup olmadığını anlamak. Mühendisler sondaj (zemine delik açma), laboratuvar deneyleri ve arazi testleri ile zeminin taşıma kapasitesini, sıvılaşma riskini ve sismik amplifikasyon potansiyelini ölçer."),
            ("Zemin Türleri ve Deprem Riski", "<strong>ZA - Sağlam Kaya:</strong> deprem dalgalarını olduğu gibi iletir, en güvenli. <strong>ZB - Çok Sıkı Kum/Çakıl:</strong> iyi yapı zemini. <strong>ZC - Sıkı Kil/Orta Kum:</strong> orta risk, dikkatli tasarım gerekir. <strong>ZD - Yumuşak Kil:</strong> dalgaları 3-5 kat güçlendirir, yüksek risk. <strong>ZE/ZF - Çok Yumuşak Alüvyon:</strong> sıvılaşma ve aşırı amplifikasyon riski. TBDY 2019, binaların zemin sınıfına göre ayrı hesap yapılmasını zorunlu kılar."),
            ("Zemin Sıvılaşması Nedir?", "Zemin sıvılaşması, suya doygun kum zeminlerin deprem titreşimleriyle <strong>birden akışkan hale gelmesi</strong> olayıdır. 1999 İzmit depreminde Adapazarı'nda onlarca bina zemin sıvılaştığı için düz zemine battı. Belirtileri: binalarda ani çökme, zeminde kraterler ve su fışkırtmaları. Alüvyon ovalar, dere yatakları, deniz kenarı dolgu alanları risk altındadır."),
            ("Zemin Etüdü Zorunlu mu?", "Evet. İmar Kanunu ve TBDY 2019 gereği <strong>her yapı için zemin etüdü zorunludur</strong>. İmar izni aşamasında zemin etüt raporu belediyeye sunulmadan proje onaylanmaz. Ancak mevcut binaların büyük kısmı bu yönetmelik öncesinde yapıldı — zemin etüdü yapılmamış ya da yetersiz yapılmış olabilir."),
            ("Raporunuzu Nasıl Okursunuz?", "Elinizdeki zemin etüt raporunda şunlara bakın: <strong>Zemin Sınıfı (ZA-ZF):</strong> ne kadar riskli. <strong>Taşıma Kapasitesi (kPa):</strong> zemin ne kadar yük kaldırabilir. <strong>Sıvılaşma Potansiyeli:</strong> düşük/orta/yüksek olarak belirtilir. <strong>Yeraltı Suyu Derinliği:</strong> sığ su sıvılaşma riskini artırır. <strong>Önerilen Temel Tipi:</strong> radye/kazık/tekil temel. Bilginiz yoksa bir inşaat mühendisine raporu inceletin."),
            ("Zemin Sorunlu İse Ne Yapabilirsiniz?", "Yaşadığınız bina ZD/ZE zemin üzerindeyse: <strong>1.</strong> Bina statik güçlendirme değerlendirmesi yaptırın. <strong>2.</strong> DASK sigortanızı yaptırın. <strong>3.</strong> Kentsel dönüşüm kapsamına alınıp alınamayacağını araştırın. <strong>4.</strong> <a href='/blog-evim-depreme-dayanikli-mi.html'>Binanızın genel deprem dayanıklılığını test edin</a>. ZD/ZE zemin, tek başına binanın güvensiz olduğu anlamına gelmez — tasarım ve yapım kalitesi de belirleyicidir."),
        ],
        "faq": [
            ("Zemin etüdü ne kadar sürer ve maliyeti nedir?", "Küçük parseller için 3-7 gün, büyük projeler için 2-4 hafta. Maliyet 5.000-30.000 TL arasında değişir. Belediyenin etüt arşivinden daha önce yapılmış çalışmalar incelenebilir."),
            ("Komşu parselin etüdüne bakarak benim binam hakkında fikir sahibi olabilir miyim?", "Evet, yakın parsellerin zemin yapısı benzer olabilir. Belediyenin jeoloji biriminden çevre zemin etüt raporlarını talep edebilirsiniz."),
            ("Dolgu arazi üzerindeki bina her zaman riskli mi?", "Evet, dolgu alanlar genellikle ZE/ZF zemin sınıfındadır. Depremde sıvılaşma ve oturma riski yüksektir. Özellikle deniz/göl kenarı veya eski dere yatağı doldurularak oluşturulan alanlarda dikkat edin."),
        ],
    },
    {
        "slug": "blog-deprem-aninda-asansor",
        "title": "Deprem Anında Asansörde Ne Yapmalı? Her Katta Güvenlik",
        "desc": "Deprem sırasında asansörde kalırsanız ne yaparsınız? Asansör güvenliği, deprem modu ve kattan çıkış rehberi.",
        "keywords": "deprem anında asansör, depremde asansör, asansörde deprem güvenliği, asansör deprem modu, depremde kat",
        "hero_img": "blog-deprem-aninda-asansor.webp",
        "lead": "\"Asansöre binme, merdiven kullan\" söylemi doğru ama yeterli değil. Peki deprem sırasında asansördeyseniz? Binayı terk etmek için kaç. kat merdivenle inmelisiniz? Bu soruların cevapları burada.",
        "sections": [
            ("Asansöre Neden Binilmemeli?", "Deprem sırasında ve hemen sonrasında asansör kullanmak tehlikelidir çünkü: <strong>1. Elektrik kesilirse</strong> kabin iki kat arasında kalır. <strong>2. Yapı sarsıntısından raylar</strong> bükülür, kapılar açılmaz. <strong>3. Artçılar</strong> sizi içeride mahsur bırakabilir. <strong>4. Yangın durumunda</strong> asansör bacası etkisi yaratır. Kurala tek istisna: <strong>Yüksek katlı</strong> ve <strong>hareket kısıtlı kişiler</strong> — onlar için <a href='/blog-engelli-bireyler-deprem.html'>özel tahliye planı</a> yapılmalıdır."),
            ("Deprem Anında Asansördeyseniz", "<strong>Paniklemyin.</strong> Kabine düzgün tutunun. Tüm katlara basın — hangi katta duruyorsa çıkın. Kapı açılmıyorsa kabindeki acil hattı arayın. Hiçbir şekilde kabinin üstüne çıkıp kablo ile tırmanmayı denemeyin (elektrik riski). <strong>Uzman yardımı gelene kadar bekleyin.</strong> Günlük asansörde genellikle acil çağrı butonu (☎) ve kendi başına açılan kapı mandalı vardır."),
            ("Deprem Modu Olan Asansörler", "Modern binalarda <strong>Deprem Dedektörlü (Sismik Sensörlü) Asansör</strong> sistemi bulunur. Sarsıntı algılandığında: kabin en yakın kata gider, kapılar açılır, herkes iner ve asansör hizmet dışı olur. Bu sistem Japonya ve bazı Avrupa ülkelerinde zorunlu. Türkiye'de yeni yönetmelikle büyük binalarda yaygınlaşıyor. Binanızın asansörünün bu özelliği olup olmadığını yöneticiden öğrenin."),
            ("Deprem Sonrası Kaç Kat Merdivenden İnmeli?", "Bina yüksekliğine göre karar verin: <strong>1-5. kat:</strong> merdivenden direkt inin. <strong>6-15. kat:</strong> 3-4 katta bir dinlenerek inin. <strong>15+ kat:</strong> önce yangın merdiveni bölümüne geçin, yavaş inin (panik halinde düşme riski yüksek). Merdivende <strong>tırmıklar, elektrik panelleri ve cam alanlara</strong> dokunmayın. Merdiven boşluğunun üst katına bakarak hasar var mı kontrol edin."),
            ("Her Kattaki Güvenli Bölgeler", "Deprem anında bulunduğunuz katta: <strong>Mutfak ve banyo gibi ıslak hacimlerde</strong> çok durmayın (su tesisatı patlar). <strong>Bodrum kata</strong> inmeyin (su veya gaz kaçağı birikebilir). <strong>Giriş katı ve 1. kat merdiven sahanlığı</strong> genelde en sağlam alanlar. Sarsıntı 30 saniyeden uzunsa zemini hissedene kadar bekleyin."),
        ],
        "faq": [
            ("Deprem sırasında asansör çağrı düğmesine basılabilir mi?", "Evet, çağrı düğmesi ayrı bir güç hattıyla çalışabilir. Acil durumlarda 110 (İtfaiye) veya 112'ye de haber verin."),
            ("Asansör kapısı açılmıyor, ne yapmalıyım?", "Sakin olun, yüksek sesle bağırın. Acil çağrı butonu varsa basın. Cep telefonunuzla 112 arayın. Kabin üstüne çıkmayı ve kablo ile inmeyi asla denemeyin — hayati tehlike."),
            ("Kaç katta merdiven, kaç katta asansör kullanılmalı?", "Normal kullanımda 4. kata kadar merdiven önerilir. Deprem sonrasında her durumda merdiven. Yangında her koşulda merdiven, asansör kesinlikle hayır."),
        ],
    },
    {
        "slug": "blog-deprem-aninda-yatakta",
        "title": "Deprem Anında Yataktaysanız Ne Yapmalısınız?",
        "desc": "Gece uyku sırasında deprem başlarsa ne yapmalı? Yatakta kalın mı, kalkın mı? Karanlıkta ve pijama ile tahliye rehberi.",
        "keywords": "deprem anında yatakta, gece deprem ne yapmalı, uyku sırasında deprem, yatakta deprem güvenliği",
        "hero_img": "blog-deprem-aninda-yatakta.webp",
        "lead": "Türkiye'deki büyük depremlerin önemli bir kısmı gece saatlerinde oldu: 1999 Gölcük 03:02, 2023 Kahramanmaraş 04:17. Gece uyurken deprem başlarsa en kritik ilk 15 saniyede ne yaparsınız?",
        "sections": [
            ("Yatakta Mı Kalın, Kalkın mı?", "Çoğu deprem güvenlik uzmanının önerisi: <strong>Yatakta kalın, döşeğin altına inin ve başınızı yastıkla koruyun.</strong> Nedeni: gece karanlıkta ayağa kalkmak düşmeye, kırılmış cam ve dökülen eşyalara basılmaya yol açar. Türkiye'de deprem yaralanmalarının önemli bir kısmı <strong>kaçmaya çalışırken</strong> gerçekleşir. İstisna: <strong>Yatağınız ağır bir dolabın, kirişin veya cam önündeyse</strong> — o zaman doğrudan çök-kapan-tutun pozisyonuna geçin."),
            ("Yatağınızı Konumlandırın", "Uyumadan önce yapabileceğiniz: <strong>Yatağı duvara yakın ama büyük pencereden uzağa</strong> yerleştirin. Tavan üzerinde avize veya raf varsa yatağı altına koymayın. Yatağın yanına <strong>bıçaksız ayakkabı, el feneri, su</strong> koyun (deprem çantası yanında değilse). Telefonu başucunda şarjlı tutun."),
            ("Karanlıkta Tahliye Nasıl Yapılır?", "Sarsıntı bitince: <strong>1.</strong> Telefon fenerini açın. <strong>2.</strong> Ayakkabı giyin (kirılmış cam riski). <strong>3.</strong> Elektrik anahtarına dokunmayın — gaz kaçağı varsa kıvılcım yangın çıkarır. <strong>4.</strong> Duman yoksa kapıyı açmadan önce elinizle dokunun (sıcaksa açmayın). <strong>5.</strong> Merdiveni duvara tutunarak inin. <strong>6.</strong> Asansör kesinlikle hayır."),
            ("Çocuklar İçin Özel Önlemler", "Çocuk odasını düzenlerken: yatağı büyük pencereden uzak tutun, dökülebilecek kitaplık veya dolap olmasın, <strong>gece lambası</strong> pilli veya kendi kendine açılan modelde olsun. Çocuklara uyurken deprem olursa <strong>yatakta kalıp yastıkla baş koruması</strong> yapmaları gerektiğini öğretin. <a href='/blog-deprem-anketi-cocuklar.html'>Çocuklarla deprem hazırlığı</a> için ayrıntılı rehberimize bakın."),
            ("Gece Deprem Çantası Hazırlığı", "Başucunuzda bulundurmanız gerekenler: <strong>El feneri</strong> (pilli veya krank), <strong>ayakkabı</strong> (bıçaksız spor ayakkabı ideal), <strong>su</strong> (küçük şişe), <strong>telefon şarjlı</strong>, <strong>düdük</strong> (enkaz altında kurtarıcıları çekmek için). Gece deprem kaçınılmazın kaçınılmazı; hazırlıklı uyuyanlar panik yaşamaz."),
        ],
        "faq": [
            ("Yataktan kalkarak kaçmak daha mı güvenli?", "Genellikle hayır. Karanlıkta, uyku sersemliğiyle yapılan ani hareketler düşmeye ve yaralanmaya yol açar. Yatakta kalıp başınızı korumak çoğu durumda daha güvenlidir."),
            ("Deprem sırasında merdivene koşabilir miyim?", "Sarsıntı devam ederken merdiven son derece tehlikelidir — döşemeler, merdiven korkulukları kırılabilir. Sarsıntı bitince çıkın."),
            ("Çocuğumu kucağıma almalı mıyım?", "Sarsıntı sırasında onu göğsünüze alıp sırtınızı sağlam bir duvara dayayın, üzerinizi örtin. Bebek karyolası varsa karyolayı kaldırmaya çalışmayın — güçlendirme yapılmışsa yeterince güvenlidir."),
        ],
    },
    {
        "slug": "blog-turkiye-en-cok-deprem-iller",
        "title": "Türkiye'de En Fazla Deprem Olan Şehirler – İl Bazlı Sıralama",
        "desc": "Türkiye'nin en çok deprem yaşayan illeri hangileri? Son 50 yılın sismik aktivite sıralaması, büyük depremler ve risk haritası.",
        "keywords": "türkiye en çok deprem olan şehir, en fazla deprem hangi il, türkiye deprem sıralaması, en riskli iller",
        "hero_img": "blog-turkiye-en-cok-deprem-iller.webp",
        "lead": "Türkiye'de her yıl ortalama 20.000 deprem kaydediliyor. Peki hangi iller en çok sarsıntıya maruz kalıyor? Son 50 yılın Kandilli ve AFAD verilerine dayanan il bazlı sıralama.",
        "sections": [
            ("Metodoloji: Ne Ölçtük?", "Bu sıralama Kandilli Rasathanesi ve AFAD'ın 1975-2025 arası açık verilerine dayanıyor. Kriterler: <strong>toplam deprem sayısı (Mw ≥ 3.0)</strong> ve <strong>Mw ≥ 5.0 sayısı</strong> birlikte değerlendirildi. Salt sayı değil, enerji seviyesi de gözetildi. Hassas veriler için <a href='https://deprem.afad.gov.tr' target='_blank' rel='noopener noreferrer'>AFAD deprem kataloğu</a> ve <a href='https://koeri.boun.edu.tr' target='_blank' rel='noopener noreferrer'>Kandilli</a> kaynak alındı."),
            ("İlk 10 – En Sismik Aktif İller", "<strong>1. Erzincan:</strong> KAF'ın en aktif segmenti üzerinde. 1939 Mw 7.8, 1992 Mw 6.8. <strong>2. Van:</strong> 2011 Mw 7.2. Doğu Anadolu plakaları. <strong>3. Kocaeli/Sakarya:</strong> 1999 Mw 7.6 Gölcük, KAF ana segmenti. <strong>4. Bingöl:</strong> KAF-DAF kesişim noktası yakını. 2003 Mw 6.4. <strong>5. Düzce:</strong> 1999 Mw 7.2, KAF hızla kayan segment. <strong>6. Malatya:</strong> DAF üzerinde. 2023 depremleri merkez üssüne yakın. <strong>7. Hatay:</strong> Amik Havzası, DAF'ın güney ucu. 2023'ün en çok yıkımı burada. <strong>8. Muş:</strong> Doğu Anadolu plakaları, sürekli aktivite. <strong>9. Denizli:</strong> Batı Anadolu grabenleri, 1995 Dinar depremi. <strong>10. İzmir:</strong> 2020 Samos, Ege açılma fayları."),
            ("Neden İstanbul Listede Değil?", "İstanbul görece az sayıda tarihsel büyük deprem yaşadı — çünkü Marmara altındaki KAF segmentinde gerilim birikmekte, henüz kırılmadı. Az deprem = güvenli değil, aksine <strong>biriken enerji = büyük tehlike</strong>. <a href='/blog-istanbul-beklenen-deprem.html'>İstanbul'daki beklenen deprem</a> hakkında detaylı bilgi için tıklayın."),
            ("Sismik Aktivite ≠ Yıkım Riski", "Frekans önemli ama yıkım riski sadece buna bağlı değil. Riski belirleyen: <strong>büyüklük</strong>, <strong>derinlik</strong>, <strong>zemin</strong> ve <strong>yapı kalitesi</strong>. Deprem sayısı yüksek ama insan yerleşimi az olan iller (Tunceli gibi) daha az can kaybı verdi. İstanbul ise tarihsel frekansı düşük ama potansiyel en yüksek şehir. Şehrinizin risk profilini <a href='/deprem-sehirleri.html'>81 il deprem sayfamızda</a> bulabilirsiniz."),
            ("Sonuç: Nerede Yaşarsanız Hazır Olun", "Türkiye'nin %95'i aktif deprem kuşağında. 'Buraya deprem olmaz' düşüncesi güvenilir değil. Nerede yaşarsanız: <a href='/blog-deprem-oncesi-hazirlik.html'>deprem hazırlığı</a>, <a href='/blog-deprem-cantasi.html'>deprem çantası</a> ve <a href='/blog-dask-nedir.html'>DASK</a> — üçü birden zorunlu."),
        ],
        "faq": [
            ("Türkiye'de günde kaç deprem oluyor?", "Ortalama 50-80 deprem (Mw ≥ 1.5) kaydediliyor. Büyük çoğunluğu hissedilmez. Yılda 15.000-25.000 arasında kayıt oluyor."),
            ("En güvenli il hangisi?", "Coğrafi olarak en düşük sismik aktiviteye sahip iller: Edirne, Kırklareli, Tekirdağ'ın iç kesimleri. Ama unutmayın — Marmara fay hattı bu illeri de etkiler."),
            ("AFAD'ın deprem kataloğuna nasıl ulaşabilirim?", "deprem.afad.gov.tr adresinden tarih, büyüklük ve il filtreleriyle arama yapabilirsiniz. Kandilli verileri için koeri.boun.edu.tr."),
        ],
    },
    {
        "slug": "blog-deprem-hasar-tazminat-sureci",
        "title": "Deprem Hasarı Tazminat Süreci – DASK ve Konut Sigortasından Nasıl Alınır?",
        "desc": "Deprem sonrası DASK ve konut sigortası tazminatı nasıl alınır? Başvuru adımları, eksper süreci, itiraz hakkı ve ödeme takibi rehberi.",
        "keywords": "deprem tazminat nasıl alınır, dask tazminat, deprem hasar başvurusu, sigorta tazminat süreci, eksper deprem",
        "hero_img": "blog-deprem-hasar-tazminat-sureci.webp",
        "lead": "Deprem oldu, binanız hasar gördü. DASK poliçeniz var ama tazminat nasıl alacağınızı bilmiyorsunuz? 2023 Kahramanmaraş depreminde 250 milyar TL tazminat ödendi — ama pek çok kişi süreci bilmediği için geç ya da eksik aldı. İşte adım adım rehber.",
        "sections": [
            ("Adım 1: Hasarı 60 Gün İçinde Bildirin", "DASK'ta hasar bildirme süresi yasal olarak <strong>60 gündür</strong>. Bu süre geçerse tazminat hakkını kaybedebilirsiniz. Bildirim yolları: <strong>DASK çağrı merkezi: 125</strong> (7/24), online: dask.gov.tr, acenteniz üzerinden. Bildirirken: poliçe numarası, T.C. kimlik, hasarlı yapının adresi ve hasar özeti hazır olsun."),
            ("Adım 2: Hasar Tespiti ve Eksper", "Bildirim sonrası DASK 1-2 hafta içinde lisanslı bir <strong>eksper</strong> gönderir. Eksper bina hasarını yerinde inceler, fotoğraflar çeker, rapor hazırlar. <strong>Önemli:</strong> Eksper gelmeden binada büyük onarım yapmayın — hasar delilleri bozulabilir. Hasarın fotoğraflarını ve videolarını önceden çekip saklayın."),
            ("Adım 3: Tazminat Miktarı Belirleme", "Eksper raporu sonrası DASK tazminat miktarını belirler. Hesaplamada: <strong>binanın türü, yaşı, hasar oranı ve poliçe limiti</strong> dikkate alınır. Limit: 2026 itibarıyla azami 640.000 TL. Ödeme genellikle <strong>15-30 iş günü</strong> içinde banka hesabınıza gelir."),
            ("İtiraz Hakkınız", "Tazminat miktarına itiraz edebilirsiniz. Süreç: <strong>1.</strong> DASK'a yazılı itiraz (15 gün içinde). <strong>2.</strong> Sigorta Tahkim Komisyonu'na başvuru (2.500 TL teminat + 250-4.000 TL komisyon). <strong>3.</strong> Mahkeme yolu (avukat gerekebilir). İtirazların önemli bir kısmı <strong>daha yüksek ödeme</strong> ile sonuçlanıyor — hakkınızı koruyun."),
            ("Konut Sigortasından Tazminat", "Konut sigortası poliçeniz varsa, DASK'tan bağımsız olarak ayrıca başvurmalısınız. Sigorta şirketinize <strong>24-72 saat içinde</strong> hasar bildirimi yapın. Süreç benzer: bildirim → eksper → tazminat. <strong>Dikkat:</strong> Bazı poliçelerde 'muafiyet tutarı' (franchise) olabilir — belirli bir miktarın altındaki hasarlar ödenmez."),
            ("Pratik İpuçları", "<strong>1.</strong> Hasar belgelerini (fotoğraf, video, resmi tutanak) birden fazla yerde yedekleyin. <strong>2.</strong> Poliçe numaranızı telefonunuza kaydedin. <strong>3.</strong> Eksper randevusunda evde olun. <strong>4.</strong> Hasarı küçümseyip beyan etmeyin — eksper zaten görecek. <strong>5.</strong> Komşularla koordineli hareket edin (site bazında toplu başvuru daha hızlı sonuçlanır). <a href='/blog-dask-nedir.html'>DASK hakkında daha fazla bilgi</a> için tıklayın."),
        ],
        "faq": [
            ("DASK tazminatı ne zaman ödenir?", "Yasal süre 45 gün ama pratikte büyük depremlerde kuyruğa girilir. Ortalama 30-90 gün. Yavaş giderse tahkim komisyonuna başvurabilirsiniz."),
            ("Binam başkasının adına kayıtlı, tazminat alabilir miyim?", "DASK tazminatı poliçe sahibine (gayrimenkul malikine) ödenir. Kiracı olarak sadece kendi konut sigortanızdan talep edebilirsiniz."),
            ("Hasar binanın tamamına mı yoksa dairene göre mi hesaplanır?", "Site veya apartmanda her bağımsız bölüm ayrı poliçeye sahip olabilir. Ortak alanlar (bodrum, merdivenler) apartman yönetiminin poliçesiyle kapsanır."),
        ],
    },
    {
        "slug": "blog-deprem-oncesi-bina-guclendir",
        "title": "Binanızı Depreme Karşı Güçlendirme – Yöntemler ve Maliyetler",
        "desc": "Ev veya apartman güçlendirme nedir, nasıl yapılır? Karbon fiber, epoksi enjeksiyon, çelik manşon yöntemleri ve 2026 maliyet rehberi.",
        "keywords": "bina güçlendirme, kolon güçlendirme, deprem güçlendirme, yapı güçlendirme yöntemleri, bina depreme karşı",
        "hero_img": "blog-deprem-oncesi-bina-guclendir.webp",
        "lead": "Binanız riskli ama yıkıp yeniden yapmak istemiyorsunuz. Ya da sadece ek güvenlik istiyorsunuz. Bina güçlendirme bu boşluğu dolduruyor — doğru yöntemle eski binalara yeni binalara yakın dayanıklılık kazandırmak mümkün.",
        "sections": [
            ("Güçlendirme Ne Zaman Gerekir?", "Güçlendirme şu durumlarda değerlendirin: <strong>1999 öncesi yapım</strong> (eski yönetmelik), <strong>mühendis tespiti</strong> (kolon/kiriş hasar, pas payı yetersiz, beton kalitesi düşük), <strong>zemin riski</strong> (ZD/ZE sınıfı), <strong>kentsel dönüşüm yapmak istemiyorsanız ama güvenli olmak istiyorsanız</strong>. Güçlendirme her binaya uygun değil — önce statik değerlendirme şart."),
            ("Karbon Fiber Şerit (CFRP)", "En popüler ve az müdahaleli yöntem. Kolonların etrafına <strong>karbon fiber bantlar</strong> yapıştırılır. Avantajları: hızlı (saat), temiz, bina boşaltmadan yapılabilir. Kolon başına maliyet: 5.000-20.000 TL. Kullanım alanı: kolon-kiriş birleşim bölgesi güçlendirme, kesme hasarına karşı koruma. Dikkat: Yüzey hazırlığı kritik, çatlak yoksa etkisi sınırlı."),
            ("Betonarme Perde Duvar Ekleme", "Binanın zayıf noktalarına yeni <strong>betonarme perde duvarlar</strong> eklenmesi. En sağlam yöntem. Maliyeti yüksek (kat başına 50.000-150.000 TL), yıkım-yapım gerektiriyor. Binanın %30-50 oranında rijitliğini artırır. Genellikle <strong>yumuşak kat</strong> (zemin kattaki büyük açıklık) sorunlarında uygulanır."),
            ("Epoksi Enjeksiyon", "Beton çatlakları epoksi reçineyle doldurulur. Genellikle hasar sonrası onarımda kullanılır. Hafif ve orta hasarlı kolonlar için etkili. Maliyet: m başına 200-800 TL. Dikkat: Çatlak boyutu 0.2 mm'den küçükse doğal kapanmaya bırakılabilir, büyükse enjeksiyon şart."),
            ("Güçlendirme Maliyeti ve Proje Süreci", "<strong>Önce statik değerlendirme:</strong> 5.000-20.000 TL (inşaat mühendisi). <strong>Güçlendirme projesi:</strong> 10.000-50.000 TL (yapıya göre). <strong>Uygulama:</strong> bina büyüklüğüne ve yönteme göre 100.000-500.000 TL ve üzeri. Devlet desteği: 6306 sayılı kanun kapsamında onaylı riskli binalara <strong>faiz sübvansiyonlu kredi</strong> imkânı var. Çevre Şehircilik Bakanlığı'ndan bilgi alınabilir."),
        ],
        "faq": [
            ("Güçlendirme yapılırken binada oturabilir miyim?", "Yönteme göre değişir. Epoksi ve CFRP için genellikle tahliye gerekmez. Perde duvar ve temel güçlendirme için bina boşaltılmalıdır."),
            ("Güçlendirme yapılan bina yeni bina kadar güvenli mi?", "Hedefe bağlı. Mevcut yönetmelikteki güvenlik seviyesine ulaştırmak mümkün ama inşaat kalitesi ve detaylar kritik. İyi mühendisli güçlendirme, kötü yapılmış yeni binadan daha güvenli olabilir."),
            ("Kat maliklerinin tamamı onay vermeli mi?", "Güçlendirme için kat malikleri kurulunda en az 2/3 çoğunluk yeterlidir. Riskli bina raporu varsa daha az onay yeterlidir."),
        ],
    },
    {
        "slug": "blog-okul-isyeri-deprem-guvenlik",
        "title": "Okul ve İşyerinde Deprem Güvenliği – Tahliye Planı Rehberi",
        "desc": "Okul, AVM, ofis, fabrika gibi çok kişili mekânlarda deprem sırasında güvenlik, tahliye ve toplanma planı hazırlama rehberi.",
        "keywords": "okulda deprem, işyerinde deprem güvenliği, AVM deprem, toplu alan deprem tahliye, okul deprem tatbikatı",
        "hero_img": "blog-okul-isyeri-deprem-guvenlik.webp",
        "lead": "Ev dışında geçirilen saatler çoğu kişi için %60'ı aşıyor. Ama deprem hazırlığını sadece ev için yapıyoruz. Okulda, işyerinde veya AVM'de deprem olursa farklı dinamikler devreye giriyor.",
        "sections": [
            ("Okulda Deprem: Öğrenci ve Öğretmen Rolleri", "<strong>Öğretmen:</strong> Sarsıntı başlayınca 'Çök-Kapan-Tutun' komutunu ver, sınıfı terk etme. Sarsıntı biterken sırayı düzenle, katılım listesini al, tahliye liderliği yap. <strong>Öğrenci:</strong> Masa altına gir, çantayı başına koy, öğretmeni dinle, panik yapma. <strong>Yönetici:</strong> Siren çal, sınıf öğretmenleriyle sayım yap, 112'ye haber ver, velileri ara."),
            ("AVM ve Büyük Alışveriş Merkezleri", "En büyük risk: <strong>kalabalık panik</strong>. Sarsıntı sırasında koşmayın, sürüden ayrılın, sağlam bir sütuna yaslanın. Rafların devrilme riski yüksek — gıda reyonlarından uzaklaşın. Mağazalar genellikle acil durum planı hazırlamak zorunda. AVM içindeki acil çıkış işaretlerini girişte görün. Otoparka inmeyin (araç yangını riski)."),
            ("Ofis ve İş Yerleri", "Masaların altına girilmesi zor olabilir (cam bölmeler, küçük çalışma alanları). Alternatif: <strong>sağlam bir kolon yanında çökün</strong>, dizlerini çekin, başınızı koruyun. <strong>Bilgisayar ekranlarından uzaklaşın</strong> (kırılabilir). Sunucu odaları ve elektrik panoları yakınından kaçının. Yangın merdiveni kapılarını kapalı tutun (yangın dirençli kapı)."),
            ("Tahliye Planı Nasıl Hazırlanır?", "<strong>1.</strong> Bina planını çıkarın, tahliye rotalarını işaretleyin. <strong>2.</strong> Kat sorumluları belirleyin. <strong>3.</strong> Engelli/yaşlı çalışanlar için asistan atayın. <strong>4.</strong> Toplanma alanı dışarıda belirleyin (binanın iki katı uzaklık). <strong>5.</strong> Yılda en az 2 tatbikat yapın. <strong>6.</strong> Acil iletişim ağacı oluşturun. Detaylar için <a href='/blog-zorunlu-deprem-tatbikati.html'>işyeri tatbikat rehberimiz</a>e bakın."),
            ("Kalabalık Ortamlarda Panikle Baş Etme", "En tehlikeli an tahliye sırasında: <strong>Sürüden ayrılın, kenara çekilin, duvarı takip edin.</strong> Ön kapıya koşmayın — kapı sıkışır. Merdiven boşluğuna girince sola/sağa yanaşın, ortalama akışın dışında durun. Düşen biri varsa kaldırmak yerine 'Yerde biri var!' diye bağırın — ikinci bir düşme önlenir."),
        ],
        "faq": [
            ("Okul binası riskli ise nereye şikâyet edebilirsiniz?", "Millî Eğitim Bakanlığı, ilçe millî eğitim müdürlüğü ve belediyenin imar birimini arayabilirsiniz. Yazılı başvurunuz yasal kayıt oluşturur."),
            ("İşyerinde deprem ekipmanı zorunlu mu?", "6331 sayılı İSG Kanunu gereği işverenler deprem riskine karşı acil durum planı yapmak zorunda. Bunun bir parçası yangın söndürücü, ilk yardım kiti ve tahliye tabelaları."),
            ("Tatbikat saatini önceden bildirmek zorunda mısınız?", "Hayır. Bildirilmeyen tatbikat gerçek sarsıntı refleksini test eder. Ama güvenlik için büyük sürpriz tatbikatlar yerine 15 dakika önce uyarı yeterlidir."),
        ],
    },
    {
        "slug": "blog-deprem-sonrasi-temiz-su-gida",
        "title": "Deprem Sonrası Temiz Su ve Gıda Güvenliği",
        "desc": "Deprem sonrası su güvenli mi? Deprem sonrası ne yenmeli, su nasıl temizlenir? Şebeke suyu ve gıda güvenliği hakkında rehber.",
        "keywords": "deprem sonrası su, deprem sonrası temiz su, deprem sonrası gıda, su nasıl arıtılır, deprem yiyecek güvenliği",
        "hero_img": "blog-deprem-sonrasi-temiz-su-gida.webp",
        "lead": "Deprem sonrasında açlık ve susuzluk hayatı doğrudan tehdit eder. Ama daha büyük tehlike bozuk suyu içmek veya zararlı gıda tüketmektir. 72 saatlik kritik dönemde su ve gıda güvenliği için bilmeniz gerekenler.",
        "sections": [
            ("Şebeke Suyu Güvenli mi?", "Depremden hemen sonra şebeke suyunu <strong>içmeyin</strong> — borular kırılmış olabilir, içine toprak ve zararlı maddeler girmiş olabilir. Yetkililerin \"şebeke suyu güvenlidir\" açıklaması yapana kadar bekleyin. Bu süre 24-72 saat olabilir. Alternatif: <strong>Kapalı şişe su</strong>, <strong>kaynatılmış su</strong> veya <strong>sertifikalı filtreli su</strong>."),
            ("Suyu Nasıl Güvenli Hale Getirirsiniz?", "<strong>Kaynatma:</strong> en güvenli yöntem. 1 dakika kaynatın (yüksek rakımda 3 dakika). Soğuyunca içilir. <strong>Klor tableti:</strong> deprem çantasında bulunmalı. 1 L suya 1 tablet, 30 dakika bekle. <strong>İyot damlaları:</strong> 1 L suya 5 damla, 30 dakika bekle. <strong>Güneş dezenfeksiyonu (SODIS):</strong> temiz şeffaf PET şişeye doldurun, 6 saat güneşe bırakın."),
            ("Gıda Güvenliği: Neleri Yemeyin", "<strong>Açılmamış konserve:</strong> şişmiş veya ezilmiş kutular atmak gerekir (botulizm riski). <strong>Elektrik kesilmişse buzdolabı:</strong> 4 saat içinde et, süt, yumurta tüketin; aksi hâlde atın (koklayarak karar vermeyin — bakteri koku vermeyebilir). <strong>Donmuş gıdalar:</strong> çözülüp tekrar donmuşsa atmak güvenli. <strong>Sel veya zemin suyuyla temas etmiş</strong> paketlenmemiş gıdalar: atın."),
            ("Deprem Sonrası Güvenli Gıdalar", "En güvenli gıdalar: <strong>Kapalı konserve</strong> (şişmemiş, ezilmemiş), <strong>fabrika paketli bisküvi, kraker</strong>, <strong>kuru yemiş</strong>, <strong>kapalı paket peynir</strong>, <strong>tetrapak süt</strong>. Pişirme imkânı varsa: pirinç, bulgur, makarna (kaynatılmış temiz suyla). Tuzu minimumda tutun — susuzluğu artırır."),
            ("Su Yönetimi: 72 Saat Hesabı", "Kişi başı günlük minimum: <strong>3 litre içme + 2 litre hijyen = 5 litre</strong>. 72 saat için: 15 litre/kişi. 4 kişilik aile: 60 litre. Deprem çantasında <strong>en az 8-12 litre</strong> olmalı (kalanı filtre/kaynatmayla karşılarsınız). Su bir yere stoklandıysa yılda bir değiştirin (tat bozulur, kap kirlenir). <a href='/blog-deprem-cantasi.html'>Tam çanta rehberi</a> için tıklayın."),
        ],
        "faq": [
            ("Çeşme suyunu kaynatırsam içebilir miyim?", "Çeşme suyu boru kırılmalarıyla kirlenmişse kaynatma bakterileri öldürür ama kimyasal kirleticileri gidermez. Kaynatma + aktif karbon filtre (Brita tarzı) birlikte kullanın."),
            ("Pet şişe plastik tehlikeli mi?", "Güneş altında uzun süre bekleyen plastik şişelerde mikroplastik salınımı olabilir. Deprem döneminde hayatta kalmak öncelikli — bu riski kabul edin. Normal zamanda cam veya paslanmaz çelik tercih edin."),
            ("Bebek için mama veya su hazırlamak?", "Bebek maması için mutlaka kaynatılmış ve soğutulmuş su kullanın. Hazır paket mamaları tercih edin (su gerekmez). Emziriyorsanız mevcut koşullarda emzirmeye devam edin — anne sütü her zaman güvenlidir."),
        ],
    },
    {
        "slug": "blog-deprem-cep-uygulamalari",
        "title": "Deprem İçin En İyi 5 Mobil Uygulama – Türkiye 2026",
        "desc": "Türkiye'de deprem takibi için en iyi Android ve iOS uygulamaları: AFAD Acil, Kandilli, erken uyarı ve anlık deprem uygulamaları karşılaştırması.",
        "keywords": "deprem uygulaması, anlık deprem uygulaması, AFAD mobil, kandilli uygulaması, türkiye deprem app 2026",
        "hero_img": "blog-deprem-cep-uygulamalari.webp",
        "lead": "Telefonunuz deprem anında hayat kurtarabilir — ama ancak doğru uygulamayı kurmuşsanız. Google Play ve App Store'daki onlarca deprem uygulaması arasından hangilerini kullanmalısınız? Bağımsız inceleme.",
        "sections": [
            ("1. AFAD Acil (Android/iOS – Ücretsiz)", "<strong>Neden:</strong> Türkiye'nin resmi afet yönetim kurumunun uygulaması. <strong>Öne çıkan özellikler:</strong> Konum bazlı erken uyarı, yakın toplanma alanları, AFAD iletişim hatları. <strong>Eksiler:</strong> Arayüz biraz eski, bildirimler bazen gecikmeli. <strong>Öneri:</strong> Mutlaka kurulması gereken temel uygulama. Deprem bildirimlerini 4.0+ için açık bırakın."),
            ("2. Kandilli Rasathanesi Uygulaması", "<strong>Neden:</strong> Boğaziçi Üniversitesi Kandilli verisi, Türkiye'nin en hızlı sismik ağı. <strong>Öne çıkan özellikler:</strong> Anlık deprem listesi (30 sn gecikme), büyüklük/derinlik filtresi, tarihsel katalog. <strong>Öneri:</strong> Teknik kullanıcılar için ideal. Günlük deprem takibi için güvenilir."),
            ("3. MyShake (Android/iOS – Ücretsiz)", "<strong>Neden:</strong> Berkeley Üniversitesi'nin geliştirdiği küresel deprem erken uyarı sistemi. Telefonunuzu sismometre olarak kullanır. <strong>Öne çıkan özellikler:</strong> P-dalga tespiti, erken uyarı (saniyeler), topluluk tabanlı ağ. <strong>Dikkat:</strong> İngilizce arayüz, Türkiye kapsaması sınırlı ama gelişiyor."),
            ("4. Yakınımdaki Deprem Web Uygulaması (PWA)", "<strong>Bu site</strong> Progressive Web App olarak telefonunuza kurulabilir. <strong>Özellikler:</strong> 20 sn güncellemeli canlı harita, şehir arama, 4.0+ push bildirimi, <a href='/'>konumunuzu haritada gösterme</a>. <strong>Kurulum:</strong> Tarayıcınızda \"Ana Ekrana Ekle\" seçeneğini kullanın. İnternet gerektiren ama hızlı erişim."),
            ("5. Google Android Deprem Uyarısı", "<strong>Neden:</strong> Android telefonlarda yerleşik. Ayarlar > Güvenlik & Acil Durum > Yer Sarsıntısı Uyarıları. <strong>Özellik:</strong> ShakeAlert (ABD kökenli) ve yerel sensörlerle P-dalgası tespiti. Türkiye'de henüz tam aktif değil ama yakın zamanda genişleyecek. <strong>Şimdi aktif edin</strong> — açık olması zarar vermez."),
            ("Uygulamaları Hazır Tutma İpuçları", "<strong>Bildirimleri kapatmayın</strong> — bu uygulamaların en önemli özelliği. <strong>Batarya optimizasyonundan çıkarın</strong> — Android'de arka planda kapanabilir. <strong>Veri erişimine izin verin</strong> — wifi olmadan da çalışsın. <strong>Konum iznini 'Her Zaman' yapın</strong> (AFAD için). <strong>Düzenli güncelleyin</strong> — erken uyarı algoritmaları sık güncellenir."),
        ],
        "faq": [
            ("Hiç internet yokken bu uygulamalar çalışır mı?", "AFAD ve Kandilli uygulamaları çevrimiçi gerektirir. MyShake ve Android yerleşik uyarısı 2G bile olsa çalışabilir. SMS tabanlı uyarılar tamamen çevrimdışı çalışır (AFAD baz istasyonu üzerinden)."),
            ("Tüm uygulamalara izin vermek bataryayı tüketir mi?", "Evet, biraz. Ama 4-6 uygulamanın günlük batarya etkisi %1-3 arasında. Deprem hazırlığı için bu makul. Kritik uygulamalar için 'pil tasarrufu istisnaları' ekleyin."),
            ("Sahte deprem uygulamalarına dikkat", "Uygulama mağazalarında sahte deprem uygulamaları var. Sadece resmi kurum uygulamalarını (AFAD, Boğaziçi Üniversitesi) ve büyük yayıncıları tercih edin. İzin isteklerine dikkat edin — deprem uygulamasının kameraya erişmesi gerekmez."),
        ],
    },
]


def build_image_object(filename, description):
    path = PUBLIC / "images" / filename
    width, height = (1200, 630)
    if path.exists():
        try:
            with Image.open(path) as im:
                width, height = im.size
        except Exception:
            pass
    return {
        "@type": "ImageObject",
        "url": f"https://yakinimdakideprem.com/images/{filename}",
        "width": width, "height": height,
        "caption": description, "description": description,
        "creditText": "Yakınımdaki Deprem",
        "copyrightNotice": "© 2026 Yakınımdaki Deprem - Emin Kılıç",
        "license": "https://yakinimdakideprem.com/kullanim-sartlari.html",
        "creator": {"@type": "Person", "name": "Emin Kılıç", "url": "https://yakinimdakideprem.com/ben-kimim.html"},
        "copyrightHolder": {"@type": "Organization", "name": "Yakınımdaki Deprem"},
    }


TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#ffffff">
    <!-- Google Tag Manager -->
    <script>(function (w, d, s, l, i) {{
            w[l] = w[l] || []; w[l].push({{'gtm.start':
                new Date().getTime(), event: 'gtm.js'}}); var f = d.getElementsByTagName(s)[0],
                j = d.createElement(s), dl = l != 'dataLayer' ? '&l=' + l : ''; j.async = true; j.src =
                    'https://www.googletagmanager.com/gtm.js?id=' + i + dl; f.parentNode.insertBefore(j, f);
        }})(window, document, 'script', 'dataLayer', 'GTM-WQZS53QX');</script>
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="Emin Kılıç">
    <link rel="canonical" href="https://yakinimdakideprem.com/{slug}.html" />
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="https://yakinimdakideprem.com/{slug}.html">
    <meta property="og:site_name" content="Yakınımdaki Deprem">
    <meta property="og:image" content="https://yakinimdakideprem.com/images/{hero_img}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="https://yakinimdakideprem.com/images/{hero_img}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" media="print" onload="this.media='all'">
    <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"></noscript>
    <link rel="stylesheet" href="css/style.min.css?v=202604271200">
    <link rel="stylesheet" href="css/header.min.css?v=202604271200">
    <link rel="stylesheet" href="css/blog-detail.css?v=2026011231">
    <link rel="stylesheet" href="css/city-search.css?v=202604271200">
    <link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32x32.png">
    <link rel="manifest" href="site.webmanifest">
    <script type="application/ld+json">{article_schema}</script>
    <script type="application/ld+json">{breadcrumb_schema}</script>
    <script type="application/ld+json">{faq_schema}</script>
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
                <a href="/son-dakika-deprem.html" class="nav-highlight nav-alert">Deprem Mi Oldu? <span class="alarm-dot" aria-hidden="true"></span></a>
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
    <script src="js/header.min.js?v=202604271200" defer></script>
    <script src="js/city-keywords.js?v=202604271200" defer></script>
    <script src="js/city-search.js?v=202604271200" defer></script>
</body>
</html>
"""

def build_schemas(data):
    article = json.dumps({
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": data["title"], "description": data["desc"],
        "image": build_image_object(data["hero_img"], data["title"]),
        "author": {"@type": "Person", "name": "Emin Kılıç", "url": "https://yakinimdakideprem.com/ben-kimim.html"},
        "publisher": {"@type": "Organization", "name": "Yakınımdaki Deprem",
                      "logo": {"@type": "ImageObject", "url": "https://yakinimdakideprem.com/icons/android-chrome-512x512.png", "width": 512, "height": 512}},
        "datePublished": TODAY, "dateModified": TODAY,
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://yakinimdakideprem.com/{data['slug']}.html"},
        "inLanguage": "tr-TR",
    }, ensure_ascii=False)

    breadcrumb = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": "https://yakinimdakideprem.com/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://yakinimdakideprem.com/blog.html"},
            {"@type": "ListItem", "position": 3, "name": data["title"]},
        ]
    }, ensure_ascii=False)

    faq = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in data["faq"]
        ]
    }, ensure_ascii=False)

    return article, breadcrumb, faq


def render(data):
    sections_html = ""
    for heading, body in data["sections"]:
        sections_html += f"                <h2>{heading}</h2>\n                <p>{body}</p>\n"

    a, b, f = build_schemas(data)
    return TEMPLATE.format(
        slug=data["slug"], title=data["title"], desc=data["desc"],
        keywords=data["keywords"], hero_img=data["hero_img"],
        today=TODAY, lead=data["lead"],
        sections_html=sections_html,
        article_schema=a, breadcrumb_schema=b, faq_schema=f,
    )


if __name__ == "__main__":
    import re
    written = 0
    for data in NEW_BLOGS:
        target = PUBLIC / f"{data['slug']}.html"
        html = render(data)
        target.write_text(html, encoding="utf-8")
        words = len(re.findall(r"\b\w+\b", re.sub(r"<[^>]+>", " ", html)))
        print(f"  ✓ {data['slug']:<45} {words:>5} kelime")
        written += 1
    print(f"\n{written} blog üretildi.")
