from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Count
from .models import (
    SiteSettings, News, Writer, Article, 
    GalleryCategory, GalleryImage, Link, ContactMessage
)


# =============================================================================
# SITE AYARLARI
# =============================================================================
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    Site Ayarları Yönetimi
    ---------------------
    Sitenin genel ayarlarını buradan yönetebilirsiniz.
    """
    
    fieldsets = (
        ('🏠 Genel Bilgiler', {
            'fields': ('site_title', 'slogan', 'about_text'),
            'description': 'Sitenin temel bilgilerini buradan düzenleyebilirsiniz.'
        }),
        ('📞 İletişim Bilgileri', {
            'fields': ('contact_phone', 'contact_email', 'contact_address'),
            'description': 'Ziyaretçilerin size ulaşabileceği iletişim bilgileri.'
        }),
        ('🏦 Bağış / Banka Bilgileri', {
            'fields': ('bank_name', 'bank_account', 'bank_iban'),
            'description': 'Bağış yapılacak banka hesap bilgileri. Footer ve iletişim sayfasında görünür.'
        }),
        ('📱 Sosyal Medya Hesapları', {
            'fields': ('instagram_url', 'facebook_url', 'twitter_url', 'youtube_url'),
            'description': 'Sosyal medya hesaplarınızın tam URL adreslerini girin.',
            'classes': ('collapse',)
        }),
        ('📊 Ana Sayfa İstatistikleri', {
            'fields': ('stat_lives_touched', 'stat_projects', 'stat_volunteers', 'stat_cities'),
            'description': 'Ana sayfada gösterilen istatistik rakamları. Bu sayılar animasyonlu olarak gösterilir.'
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
        # Direkt düzenleme sayfasına yönlendir
        obj = SiteSettings.objects.first()
        from django.shortcuts import redirect
        return redirect(f'../sitesettings/{obj.pk}/change/')


# =============================================================================
# HABERLER
# =============================================================================
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """
    Haber Yönetimi
    --------------
    Derneğin haberlerini buradan ekleyip düzenleyebilirsiniz.
    """
    
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
    
    fieldsets = (
        ('📰 Haber Bilgileri', {
            'fields': ('title', 'slug', 'image'),
            'description': 'Haberin başlığı ve kapak görseli. Slug otomatik oluşturulur.'
        }),
        ('📝 Haber İçeriği', {
            'fields': ('summary', 'content'),
            'description': 'Özet: Haber listelerinde görünür (max 2-3 cümle). İçerik: Haberin tam metni.'
        }),
        ('⚙️ Yayın Ayarları', {
            'fields': ('is_published', 'is_featured', 'published_date'),
            'description': 'Öne çıkan haberler ana sayfada büyük olarak gösterilir.'
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html('<span style="color: #999; font-size: 12px;">Görsel yok</span>')
    image_preview.short_description = "Kapak"
    
    def status_badge(self, obj):
        if obj.is_published:
            return format_html(
                '<span style="background: #10B981; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;">Yayında</span>'
            )
        return format_html(
            '<span style="background: #F59E0B; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;">Taslak</span>'
        )
    status_badge.short_description = "Durum"
    
    def featured_badge(self, obj):
        if obj.is_featured:
            return format_html('<span style="color: #F59E0B; font-size: 18px;">⭐</span>')
        return format_html('<span style="color: #DDD;">-</span>')
    featured_badge.short_description = "Öne Çıkan"
    
    def view_on_site_link(self, obj):
        if obj.is_published:
            return format_html(
                '<a href="/haberler/{}" target="_blank" style="color: #3B82F6; text-decoration: none;">🔗 Görüntüle</a>',
                obj.slug
            )
        return "-"
    view_on_site_link.short_description = "Site"
    
    actions = ['make_published', 'make_draft', 'make_featured', 'remove_featured']
    
    @admin.action(description="✅ Seçili haberleri yayınla")
    def make_published(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f"{count} haber yayınlandı.")
    
    @admin.action(description="📝 Seçili haberleri taslak yap")
    def make_draft(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f"{count} haber taslağa alındı.")
    
    @admin.action(description="⭐ Seçili haberleri öne çıkar")
    def make_featured(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f"{count} haber öne çıkarıldı.")
    
    @admin.action(description="❌ Öne çıkarmayı kaldır")
    def remove_featured(self, request, queryset):
        count = queryset.update(is_featured=False)
        self.message_user(request, f"{count} haberden öne çıkarma kaldırıldı.")


# =============================================================================
# YAZARLAR
# =============================================================================
@admin.register(Writer)
class WriterAdmin(admin.ModelAdmin):
    """
    Yazar Yönetimi
    --------------
    Köşe yazarlarını buradan yönetebilirsiniz.
    """
    
    list_display = ['photo_preview', 'name', 'email', 'article_count', 'active_badge', 'order']
    list_display_links = ['name']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'bio', 'email']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']
    ordering = ['order', 'name']
    list_per_page = 20
    
    fieldsets = (
        ('👤 Yazar Bilgileri', {
            'fields': ('name', 'slug', 'photo'),
            'description': 'Yazarın adı ve profil fotoğrafı.'
        }),
        ('📋 Biyografi', {
            'fields': ('bio',),
            'description': 'Yazarın kısa özgeçmişi. Yazar sayfasında görünür.'
        }),
        ('📧 İletişim', {
            'fields': ('email',),
            'description': 'Opsiyonel. Okuyucuların yazara ulaşması için.'
        }),
        ('⚙️ Ayarlar', {
            'fields': ('is_active', 'order'),
            'description': 'Sıralama: Küçük sayı önce görünür.'
        }),
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 50%; border: 2px solid #3EB89A;" />',
                obj.photo.url
            )
        return format_html(
            '<div style="width: 45px; height: 45px; background: #E5E7EB; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #9CA3AF; font-size: 18px;">👤</div>'
        )
    photo_preview.short_description = "Foto"
    
    def article_count(self, obj):
        count = obj.articles.filter(is_published=True).count()
        if count > 0:
            return format_html(
                '<span style="background: #3EB89A; color: white; padding: 3px 10px; border-radius: 10px; font-size: 12px;">{} yazı</span>',
                count
            )
        return format_html('<span style="color: #999;">Yazı yok</span>')
    article_count.short_description = "Yazılar"
    
    def active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: #10B981;">✓ Aktif</span>')
        return format_html('<span style="color: #EF4444;">✗ Pasif</span>')
    active_badge.short_description = "Durum"


# =============================================================================
# KÖŞE YAZILARI
# =============================================================================
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Köşe Yazısı Yönetimi
    --------------------
    Yazarların köşe yazılarını buradan yönetebilirsiniz.
    """
    
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
    
    fieldsets = (
        ('✍️ Yazı Bilgileri', {
            'fields': ('writer', 'title', 'slug', 'image'),
            'description': 'Yazının yazarı, başlığı ve opsiyonel kapak görseli.'
        }),
        ('📝 Yazı İçeriği', {
            'fields': ('content',),
            'description': 'Yazının tam metni. HTML desteklenmez, paragraflar otomatik oluşturulur.'
        }),
        ('⚙️ Yayın Ayarları', {
            'fields': ('is_published', 'published_date'),
        }),
    )
    
    def writer_link(self, obj):
        return format_html(
            '<a href="/admin/landing/writer/{}/change/" style="color: #3EB89A; text-decoration: none; font-weight: 500;">{}</a>',
            obj.writer.pk, obj.writer.name
        )
    writer_link.short_description = "Yazar"
    
    def status_badge(self, obj):
        if obj.is_published:
            return format_html(
                '<span style="background: #10B981; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">Yayında</span>'
            )
        return format_html(
            '<span style="background: #F59E0B; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">Taslak</span>'
        )
    status_badge.short_description = "Durum"
    
    actions = ['make_published', 'make_draft']
    
    @admin.action(description="✅ Seçili yazıları yayınla")
    def make_published(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f"{count} yazı yayınlandı.")
    
    @admin.action(description="📝 Seçili yazıları taslak yap")
    def make_draft(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f"{count} yazı taslağa alındı.")


