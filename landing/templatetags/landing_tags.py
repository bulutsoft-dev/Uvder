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

@register.simple_tag(takes_context=True)
def is_active(context, view_name):
    """
    Eğer render edilen view ile view_name eşleşiyorsa 'active' döner.
    """
    try:
        from django.urls import resolve
        request = context.get('request')
        if not request:
            return ""
        resolved_view = resolve(request.path_info)
        if resolved_view.view_name == view_name:
            return "active"
        # Namespace kontrolü (örneğin 'landing:' ile başlıyorsa)
        if view_name.endswith(':*') and resolved_view.view_name.startswith(view_name[:-2]):
            return "active"
    except:
        pass
    return ""
