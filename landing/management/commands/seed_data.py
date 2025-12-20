"""
Umut Vagonu Seed Data
=====================
Bu komut veritabanına örnek veriler ekler.
Kullanım: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from landing.models import (
    SiteSettings, News, Writer, Article, 
    GalleryCategory, GalleryImage, Link, ContactMessage
)


class Command(BaseCommand):
    help = 'Veritabanına Umut Vagonu örnek verilerini ekler'

    def handle(self, *args, **options):
        self.stdout.write('🌿 Umut Vagonu seed data oluşturuluyor...\n')
        
        # 1. Site Ayarları
        self.create_site_settings()
        
        # 2. Haberler
        self.create_news()
        
        # 3. Yazarlar ve Makaleler
        self.create_writers_and_articles()
        
        # 4. Galeri Kategorileri ve Görseller
        self.create_gallery()
        
        # 5. Bağlantılar
        self.create_links()
        
        self.stdout.write(self.style.SUCCESS('\n✅ Seed data başarıyla oluşturuldu!'))

    def create_site_settings(self):
        """Site ayarlarını oluştur"""
        settings, created = SiteSettings.objects.get_or_create(pk=1)
        settings.site_title = "Umut Vagonu Manisa"
        settings.slogan = "Geleceğe Umut Taşıyoruz"
        settings.about_text = """Umut Vagonu Derneği, 2018 yılında Manisa'da kurulmuş bir sivil toplum kuruluşudur. 
        
Amacımız; ihtiyaç sahiplerine ulaşmak, yüzlerde bir tebessüm oluşturmak ve toplumsal dayanışmayı güçlendirmektir.

