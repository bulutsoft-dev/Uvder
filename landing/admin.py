from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django.utils import timezone
from django.db.models import Count
from django.urls import reverse
from django.shortcuts import redirect

# Django Unfold imports
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import action, display

from .models import (
    SiteSettings, News, Writer, Article, 
    GalleryCategory, GalleryImage, Link, ContactMessage,
    SiteContent, OrganizationMember, AboutCard,
    NavbarContent, AboutContent, ContactContent, FooterContent,
    HomeContent, OrgPageContent, NewsContent, GalleryContent,
    WriterContent, LinkContent, ErrorPageContent, AdminDashboardContent, ArticleDetailContent
)


# =============================================================================
# SITE AYARLARI
# =============================================================================
@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    """
    Site Ayarları Yönetimi
    ---------------------
    Sitenin genel ayarlarını buradan yönetebilirsiniz.
    """
    
    # Unfold specific
    warn_unsaved_form = True
    
    fieldsets = (
        ('🏠 Genel Bilgiler', {
            'fields': ('site_title', 'slogan', 'about_text', 'logo', 'favicon'),
            'description': 'Sitenin temel bilgileri, logo ve favicon ayarları.',
            'classes': ['tab'],
        }),
        ('📞 İletişim Bilgileri', {
            'fields': ('contact_phone', 'contact_email', 'contact_address'),
            'description': 'Ziyaretçilerin size ulaşabileceği iletişim bilgileri.',
            'classes': ['tab'],
        }),
        ('🏦 Bağış / Banka Bilgileri', {
            'fields': ('bank_name', 'bank_account', 'bank_iban'),
            'description': 'Bağış yapılacak banka hesap bilgileri. Footer ve iletişim sayfasında görünür.',
            'classes': ['tab'],
        }),
        ('📱 Sosyal Medya Hesapları', {
            'fields': ('instagram_url', 'facebook_url', 'twitter_url', 'youtube_url'),
            'description': 'Sosyal medya hesaplarınızın tam URL adreslerini girin.',
            'classes': ['tab'],
        }),
        ('📊 Ana Sayfa İstatistikleri', {
            'fields': ('stat_lives_touched', 'stat_projects', 'stat_volunteers', 'stat_cities'),
            'description': 'Ana sayfada gösterilen istatistik rakamları. Bu sayılar animasyonlu olarak gösterilir.',
            'classes': ['tab'],
        }),
        ('👨‍💻 Geliştirici Bilgileri', {
            'fields': ('developer_name', 'developer_url'),
            'description': 'Footer kısmında görünecek geliştirici bilgileri.',
            'classes': ['tab'],
        }),
    )
    
    def has_add_permission(self, request):
        # Sadece bir kayıt olabilir (Singleton pattern)
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Site ayarları silinemez
        return False
    
    def changelist_view(self, request, extra_context=None):
        # Eğer kayıt yoksa otomatik oluştur
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create()
            
        obj = SiteSettings.objects.first()
        return redirect(reverse('admin:landing_sitesettings_change', args=[obj.pk]))


