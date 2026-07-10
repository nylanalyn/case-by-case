from django.core.management.base import BaseCommand, CommandError

from towns.models import Town
from towns.townsfolk import create_townsfolk


class Command(BaseCommand):
    help = "Add persistent generated townsfolk to one town."

    def add_arguments(self, parser):
        parser.add_argument("town_slug")
        parser.add_argument("--count", type=int, default=4)

    def handle(self, *args, **options):
        if options["count"] < 1:
            raise CommandError("Count must be at least 1.")
        town = Town.objects.filter(slug=options["town_slug"]).first()
        if town is None:
            raise CommandError(f"No town found with slug '{options['town_slug']}'.")
        townsfolk = create_townsfolk(town, options["count"])
        self.stdout.write(self.style.SUCCESS(f"Added {len(townsfolk)} townsfolk to {town.name}."))
