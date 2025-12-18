from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class SiteSettings(models.Model):
    """Site geneli ayarlar - Singleton model"""
    site_title = models.CharField(max_length=200, default="Umut Vagonu", verbose_name="Site Başlığı")
    slogan = models.CharField(max_length=300, default="Geleceğe Umut Taşıyoruz", verbose_name="Slogan")
    about_text = models.TextField(
        blank=True,
        verbose_name="Hakkımızda Metni",
        default="Umut Vagonu Derneği, ihtiyaç sahiplerine ulaşmak, yüzlerde bir tebessüm oluşturmak için durmaksızın çalışan bir sivil toplum kuruluşudur."
    )
    
    # İletişim Bilgileri
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    contact_email = models.EmailField(blank=True, verbose_name="E-posta")
    contact_address = models.TextField(blank=True, verbose_name="Adres")
    
    # Banka Bilgileri
    bank_name = models.CharField(max_length=100, blank=True, verbose_name="Banka Adı")
    bank_account = models.CharField(max_length=100, blank=True, verbose_name="Hesap No")
    bank_iban = models.CharField(max_length=50, blank=True, verbose_name="IBAN")
    
    # Sosyal Medya
    instagram_url = models.URLField(blank=True, verbose_name="Instagram")
    facebook_url = models.URLField(blank=True, verbose_name="Facebook")
    twitter_url = models.URLField(blank=True, verbose_name="Twitter/X")
    youtube_url = models.URLField(blank=True, verbose_name="YouTube")
    
    # İstatistikler
    stat_lives_touched = models.IntegerField(default=10000, verbose_name="Ulaşılan Hayat")
    stat_projects = models.IntegerField(default=100, verbose_name="Tamamlanan Proje")
    stat_volunteers = models.IntegerField(default=1000, verbose_name="Gönüllü Sayısı")
    stat_cities = models.IntegerField(default=81, verbose_name="Hizmet Verilen İl")

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
    """Haberler modeli"""
    title = models.CharField(max_length=300, verbose_name="Başlık")
    slug = models.SlugField(max_length=300, unique=True, blank=True, verbose_name="URL Slug")
    summary = models.TextField(max_length=500, verbose_name="Özet")
    content = models.TextField(verbose_name="İçerik")
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name="Kapak Görseli")
    
    is_featured = models.BooleanField(default=False, verbose_name="Öne Çıkan")
    is_published = models.BooleanField(default=True, verbose_name="Yayında")
    
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Yayın Tarihi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")

    class Meta:
        verbose_name = "Haber"
        verbose_name_plural = "Haberler"
        ordering = ['-published_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Benzersizlik kontrolü
            original_slug = self.slug
            counter = 1
            while News.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Writer(models.Model):
    """Yazarlar modeli"""
    name = models.CharField(max_length=200, verbose_name="Ad Soyad")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="URL Slug")
    bio = models.TextField(blank=True, verbose_name="Biyografi")
    photo = models.ImageField(upload_to='writers/', blank=True, null=True, verbose_name="Fotoğraf")
    email = models.EmailField(blank=True, verbose_name="E-posta")
    
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    order = models.IntegerField(default=0, verbose_name="Sıralama")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        verbose_name = "Yazar"
        verbose_name_plural = "Yazarlar"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            counter = 1
            while Writer.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    """Yazar köşesi yazıları"""
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, related_name='articles', verbose_name="Yazar")
    title = models.CharField(max_length=300, verbose_name="Başlık")
    slug = models.SlugField(max_length=300, unique=True, blank=True, verbose_name="URL Slug")
    content = models.TextField(verbose_name="İçerik")
    image = models.ImageField(upload_to='articles/', blank=True, null=True, verbose_name="Görsel")
    
    is_published = models.BooleanField(default=True, verbose_name="Yayında")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Yayın Tarihi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        verbose_name = "Yazı"
        verbose_name_plural = "Yazılar"
        ordering = ['-published_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            counter = 1
            while Article.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.writer.name}"


class GalleryCategory(models.Model):
    """Galeri kategorileri"""
    name = models.CharField(max_length=200, verbose_name="Kategori Adı")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="URL Slug")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    order = models.IntegerField(default=0, verbose_name="Sıralama")

    class Meta:
        verbose_name = "Galeri Kategorisi"
        verbose_name_plural = "Galeri Kategorileri"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    """Galeri görselleri"""
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='images', verbose_name="Kategori")
    title = models.CharField(max_length=200, verbose_name="Başlık")
    image = models.ImageField(upload_to='gallery/', verbose_name="Görsel")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    
    is_featured = models.BooleanField(default=False, verbose_name="Öne Çıkan")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Yükleme Tarihi")

    class Meta:
        verbose_name = "Galeri Görseli"
        verbose_name_plural = "Galeri Görselleri"
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title


class Link(models.Model):
    """Bağlantı linkleri"""
    ICON_CHOICES = [
        ('fas fa-link', 'Genel Link'),
        ('fab fa-instagram', 'Instagram'),
        ('fab fa-facebook', 'Facebook'),
        ('fab fa-twitter', 'Twitter/X'),
        ('fab fa-youtube', 'YouTube'),
        ('fab fa-whatsapp', 'WhatsApp'),
        ('fas fa-globe', 'Web Sitesi'),
        ('fas fa-newspaper', 'Haber'),
        ('fas fa-file-pdf', 'PDF'),
        ('fas fa-hand-holding-heart', 'Bağış'),
        ('fas fa-users', 'Gönüllü'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Başlık")
    url = models.URLField(verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='fas fa-link', verbose_name="İkon")
    
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    is_featured = models.BooleanField(default=False, verbose_name="Öne Çıkan")
    order = models.IntegerField(default=0, verbose_name="Sıralama")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        verbose_name = "Bağlantı"
        verbose_name_plural = "Bağlantılar"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """İletişim formu mesajları"""
    name = models.CharField(max_length=200, verbose_name="Ad Soyad")
    email = models.EmailField(verbose_name="E-posta")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    subject = models.CharField(max_length=300, verbose_name="Konu")
    message = models.TextField(verbose_name="Mesaj")
    
    is_read = models.BooleanField(default=False, verbose_name="Okundu")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Gönderim Tarihi")

    class Meta:
        verbose_name = "İletişim Mesajı"
        verbose_name_plural = "İletişim Mesajları"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
