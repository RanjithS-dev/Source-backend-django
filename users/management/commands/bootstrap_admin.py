from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from common.permissions import ROLE_ADMIN


class Command(BaseCommand):
    help = "Create or update the initial admin user for JWT login."

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True)
        parser.add_argument("--password", required=True)
        parser.add_argument("--email", default="")
        parser.add_argument("--full-name", default="Workspace Admin")

    def handle(self, *args, **options):
        username = options["username"].strip()
        password = options["password"]
        if not username or not password:
            raise CommandError("Username and password are required")

        full_name = options["full_name"].strip()
        first_name, _, last_name = full_name.partition(" ")

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": options["email"].strip(),
                "first_name": first_name,
                "last_name": last_name,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )
        if not created:
            user.email = options["email"].strip()
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True

        user.set_password(password)
        user.save()

        profile = user.profile
        profile.role = ROLE_ADMIN
        profile.save()

        self.stdout.write(self.style.SUCCESS(f"Admin user '{username}' is ready."))
