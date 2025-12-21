from django.urls import path
from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.home, name='home'),
    path('hakkimizda/', views.about, name='about'),
    path('organizasyon/', views.organization, name='organization'),
    path('haberler/', views.news_list, name='news_list'),

    path('haberler/<slug:slug>/', views.news_detail, name='news_detail'),
    path('galeri/', views.gallery, name='gallery'),
    path('galeri/<slug:slug>/', views.gallery_category, name='gallery_category'),
    path('yazar-kosesi/', views.writers, name='writers'),
    path('yazar-kosesi/yazi/<slug:slug>/', views.article_detail, name='article_detail'),
    path('yazar-kosesi/<slug:slug>/', views.writer_detail, name='writer_detail'),
    path('baglantilar/', views.links, name='links'),
    path('iletisim/', views.contact, name='contact'),
    
    # Test error pages (Development)
    path('test/400/', views.test_error_400, name='test_error_400'),
    path('test/403/', views.test_error_403, name='test_error_403'),
    path('test/404/', views.test_error_404, name='test_error_404'),
    path('test/500/', views.test_error_500, name='test_error_500'),
]