# =============================================================================
# HABERLER
# =============================================================================
@admin.register(News)
class NewsAdmin(ModelAdmin):
    """
    Haber Yönetimi
    --------------
    Derneğin haberlerini buradan ekleyip düzenleyebilirsiniz.
    """
    
    # Unfold specific
    warn_unsaved_form = True
    list_filter_submit = True
    list_fullwidth = True
    
    list_display = [
        'image_preview', 'title', 'status_badge', 
        'is_featured', 'published_date', 'view_on_site_link'
    ]
    list_display_links = ['title']
    list_filter = ['is_published', 'is_featured', 'published_date', 'created_at']
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured']
    date_hierarchy = 'published_date'
    ordering = ['-published_date']
    list_per_page = 20
    save_on_top = True
    
    # Gruplandırma olmadan düz alan listesi
    fields = ['title', 'slug', 'image', 'summary', 'content', 'is_published', 'is_featured', 'published_date']
    
    @display(description="Kapak", label=True)
    def image_preview(self, obj):
        if obj.image:
            try:
                return format_html(
                    '<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                    obj.image.url
                )
            except Exception:
                pass
        return mark_safe('<span style="color: #999; font-size: 12px;">Görsel yok</span>')
    
    @display(description="Durum", label={"Yayında": "success", "Taslak": "warning"})
    def status_badge(self, obj):
        return "Yayında" if obj.is_published else "Taslak"
    
    @display(description="Site")
    def view_on_site_link(self, obj):
        if obj.is_published:
            return format_html(
                '<a href="/haberler/{}" target="_blank" class="text-primary-600 hover:text-primary-700">🔗 Görüntüle</a>',
                obj.slug
            )
        return "-"
    
    actions = ['make_published', 'make_draft', 'make_featured', 'remove_featured']
    
    @action(description="✅ Seçili haberleri yayınla")
    def make_published(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f"{count} haber yayınlandı.")
    
    @action(description="📝 Seçili haberleri taslak yap")
    def make_draft(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f"{count} haber taslağa alındı.")
    
    @action(description="⭐ Seçili haberleri öne çıkar")
    def make_featured(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f"{count} haber öne çıkarıldı.")
    
    @action(description="❌ Öne çıkarmayı kaldır")
    def remove_featured(self, request, queryset):
        count = queryset.update(is_featured=False)
        self.message_user(request, f"{count} haberden öne çıkarma kaldırıldı.")


# =============================================================================
# YAZARLAR
# =============================================================================
@admin.register(Writer)
class WriterAdmin(ModelAdmin):
    """
    Yazar Yönetimi
    --------------
    Köşe yazarlarını buradan yönetebilirsiniz.
    """
    
    warn_unsaved_form = True
    list_filter_submit = True
    
    list_display = ['photo_preview', 'name', 'email', 'article_count', 'active_badge', 'order']
    list_display_links = ['name']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'bio', 'email']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']
    ordering = ['order', 'name']
    list_per_page = 20
    
    # Gruplandırma olmadan düz alan listesi
    fields = ['name', 'slug', 'photo', 'bio', 'email', 'is_active', 'order']
    
    @display(description="Foto")
    def photo_preview(self, obj):
        if obj.photo:
            try:
                return format_html(
                    '<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 50%; border: 2px solid #10b981;" />',
                    obj.photo.url
                )
            except Exception:
                pass
        return mark_safe(
            '<div style="width: 45px; height: 45px; background: #E5E7EB; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #9CA3AF; font-size: 18px;">👤</div>'
        )
    
    @display(description="Yazılar", label=True)
    def article_count(self, obj):
        count = obj.articles.filter(is_published=True).count()
        if count > 0:
            return f"{count} yazı"
        return "Yazı yok"
    
    @display(description="Durum", label={"Aktif": "success", "Pasif": "danger"})
    def active_badge(self, obj):
        return "Aktif" if obj.is_active else "Pasif"


# =============================================================================
# KÖŞE YAZILARI
# =============================================================================
@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    """
    Köşe Yazısı Yönetimi
    --------------------
    Yazarların köşe yazılarını buradan yönetebilirsiniz.
    """
    
    warn_unsaved_form = True
    list_filter_submit = True
    list_fullwidth = True
    
    list_display = ['title', 'writer_link', 'status_badge', 'published_date']
    list_display_links = ['title']
    list_filter = ['writer', 'is_published', 'published_date']
    search_fields = ['title', 'content', 'writer__name']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = []
    date_hierarchy = 'published_date'
    autocomplete_fields = ['writer']
    ordering = ['-published_date']
    list_per_page = 20
    save_on_top = True
    
    # Gruplandırma olmadan düz alan listesi
    fields = ['writer', 'title', 'slug', 'image', 'content', 'is_published', 'published_date']
    
    @display(description="Yazar")
    def writer_link(self, obj):
        return format_html(
            '<a href="/admin/landing/writer/{}/change/" class="text-primary-600 hover:text-primary-700 font-medium">{}</a>',
            obj.writer.pk, obj.writer.name
        )
    
    @display(description="Durum", label={"Yayında": "success", "Taslak": "warning"})
    def status_badge(self, obj):
        return "Yayında" if obj.is_published else "Taslak"
    
    actions = ['make_published', 'make_draft']
    
    @action(description="✅ Seçili yazıları yayınla")
    def make_published(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f"{count} yazı yayınlandı.")
    
    @action(description="📝 Seçili yazıları taslak yap")
    def make_draft(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f"{count} yazı taslağa alındı.")


