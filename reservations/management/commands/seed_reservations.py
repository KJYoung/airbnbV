import random
from datetime import datetime, timedelta

from django.core.management import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from reservations import models as reservation_models
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):
    help = "This command creates many reservations"

    def add_arguments(self, parser):
        parser.add_argument(
            "-n", "--number", type=int, default=0, help="# of reservations to create."
        )

    def handle(self, *args, **options):
        # Subclass must implement this method.
        number = options.get("number")
        seeder = Seed.seeder()

        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()

        """
        status = models.CharField(
        choices=STATUS_CHOICES, max_length=16, default=STATUS_PENDING
        )
        check_in = models.DateField()
        check_out = models.DateField()

        guest = models.ForeignKey(
            "users.User", related_name="reservations", on_delete=models.CASCADE
        )
        room = models.ForeignKey(
            "rooms.Room", related_name="reservations", on_delete=models.CASCADE
        )
        """
        seeder.add_entity(
            reservation_models.Reservation,
            number,
            {
                "status": lambda x: random.choice(["pending", "canceled", "confirmed"]),
                "guest": lambda x: random.choice(all_users),
                "room": lambda x: random.choice(all_rooms),
                "check_in": lambda x: datetime.now()
                + timedelta(days=random.randint(0, 3)),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(5, 12)),
            },
        )

        seeder.execute()

        self.stdout.write(
            self.style.SUCCESS(f"{number} Reservations are generated automatically.")
        )
