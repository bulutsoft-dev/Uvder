from .models import SiteSettings, Link


def site_settings(request):
    """Site ayarlarını tüm template'lere ekle"""
    try:
        settings = SiteSettings.get_settings()
    except Exception:
        # Veritabanı bağlantısı yoksa veya hata oluşursa varsayılan bir SiteSettings nesnesi oluştur
        settings = SiteSettings()

    # Footer için aktif linkleri al
    try:
        footer_links = Link.objects.filter(is_active=True)[:5]
    except Exception:
        footer_links = []
    
    return {
        'site_settings': settings,
        'footer_links': footer_links,
    }
