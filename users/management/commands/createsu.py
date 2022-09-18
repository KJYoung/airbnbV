from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = "This command creates a super user."

    def handle(self, *args, **options):
        # Subclass must implement this method.
        admin = User.objects.get_or_none(username="ebadmin")
        if admin is None:
            User.objects.create_superuser("ebadmin", "jykim157@snu.ac.kr", "123456")
            self.stdout.write(self.style.SUCCESS("SuperUsers are generated."))
