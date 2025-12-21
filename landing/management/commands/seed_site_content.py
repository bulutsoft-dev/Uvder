from django.core.management.base import BaseCommand
from landing.models import SiteContent

class Command(BaseCommand):
    help = 'Populates SiteContent with default values based on templates'

    def handle(self, *args, **options):
        # A list of all keys and their defaults. 
        # This list mimics what we put in the templates.
        defaults = [
            # Navbar
            ('nav_brand_title', 'Umut Vagonu', 'Navbar: Marka Başlığı'),
            ('nav_brand_slogan', 'Geleceğe Umut Taşıyoruz', 'Navbar: Marka Sloganı'),
            ('nav_home', 'Ana Sayfa', 'Navbar: Ana Sayfa Linki'),
            ('nav_about', 'Hakkımızda', 'Navbar: Hakkımızda Linki'),
            ('nav_news', 'Haberler', 'Navbar: Haberler Linki'),
            ('nav_gallery', 'Galeri', 'Navbar: Galeri Linki'),
            ('nav_writers', 'Yazar Köşesi', 'Navbar: Yazar Köşesi Linki'),
            ('nav_links', 'Bağlantılar', 'Navbar: Bağlantılar Linki'),
            ('nav_contact', 'İletişim', 'Navbar: İletişim Linki'),
            ('nav_donate_btn', 'Bağış Yap', 'Navbar: Bağış Yap Butonu'),
            
            # Footer
            ('footer_brand_title', 'Umut Vagonu', 'Footer: Marka Başlığı'),
            ('footer_links_title', 'Hızlı Linkler', 'Footer: Hızlı Linkler Başlığı'),
            ('footer_link_about', 'Hakkımızda', 'Footer: Hakkımızda Linki'),
            ('footer_link_news', 'Haberler', 'Footer: Haberler Linki'),
            ('footer_link_gallery', 'Galeri', 'Footer: Galeri Linki'),
            ('footer_link_writers', 'Yazar Köşesi', 'Footer: Yazar Köşesi Linki'),
            ('footer_link_contact', 'İletişim', 'Footer: İletişim Linki'),
            ('footer_contact_title', 'İletişim', 'Footer: İletişim Başlığı'),
            ('footer_donate_title', 'Bağış Bilgileri', 'Footer: Bağış Bilgileri Başlığı'),
            ('footer_donate_btn', 'Bağış Yap', 'Footer: Bağış Butonu'),
            ('footer_copyright', '&copy; 2024 Umut Vagonu Derneği. Tüm Hakları Saklıdır.', 'Footer: Telif Hakkı Metni'),

            # Home
            ('home_hero_title_1', 'Umut Yüklü Vagonlar', 'Home: Hero Başlık 1. Satır'),
            ('home_hero_title_2', 'Yola Çıkıyor', 'Home: Hero Başlık 2. Satır (Vurgulu)'),
            ('home_hero_subtitle', 'İhtiyaç sahiplerine ulaşmak, yüzlerde bir tebessüm oluşturmak için durmaksızın çalışıyoruz. Siz de bu iyilik hareketinin bir parçası olun.', 'Home: Hero Alt Başlık'),
            ('home_hero_btn_news', 'Haberlerimiz', 'Home: Hero Haberler Butonu'),
            ('home_hero_btn_volunteer', 'Gönüllü Ol', 'Home: Hero Gönüllü Butonu'),
            
            ('home_stat_1_label', 'Ulaşılan Hayat', 'Home: İstatistik 1 Etiketi'),
            ('home_stat_2_label', 'Tamamlanan Proje', 'Home: İstatistik 2 Etiketi'),
            ('home_stat_3_label', 'Gönüllü Ordusu', 'Home: İstatistik 3 Etiketi'),
            ('home_stat_4_label', 'Hizmet Verilen İl', 'Home: İstatistik 4 Etiketi'),
            
            ('home_projects_tag', 'Neler Yapıyoruz?', 'Home: Projeler Üst Başlığı'),
            ('home_projects_title', 'Umut Dolu Projelerimiz', 'Home: Projeler Başlığı'),
            
            ('home_project_1_title', 'Eğitim Desteği', 'Home: Proje 1 Başlığı'),
            ('home_project_1_text', 'Geleceğimizin teminatı çocuklarımızın eğitim materyallerine ulaşmasını sağlıyor, köy okullarına destek oluyoruz.', 'Home: Proje 1 Açıklaması'),
            ('home_project_2_title', 'İnsani Yardım', 'Home: Proje 2 Başlığı'),
            ('home_project_2_text', 'Afet bölgeleri ve ihtiyaç sahibi ailelere gıda, giyim ve barınma gibi temel yaşam malzemeleri ulaştırıyoruz.', 'Home: Proje 2 Açıklaması'),
            ('home_project_3_title', 'Sürdürülebilir Projeler', 'Home: Proje 3 Başlığı'),
            ('home_project_3_text', 'Sadece anlık yardım değil, kalıcı çözümler üreterek toplumsal kalkınmaya destek veriyoruz.', 'Home: Proje 3 Açıklaması'),

            ('home_cta_title', 'Bir Hayata Dokun', 'Home: Alt CTA Başlığı'),
            ('home_cta_text', 'Küçük destekleriniz, büyük umutlara dönüşebilir. Bugün bir değişiklik yapın.', 'Home: Alt CTA Metni'),
            ('home_cta_btn_donate', 'Şimdi Bağış Yap', 'Home: Alt CTA Bağış Butonu'),
            ('home_cta_btn_volunteer', 'Gönüllü Ol', 'Home: Alt CTA Gönüllü Butonu'),

            # About
            ('about_mission_title', 'Misyonumuz', 'Hakkımızda: Misyon Başlığı'),
            ('about_mission_text', 'İhtiyaç sahiplerine eğitim, insani yardım ve sürdürülebilir projelerle ulaşarak toplumsal dayanışmayı güçlendirmek.', 'Hakkımızda: Misyon Metni'),
            ('about_vision_title', 'Vizyonumuz', 'Hakkımızda: Vizyon Başlığı'),
            ('about_vision_text', 'Türkiye\'nin her köşesine umut taşıyan, gönüllülük kültürünü yaygınlaştıran öncü bir sivil tolpum kuruluşu olmak.', 'Hakkımızda: Vizyon Metni'),
            ('about_values_title', 'Değerlerimiz', 'Hakkımızda: Değerler Başlığı'),
            ('about_values_text', 'Şeffaflık, hesap verebilirlik, gönüllülük, dayanışma ve sürdürülebilirlik ilkeleriyle hareket ediyoruz.', 'Hakkımızda: Değerler Metni'),
            
            ('about_activities_title', 'Neler Yapıyoruz?', 'Hakkımızda: Faaliyetler Başlığı'),
            ('about_activity_1_title', 'Eğitim Desteği', 'Hakkımızda: Faaliyet 1 Başlığı'),
            ('about_activity_1_text', 'Doğu\'daki köy okullarında eğitim gören çocuklara kırtasiye ve oyuncak yardımı yapıyor, köy okullarının tadilatını gerçekleştiriyor ve kütüphaneler kazandırıyoruz.', 'Hakkımızda: Faaliyet 1 Metni'),
            ('about_activity_2_title', 'İnsani Yardım', 'Hakkımızda: Faaliyet 2 Başlığı'),
            ('about_activity_2_text', 'Afet bölgeleri ve ihtiyaç sahibi ailelere gıda, giyim ve barınma gibi temel yaşam malzemeleri ulaştırıyoruz.', 'Hakkımızda: Faaliyet 2 Metni'),
            ('about_activity_3_title', 'Sürdürülebilir Projeler', 'Hakkımızda: Faaliyet 3 Başlığı'),
            ('about_activity_3_text', 'Kalıcı çözümler üreterek toplumsal kalkınmaya destek veriyor, gönüllülük temalı festivaller düzenliyoruz.', 'Hakkımızda: Faaliyet 3 Metni'),
            ('about_activity_4_title', 'Gönüllü Ağı', 'Hakkımızda: Faaliyet 4 Başlığı'),
            ('about_activity_4_text', 'Öğrenci, mühendis, avukat, öğretmen ve daha birçok meslek grubundan 1000+ gönüllü ile çalışıyoruz.', 'Hakkımızda: Faaliyet 4 Metni'),

            ('about_impact_title', 'Etkimiz', 'Hakkımızda: Etki Bölümü Başlığı'),
            ('about_stat_1_label', 'Ulaşılan Hayat', 'Hakkımızda: İstatistik 1 Etiketi'),
            ('about_stat_2_label', 'Tamamlanan Proje', 'Hakkımızda: İstatistik 2 Etiketi'),
            ('about_stat_3_label', 'Gönüllü', 'Hakkımızda: İstatistik 3 Etiketi'),
            ('about_stat_4_label', 'İl', 'Hakkımızda: İstatistik 4 Etiketi'),
            
            ('about_cta_title', 'Siz de Aramıza Katılın', 'Hakkımızda: Alt CTA Başlığı'),
            ('about_cta_text', 'Gönüllü ordumuza katılarak umut taşıyan bir hareketin parçası olun.', 'Hakkımızda: Alt CTA Metni'),
            ('about_cta_btn', 'Gönüllü Ol', 'Hakkımızda: Alt CTA Butonu'),

            # Contact
            ('contact_title', 'Bize Ulaşın', 'İletişim: Başlık'),
            ('contact_subtitle', 'Sorularınız, önerileriniz veya gönüllülük başvuruları için bizimle iletişime geçebilirsiniz.', 'İletişim: Alt Başlık'),
            ('contact_form_title', 'Mesaj Gönderin', 'İletişim: Form Başlığı'),

            # News/Gallery/Writers Empty States
            ('news_empty_title', 'Henüz haber bulunmuyor', 'Haberler: Boş Liste Başlığı'),
            ('news_empty_text', 'Yakında haberlerimizi buradan takip edebileceksiniz.', 'Haberler: Boş Liste Metni'),
            ('gallery_empty_title', 'Henüz fotoğraf bulunmuyor', 'Galeri: Boş Liste Başlığı'),
            ('gallery_empty_text', 'Yakında etkinlik fotoğraflarımızı buradan görebileceksiniz.', 'Galeri: Boş Liste Metni'),
            ('writers_empty_title', 'Henüz yazar bulunmuyor', 'Yazarlar: Boş Liste Başlığı'),
            ('writers_empty_text', 'Yakında yazarlarımızın köşe yazılarını buradan okuyabileceksiniz.', 'Yazarlar: Boş Liste Metni'),
            ('writers_latest_articles_title', 'Son Yazılar', 'Yazarlar: Son Yazılar Başlığı'),
        ]

        created_count = 0
        updated_count = 0

        for key, text, desc in defaults:
            obj, created = SiteContent.objects.get_or_create(
                key=key,
                defaults={
                    'content_text': text,
                    'description': desc,
                    'is_active': True
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created: {key}"))
            else:
                updated_count += 1
                # Optional: Uncomment if you want to force update content
                # obj.content_text = text
                # obj.save()
                self.stdout.write(f"Skipped (already exists): {key}")

        self.stdout.write(self.style.SUCCESS(f"\nDone! Created: {created_count}, Skipped: {updated_count}"))
