from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import PlayerProfile
from towns.models import Town, TownEvent


class Command(BaseCommand):
    help = "Restore daily actions and record a public town rollover event."

    def handle(self, *args, **options):
        today = timezone.localdate()
        updated = PlayerProfile.objects.update(
            daily_actions_remaining=settings.DAILY_ACTION_ALLOWANCE,
            last_rollover_date=today,
        )
        for town in Town.objects.all():
            TownEvent.objects.create(
                town=town,
                title="A new day settles over town",
                body="Actions have refreshed. The coffee is still bad.",
            )
        self.stdout.write(self.style.SUCCESS(f"Restored actions for {updated} player(s)."))
