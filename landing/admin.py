from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Count

# Django Unfold imports
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import action, display

from .models import (
    SiteSettings, News, Writer, Article, 
    GalleryCategory, GalleryImage, Link, ContactMessage,
    SiteContent
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
            'fields': ('site_title', 'slogan', 'about_text'),
            'description': 'Sitenin temel bilgilerini buradan düzenleyebilirsiniz.',
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
    
    fieldsets = (
        ('📰 Haber Bilgileri', {
            'fields': ('title', 'slug', 'image'),
            'description': 'Haberin başlığı ve kapak görseli. Slug otomatik oluşturulur.',
            'classes': ['tab'],
        }),
        ('📝 Haber İçeriği', {
            'fields': ('summary', 'content'),
            'description': 'Özet: Haber listelerinde görünür (max 2-3 cümle). İçerik: Haberin tam metni.',
            'classes': ['tab'],
        }),
        ('⚙️ Yayın Ayarları', {
            'fields': ('is_published', 'is_featured', 'published_date'),
            'description': 'Öne çıkan haberler ana sayfada büyük olarak gösterilir.',
            'classes': ['tab'],
        }),
    )
    
    @display(description="Kapak", label=True)
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html('<span style="color: #999; font-size: 12px;">Görsel yok</span>')
    
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
    
    fieldsets = (
        ('👤 Yazar Bilgileri', {
            'fields': ('name', 'slug', 'photo'),
            'description': 'Yazarın adı ve profil fotoğrafı.',
            'classes': ['tab'],
        }),
        ('📋 Biyografi', {
            'fields': ('bio',),
            'description': 'Yazarın kısa özgeçmişi. Yazar sayfasında görünür.',
            'classes': ['tab'],
        }),
        ('📧 İletişim', {
            'fields': ('email',),
            'description': 'Opsiyonel. Okuyucuların yazara ulaşması için.',
            'classes': ['tab'],
        }),
        ('⚙️ Ayarlar', {
            'fields': ('is_active', 'order'),
            'description': 'Sıralama: Küçük sayı önce görünür.',
            'classes': ['tab'],
        }),
    )
    
    @display(description="Foto")
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 50%; border: 2px solid #10b981;" />',
                obj.photo.url
            )
        return format_html(
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
    
    fieldsets = (
        ('✍️ Yazı Bilgileri', {
            'fields': ('writer', 'title', 'slug', 'image'),
            'description': 'Yazının yazarı, başlığı ve opsiyonel kapak görseli.',
            'classes': ['tab'],
        }),
        ('📝 Yazı İçeriği', {
            'fields': ('content',),
            'description': 'Yazının tam metni. HTML desteklenmez, paragraflar otomatik oluşturulur.',
            'classes': ['tab'],
        }),
        ('⚙️ Yayın Ayarları', {
            'fields': ('is_published', 'published_date'),
            'classes': ['tab'],
        }),
    )
    
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
    
    fieldsets = (
        ('📁 Kategori Bilgileri', {
            'fields': ('name', 'slug', 'description'),
            'description': 'Kategori adı ve opsiyonel açıklama.',
            'classes': ['tab'],
        }),
        ('⚙️ Ayarlar', {
            'fields': ('order',),
            'description': 'Sıralama: Küçük sayı önce görünür.',
            'classes': ['tab'],
        }),
    )
    
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
    
    fieldsets = (
        ('🖼️ Görsel Bilgileri', {
            'fields': ('image', 'title', 'description'),
            'description': 'Görsel dosyası ve açıklaması.',
            'classes': ['tab'],
        }),
        ('📁 Kategori', {
            'fields': ('category',),
            'classes': ['tab'],
        }),
        ('⚙️ Ayarlar', {
            'fields': ('is_featured',),
            'description': 'Öne çıkan görseller ana sayfada görünür.',
            'classes': ['tab'],
        }),
    )
    
    @display(description="Önizleme")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 60px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.15);" />',
                obj.image.url
            )
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
    
    fieldsets = (
        ('🔗 Bağlantı Bilgileri', {
            'fields': ('title', 'url', 'description'),
            'description': 'Bağlantının adı ve adresi.',
            'classes': ['tab'],
        }),
        ('🎨 Görünüm', {
            'fields': ('icon',),
            'description': 'Bağlantı yanında gösterilecek ikon.',
            'classes': ['tab'],
        }),
        ('⚙️ Ayarlar', {
            'fields': ('is_active', 'is_featured', 'order'),
            'description': 'Öne çıkan bağlantılar ana sayfada görünür.',
            'classes': ['tab'],
        }),
    )
    
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
