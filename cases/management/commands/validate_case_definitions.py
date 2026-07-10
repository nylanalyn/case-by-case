from django.core.management.base import BaseCommand, CommandError

from cases.definitions import CASE_DEFINITIONS
from cases.validation import validate_case_definitions


class Command(BaseCommand):
    help = "Validate authored cases in cases/definitions.py."

    def handle(self, *args, **options):
        errors = validate_case_definitions(CASE_DEFINITIONS)
        if errors:
            raise CommandError("\n".join(errors))
        self.stdout.write(self.style.SUCCESS(f"Validated {len(CASE_DEFINITIONS)} case definitions."))
