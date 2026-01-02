from django.db import models
from django.utils import timezone
from .utils import get_unique_slug


class SiteSettings(models.Model):
    """
    Site Ayarları - Singleton Model
    --------------------------------
    Sitenin genel yapılandırması burada tutulur.
    Sadece tek bir kayıt olabilir.
    """
    site_title = models.CharField(
        max_length=200, 
        default="Umut Vagonu", 
        verbose_name="Site Başlığı",
        help_text="Tarayıcı sekmesinde ve logoda görünecek başlık."
    )
    slogan = models.CharField(
        max_length=300, 
        default="Geleceğe Umut Taşıyoruz", 
        verbose_name="Slogan",
        help_text="Logo altında ve sayfa başlıklarında görünür."
    )

    about_text = models.TextField(
        blank=True,
        verbose_name="Hakkımızda Metni",
        default="Umut Vagonu Derneği, ihtiyaç sahiplerine ulaşmak, yüzlerde bir tebessüm oluşturmak için durmaksızın çalışan bir sivil toplum kuruluşudur.",
        help_text="Footer ve meta açıklamalarında kullanılır."
    )

    # Görsel ve Varlıklar
    logo = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True,
        verbose_name="Logo",
        help_text="Site logosu. Önerilen boyut: 200x60 piksel (PNG veya SVG)."
    )
    favicon = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True,
        verbose_name="Favicon",
        help_text="Tarayıcı sekmesinde görünen ikon. Önerilen: 32x32 piksel (PNG)."
    )

    # Geliştirici Bilgileri
    developer_name = models.CharField(
        max_length=100,
        default="Furkan Bulut",
        verbose_name="Geliştirici Adı",
        help_text="Footer'da görünecek geliştirici adı."
    )
    developer_url = models.URLField(
        default="https://furkanbulut.vercel.app/",
        verbose_name="Geliştirici Linki",
        help_text="Geliştiricinin web sitesi."
    )
    
    # Site URL - Linktree için
    site_url = models.URLField(
        default="https://umutvagonu.org/",
        verbose_name="Site Adresi",
        help_text="Linktree sayfasında 'Ana Siteye Git' butonu için kullanılacak adres."
    )
    
    
    # İletişim Bilgileri
    contact_phone = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name="Telefon",
        help_text="Örn: 0555 123 45 67"
    )
    contact_email = models.EmailField(
        blank=True, 
        verbose_name="E-posta",
        help_text="Örn: bilgi@umutvagonu.org"
    )
    contact_address = models.TextField(
        blank=True, 
        verbose_name="Adres",
        help_text="Dernek merkez adresi."
    )
    
    # Banka Bilgileri
    bank_name = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Banka Adı",
        help_text="Örn: Ziraat Bankası"
    )
    bank_account = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Hesap No",
        help_text="Banka hesap numarası."
    )
    bank_iban = models.CharField(
        max_length=50, 
        blank=True, 
        verbose_name="IBAN",
        help_text="TR ile başlayan IBAN numarası."
    )
    
    # Sosyal Medya
    instagram_url = models.URLField(
        blank=True, 
        verbose_name="Instagram",
        help_text="Instagram profil URL'si. Örn: https://instagram.com/umutvagonumanisa"
    )
    facebook_url = models.URLField(
        blank=True, 
        verbose_name="Facebook",
        help_text="Facebook sayfa URL'si."
    )
    twitter_url = models.URLField(
        blank=True, 
        verbose_name="Twitter/X",
        help_text="Twitter profil URL'si."
    )
    youtube_url = models.URLField(
        blank=True, 
        verbose_name="YouTube",
        help_text="YouTube kanal URL'si."
    )
    
    # İstatistikler
    stat_lives_touched = models.IntegerField(
        default=10000, 
        verbose_name="Ulaşılan Hayat",
        help_text="Ana sayfada gösterilen 'Ulaşılan Hayat' sayısı."
    )
    stat_projects = models.IntegerField(
        default=100, 
        verbose_name="Tamamlanan Proje",
        help_text="Ana sayfada gösterilen 'Tamamlanan Proje' sayısı."
    )
    stat_volunteers = models.IntegerField(
        default=1000, 
        verbose_name="Gönüllü Sayısı",
        help_text="Ana sayfada gösterilen 'Gönüllü Ordusu' sayısı."
    )
    stat_cities = models.IntegerField(
        default=81, 
        verbose_name="Hizmet Verilen İl",
        help_text="Ana sayfada gösterilen 'Hizmet Verilen İl' sayısı."
    )

    class Meta:
        verbose_name = "Site Ayarları"
        verbose_name_plural = "Site Ayarları"

    def save(self, *args, **kwargs):
        # Singleton pattern - sadece bir kayıt olabilir
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # Silmeyi engelle

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Site Ayarları"


