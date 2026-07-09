from django.contrib.auth.models import User
from django.test import TestCase

from accounts.services import ensure_player_profile
from cases.models import Case, PlayerCaseProgress, PlayerClue
from cases.services import WrongLocation, advance_case
from towns.models import Location, TownEvent


class CaseTests(TestCase):
    def test_starter_case_can_be_completed(self):
        user = User.objects.create_user(username="nico", password="safe-password-123")
        profile = ensure_player_profile(user)
        case = Case.objects.get(title="The Missing Ledger", town=profile.town)
        locations = [
            Location.objects.get(town=profile.town, slug="diner"),
            Location.objects.get(town=profile.town, slug="library"),
            Location.objects.get(town=profile.town, slug="sheriffs-office"),
            Location.objects.get(town=profile.town, slug="river-walk"),
        ]

        for location in locations:
            progress, _clue = advance_case(profile, case, location=location)

        self.assertEqual(progress.status, PlayerCaseProgress.COMPLETE)
        self.assertEqual(PlayerClue.objects.filter(player=profile, clue__case=case).count(), 4)
        self.assertEqual(TownEvent.objects.filter(town=profile.town, title__contains=case.title).count(), 1)
        profile.refresh_from_db()
        self.assertEqual(profile.daily_actions_remaining, 16)

    def test_case_step_requires_correct_location(self):
        user = User.objects.create_user(username="mara", password="safe-password-123")
        profile = ensure_player_profile(user)
        case = Case.objects.get(title="The Missing Ledger", town=profile.town)
        library = Location.objects.get(town=profile.town, slug="library")

        with self.assertRaises(WrongLocation):
            advance_case(profile, case, location=library)
