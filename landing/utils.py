"""
Admin Dashboard Utilities
-------------------------
Dashboard için istatistik ve yardımcı fonksiyonlar.
"""
from django.utils.text import slugify


def turkish_slugify(text):
    """
    Türkçe karakterleri düzgün şekilde dönüştüren slug fonksiyonu.
    """
    tr_map = {
        'ı': 'i', 'İ': 'i', 'ş': 's', 'Ş': 's', 'ğ': 'g', 'Ğ': 'g',
        'ü': 'u', 'Ü': 'u', 'ö': 'o', 'Ö': 'o', 'ç': 'c', 'Ç': 'c'
    }
    for tr, eng in tr_map.items():
        text = text.replace(tr, eng)
    return slugify(text)


def get_unique_slug(model_instance, slugable_field_name, slug_field_name):
    """
    Model instance için benzersiz slug oluşturur.
    """
    slug = turkish_slugify(getattr(model_instance, slugable_field_name))
    unique_slug = slug
    extension = 1
    model_class = model_instance.__class__
    
    while model_class.objects.filter(**{slug_field_name: unique_slug}).exclude(pk=model_instance.pk).exists():
        unique_slug = f'{slug}-{extension}'
        extension += 1
        
    return unique_slug


def dashboard_callback(request, context):
    """
    Dashboard için context verileri sağlar.
    Settings.py'de UNFOLD["DASHBOARD_CALLBACK"] olarak kullanılır.
    """
    from .models import News, Writer, Article, GalleryCategory, GalleryImage, Link, ContactMessage
    context.update({
        "stats": {
            # Haberler
            "news_count": News.objects.count(),
            "published_news": News.objects.filter(is_published=True).count(),
            
            # Yazarlar ve Yazılar
            "writers_count": Writer.objects.filter(is_active=True).count(),
            "articles_count": Article.objects.filter(is_published=True).count(),
            
            # Galeri
            "images_count": GalleryImage.objects.count(),
            "categories_count": GalleryCategory.objects.count(),
            
            # Mesajlar
            "messages_count": ContactMessage.objects.count(),
            "unread_messages": ContactMessage.objects.filter(is_read=False).count(),
            
            # Bağlantılar
            "links_count": Link.objects.filter(is_active=True).count(),
        }
    })
    return context


def get_news_count(request):
    """Sidebar badge için haber sayısı"""
    from .models import News
    return News.objects.filter(is_published=True).count()


def get_unread_messages_count(request):
    """Sidebar badge için okunmamış mesaj sayısı"""
    from .models import ContactMessage
    count = ContactMessage.objects.filter(is_read=False).count()
    return count if count > 0 else None