# =============================================================================
# GALERİ KATEGORİLERİ
# =============================================================================
@admin.register(GalleryCategory)
class GalleryCategoryAdmin(ModelAdmin):
    """
    Galeri Kategori Yönetimi
    ------------------------
    Fotoğraf galerisi kategorilerini buradan yönetebilirsiniz.
    """
    
    warn_unsaved_form = True
    
    list_display = ['name', 'image_count_badge', 'order', 'description_short']
    list_display_links = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']
    
    # Gruplandırma olmadan düz alan listesi
    fields = ['name', 'slug', 'description', 'order']
    
    @display(description="Görseller", label=True)
    def image_count_badge(self, obj):
        count = obj.images.count()
        if count > 0:
            return f"📷 {count} görsel"
        return "Boş"
    
    @display(description="Açıklama")
    def description_short(self, obj):
        if obj.description:
            return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
        return "-"


# =============================================================================
# GALERİ GÖRSELLERİ
# =============================================================================
class GalleryImageInline(TabularInline):
    """Kategoriye görsel ekleme"""
    model = GalleryImage
    extra = 1
    fields = ['image', 'title', 'is_featured']
    tab = True


@admin.register(GalleryImage)
class GalleryImageAdmin(ModelAdmin):
    """
    Galeri Görsel Yönetimi
    ----------------------
    Fotoğraf galerisi görsellerini buradan yönetebilirsiniz.
    """
    
    warn_unsaved_form = True
    list_filter_submit = True
    list_fullwidth = True
    
    list_display = ['image_preview', 'title', 'category', 'is_featured', 'uploaded_at']
    list_display_links = ['title']
    list_filter = ['category', 'is_featured', 'uploaded_at']
    search_fields = ['title', 'description']
    list_editable = ['is_featured']
    ordering = ['-uploaded_at']
    list_per_page = 24
    
    # Gruplandırma olmadan düz alan listesi
    fields = ['category', 'title', 'image', 'description', 'is_featured']
    
    @display(description="Önizleme")
    def image_preview(self, obj):
        if obj.image:
            try:
                return format_html(
                    '<img src="{}" style="width: 80px; height: 60px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.15);" />',
                    obj.image.url
                )
            except Exception:
                pass
        return "-"
    
    actions = ['make_featured', 'remove_featured']
    
    @action(description="⭐ Seçili görselleri öne çıkar")
    def make_featured(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f"{count} görsel öne çıkarıldı.")
    
    @action(description="❌ Öne çıkarmayı kaldır")
    def remove_featured(self, request, queryset):
        count = queryset.update(is_featured=False)
        self.message_user(request, f"{count} görselden öne çıkarma kaldırıldı.")


