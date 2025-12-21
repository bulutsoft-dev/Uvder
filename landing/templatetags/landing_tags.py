from django import template
from django.utils.safestring import mark_safe
from landing.models import SiteContent

register = template.Library()

@register.simple_tag
def get_site_content(key, default_text=""):
    """
    Veritabanından SiteContent değerini çeker.
    Eğer kayıt yoksa veya aktif değilse 'default_text' döner.
    """
    try:
        content = SiteContent.objects.get(key=key, is_active=True)
        return mark_safe(content.content_text)
    except SiteContent.DoesNotExist:
        return mark_safe(default_text)
