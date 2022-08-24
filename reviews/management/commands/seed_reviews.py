import random

from django.core.management import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from reviews import models as review_models
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):
    help = "This command creates many reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "-n", "--number", type=int, default=0, help="# of reviews to create."
        )

    def handle(self, *args, **options):
        # Subclass must implement this method.
        number = options.get("number")
        seeder = Seed.seeder()

        """
            review = models.TextField()
            accuracy = models.IntegerField()
            communication = models.IntegerField()
            cleanliness = models.IntegerField()
            location = models.IntegerField()
            check_in = models.IntegerField()
            value = models.IntegerField()

            user = models.ForeignKey(
                "users.User", related_name="reviews", on_delete=models.SET_NULL, null=True
            )
            room = models.ForeignKey(
                "rooms.Room", related_name="reviews", on_delete=models.CASCADE
            )

        """

        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()

        seeder.add_entity(
            review_models.Review,
            number,
            {
                "review": seeder.faker.sentence(),
                "accuracy": lambda x: random.randint(1, 5),
                "communication": lambda x: random.randint(1, 5),
                "cleanliness": lambda x: random.randint(1, 5),
                "location": lambda x: random.randint(1, 5),
                "check_in": lambda x: random.randint(1, 5),
                "value": lambda x: random.randint(1, 5),
                "user": lambda x: random.choice(all_users),
                "room": lambda x: random.choice(all_rooms),
            },
        )

        seeder.execute()

        self.stdout.write(
            self.style.SUCCESS(f"{number} Reviews are generated automatically.")
        )