# =============================================================================
# BAĞLANTILAR
# =============================================================================
@admin.register(Link)
class LinkAdmin(ModelAdmin):
    """
    Bağlantı Yönetimi
    -----------------
    Önemli linkleri buradan yönetebilirsiniz.
    """
    
    warn_unsaved_form = True
    list_filter_submit = True
    
    list_display = ['icon_preview', 'title', 'url_short', 'is_active', 'is_featured', 'order']
    list_display_links = ['title']
    list_filter = ['is_active', 'is_featured', 'icon']
    search_fields = ['title', 'description', 'url']
    list_editable = ['is_active', 'is_featured', 'order']
    ordering = ['order', 'title']
    
    # Gruplandırma olmadan düz alan listesi
    fields = ['title', 'url', 'description', 'icon', 'is_active', 'is_featured', 'order']
    
    @display(description="İkon")
    def icon_preview(self, obj):
        return format_html(
            '<span style="display: inline-flex; align-items: center; justify-content: center; width: 35px; height: 35px; background: #10b981; border-radius: 8px; color: white;"><i class="{}"></i></span>',
            obj.icon
        )
    
    @display(description="URL")
    def url_short(self, obj):
        short_url = obj.url[:40] + "..." if len(obj.url) > 40 else obj.url
        return format_html(
            '<a href="{}" target="_blank" class="text-primary-600 hover:text-primary-700">{}</a>',
            obj.url, short_url
        )


# =============================================================================
# İLETİŞİM MESAJLARI
# =============================================================================
@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    """
    İletişim Mesajları
    ------------------
    Ziyaretçilerden gelen mesajları buradan görüntüleyebilirsiniz.
    """
    
    warn_unsaved_form = True
    list_filter_submit = True
    list_fullwidth = True
    
    list_display = ['sender_info', 'subject', 'read_badge', 'created_at']
    list_display_links = ['subject']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = []
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    list_per_page = 25
    
    fieldsets = (
        ('👤 Gönderen Bilgileri', {
            'fields': ('name', 'email', 'phone'),
            'classes': ['tab'],
        }),
        ('📧 Mesaj', {
            'fields': ('subject', 'message'),
            'classes': ['tab'],
        }),
        ('📅 Tarih Bilgisi', {
            'fields': ('created_at', 'is_read'),
            'classes': ['tab'],
        }),
    )
    
    @display(description="Gönderen")
    def sender_info(self, obj):
        return format_html(
            '<div><strong>{}</strong><br><span class="text-gray-500 text-sm">{}</span></div>',
            obj.name, obj.email
        )
    
    @display(description="Durum", label={"Okundu": "success", "Yeni": "danger"})
    def read_badge(self, obj):
        return "Okundu" if obj.is_read else "Yeni"
    
    def has_add_permission(self, request):
        # Mesajlar sadece form üzerinden eklenir
        return False
    
    def has_delete_permission(self, request, obj=None):
        return True
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    @action(description="✓ Seçili mesajları okundu işaretle")
    def mark_as_read(self, request, queryset):
        count = queryset.update(is_read=True)
        self.message_user(request, f"{count} mesaj okundu olarak işaretlendi.")
    
    @action(description="● Seçili mesajları okunmadı işaretle")
    def mark_as_unread(self, request, queryset):
        count = queryset.update(is_read=False)
        self.message_user(request, f"{count} mesaj okunmadı olarak işaretlendi.")


# =============================================================================
# ADMIN SİTE ÖZELLEŞTİRMELERİ (Unfold handles these via UNFOLD settings)
# =============================================================================
# admin.site.site_header = "🌿 Umut Vagonu Yönetim Paneli"
# admin.site.site_title = "Umut Vagonu Admin"
# admin.site.index_title = "Hoş Geldiniz! Buradan sitenizi yönetebilirsiniz."
admin.site.empty_value_display = "-"

@admin.register(SiteContent)
class SiteContentAdmin(ModelAdmin):
    """
    Site İçerik Yönetimi
    --------------------
    Sabit metin alanlarını buradan güncelleyebilirsiniz.
    """
    warn_unsaved_form = True
    list_filter_submit = True
    
    list_display = ['key', 'description', 'content_preview', 'is_active', 'updated_at']
    list_display_links = ['key', 'description']
    search_fields = ['key', 'description', 'content_text']
    list_filter = ['is_active', 'updated_at']
    list_editable = ['is_active']
    ordering = ['key']
    
    fieldsets = (
        ('📝 İçerik Bilgileri', {
            'fields': ('key', 'description', 'content_text'),
            'description': 'Key alanını değiştirmeyiniz.',
            'classes': ['tab'],
        }),
        ('⚙️ Ayarlar', {
            'fields': ('is_active',),
            'classes': ['tab'],
        }),
    )
    
    @display(description="Önizleme")
    def content_preview(self, obj):
        text = obj.content_text
        return text[:50] + "..." if len(text) > 50 else text


