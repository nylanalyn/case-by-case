from django.contrib.auth.models import User
from django.test import TestCase

from accounts.services import ensure_player_profile
from towns.models import Location, Town
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

    def test_new_players_are_assigned_to_new_pod_when_town_is_full(self):
        first_user = User.objects.create_user(username="mara", password="safe-password-123")
        first_profile = ensure_player_profile(first_user)
        first_profile.town.capacity = 1
        first_profile.town.save()

        second_user = User.objects.create_user(username="halden", password="safe-password-123")
        second_profile = ensure_player_profile(second_user)

        self.assertNotEqual(first_profile.town_id, second_profile.town_id)
        self.assertEqual(second_profile.town.slug, "brindle-creek-2")
        self.assertEqual(Location.objects.filter(town=second_profile.town).count(), 8)
