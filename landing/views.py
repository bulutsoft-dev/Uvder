from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import (
    SiteSettings, News, Writer, Article,
    GalleryCategory, GalleryImage, Link, ContactMessage
)


def home(request):
    """Ana sayfa"""
    context = {
        'featured_news': News.objects.filter(is_published=True, is_featured=True)[:3],
        'latest_news': News.objects.filter(is_published=True)[:6],
        'featured_images': GalleryImage.objects.filter(is_featured=True)[:6],
        'featured_links': Link.objects.filter(is_active=True, is_featured=True)[:4],
    }
    return render(request, 'pages/home.html', context)


def about(request):
    """Hakkımızda sayfası"""
    return render(request, 'pages/about.html')


def news_list(request):
    """Haberler listesi"""
    news_qs = News.objects.filter(is_published=True)
    paginator = Paginator(news_qs, 9)  # 9 haber per sayfa
    
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    
    context = {
        'news': news,
        'featured_news': News.objects.filter(is_published=True, is_featured=True).first(),
    }
    return render(request, 'pages/news_list.html', context)


def news_detail(request, slug):
    """Haber detay sayfası"""
    news_item = get_object_or_404(News, slug=slug, is_published=True)
    related_news = News.objects.filter(is_published=True).exclude(pk=news_item.pk)[:3]
    
    context = {
        'news': news_item,
        'related_news': related_news,
    }
    return render(request, 'pages/news_detail.html', context)


def gallery(request):
    """Fotoğraf galerisi"""
    categories = GalleryCategory.objects.all()
    
    # Tüm görselleri veya kategoriye göre filtrele
    category_slug = request.GET.get('category')
    if category_slug:
        selected_category = get_object_or_404(GalleryCategory, slug=category_slug)
        images = GalleryImage.objects.filter(category=selected_category)
    else:
        selected_category = None
        images = GalleryImage.objects.all()
    
    paginator = Paginator(images, 12)
    page_number = request.GET.get('page')
    images = paginator.get_page(page_number)
    
    context = {
        'categories': categories,
        'images': images,
        'selected_category': selected_category,
    }
    return render(request, 'pages/gallery.html', context)


def gallery_category(request, slug):
    """Kategori bazlı galeri görünümü"""
    category = get_object_or_404(GalleryCategory, slug=slug)
    images = GalleryImage.objects.filter(category=category)
    
    paginator = Paginator(images, 12)
    page_number = request.GET.get('page')
    images = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'images': images,
        'categories': GalleryCategory.objects.all(),
    }
    return render(request, 'pages/gallery.html', context)


def writers(request):
    """Yazar köşesi"""
    writers_list = Writer.objects.filter(is_active=True)
    latest_articles = Article.objects.filter(is_published=True)[:5]
    
    context = {
        'writers': writers_list,
        'latest_articles': latest_articles,
    }
    return render(request, 'pages/writers.html', context)


def writer_detail(request, slug):
    """Yazar profili ve yazıları"""
    writer = get_object_or_404(Writer, slug=slug, is_active=True)
    articles = Article.objects.filter(writer=writer, is_published=True)
    
    paginator = Paginator(articles, 6)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    
    context = {
        'writer': writer,
        'articles': articles,
    }
    return render(request, 'pages/writer_detail.html', context)


def article_detail(request, slug):
    """Köşe yazısı detay"""
    article = get_object_or_404(Article, slug=slug, is_published=True)
    related_articles = Article.objects.filter(
        writer=article.writer, is_published=True
    ).exclude(pk=article.pk)[:3]
    
    context = {
        'article': article,
        'related_articles': related_articles,
    }
    return render(request, 'pages/article_detail.html', context)


def links(request):
    """Bağlantı linkleri"""
    links_list = Link.objects.filter(is_active=True)
    
    context = {
        'links': links_list,
    }
    return render(request, 'pages/links.html', context)


def contact(request):
    """İletişim sayfası"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()
        
        if name and email and subject and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message_text
            )
            messages.success(request, 'Mesajınız başarıyla gönderildi. En kısa sürede size dönüş yapacağız.')
            return redirect('landing:contact')
        else:
            messages.error(request, 'Lütfen tüm zorunlu alanları doldurun.')
    
    return render(request, 'pages/contact.html')
