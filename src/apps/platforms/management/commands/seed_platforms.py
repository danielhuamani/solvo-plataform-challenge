from django.core.management.base import BaseCommand

from apps.platforms.models import Platform, PlatformSetting


class Command(BaseCommand):
    help = "Seed example platforms and settings for local development."

    def handle(self, *args, **options):
        examples = [
            {
                "name": "Plataforma A",
                "slug": "plataforma-a",
                "settings": {"max_devices": 2, "allow_inactive_login": False},
            },
            {
                "name": "Plataforma B",
                "slug": "plataforma-b",
                "settings": {"max_devices": 5, "allow_inactive_login": True},
            },
        ]

        for item in examples:
            platform, _ = Platform.objects.update_or_create(
                slug=item["slug"],
                defaults={"name": item["name"], "is_active": True},
            )
            PlatformSetting.objects.update_or_create(
                platform=platform,
                defaults=item["settings"],
            )

        self.stdout.write(self.style.SUCCESS("Seeded example platforms."))
