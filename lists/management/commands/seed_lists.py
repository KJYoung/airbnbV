import random

from django.core.management import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from users import models as user_models
from rooms import models as room_models
from lists import models as list_models


class Command(BaseCommand):
    help = "This command creates many lists"

    def add_arguments(self, parser):
        parser.add_argument(
            "-n", "--number", type=int, default=0, help="# of lists to create."
        )

    def handle(self, *args, **options):
        # Subclass must implement this method.
        number = options.get("number")
        seeder = Seed.seeder()

        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()

        """
        name = models.CharField(max_length=80)
        user = models.ForeignKey(
            "users.User", related_name="lists", on_delete=models.CASCADE
        )
        rooms = models.ManyToManyField("rooms.Room", related_name="lists", blank=True)
        """
        seeder.add_entity(
            list_models.List,
            number,
            {
                # "name": seeder.faker.text(max_nb_chars=40),
                "user": lambda x: random.choice(all_users),
            },
        )

        created_lists_ = seeder.execute()
        created_list = flatten(list(created_lists_.values()))

        for pk in created_list:
            list_obj = list_models.List.objects.get(pk=pk)
            rooms_shuffled = all_rooms.order_by("?")
            # rooms_shuffled = random.shuffle(all_rooms)
            to_add = rooms_shuffled[random.randint(0, 5) : random.randint(8, 16)]
            list_obj.rooms.add(*to_add)

        self.stdout.write(
            self.style.SUCCESS(f"{number} Lists are generated automatically.")
        )