6.400'den fazla takipçimiz ve yüzlerce gönüllümüzle birlikte, eğitimden sağlığa, gıdadan giyime kadar pek çok alanda faaliyetler yürütüyoruz."""
        
        settings.contact_phone = "0555 123 45 67"
        settings.contact_email = "bilgi@umutvagonu.org"
        settings.contact_address = "Manisa, Türkiye"
        
        settings.instagram_url = "https://www.instagram.com/umutvagonumanisa/"
        settings.facebook_url = "https://www.facebook.com/umutvagonutr/"
        settings.twitter_url = "https://x.com/umutvagonu45"
        settings.youtube_url = ""
        
        settings.stat_lives_touched = 15000
        settings.stat_projects = 250
        settings.stat_volunteers = 500
        settings.stat_cities = 5
        
        settings.save()
        self.stdout.write(self.style.SUCCESS('  ✓ Site ayarları güncellendi'))

    def create_news(self):
        """Örnek haberler oluştur"""
        news_data = [
            {
                'title': 'Umut Vagonu Ramazan Yardımlarına Başladı',
                'summary': 'Derneğimiz, Ramazan ayı boyunca ihtiyaç sahibi ailelere gıda kolisi dağıtımına başladı.',
                'content': '''Umut Vagonu Derneği olarak, Ramazan ayının bereketini ihtiyaç sahibi ailelerimizle paylaşmak için yoğun bir çalışma içerisindeyiz.

Bu yıl hedefimiz 500 aileye ulaşmak. Her gıda kolisinde; pirinç, bulgur, makarna, un, şeker, çay, yağ ve konserve ürünler bulunmaktadır.

Bağışlarınızla bu güzel işe ortak olabilirsiniz.''',
                'is_featured': True,
                'is_published': True,
            },
            {
                'title': 'Okul Öncesi Eğitim Desteği Projemiz Başlıyor',
                'summary': 'Dezavantajlı bölgelerdeki çocuklarımız için okul öncesi eğitim desteği projemizi hayata geçiriyoruz.',
                'content': '''Eğitimde fırsat eşitliği için önemli bir adım atıyoruz. Dezavantajlı bölgelerdeki 3-6 yaş arası çocuklarımız için okul öncesi eğitim desteği projemizi başlatıyoruz.

Proje kapsamında:
- Okul malzemesi desteği
- Kırtasiye yardımı
- Eğitim materyalleri
- Pedagog desteği sağlanacaktır.

Gönüllülerimizle birlikte çocuklarımızın geleceğine umut taşıyoruz.''',
                'is_featured': False,
                'is_published': True,
            },
            {
                'title': 'Kış Yardımları Kampanyamız Devam Ediyor',
                'summary': 'Soğuk kış günlerinde ihtiyaç sahibi ailelerimize kışlık giysi ve battaniye yardımı yapıyoruz.',
                'content': '''Kış aylarının yaklaşmasıyla birlikte "Üşüyen Kalmasın" kampanyamızı başlattık.

Kampanya kapsamında:
- Kışlık mont ve kaban
- Battaniye ve yorgan
- Bot ve kışlık ayakkabı
- Bere, eldiven, atkı

Bağışlarınızı dernek merkezimize ulaştırabilir veya bizi arayarak bilgi alabilirsiniz.''',
                'is_featured': True,
                'is_published': True,
            },
            {
                'title': 'Gönüllü Eğitim Programı Başvuruları Açıldı',
                'summary': 'Derneğimizde gönüllü olmak isteyen herkes için eğitim programımız başlıyor.',
                'content': '''Umut Vagonu ailesine katılmak isteyen herkesi gönüllü eğitim programımıza davet ediyoruz.

Eğitim programımızda:
- Sivil toplum bilinci
- Proje yönetimi
- İletişim becerileri
- Saha çalışması

konuları işlenecektir. Başvurularınızı web sitemiz üzerinden yapabilirsiniz.''',
                'is_featured': False,
                'is_published': True,
            },
            {
                'title': 'Bayram Öncesi Çocuklara Bayramlık Dağıtımı',
                'summary': 'Bayramın sevincini çocuklarımızla paylaşmak için bayramlık kıyafet dağıtımı yapıyoruz.',
                'content': '''Her çocuk bayramda yeni kıyafetleri hak ediyor!

Bayram öncesi gerçekleştirdiğimiz "Mutlu Bayramlar" projemiz kapsamında 200 çocuğumuza bayramlık kıyafet hediye ettik.

Gönüllülerimizin özverili çalışmalarıyla gerçekleştirdiğimiz bu etkinlikte çocukların yüzlerindeki mutluluk bizim en büyük ödülümüz oldu.''',
                'is_featured': False,
                'is_published': True,
            },
        ]
        
        for i, data in enumerate(news_data):
            news, created = News.objects.get_or_create(
                title=data['title'],
                defaults={
                    'summary': data['summary'],
                    'content': data['content'],
                    'is_featured': data['is_featured'],
                    'is_published': data['is_published'],
                    'published_date': timezone.now() - timezone.timedelta(days=i*7),
                }
            )
            if created:
                self.stdout.write(f'  ✓ Haber oluşturuldu: {news.title[:40]}...')

    def create_writers_and_articles(self):
        """Yazarlar ve makaleleri oluştur"""
        writers_data = [
            {
                'name': 'Ahmet Yılmaz',
                'bio': 'Umut Vagonu Derneği Yönetim Kurulu Başkanı. 10 yılı aşkın sivil toplum deneyimi.',
                'email': 'ahmet@umutvagonu.org',
                'order': 1,
            },
            {
                'name': 'Ayşe Demir',
                'bio': 'Gönüllü koordinatörü ve sosyal hizmet uzmanı. Toplumsal dayanışma projelerinde aktif görev alıyor.',
                'email': 'ayse@umutvagonu.org',
                'order': 2,
            },
            {
                'name': 'Mehmet Kaya',
                'bio': 'Proje yöneticisi ve eğitimci. Çocuk hakları alanında çalışmalar yürütüyor.',
                'email': 'mehmet@umutvagonu.org',
                'order': 3,
            },
        ]
        
        for data in writers_data:
            writer, created = Writer.objects.get_or_create(
                name=data['name'],
                defaults={
                    'bio': data['bio'],
                    'email': data['email'],
                    'order': data['order'],
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(f'  ✓ Yazar oluşturuldu: {writer.name}')
        
        # Makaleler
        articles_data = [
            {
                'writer': 'Ahmet Yılmaz',
                'title': 'Gönüllülüğün Gücü',
                'content': '''Gönüllülük, toplumsal dayanışmanın en güzel örneğidir. Hiçbir karşılık beklemeden, sadece insanlık adına bir şeyler yapmak...

Umut Vagonu'nda geçirdiğim yıllar boyunca yüzlerce gönüllümüzle tanıştım. Her birinin hikayesi birbirinden güzel ve ilham verici.

Gönüllülük sadece yardım etmek değil; aynı zamanda öğrenmek, gelişmek ve dönüşmektir. Bir çocuğun gözlerindeki ışığı görmek, bir annenin teşekkür dolu bakışlarına muhatap olmak... Bunlar para ile satın alınamayacak deneyimler.

Siz de bu güzel ailenin bir parçası olabilirsiniz.''',
            },
            {
                'writer': 'Ayşe Demir',
                'title': 'Toplumsal Dayanışma ve Sivil Toplum',
                'content': '''Sivil toplum kuruluşları, devlet ve özel sektör arasındaki boşluğu dolduran önemli aktörlerdir.

Biz Umut Vagonu olarak, ihtiyaç sahiplerine ulaşırken aynı zamanda toplumsal bilinci de artırmaya çalışıyoruz.

Her bağış, her yardım eli, her gönüllü katılım; toplumsal dayanışmamızı güçlendiren bir tuğla gibidir. Hep birlikte daha adil, daha eşit bir toplum inşa edebiliriz.''',
            },
            {
                'writer': 'Mehmet Kaya',
                'title': 'Eğitimde Fırsat Eşitliği',
                'content': '''Her çocuk kaliteli eğitime erişim hakkına sahiptir. Ancak maalesef ülkemizde pek çok çocuk bu haktan yoksundur.

Umut Vagonu olarak eğitim projelerimizle bu eşitsizliği azaltmaya çalışıyoruz. Burslayan öğrenciler, okul malzemesi desteği, eğitim materyalleri...

Bir çocuğun eğitimine yatırım yapmak, geleceğe yatırım yapmaktır. Bu yolda bizimle yürümek ister misiniz?''',
            },
        ]
        
        for data in articles_data:
            try:
                writer = Writer.objects.get(name=data['writer'])
                article, created = Article.objects.get_or_create(
                    title=data['title'],
                    defaults={
                        'writer': writer,
                        'content': data['content'],
                        'is_published': True,
                    }
                )
                if created:
                    self.stdout.write(f'  ✓ Makale oluşturuldu: {article.title[:40]}...')
            except Writer.DoesNotExist:
                pass

    def create_gallery(self):
        """Galeri kategorileri oluştur"""
        categories_data = [
            {'name': 'Yardım Faaliyetleri', 'description': 'Gıda, giysi ve diğer yardım dağıtımları', 'order': 1},
            {'name': 'Eğitim Projeleri', 'description': 'Eğitim desteği ve okul projeleri', 'order': 2},
            {'name': 'Etkinlikler', 'description': 'Dernek etkinlikleri ve organizasyonlar', 'order': 3},
            {'name': 'Gönüllü Çalışmaları', 'description': 'Gönüllülerimizle gerçekleştirilen çalışmalar', 'order': 4},
        ]
        
        for data in categories_data:
            category, created = GalleryCategory.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'order': data['order'],
                }
            )
            if created:
                self.stdout.write(f'  ✓ Kategori oluşturuldu: {category.name}')

    def create_links(self):
        """Bağlantılar oluştur"""
        links_data = [
            {
                'title': 'Gönüllü Başvuru Formu',
                'url': 'https://form.jotform.com/203173309074046',
                'description': 'Umut Vagonu ailesine katılmak için gönüllü başvuru formunu doldurun.',
                'icon': 'fa-solid fa-hand-holding-heart',
                'is_featured': True,
                'order': 1,
            },
            {
                'title': 'Instagram',
                'url': 'https://www.instagram.com/umutvagonumanisa/',
                'description': 'Instagram hesabımızı takip edin.',
                'icon': 'fa-brands fa-instagram',
                'is_featured': True,
                'order': 2,
            },
            {
                'title': 'Facebook',
                'url': 'https://www.facebook.com/umutvagonutr/',
                'description': 'Facebook sayfamızı takip edin.',
                'icon': 'fa-brands fa-facebook',
                'is_featured': True,
                'order': 3,
            },
            {
                'title': 'Twitter/X',
                'url': 'https://x.com/umutvagonu45',
                'description': 'X hesabımızı takip edin.',
                'icon': 'fa-brands fa-x-twitter',
                'is_featured': False,
                'order': 4,
            },
            {
                'title': 'Bağış Hesabı',
                'url': '#',
                'description': 'Bağış yapmak için tıklayın.',
                'icon': 'fa-solid fa-circle-dollar-to-slot',
                'is_featured': True,
                'order': 5,
            },
        ]
        
        for data in links_data:
            link, created = Link.objects.get_or_create(
                title=data['title'],
                defaults={
                    'url': data['url'],
                    'description': data['description'],
                    'icon': data['icon'],
                    'is_featured': data['is_featured'],
                    'is_active': True,
                    'order': data['order'],
                }
            )
            if created:
                self.stdout.write(f'  ✓ Bağlantı oluşturuldu: {link.title}')
