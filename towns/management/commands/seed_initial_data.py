from django.core.management.base import BaseCommand

from towns.seed import ensure_initial_town


class Command(BaseCommand):
    help = "Create the default town, locations, NPCs, and starter case."

    def handle(self, *args, **options):
        town = ensure_initial_town()
        self.stdout.write(self.style.SUCCESS(f"Seeded {town.name}."))
