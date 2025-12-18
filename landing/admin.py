from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings, News, Writer, Article, 
    GalleryCategory, GalleryImage, Link, ContactMessage
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Site Ayarları Admin"""
    fieldsets = (
        ('Genel Bilgiler', {
            'fields': ('site_title', 'slogan', 'about_text')
        }),
        ('İletişim Bilgileri', {
            'fields': ('contact_phone', 'contact_email', 'contact_address')
        }),
        ('Banka Bilgileri', {
            'fields': ('bank_name', 'bank_account', 'bank_iban')
        }),
        ('Sosyal Medya', {
            'fields': ('instagram_url', 'facebook_url', 'twitter_url', 'youtube_url')
        }),
        ('İstatistikler', {
            'fields': ('stat_lives_touched', 'stat_projects', 'stat_volunteers', 'stat_cities')
        }),
    )
    
    def has_add_permission(self, request):
        # Sadece bir kayıt olabilir
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Haberler Admin"""
    list_display = ['title', 'image_preview', 'is_featured', 'is_published', 'published_date']
    list_filter = ['is_featured', 'is_published', 'published_date']
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'is_published']
    date_hierarchy = 'published_date'
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'image')
        }),
        ('İçerik', {
            'fields': ('summary', 'content')
        }),
        ('Yayın Ayarları', {
            'fields': ('is_featured', 'is_published', 'published_date')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; border-radius: 5px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Görsel"


@admin.register(Writer)
class WriterAdmin(admin.ModelAdmin):
    """Yazarlar Admin"""
    list_display = ['name', 'photo_preview', 'email', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'bio', 'email']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'order']
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 50px; border-radius: 50%;" />', obj.photo.url)
        return "-"
    photo_preview.short_description = "Fotoğraf"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Yazılar Admin"""
    list_display = ['title', 'writer', 'is_published', 'published_date']
    list_filter = ['writer', 'is_published', 'published_date']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']
    date_hierarchy = 'published_date'
    autocomplete_fields = ['writer']


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    """Galeri Kategorileri Admin"""
    list_display = ['name', 'image_count', 'order']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']
    
    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = "Görsel Sayısı"


class GalleryImageInline(admin.TabularInline):
    """Galeri Görselleri Inline"""
    model = GalleryImage
    extra = 1
    fields = ['title', 'image', 'is_featured']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    """Galeri Görselleri Admin"""
    list_display = ['title', 'image_preview', 'category', 'is_featured', 'uploaded_at']
    list_filter = ['category', 'is_featured', 'uploaded_at']
    search_fields = ['title', 'description']
    list_editable = ['is_featured']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; border-radius: 5px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Görsel"


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    """Bağlantılar Admin"""
    list_display = ['title', 'icon_preview', 'url', 'is_active', 'is_featured', 'order']
    list_filter = ['is_active', 'is_featured', 'icon']
    search_fields = ['title', 'description', 'url']
    list_editable = ['is_active', 'is_featured', 'order']
    
    def icon_preview(self, obj):
        return format_html('<i class="{}"></i>', obj.icon)
    icon_preview.short_description = "İkon"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """İletişim Mesajları Admin"""
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return False


# Admin site özelleştirmeleri
admin.site.site_header = "Umut Vagonu Yönetim Paneli"
admin.site.site_title = "Umut Vagonu Admin"
admin.site.index_title = "Hoş Geldiniz"