class News(models.Model):
    """
    Haberler
    --------
    Derneğin güncel haberlerini yönetir.
    """
    title = models.CharField(
        max_length=300, 
        verbose_name="Başlık",
        help_text="Haberin başlığı. Kısa ve etkileyici olmalı."
    )
    slug = models.SlugField(
        max_length=300, 
        unique=True, 
        blank=True, 
        verbose_name="URL Slug",
        help_text="Otomatik oluşturulur. Haberin web adresinde görünür (örn: /haberler/haber-basligi)"
    )
    summary = models.TextField(
        max_length=500, 
        verbose_name="Özet",
        help_text="Haber listelerinde görünen kısa açıklama. 2-3 cümle yeterli."
    )
    content = models.TextField(
        verbose_name="İçerik",
        help_text="Haberin tam metni. Paragraflar arasında boş satır bırakın."
    )
    image = models.ImageField(
        upload_to='news/', 
        blank=True, 
        null=True, 
        verbose_name="Kapak Görseli",
        help_text="Önerilen boyut: 1200x630 piksel (16:9 oran)."
    )
    
    is_featured = models.BooleanField(
        default=False, 
        verbose_name="Öne Çıkan",
        help_text="İşaretlenirse haber ana sayfada büyük olarak gösterilir."
    )
    is_published = models.BooleanField(
        default=True, 
        verbose_name="Yayında",
        help_text="İşaretlenmezse haber sitede görünmez (Taslak)."
    )
    
    published_date = models.DateTimeField(
        default=timezone.now, 
        verbose_name="Yayın Tarihi",
        help_text="Haber bu tarihten itibaren görünür olur."
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")

    class Meta:
        verbose_name = "Haber"
        verbose_name_plural = "Haberler"
        ordering = ['-published_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'title', 'slug')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Writer(models.Model):
    """
    Yazarlar
    --------
    Köşe yazarları profilleri.
    """
    name = models.CharField(
        max_length=200, 
        verbose_name="Ad Soyad",
        help_text="Yazarın tam adı."
    )
    slug = models.SlugField(
        max_length=200, 
        unique=True, 
        blank=True, 
        verbose_name="URL Slug",
        help_text="Otomatik oluşturulur."
    )
    bio = models.TextField(
        blank=True, 
        verbose_name="Biyografi",
        help_text="Yazarın kısa özgeçmişi. Yazar profil sayfasında görünür."
    )
    photo = models.ImageField(
        upload_to='writers/', 
        blank=True, 
        null=True, 
        verbose_name="Fotoğraf",
        help_text="Profil fotoğrafı. Kare formatta (1:1 oran) önerilir."
    )
    email = models.EmailField(
        blank=True, 
        verbose_name="E-posta",
        help_text="Opsiyonel. Okuyucuların yazara ulaşması için."
    )
    
    is_active = models.BooleanField(
        default=True, 
        verbose_name="Aktif",
        help_text="Pasif yazarlar listede görünmez."
    )
    order = models.IntegerField(
        default=0, 
        verbose_name="Sıralama",
        help_text="Küçük sayı önce görünür. Örn: 1, 2, 3..."
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        verbose_name = "Yazar"
        verbose_name_plural = "Yazarlar"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'name', 'slug')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    Köşe Yazıları
    -------------
    Yazarların köşe yazıları.
    """
    writer = models.ForeignKey(
        Writer, 
        on_delete=models.PROTECT, 
        related_name='articles', 
        verbose_name="Yazar",
        help_text="Bu yazıyı yazan kişi."
    )
    title = models.CharField(
        max_length=300, 
        verbose_name="Başlık",
        help_text="Yazının başlığı."
    )
    slug = models.SlugField(
        max_length=300, 
        unique=True, 
        blank=True, 
        verbose_name="URL Slug",
        help_text="Otomatik oluşturulur."
    )
    content = models.TextField(
        verbose_name="İçerik",
        help_text="Yazının tam metni. Paragraflar arasında boş satır bırakın."
    )
    image = models.ImageField(
        upload_to='articles/', 
        blank=True, 
        null=True, 
        verbose_name="Görsel",
        help_text="Opsiyonel kapak görseli."
    )
    
    is_published = models.BooleanField(
        default=True, 
        verbose_name="Yayında",
        help_text="İşaretlenmezse yazı sitede görünmez."
    )
    published_date = models.DateTimeField(
        default=timezone.now, 
        verbose_name="Yayın Tarihi"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        verbose_name = "Köşe Yazısı"
        verbose_name_plural = "Köşe Yazıları"
        ordering = ['-published_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'title', 'slug')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.writer.name}"


class GalleryCategory(models.Model):
    """
    Galeri Kategorileri
    -------------------
    Fotoğrafları gruplamak için kullanılır.
    """
    name = models.CharField(
        max_length=200, 
        verbose_name="Kategori Adı",
        help_text="Örn: Eğitim Projeleri, Yardım Dağıtımları, Etkinlikler..."
    )
    slug = models.SlugField(
        max_length=200, 
        unique=True, 
        blank=True, 
        verbose_name="URL Slug",
        help_text="Otomatik oluşturulur."
    )
    description = models.TextField(
        blank=True, 
        verbose_name="Açıklama",
        help_text="Kategori hakkında kısa açıklama (opsiyonel)."
    )
    order = models.IntegerField(
        default=0, 
        verbose_name="Sıralama",
        help_text="Küçük sayı önce görünür."
    )

    class Meta:
        verbose_name = "Galeri Kategorisi"
        verbose_name_plural = "Galeri Kategorileri"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'name', 'slug')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    """
    Galeri Görselleri
    -----------------
    Fotoğraf galerisi görselleri.
    """
    category = models.ForeignKey(
        GalleryCategory, 
        on_delete=models.CASCADE, 
        related_name='images', 
        verbose_name="Kategori",
        help_text="Bu görsel hangi kategoriye ait?"
    )
    title = models.CharField(
        max_length=200, 
        verbose_name="Başlık",
        help_text="Görseli tanımlayan kısa başlık."
    )
    image = models.ImageField(
        upload_to='gallery/', 
        verbose_name="Görsel",
        help_text="JPG veya PNG formatında. Önerilen max boyut: 2MB."
    )
    description = models.TextField(
        blank=True, 
        verbose_name="Açıklama",
        help_text="Görsel hakkında detaylı bilgi (opsiyonel)."
    )
    
    is_featured = models.BooleanField(
        default=False, 
        verbose_name="Öne Çıkan",
        help_text="Ana sayfada görünsün mü?"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Yükleme Tarihi")

    class Meta:
        verbose_name = "Galeri Görseli"
        verbose_name_plural = "Galeri Görselleri"
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title


class Link(models.Model):
    """
    Bağlantılar
    -----------
    Önemli dış bağlantılar ve sosyal medya linkleri.
    """
    ICON_CHOICES = [
        ('fas fa-link', '🔗 Genel Link'),
        ('fab fa-instagram', '📷 Instagram'),
        ('fab fa-facebook', '📘 Facebook'),
        ('fab fa-twitter', '🐦 Twitter/X'),
        ('fab fa-youtube', '📺 YouTube'),
        ('fab fa-whatsapp', '💬 WhatsApp'),
        ('fas fa-globe', '🌐 Web Sitesi'),
        ('fas fa-newspaper', '📰 Haber'),
        ('fas fa-file-pdf', '📄 PDF'),
        ('fas fa-hand-holding-heart', '❤️ Bağış'),
        ('fas fa-users', '👥 Gönüllü'),
        ('fas fa-envelope', '📧 E-posta'),
        ('fas fa-phone', '📞 Telefon'),
    ]
    
    title = models.CharField(
        max_length=200, 
        verbose_name="Başlık",
        help_text="Bağlantının görünen adı."
    )
    url = models.URLField(
        verbose_name="URL",
        help_text="Tam web adresi. Örn: https://instagram.com/kullanici"
    )
    description = models.TextField(
        blank=True, 
        verbose_name="Açıklama",
        help_text="Bağlantı hakkında kısa açıklama (opsiyonel)."
    )
    icon = models.CharField(
        max_length=50, 
        choices=ICON_CHOICES, 
        default='fas fa-link', 
        verbose_name="İkon",
        help_text="Bağlantı yanında gösterilecek simge."
    )
    
    is_active = models.BooleanField(
        default=True, 
        verbose_name="Aktif",
        help_text="Pasif bağlantılar sitede görünmez."
    )
    is_featured = models.BooleanField(
        default=False, 
        verbose_name="Öne Çıkan",
        help_text="Ana sayfada 'Hızlı Erişim' bölümünde görünsün mü?"
    )
    order = models.IntegerField(
        default=0, 
        verbose_name="Sıralama",
        help_text="Küçük sayı önce görünür."
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        verbose_name = "Bağlantı"
        verbose_name_plural = "Bağlantılar"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """
    İletişim Mesajları
    ------------------
    İletişim formu üzerinden gelen mesajlar.
    """
    name = models.CharField(
        max_length=200, 
        verbose_name="Ad Soyad"
    )
    email = models.EmailField(
        verbose_name="E-posta"
    )
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name="Telefon"
    )
    subject = models.CharField(
        max_length=300, 
        verbose_name="Konu"
    )
    message = models.TextField(
        verbose_name="Mesaj"
    )
    
    is_read = models.BooleanField(
        default=False, 
        verbose_name="Okundu",
        help_text="Mesaj incelendi mi?"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Gönderim Tarihi")

    class Meta:
        verbose_name = "İletişim Mesajı"
        verbose_name_plural = "İletişim Mesajları"
        ordering = ['-created_at']


class SiteContent(models.Model):
    """
    Site İçerikleri
    ---------------
    Sabit alanlardaki dinamik içerikleri yönetir.
    (Navbar menüleri, buton yazıları, başlıklar vb.)
    """
    key = models.SlugField(
        max_length=200, 
        unique=True, 
        verbose_name="İçerik Anahtarı",
        help_text="Yazılımcı tarafından belirlenen benzersiz kod. Örn: 'nav_home', 'footer_about_title'. DEĞİŞTİRMEYİNİZ!"
    )
    content_text = models.TextField(
        verbose_name="İçerik",
        help_text="Görünecek metin veya HTML kodu."
    )
    description = models.CharField(
        max_length=300, 
        verbose_name="Açıklama",
        help_text="Bu içeriğin nerede kullanıldığını hatırlatmak için kısa not."
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name="Aktif",
        help_text="Pasif yapılırsa varsayılan metin görünür."
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")

    class Meta:
        verbose_name = "Site İçeriği"
        verbose_name_plural = "Site İçerikleri"
        ordering = ['key']

    def __str__(self):
        return f"{self.description} ({self.key})"


class NavbarContent(SiteContent):
    class Meta:
        proxy = True
        verbose_name = "Navbar Ayarı"
        verbose_name_plural = "Navbar Ayarları"


class HomeContent(SiteContent):
    class Meta:
        proxy = True
        verbose_name = "Ana Sayfa Ayarı"
        verbose_name_plural = "Ana Sayfa Ayarları"


class AboutContent(SiteContent):
    class Meta:
        proxy = True
        verbose_name = "Hakkımızda Ayarı"
        verbose_name_plural = "Hakkımızda Ayarları"


class OrgPageContent(SiteContent):
    class Meta:
        proxy = True
        verbose_name = "Organizasyon Sayfası Ayarı"
        verbose_name_plural = "Organizasyon Sayfası Ayarları"


class ContactContent(SiteContent):
    class Meta:
        proxy = True
        verbose_name = "İletişim Ayarı"
        verbose_name_plural = "İletişim Ayarları"


class FooterContent(SiteContent):
    class Meta:
        proxy = True
        verbose_name = "Footer Ayarı"
        verbose_name_plural = "Footer Ayarları"


class NewsContent(SiteContent):
    class Meta:
        proxy = True
        verbose_name = "Haber Sayfası Ayarı"
        verbose_name_plural = "Haber Sayfası Ayarları"


class GalleryContent(SiteContent):
    class Meta:
        proxy = True
        verbose_name = "Galeri Sayfası Ayarı"
        verbose_name_plural = "Galeri Sayfası Ayarları"


class WriterContent(SiteContent):
    class Meta:
        proxy = True
        verbose_name = "Yazar Köşesi Ayarı"
        verbose_name_plural = "Yazar Köşesi Ayarları"


class LinkContent(SiteContent):
    class Meta:
        proxy = True
        verbose_name = "Bağlantılar Sayfası Ayarı"
        verbose_name_plural = "Bağlantılar Sayfası Ayarları"


class ErrorPageContent(SiteContent):
    class Meta:
        proxy = True
        verbose_name = "Hata Sayfaları Ayarı"
        verbose_name_plural = "Hata Sayfaları Ayarları"


class AdminDashboardContent(SiteContent):
    class Meta:
        proxy = True
        verbose_name = "Admin Panel İçerik Ayarı"
        verbose_name_plural = "Admin Panel İçerik Ayarları"


class ArticleDetailContent(SiteContent):
    class Meta:
        proxy = True
        verbose_name = "Yazı Detay Sayfası Ayarı"
        verbose_name_plural = "Yazı Detay Sayfası Ayarları"


class AboutCard(models.Model):
    """
    Hakkımızda Sayfası Kartları
    ----------------------------
    Misyon, Vizyon, Değerler gibi kartları dinamik olarak yönetir.
    """
    CARD_TYPE_CHOICES = [
        ('mission_vision', 'Misyon & Vizyon Kartları'),
        ('activity', 'Neler Yapıyoruz Kartları'),
    ]

    ICON_CHOICES = [
        ('fas fa-bullseye', '🎯 Hedef (Misyon)'),
        ('fas fa-eye', '👁️ Göz (Vizyon)'),
        ('fas fa-gem', '💎 Değer'),
        ('fas fa-heart', '❤️ Kalp'),
        ('fas fa-hand-holding-heart', '🤲 Yardım'),
        ('fas fa-graduation-cap', '🎓 Eğitim'),
        ('fas fa-users', '👥 İnsanlar'),
        ('fas fa-globe', '🌍 Dünya'),
        ('fas fa-lightbulb', '💡 Ampul'),
        ('fas fa-star', '⭐ Yıldız'),
        ('fas fa-seedling', '🌱 Fidan'),
        ('fas fa-hands-helping', '🤝 Dayanışma'),
        ('fas fa-book', '📖 Kitap'),
        ('fas fa-school', '🏫 Okul'),
        ('fas fa-home', '🏠 Ev'),
        ('fas fa-gift', '🎁 Hediye'),
    ]

    card_type = models.CharField(
        max_length=20,
        choices=CARD_TYPE_CHOICES,
        default='mission_vision',
        verbose_name="Kart Türü",
        help_text="Kartın nerede görüneceğini belirler."
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Başlık",
        help_text="Kartın başlığı. Örn: Misyonumuz, Vizyonumuz"
    )
    content = models.TextField(
        verbose_name="İçerik",
        help_text="Kartın açıklama metni."
    )
    icon = models.CharField(
        max_length=50,
        choices=ICON_CHOICES,
        default='fas fa-star',
        verbose_name="İkon",
        help_text="Kartın ikonu."
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Sıralama",
        help_text="Küçük sayı önce görünür."
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktif",
        help_text="Pasif kartlar sitede görünmez."
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")

    class Meta:
        verbose_name = "Hakkımızda Kartı"
        verbose_name_plural = "Hakkımızda Kartları"
        ordering = ['card_type', 'order']

    def __str__(self):
        return f"{self.get_card_type_display()} - {self.title}"


class OrganizationMember(models.Model):
    """
    Organizasyon Üyeleri
    --------------------
    Dernek yönetim kadrosunu ve üye hiyerarşisini yönetir.
    """
    
    # Rol türleri (hiyerarşi sırası)
    ROLE_FOUNDER = 1
    ROLE_BOARD = 2
    ROLE_SUPERVISOR = 3
    ROLE_TEAM_LEAD = 4
    ROLE_VOLUNTEER = 5
    
    ROLE_CHOICES = [
        (ROLE_FOUNDER, 'Kurucu Üye'),
        (ROLE_BOARD, 'Yönetim Kurulu'),
        (ROLE_SUPERVISOR, 'Denetim Kurulu'),
        (ROLE_TEAM_LEAD, 'Takım Lideri'),
        (ROLE_VOLUNTEER, 'Gönüllü'),
    ]
    
    name = models.CharField(
        max_length=200, 
        verbose_name="Ad Soyad",
        help_text="Üyenin tam adı."
    )
    title = models.CharField(
        max_length=200, 
        verbose_name="Unvan",
        help_text="Görevi/Pozisyonu. Örn: Başkan, Genel Sekreter, Sayman."
    )
    photo = models.ImageField(
        upload_to='organization/', 
        blank=True, 
        null=True,
        verbose_name="Fotoğraf",
        help_text="Profil fotoğrafı. Önerilen boyut: 400x400 piksel (kare)."
    )
    bio = models.TextField(
        blank=True, 
        verbose_name="Biyografi",
        help_text="Kısa özgeçmiş veya tanıtım metni."
    )
    
    role_type = models.IntegerField(
        choices=ROLE_CHOICES,
        default=ROLE_VOLUNTEER,
        verbose_name="Rol Türü",
        help_text="Hiyerarşideki pozisyonu. Sayfada gruplama için kullanılır."
    )
    order = models.IntegerField(
        default=0, 
        verbose_name="Sıralama",
        help_text="Aynı rol grubundaki sıralama. Küçük sayı önce görünür."
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name="Aktif",
        help_text="Pasif üyeler sitede görünmez."
    )
    
    # Opsiyonel iletişim
    email = models.EmailField(blank=True, verbose_name="E-posta")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    
    # Sosyal medya (opsiyonel)
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn")
    twitter_url = models.URLField(blank=True, verbose_name="Twitter/X")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")

    class Meta:
        verbose_name = "Organizasyon Üyesi"
        verbose_name_plural = "Organizasyon Üyeleri"
        ordering = ['role_type', 'order', 'name']

    def __str__(self):
        return f"{self.name} - {self.get_role_type_display()}"
