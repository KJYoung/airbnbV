from django.core.management import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):
    help = "This command creates all the facilities"

    def handle(self, *args, **options):
        # Subclass must implement this method.
        FACILITIES = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]

        for facil in FACILITIES:
            Facility.objects.create(name=facil)

        self.stdout.write(self.style.SUCCESS("Facilities are generated automatically."))
