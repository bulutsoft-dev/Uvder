from django.urls import path
from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.home, name='home'),
    path('hakkimizda/', views.about, name='about'),
    path('haberler/', views.news_list, name='news_list'),
    path('haberler/<slug:slug>/', views.news_detail, name='news_detail'),
    path('galeri/', views.gallery, name='gallery'),
    path('galeri/<slug:slug>/', views.gallery_category, name='gallery_category'),
    path('yazar-kosesi/', views.writers, name='writers'),
    path('yazar-kosesi/yazi/<slug:slug>/', views.article_detail, name='article_detail'),
    path('yazar-kosesi/<slug:slug>/', views.writer_detail, name='writer_detail'),
    path('baglantilar/', views.links, name='links'),
    path('iletisim/', views.contact, name='contact'),
]