@admin.register(NavbarContent)
class NavbarContentAdmin(SiteContentAdmin):
    """Navbar Ayarları"""
    def get_queryset(self, request):
        return super().get_queryset(request).filter(key__startswith='nav_')
    
    def has_add_permission(self, request):
        return False


@admin.register(AboutContent)
class AboutContentAdmin(SiteContentAdmin):
    """Hakkımızda Sayfası Ayarları"""
    def get_queryset(self, request):
        return super().get_queryset(request).filter(key__startswith='about_')

    def has_add_permission(self, request):
        return False


@admin.register(ContactContent)
class ContactContentAdmin(SiteContentAdmin):
    """İletişim Sayfası Ayarları"""
    def get_queryset(self, request):
        return super().get_queryset(request).filter(key__startswith='contact_')

    def has_add_permission(self, request):
        return False


@admin.register(FooterContent)
class FooterContentAdmin(SiteContentAdmin):
    """Footer Ayarları"""
    def get_queryset(self, request):
        return super().get_queryset(request).filter(key__startswith='footer_')

    def has_add_permission(self, request):
        return False


@admin.register(HomeContent)
class HomeContentAdmin(SiteContentAdmin):
    """Ana Sayfa Ayarları"""
    def get_queryset(self, request):
        return super().get_queryset(request).filter(key__startswith='home_')

    def has_add_permission(self, request):
        return False


@admin.register(OrgPageContent)
class OrgPageContentAdmin(SiteContentAdmin):
    """Organizasyon Sayfası Ayarları"""
    def get_queryset(self, request):
        return super().get_queryset(request).filter(key__startswith='org_')

    def has_add_permission(self, request):
        return False


@admin.register(NewsContent)
class NewsContentAdmin(SiteContentAdmin):
    """Haber Sayfası Ayarları"""
    def get_queryset(self, request):
        return super().get_queryset(request).filter(key__startswith='news_')

    def has_add_permission(self, request):
        return False


@admin.register(GalleryContent)
class GalleryContentAdmin(SiteContentAdmin):
    """Galeri Sayfası Ayarları"""
    def get_queryset(self, request):
        return super().get_queryset(request).filter(key__startswith='gallery_')

    def has_add_permission(self, request):
        return False


@admin.register(WriterContent)
class WriterContentAdmin(SiteContentAdmin):
    """Yazar Köşesi Ayarları"""
    def get_queryset(self, request):
        return super().get_queryset(request).filter(key__startswith='writer_')

    def has_add_permission(self, request):
        return False


@admin.register(LinkContent)
class LinkContentAdmin(SiteContentAdmin):
    """Bağlantılar Sayfası Ayarları"""
    def get_queryset(self, request):
        return super().get_queryset(request).filter(key__startswith='link_')

    def has_add_permission(self, request):
        return False


@admin.register(ErrorPageContent)
class ErrorPageContentAdmin(SiteContentAdmin):
    """Hata Sayfaları (400, 403, 404, 500) Ayarları"""
    def get_queryset(self, request):
        return super().get_queryset(request).filter(key__startswith='error_')

    def has_add_permission(self, request):
        return False


@admin.register(AdminDashboardContent)
class AdminDashboardContentAdmin(SiteContentAdmin):
    """Admin Dashboard Metin Ayarları"""
    def get_queryset(self, request):
        return super().get_queryset(request).filter(key__startswith='admin_')

    def has_add_permission(self, request):
        return False


@admin.register(ArticleDetailContent)
class ArticleDetailContentAdmin(SiteContentAdmin):
    """Yazı Detay Sayfası Ayarları"""
    def get_queryset(self, request):
        return super().get_queryset(request).filter(key__startswith='article_')

    def has_add_permission(self, request):
        return False


