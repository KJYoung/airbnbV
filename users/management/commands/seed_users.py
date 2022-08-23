from django.core.management import BaseCommand
from django_seed import Seed
from users.models import User


class Command(BaseCommand):
    help = "This command creates many users"

    def add_arguments(self, parser):
        parser.add_argument(
            "-n", "--number", type=int, default=0, help="# of users to create."
        )

    def handle(self, *args, **options):
        # Subclass must implement this method.
        number = int(options.get("number"))
        seeder = Seed.seeder()

        seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False})

        seeder.execute()

        self.stdout.write(self.style.SUCCESS("Users are generated automatically."))
