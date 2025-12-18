"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# Dil değiştirme URL'i (prefix olmadan)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

# Dil prefix'li URL'ler (/tr/, /en/)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),
    prefix_default_language=True,
)

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
