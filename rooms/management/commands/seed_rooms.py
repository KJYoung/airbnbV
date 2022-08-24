import random

from django.core.management import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):
    help = "This command creates many rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "-n", "--number", type=int, default=0, help="# of rooms to create."
        )

    def handle(self, *args, **options):
        # Subclass must implement this method.
        number = options.get("number")
        seeder = Seed.seeder()

        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()

        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.company(),
                # "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: (random.randint(30000, 350000) // 100) * 100,
                "guests": lambda x: random.randint(1, 4),
                "beds": lambda x: random.randint(1, 4),
                "bedrooms": lambda x: random.randint(1, 4),
                "baths": lambda x: random.randint(1, 4),
            },
        )

        created_rooms_ = seeder.execute()
        created_rooms = flatten(list(created_rooms_.values()))

        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        house_rules = room_models.HouseRule.objects.all()

        for pk in created_rooms:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(3, random.randint(6, 24)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 31)}.webp",
                )
            for amen in amenities:
                randNum = random.randint(1, 10)
                if randNum <= 3:  # 30% add
                    room.amenities.add(amen)
            for fcil in facilities:
                randNum = random.randint(1, 10)
                if randNum <= 3:  # 30% add
                    room.facilities.add(fcil)
            for rule in house_rules:
                randNum = random.randint(1, 10)
                if randNum <= 3:  # 30% add
                    room.house_rules.add(rule)
        self.stdout.write(
            self.style.SUCCESS(f"{number} Rooms are generated automatically.")
        )