# =============================================================================
# GALERİ KATEGORİLERİ
# =============================================================================
@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    """
    Galeri Kategori Yönetimi
    ------------------------
    Fotoğraf galerisi kategorilerini buradan yönetebilirsiniz.
    """
    
    list_display = ['name', 'image_count_badge', 'order', 'description_short']
    list_display_links = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('📁 Kategori Bilgileri', {
            'fields': ('name', 'slug', 'description'),
            'description': 'Kategori adı ve opsiyonel açıklama.'
        }),
        ('⚙️ Ayarlar', {
            'fields': ('order',),
            'description': 'Sıralama: Küçük sayı önce görünür.'
        }),
    )
    
    def image_count_badge(self, obj):
        count = obj.images.count()
        if count > 0:
            return format_html(
                '<span style="background: #8B5CF6; color: white; padding: 3px 12px; border-radius: 10px; font-size: 12px;">📷 {} görsel</span>',
                count
            )
        return format_html('<span style="color: #999;">Boş</span>')
    image_count_badge.short_description = "Görseller"
    
    def description_short(self, obj):
        if obj.description:
            return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
        return "-"
    description_short.short_description = "Açıklama"


# =============================================================================
# GALERİ GÖRSELLERİ
# =============================================================================
class GalleryImageInline(admin.TabularInline):
    """Kategoriye görsel ekleme"""
    model = GalleryImage
    extra = 1
    fields = ['image', 'title', 'is_featured']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    """
    Galeri Görsel Yönetimi
    ----------------------
    Fotoğraf galerisi görsellerini buradan yönetebilirsiniz.
    """
    
    list_display = ['image_preview', 'title', 'category', 'is_featured', 'uploaded_at']
    list_display_links = ['title']
    list_filter = ['category', 'is_featured', 'uploaded_at']
    search_fields = ['title', 'description']
    list_editable = ['is_featured']
    ordering = ['-uploaded_at']
    list_per_page = 24
    
    fieldsets = (
        ('🖼️ Görsel Bilgileri', {
            'fields': ('image', 'title', 'description'),
            'description': 'Görsel dosyası ve açıklaması.'
        }),
        ('📁 Kategori', {
            'fields': ('category',),
        }),
        ('⚙️ Ayarlar', {
            'fields': ('is_featured',),
            'description': 'Öne çıkan görseller ana sayfada görünür.'
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 60px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.15);" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Önizleme"
    
    def featured_badge(self, obj):
        if obj.is_featured:
            return format_html('<span style="color: #F59E0B; font-size: 16px;">⭐</span>')
        return "-"
    featured_badge.short_description = "Öne Çıkan"
    
    actions = ['make_featured', 'remove_featured']
    
    @admin.action(description="⭐ Seçili görselleri öne çıkar")
    def make_featured(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f"{count} görsel öne çıkarıldı.")
    
    @admin.action(description="❌ Öne çıkarmayı kaldır")
    def remove_featured(self, request, queryset):
        count = queryset.update(is_featured=False)
        self.message_user(request, f"{count} görselden öne çıkarma kaldırıldı.")


# =============================================================================
# BAĞLANTILAR
# =============================================================================
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    """
    Bağlantı Yönetimi
    -----------------
    Önemli linkleri buradan yönetebilirsiniz.
    """
    
    list_display = ['icon_preview', 'title', 'url_short', 'is_active', 'is_featured', 'order']
    list_display_links = ['title']
    list_filter = ['is_active', 'is_featured', 'icon']
    search_fields = ['title', 'description', 'url']
    list_editable = ['is_active', 'is_featured', 'order']
    ordering = ['order', 'title']
    
    fieldsets = (
        ('🔗 Bağlantı Bilgileri', {
            'fields': ('title', 'url', 'description'),
            'description': 'Bağlantının adı ve adresi.'
        }),
        ('🎨 Görünüm', {
            'fields': ('icon',),
            'description': 'Bağlantı yanında gösterilecek ikon.'
        }),
        ('⚙️ Ayarlar', {
            'fields': ('is_active', 'is_featured', 'order'),
            'description': 'Öne çıkan bağlantılar ana sayfada görünür.'
        }),
    )
    
    def icon_preview(self, obj):
        return format_html(
            '<span style="display: inline-flex; align-items: center; justify-content: center; width: 35px; height: 35px; background: #3EB89A; border-radius: 8px; color: white;"><i class="{}"></i></span>',
            obj.icon
        )
    icon_preview.short_description = "İkon"
    
    def url_short(self, obj):
        short_url = obj.url[:40] + "..." if len(obj.url) > 40 else obj.url
        return format_html(
            '<a href="{}" target="_blank" style="color: #3B82F6; text-decoration: none;">{}</a>',
            obj.url, short_url
        )
    url_short.short_description = "URL"
    
    def active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: #10B981;">✓</span>')
        return format_html('<span style="color: #EF4444;">✗</span>')
    active_badge.short_description = "Aktif"
    
    def featured_badge(self, obj):
        if obj.is_featured:
            return format_html('<span style="color: #F59E0B;">⭐</span>')
        return "-"
    featured_badge.short_description = "Öne Çıkan"


# =============================================================================
# İLETİŞİM MESAJLARI
# =============================================================================
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    İletişim Mesajları
    ------------------
    Ziyaretçilerden gelen mesajları buradan görüntüleyebilirsiniz.
    """
    
    list_display = ['sender_info', 'subject', 'is_read', 'created_at']
    list_display_links = ['subject']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    list_per_page = 25
    
    fieldsets = (
        ('👤 Gönderen Bilgileri', {
            'fields': ('name', 'email', 'phone'),
        }),
        ('📧 Mesaj', {
            'fields': ('subject', 'message'),
        }),
        ('📅 Tarih Bilgisi', {
            'fields': ('created_at', 'is_read'),
        }),
    )
    
    def sender_info(self, obj):
        return format_html(
            '<div><strong>{}</strong><br><span style="color: #666; font-size: 12px;">{}</span></div>',
            obj.name, obj.email
        )
    sender_info.short_description = "Gönderen"
    
    def read_badge(self, obj):
        if obj.is_read:
            return format_html(
                '<span style="background: #10B981; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">✓ Okundu</span>'
            )
        return format_html(
            '<span style="background: #EF4444; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;">● Yeni</span>'
        )
    read_badge.short_description = "Durum"
    
    def has_add_permission(self, request):
        # Mesajlar sadece form üzerinden eklenir
        return False
    
    def has_delete_permission(self, request, obj=None):
        return True
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    @admin.action(description="✓ Seçili mesajları okundu işaretle")
    def mark_as_read(self, request, queryset):
        count = queryset.update(is_read=True)
        self.message_user(request, f"{count} mesaj okundu olarak işaretlendi.")
    
    @admin.action(description="● Seçili mesajları okunmadı işaretle")
    def mark_as_unread(self, request, queryset):
        count = queryset.update(is_read=False)
        self.message_user(request, f"{count} mesaj okunmadı olarak işaretlendi.")


# =============================================================================
# ADMIN SİTE ÖZELLEŞTİRMELERİ
# =============================================================================
admin.site.site_header = "🌿 Umut Vagonu Yönetim Paneli"
admin.site.site_title = "Umut Vagonu Admin"
admin.site.index_title = "Hoş Geldiniz! Buradan sitenizi yönetebilirsiniz."
admin.site.empty_value_display = "-"
