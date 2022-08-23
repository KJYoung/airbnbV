from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "This command is just for the practice."

    def add_arguments(self, parser) -> None:
        parser.add_argument("--times", help="How many times for the practice output.")
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        # Subclass must implement this method.
        # return super().handle(*args, **options)
        time = int(options.get("times"))
        for i in range(time):
            self.stdout.write(self.style.SUCCESS("Hey, this is a practice."))
        pass
