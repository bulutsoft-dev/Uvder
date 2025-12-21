from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import (
    SiteSettings, News, Writer, Article,
    GalleryCategory, GalleryImage, Link, ContactMessage,
    OrganizationMember
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


def organization(request):
    """Organizasyon yapısı sayfası"""
    members = OrganizationMember.objects.filter(is_active=True)
    
    context = {
        'founders': members.filter(role_type=OrganizationMember.ROLE_FOUNDER),
        'board_members': members.filter(role_type=OrganizationMember.ROLE_BOARD),
        'supervisors': members.filter(role_type=OrganizationMember.ROLE_SUPERVISOR),
        'team_leads': members.filter(role_type=OrganizationMember.ROLE_TEAM_LEAD),
        'volunteers': members.filter(role_type=OrganizationMember.ROLE_VOLUNTEER),
    }
    return render(request, 'pages/organization.html', context)




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
    
    # SEO context
    og_image = None
    if news_item.image:
        og_image = f"{request.scheme}://{request.get_host()}{news_item.image.url}"
    
    context = {
        'news': news_item,
        'related_news': related_news,
        'page_title': news_item.title,
        'page_description': news_item.summary,
        'og_type': 'article',
        'og_image': og_image,
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
    
    # SEO context
    og_image = None
    if article.image:
        og_image = f"{request.scheme}://{request.get_host()}{article.image.url}"
    elif article.writer.photo:
        og_image = f"{request.scheme}://{request.get_host()}{article.writer.photo.url}"
    
    context = {
        'article': article,
        'related_articles': related_articles,
        'page_title': f"{article.title} | {article.writer.name}",
        'page_description': article.content[:200] if article.content else '',
        'og_type': 'article',
        'og_image': og_image,
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


# =============================================================================
# CUSTOM ERROR HANDLERS
# =============================================================================

def error_400(request, exception=None):
    """400 Bad Request"""
    return render(request, '400.html', status=400)


def error_403(request, exception=None):
    """403 Forbidden"""
    return render(request, '403.html', status=403)


def error_404(request, exception=None):
    """404 Not Found"""
    return render(request, '404.html', status=404)


def error_500(request):
    """500 Internal Server Error"""
    return render(request, '500.html', status=500)


# =============================================================================
# TEST ERROR PAGES (Development Only)
# =============================================================================

def test_error_400(request):
    """Test 400 error page"""
    return render(request, '400.html', status=400)


def test_error_403(request):
    """Test 403 error page"""
    return render(request, '403.html', status=403)


def test_error_404(request):
    """Test 404 error page"""
    return render(request, '404.html', status=404)


def test_error_500(request):
    """Test 500 error page"""
    return render(request, '500.html', status=500)

