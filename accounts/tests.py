from django.contrib.auth.models import User
from django.test import TestCase

from accounts.services import ensure_player_profile


class AccountTests(TestCase):
    def test_profile_is_created_with_default_town(self):
        user = User.objects.create_user(username="mara", password="safe-password-123")
        profile = ensure_player_profile(user)

        self.assertEqual(profile.town.slug, "deep-archive")
        self.assertNotEqual(user.password, "safe-password-123")
        self.assertEqual(profile.daily_actions_remaining, 20)
