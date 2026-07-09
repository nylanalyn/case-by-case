from django.contrib.auth.models import User
from django.test import TestCase

from accounts.services import ensure_player_profile
from cases.models import Case, PlayerCaseProgress, PlayerClue
from cases.services import WrongLocation, advance_case, case_cards_for_location, case_cards_for_player, reset_case_progress
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

    def test_reset_case_progress_clears_case_clues(self):
        user = User.objects.create_user(username="iris", password="safe-password-123")
        profile = ensure_player_profile(user)
        case = Case.objects.get(title="The Missing Ledger", town=profile.town)
        diner = Location.objects.get(town=profile.town, slug="diner")
        progress, _clue = advance_case(profile, case, location=diner)

        reset_case_progress(progress)

        progress.refresh_from_db()
        self.assertEqual(progress.status, PlayerCaseProgress.ACTIVE)
        self.assertEqual(progress.step, 0)
        self.assertEqual(PlayerClue.objects.filter(player=profile, clue__case=case).count(), 0)

    def test_completed_case_does_not_crash_location_cards(self):
        user = User.objects.create_user(username="rumi", password="safe-password-123")
        profile = ensure_player_profile(user)
        case = Case.objects.get(title="The Missing Ledger", town=profile.town)
        locations = [
            Location.objects.get(town=profile.town, slug="diner"),
            Location.objects.get(town=profile.town, slug="library"),
            Location.objects.get(town=profile.town, slug="sheriffs-office"),
            Location.objects.get(town=profile.town, slug="river-walk"),
        ]
        for location in locations:
            advance_case(profile, case, location=location)

        cards = case_cards_for_location(profile, locations[-1])

        self.assertEqual(cards, [])

    def test_case_cards_point_to_next_lead(self):
        user = User.objects.create_user(username="halden", password="safe-password-123")
        profile = ensure_player_profile(user)
        case = Case.objects.get(title="The Missing Ledger", town=profile.town)

        card = case_cards_for_player(profile)[0]
        self.assertEqual(card["status"], PlayerCaseProgress.NOT_STARTED)
        self.assertEqual(card["action"]["location_slug"], "diner")

        diner = Location.objects.get(town=profile.town, slug="diner")
        advance_case(profile, case, location=diner)

        card = case_cards_for_player(profile)[0]
        self.assertEqual(card["status"], PlayerCaseProgress.ACTIVE)
        self.assertEqual(card["action"]["location_slug"], "library")

    def test_case_pages_show_next_lead_link(self):
        user = User.objects.create_user(username="mara", password="safe-password-123")
        ensure_player_profile(user)

        self.client.force_login(user)
        response = self.client.get("/cases/")

        self.assertContains(response, "Next lead")
        self.assertContains(response, "/town/locations/diner/")
