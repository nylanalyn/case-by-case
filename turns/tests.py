from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from accounts.services import ensure_player_profile
from turns.services import NotEnoughActions, spend_action


class TurnTests(TestCase):
    def test_spend_action_decrements_and_blocks_at_zero(self):
        user = User.objects.create_user(username="halden", password="safe-password-123")
        profile = ensure_player_profile(user)

        spend_action(profile)
        profile.refresh_from_db()
        self.assertEqual(profile.daily_actions_remaining, 19)

        profile.daily_actions_remaining = 0
        profile.save()
        with self.assertRaises(NotEnoughActions):
            spend_action(profile)

    def test_rollover_restores_actions(self):
        user = User.objects.create_user(username="iris", password="safe-password-123")
        profile = ensure_player_profile(user)
        profile.daily_actions_remaining = 3
        profile.save()

        call_command("rollover")
        profile.refresh_from_db()

        self.assertEqual(profile.daily_actions_remaining, 20)
