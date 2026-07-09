from django.contrib.auth.models import User
from django.test import TestCase

from accounts.services import ensure_player_profile
from towns.models import TownEvent


class TownHistoryTests(TestCase):
    def test_history_page_shows_town_events(self):
        user = User.objects.create_user(username="rumi", password="safe-password-123")
        profile = ensure_player_profile(user)
        TownEvent.objects.create(
            town=profile.town,
            title="The square clock skipped twice",
            body="Nobody agreed on which hour was missing.",
        )

        self.client.force_login(user)
        response = self.client.get("/town/history/")

        self.assertContains(response, "Brindle Creek History")
        self.assertContains(response, "The square clock skipped twice")
        self.assertContains(response, "Nobody agreed on which hour was missing.")
