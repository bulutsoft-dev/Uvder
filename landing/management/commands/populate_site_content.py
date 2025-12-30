from django.core.management.base import BaseCommand
from landing.models import SiteContent

class Command(BaseCommand):
    help = 'Populates the database with default SiteContent values if they do not exist.'

    def handle(self, *args, **kwargs):
        defaults = [
            # Home
            ('home_news_tag', 'Güncel', 'Ana Sayfa - Haberler etiketi'),
            ('home_news_title', 'Son Haberler', 'Ana Sayfa - Haberler başlığı'),
            ('home_news_all_btn', 'Tüm Haberler', 'Ana Sayfa - Tüm Haberler butonu'),
            ('home_gallery_tag', 'Galeri', 'Ana Sayfa - Galeri etiketi'),
            ('home_gallery_title', 'Fotoğraf Galerisi', 'Ana Sayfa - Galeri başlığı'),
            ('home_gallery_all_btn', 'Tüm Fotoğraflar', 'Ana Sayfa - Tüm Fotoğraflar butonu'),
            ('home_links_tag', 'Hızlı Erişim', 'Ana Sayfa - Linkler etiketi'),
            ('home_links_title', 'Önemli Bağlantılar', 'Ana Sayfa - Linkler başlığı'),

            # Shared / General
            ('news_badge_featured', 'Öne Çıkan', 'Genel - Öne Çıkan etiketi'),
            ('news_read_more', 'Devamını Oku', 'Genel - Haber Devamı butonu'),
            ('article_read_more', 'Devamını Oku', 'Genel - Makale Devamı butonu'),
            ('breadcrumb_home', 'Ana Sayfa', 'Breadcrumb - Ana Sayfa'),

            # About
            ('about_main_title', 'Hakkımızda', 'Hakkımızda - Sayfa Başlığı'),
            ('breadcrumb_about', 'Hakkımızda', 'Breadcrumb - Hakkımızda'),
            ('about_intro_title', 'Umut Vagonu Derneği', 'Hakkımızda - Giriş Başlığı'),
            ('about_intro_p1', 'Manisa merkezli olarak kurulan derneğimiz, Fen Bilgisi Öğretmeni Arzu Şahin Ünal tarafından başlatılan "Umut Vagonu" projesinin dernekleşmesiyle hayata geçmiştir.', 'Hakkımızda - Giriş Paragraf 1'),
            ('about_intro_p2', '7\'den 70\'e herkesin birbiriyle kaynaşmasını sağlayarak, topluma karşı duyarlı, sorumluluk sahibi ve gelişmeye açık bireyler yetiştirmek misyonuyla çalışıyoruz.', 'Hakkımızda - Giriş Paragraf 2'),

            # Organization
            ('org_page_title', 'Organizasyon Yapısı', 'Organizasyon - Sayfa Başlığı'),
            ('breadcrumb_organization', 'Organizasyon', 'Breadcrumb - Organizasyon'),

            # Contact
            ('contact_page_title', 'İletişim', 'İletişim - Sayfa Başlığı'),
            ('breadcrumb_contact', 'İletişim', 'Breadcrumb - İletişim'),
            ('contact_address_title', 'Adres', 'İletişim - Adres Başlığı'),
            ('contact_phone_title', 'Telefon', 'İletişim - Telefon Başlığı'),
            ('contact_email_title', 'E-posta', 'İletişim - E-posta Başlığı'),
            ('contact_donation_title', 'Bağış Bilgileri', 'İletişim - Bağış Başlığı'),
            ('contact_social_title', 'Bizi Takip Edin', 'İletişim - Sosyal Medya Başlığı'),
            ('contact_form_name', 'Ad Soyad', 'İletişim Formu - İsim Label'),
            ('contact_form_name_placeholder', 'Adınız Soyadınız', 'İletişim Formu - İsim Placeholder'),
            ('contact_form_email', 'E-posta', 'İletişim Formu - E-posta Label'),
            ('contact_form_email_placeholder', 'ornek@email.com', 'İletişim Formu - E-posta Placeholder'),
            ('contact_form_phone', 'Telefon', 'İletişim Formu - Telefon Label'),
            ('contact_form_phone_placeholder', '0555 123 45 67', 'İletişim Formu - Telefon Placeholder'),
            ('contact_form_subject', 'Konu', 'İletişim Formu - Konu Label'),
            ('contact_form_subject_placeholder', 'Mesajınızın konusu', 'İletişim Formu - Konu Placeholder'),
            ('contact_form_message', 'Mesajınız', 'İletişim Formu - Mesaj Label'),
            ('contact_form_message_placeholder', 'Mesajınızı buraya yazın...', 'İletişim Formu - Mesaj Placeholder'),
            ('contact_form_btn', 'Gönder', 'İletişim Formu - Gönder Butonu'),
            ('contact_map_url', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3116.0553!2d27.4!3d38.62!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMzjCsDM3JzEyLjAiTiAyN8KwMjQnMDAuMCJF!5e0!3m2!1str!2str!4v1', 'İletişim - Google Maps URL'),

            # News
            ('news_list_title', 'Haberler', 'Haberler - Sayfa Başlığı'),
            ('breadcrumb_news', 'Haberler', 'Breadcrumb - Haberler'),
            ('news_pagination_prev', 'Önceki', 'Haberler - Pagination Önceki'),
            ('news_pagination_page', 'Sayfa', 'Haberler - Pagination Sayfa'),
            ('news_pagination_next', 'Sonraki', 'Haberler - Pagination Sonraki'),
            ('news_detail_title', 'Haber Detay', 'Haber Detay - Sayfa Başlığı'),
            ('news_share_label', 'Paylaş:', 'Haber Detay - Paylaş Label'),
            ('news_related_title', 'İlgili Haberler', 'Haber Detay - İlgili Haberler'),
            ('news_sidebar_cta_title', 'Destek Olun', 'Haber Sidebar - Destek Başlığı'),
            ('news_sidebar_cta_text', 'Umut Vagonu hareketine katılarak bir fark yaratın.', 'Haber Sidebar - Destek Metni'),
            ('news_sidebar_cta_btn', 'Bağış Yap', 'Haber Sidebar - Bağış Butonu'),
            ('news_empty_title', 'Henüz haber bulunmuyor', 'Haberler - Boş Başlık'),
            ('news_empty_text', 'Yakında haberlerimizi buradan takip edebileceksiniz.', 'Haberler - Boş Metin'),

            # Gallery
            ('gallery_page_title', 'Fotoğraf Galerisi', 'Galeri - Sayfa Başlığı'),
            ('breadcrumb_gallery', 'Galeri', 'Breadcrumb - Galeri'),
            ('gallery_filter_all', 'Tümü', 'Galeri - Filtre Tümü'),
            ('gallery_pagination_prev', 'Önceki', 'Galeri - Pagination Önceki'),
            ('gallery_pagination_page', 'Sayfa', 'Galeri - Pagination Sayfa'),
            ('gallery_pagination_next', 'Sonraki', 'Galeri - Pagination Sonraki'),
            ('gallery_empty_title', 'Henüz fotoğraf bulunmuyor', 'Galeri - Boş Başlık'),
            ('gallery_empty_text', 'Yakında etkinlik fotoğraflarımızı buradan görebileceksiniz.', 'Galeri - Boş Metin'),

            # Writers
            ('writers_page_title', 'Yazar Köşesi', 'Yazarlar - Sayfa Başlığı'),
            ('breadcrumb_writers', 'Yazar Köşesi', 'Breadcrumb - Yazarlar'),
            ('writers_article_count_label', 'yazı', 'Yazarlar - Yazı Sayısı Label'),
            ('writers_btn_view_articles', 'Yazıları Gör', 'Yazarlar - Yazıları Gör Butonu'),
            ('writers_latest_articles_title', 'Son Yazılar', 'Yazarlar - Son Yazılar Başlığı'),
            ('writers_empty_title', 'Henüz yazar bulunmuyor', 'Yazarlar - Boş Başlık'),
            ('writers_empty_text', 'Yakında yazarlarımızın köşe yazılarını buradan okuyabileceksiniz.', 'Yazarlar - Boş Metin'),
            ('writer_articles_title', 'Yazıları', 'Yazar Detay - Yazıları Başlığı'),
            ('writer_empty_title', 'Henüz yazı bulunmuyor', 'Yazar Detay - Boş Başlık'),
            ('writer_empty_text', 'Bu yazarın henüz yayınlanmış yazısı bulunmuyor.', 'Yazar Detay - Boş Metin'),

            # Links
            ('links_page_title', 'Bağlantılar', 'Linkler - Sayfa Başlığı'),
            ('breadcrumb_links', 'Bağlantılar', 'Breadcrumb - Linkler'),
            ('links_intro_text', 'Umut Vagonu ile ilgili önemli bağlantılar ve sosyal medya hesaplarımız.', 'Linkler - Giriş Metni'),
            ('links_empty_title', 'Henüz bağlantı bulunmuyor', 'Linkler - Boş Başlık'),
            ('links_empty_text', 'Yakında önemli bağlantılarımızı buradan görebileceksiniz.', 'Linkler - Boş Metin'),
            # Navbar
            ('nav_brand_title', 'Umut Vagonu', 'Navbar - Marka Başlığı'),
            ('nav_brand_slogan', 'Geleceğe Umut Taşıyoruz', 'Navbar - Slogan'),
            ('nav_home', 'Ana Sayfa', 'Navbar - Ana Sayfa Linki'),
            ('nav_about', 'Hakkımızda', 'Navbar - Hakkımızda Linki'),
            ('nav_organization', 'Organizasyon', 'Navbar - Organizasyon Linki'),
            ('nav_news', 'Haberler', 'Navbar - Haberler Linki'),
            ('nav_gallery', 'Galeri', 'Navbar - Galeri Linki'),
            ('nav_writers', 'Yazar Köşesi', 'Navbar - Yazarlar Linki'),
            ('nav_links', 'Bağlantılar', 'Navbar - Linkler Linki'),
            ('nav_contact', 'İletişim', 'Navbar - İletişim Linki'),
            ('nav_donate_btn', 'Bağış Yap', 'Navbar - Bağış Butonu'),

            # Footer
            ('footer_brand_title', 'Umut Vagonu', 'Footer - Marka Başlığı'),
            ('footer_links_title', 'Hızlı Linkler', 'Footer - Hızlı Linkler Başlığı'),
            ('footer_link_about', 'Hakkımızda', 'Footer - Hakkımızda Linki'),
            ('footer_link_organization', 'Organizasyon', 'Footer - Organizasyon Linki'),
            ('footer_link_news', 'Haberler', 'Footer - Haberler Linki'),
            ('footer_link_gallery', 'Galeri', 'Footer - Galeri Linki'),
            ('footer_link_writers', 'Yazar Köşesi', 'Footer - Yazarlar Linki'),
            ('footer_link_contact', 'İletişim', 'Footer - İletişim Linki'),
            ('footer_contact_title', 'İletişim', 'Footer - İletişim Başlığı'),
            ('footer_donate_title', 'Bağış Bilgileri', 'Footer - Bağış Başlığı'),
            ('footer_donate_btn', 'Bağış Yap', 'Footer - Bağış Butonu'),
            ('footer_copyright', '&copy; 2024 Umut Vagonu Derneği. Tüm Hakları Saklıdır.', 'Footer - Telif Hakkı Metni'),

            # 404 Error Page
            ('error_404_page_title', 'Sayfa Bulunamadı', '404 - Sayfa Başlığı'),
            ('error_404_title', 'Sayfa Bulunamadı', '404 - Başlık'),
            ('error_404_message', 'Aradığınız sayfa taşınmış, silinmiş veya hiç var olmamış olabilir. <br>Endişelenmeyin, sizi doğru yola yönlendirelim!', '404 - Mesaj'),
            ('error_404_suggestions_title', 'Ne yapabilirsiniz?', '404 - Öneriler Başlığı'),
            ('error_404_suggestion_1', 'URL adresini kontrol edin', '404 - Öneri 1'),
            ('error_404_suggestion_2', 'Ana sayfadan tekrar başlayın', '404 - Öneri 2'),
            ('error_404_suggestion_3', 'Arama yaparak içeriği bulun', '404 - Öneri 3'),
            ('error_404_btn_home', 'Ana Sayfaya Dön', '404 - Ana Sayfa Butonu'),
            ('error_404_btn_contact', 'Bize Ulaşın', '404 - İletişim Butonu'),
            ('error_404_footer_text', 'Umut Vagonu olarak her zaman yanınızdayız', '404 - Footer Metni'),

            # Article Detail
            ('article_detail_page_title', 'Yazı', 'Yazı Detay - Sayfa Başlığı'),
            ('article_share_label', 'Paylaş:', 'Yazı Detay - Paylaş Label'),
            ('article_btn_all_articles', 'Tüm Yazıları', 'Yazı Detay - Tüm Yazılar Butonu'),
            ('article_related_title', 'Bu Yazarın Diğer Yazıları', 'Yazı Detay - İlgili Yazılar Başlığı'),

            # Error 400
            ('error_400_page_title', 'Geçersiz İstek', '400 - Sayfa Başlığı'),
            ('error_400_title', 'Geçersiz İstek', '400 - Başlık'),
            ('error_400_message', 'Gönderdiğiniz istek sunucumuz tarafından anlaşılamadı. <br>Lütfen formu doğru doldurduğunuzdan emin olun ve tekrar deneyin.', '400 - Mesaj'),
            ('error_400_tip_1', 'Form alanlarını kontrol edin', '400 - İpucu 1'),
            ('error_400_tip_2', 'Sayfayı yenileyip tekrar deneyin', '400 - İpucu 2'),
            ('error_400_tip_3', 'Tarayıcı önbelleğini temizleyin', '400 - İpucu 3'),
            ('error_400_btn_home', 'Ana Sayfaya Dön', '400 - Ana Sayfa Butonu'),
            ('error_400_btn_back', 'Geri Dön', '400 - Geri Dön Butonu'),

            # Error 403
            ('error_403_page_title', 'Erişim Reddedildi', '403 - Sayfa Başlığı'),
            ('error_403_title', 'Erişim Reddedildi', '403 - Başlık'),
            ('error_403_message', 'Bu sayfaya erişim izniniz bulunmuyor. <br>Eğer bu bir hata olduğunu düşünüyorsanız, lütfen bizimle iletişime geçin.', '403 - Mesaj'),
            ('error_403_btn_home', 'Ana Sayfaya Dön', '403 - Ana Sayfa Butonu'),
            ('error_403_btn_help', 'Yardım İste', '403 - Yardım Butonu'),

            # Error 500
            ('error_500_page_title', 'Sunucu Hatası', '500 - Sayfa Başlığı'),
            ('error_500_title', 'Bir Şeyler Ters Gitti', '500 - Başlık'),
            ('error_500_message', 'Sunucumuzda beklenmeyen bir hata oluştu. <br>Teknik ekibimiz bilgilendirildi ve sorunu çözmek için çalışıyor.', '500 - Mesaj'),
            ('error_500_info_title', 'Bakım Devam Ediyor', '500 - Bilgi Başlığı'),
            ('error_500_info_text', 'Lütfen birkaç dakika sonra tekrar deneyin', '500 - Bilgi Metni'),
            ('error_500_btn_home', 'Ana Sayfaya Dön', '500 - Ana Sayfa Butonu'),
            ('error_500_btn_reload', 'Sayfayı Yenile', '500 - Yenile Butonu'),
            ('error_500_contact_text', 'Sorun devam ederse bizimle iletişime geçin:', '500 - İletişim Metni'),
            ('error_500_contact_link', 'İletişim Formu', '500 - İletişim Linki'),

            # Admin Dashboard
            ('admin_welcome_title', 'Umut Vagonu Yönetim Paneli', 'Admin - Karşılama Başlığı'),
            ('admin_welcome_text', 'Hoş geldiniz! Bu panel üzerinden sitenizi kolayca yönetebilirsiniz.', 'Admin - Karşılama Metni'),
            ('admin_quick_start_title', 'Hızlı Başlangıç', 'Admin - Hızlı Başlangıç Başlığı'),
            ('admin_tips_title', 'Kullanım İpuçları', 'Admin - İpuçları Başlığı'),
        ]

        count = 0
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
                self.stdout.write(self.style.SUCCESS(f'Created: {key}'))
                count += 1
            else:
                self.stdout.write(f'Skipped (exists): {key}')

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {count} missing site contents.'))
