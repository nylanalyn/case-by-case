from django.contrib.auth.models import User
from django.test import TestCase

from accounts.services import ensure_player_profile
from towns.models import Town
from towns.seed import ensure_initial_town


class AccountTests(TestCase):
    def test_profile_is_created_with_default_town(self):
        user = User.objects.create_user(username="mara", password="safe-password-123")
        profile = ensure_player_profile(user)

        self.assertEqual(profile.town.slug, "brindle-creek")
        self.assertNotEqual(user.password, "safe-password-123")
        self.assertEqual(profile.daily_actions_remaining, 20)

    def test_existing_old_town_slug_is_renamed(self):
        old_town = Town.objects.create(slug="deep-archive", name="Deep Archive")

        town = ensure_initial_town()
        old_town.refresh_from_db()

        self.assertEqual(town.id, old_town.id)
        self.assertEqual(town.slug, "brindle-creek")
        self.assertEqual(town.name, "Brindle Creek")
