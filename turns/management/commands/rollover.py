from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import PlayerProfile
from accounts.services import reset_daily_actions
from towns.models import Town, TownEvent
from turns.rumors import rumor_for_date


class Command(BaseCommand):
    help = "Restore daily actions and record a public town rollover event."

    def handle(self, *args, **options):
        today = timezone.localdate()
        updated = 0
        for profile in PlayerProfile.objects.all():
            reset_daily_actions(profile)
            profile.last_rollover_date = today
            profile.save(update_fields=["last_rollover_date"])
            updated += 1
        for town in Town.objects.all():
            TownEvent.objects.create(
                town=town,
                title="A new day settles over town",
                body=f"Actions have refreshed. Rumor: {rumor_for_date(today)}",
            )
        self.stdout.write(self.style.SUCCESS(f"Restored actions for {updated} player(s)."))
