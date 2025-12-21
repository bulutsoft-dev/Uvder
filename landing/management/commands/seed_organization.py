from django.core.management.base import BaseCommand
from landing.models import OrganizationMember

class Command(BaseCommand):
    help = 'Populates OrganizationMember with sample data'

    def handle(self, *args, **options):
        members = [
            # Founders
            {
                'name': 'Mehmet Yılmaz',
                'title': 'Kurucu Başkan',
                'bio': 'Umut Vagonu Derneği\'nin kurucu başkanı. 10 yılı aşkın sivil toplum deneyimine sahip.',
                'role_type': OrganizationMember.ROLE_FOUNDER,
                'order': 1,
            },
            {
                'name': 'Ayşe Demir',
                'title': 'Kurucu Üye',
                'bio': 'Derneğin kuruluşundan bu yana sosyal sorumluluk projelerinde aktif rol almaktadır.',
                'role_type': OrganizationMember.ROLE_FOUNDER,
                'order': 2,
            },
            
            # Board Members
            {
                'name': 'Ali Kaya',
                'title': 'Yönetim Kurulu Başkanı',
                'bio': 'Proje yönetimi ve stratejik planlama alanında uzman.',
                'role_type': OrganizationMember.ROLE_BOARD,
                'order': 1,
            },
            {
                'name': 'Fatma Özkan',
                'title': 'Genel Sekreter',
                'bio': 'Dernek faaliyetlerinin koordinasyonundan sorumlu.',
                'role_type': OrganizationMember.ROLE_BOARD,
                'order': 2,
            },
            {
                'name': 'Mustafa Çelik',
                'title': 'Sayman',
                'bio': 'Mali işler ve bütçe yönetiminden sorumlu.',
                'role_type': OrganizationMember.ROLE_BOARD,
                'order': 3,
            },
            
            # Supervisory Board
            {
                'name': 'Zeynep Arslan',
                'title': 'Denetim Kurulu Başkanı',
                'role_type': OrganizationMember.ROLE_SUPERVISOR,
                'order': 1,
            },
            {
                'name': 'Hakan Yıldız',
                'title': 'Denetim Kurulu Üyesi',
                'role_type': OrganizationMember.ROLE_SUPERVISOR,
                'order': 2,
            },
            
            # Team Leads
            {
                'name': 'Elif Şahin',
                'title': 'Eğitim Projeleri Lideri',
                'role_type': OrganizationMember.ROLE_TEAM_LEAD,
                'order': 1,
            },
            {
                'name': 'Burak Aydın',
                'title': 'Lojistik Koordinatörü',
                'role_type': OrganizationMember.ROLE_TEAM_LEAD,
                'order': 2,
            },
            {
                'name': 'Selin Korkmaz',
                'title': 'İletişim ve Sosyal Medya',
                'role_type': OrganizationMember.ROLE_TEAM_LEAD,
                'order': 3,
            },
        ]

        created_count = 0
        for member_data in members:
            obj, created = OrganizationMember.objects.get_or_create(
                name=member_data['name'],
                defaults=member_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created: {member_data['name']}"))
            else:
                self.stdout.write(f"Skipped (already exists): {member_data['name']}")

        self.stdout.write(self.style.SUCCESS(f"\nDone! Created {created_count} organization members."))