# =============================================================================
# HAKKIMIZDA KARTLARI (Misyon, Vizyon, Değerler vs.)
# =============================================================================
@admin.register(AboutCard)
class AboutCardAdmin(ModelAdmin):
    """
    Hakkımızda Kartları Yönetimi
    ----------------------------
    Misyon, Vizyon, Değerler ve Aktivite kartlarını buradan ekleyip çıkarabilirsiniz.
    """

    warn_unsaved_form = True
    list_filter_submit = True

    list_display = ['icon_preview', 'title', 'card_type_badge', 'content_preview', 'order', 'is_active']
    list_display_links = ['title']
    list_filter = ['card_type', 'is_active']
    search_fields = ['title', 'content']
    list_editable = ['order', 'is_active']
    ordering = ['card_type', 'order']
    list_per_page = 20

    fieldsets = (
        ('📝 Kart Bilgileri', {
            'fields': ('card_type', 'title', 'icon', 'content'),
            'description': 'Kartın içerik ve görünüm bilgileri.',
            'classes': ['tab'],
        }),
        ('⚙️ Ayarlar', {
            'fields': ('order', 'is_active'),
            'description': 'Sıralama ve görünürlük ayarları.',
            'classes': ['tab'],
        }),
    )

    @display(description="İkon")
    def icon_preview(self, obj):
        return format_html(
            '<span style="display: inline-flex; align-items: center; justify-content: center; width: 35px; height: 35px; background: #10b981; border-radius: 8px; color: white;"><i class="{}"></i></span>',
            obj.icon
        )

    @display(description="Kart Türü", label={"Misyon & Vizyon Kartları": "primary", "Neler Yapıyoruz Kartları": "info"})
    def card_type_badge(self, obj):
        return obj.get_card_type_display()

    @display(description="Önizleme")
    def content_preview(self, obj):
        text = obj.content
        return text[:80] + "..." if len(text) > 80 else text

    actions = ['make_active', 'make_inactive']

    @action(description="✅ Seçili kartları aktif yap")
    def make_active(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"{count} kart aktif yapıldı.")

    @action(description="❌ Seçili kartları pasif yap")
    def make_inactive(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} kart pasif yapıldı.")


# =============================================================================
# ORGANİZASYON ÜYELERİ
# =============================================================================
@admin.register(OrganizationMember)
class OrganizationMemberAdmin(ModelAdmin):
    """
    Organizasyon Üyesi Yönetimi
    ---------------------------
    Dernek yönetim kadrosunu buradan yönetebilirsiniz.
    """
    
    warn_unsaved_form = True
    list_filter_submit = True
    
    list_display = ['photo_preview', 'name', 'title', 'role_badge', 'order', 'is_active']
    list_display_links = ['name']
    list_filter = ['role_type', 'is_active']
    search_fields = ['name', 'title', 'bio']
    list_editable = ['order', 'is_active']
    ordering = ['role_type', 'order', 'name']
    list_per_page = 20
    
    # Gruplandırma olmadan düz alan listesi
    fields = ['name', 'title', 'photo', 'bio', 'role_type', 'order', 'is_active', 'email', 'phone', 'linkedin_url', 'twitter_url']
    
    @display(description="Foto")
    def photo_preview(self, obj):
        if obj.photo:
            try:
                return format_html(
                    '<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 50%; border: 2px solid #10b981;" />',
                    obj.photo.url
                )
            except Exception:
                pass
        return mark_safe(
            '<div style="width: 45px; height: 45px; background: #E5E7EB; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #9CA3AF; font-size: 18px;">👤</div>'
        )
    
    @display(description="Rol", label={
        "Kurucu Üye": "success",
        "Yönetim Kurulu": "primary",
        "Denetim Kurulu": "info",
        "Takım Lideri": "warning",
        "Gönüllü": "default",
    })
    def role_badge(self, obj):
        return obj.get_role_type_display()
