"""
Admin Dashboard Utilities
-------------------------
Dashboard için istatistik ve yardımcı fonksiyonlar.
"""
from .models import News, Writer, Article, GalleryCategory, GalleryImage, Link, ContactMessage


def dashboard_callback(request, context):
    """
    Dashboard için context verileri sağlar.
    Settings.py'de UNFOLD["DASHBOARD_CALLBACK"] olarak kullanılır.
    """
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
    return News.objects.filter(is_published=True).count()


def get_unread_messages_count(request):
    """Sidebar badge için okunmamış mesaj sayısı"""
    count = ContactMessage.objects.filter(is_read=False).count()
    return count if count > 0 else None
