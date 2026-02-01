import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create (or ensure) a superuser from env vars"

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not username or not email or not password:
            self.stdout.write(
                self.style.WARNING(
                    "Missing env vars. Set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD."
                )
            )
            return

        User = get_user_model()
        user = User.objects.filter(username=username).first()

        if user:
            if user.is_superuser:
                self.stdout.write(self.style.WARNING("Superuser already exists"))
                return

            user.is_staff = True
            user.is_superuser = True
            user.email = email
            user.set_password(password)
            user.save(update_fields=["is_staff", "is_superuser", "email", "password"])
            self.stdout.write(self.style.SUCCESS("Existing user promoted to superuser"))
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS("Superuser created"))