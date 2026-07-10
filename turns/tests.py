from django.contrib.auth.models import User
from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from accounts.services import ensure_player_profile
from accounts.services import reset_daily_actions
from towns.models import TownEvent
from turns.services import NotEnoughActions, pass_time, spend_action
from turns.time import action_is_available


class TurnTests(TestCase):
    def test_spend_action_decrements_and_blocks_at_zero(self):
        user = User.objects.create_user(username="halden", password="safe-password-123")
        profile = ensure_player_profile(user)

        spend_action(profile)
        profile.refresh_from_db()
        self.assertEqual(profile.daily_actions_remaining, 23)

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

        self.assertEqual(profile.daily_actions_remaining, settings.DAILY_ACTION_ALLOWANCE)
        self.assertTrue(TownEvent.objects.filter(town=profile.town, body__contains="Rumor:").exists())

    def test_reset_daily_actions_helper(self):
        user = User.objects.create_user(username="june", password="safe-password-123")
        profile = ensure_player_profile(user)
        profile.daily_actions_remaining = 2
        profile.save()

        reset_daily_actions(profile)
        profile.refresh_from_db()

        self.assertEqual(profile.daily_actions_remaining, settings.DAILY_ACTION_ALLOWANCE)

    def test_actions_advance_the_clock_and_time_can_be_passed(self):
        user = User.objects.create_user(username="mara", password="safe-password-123")
        profile = ensure_player_profile(user)

        self.assertEqual(profile.current_time_label, "12:00 AM")
        pass_time(profile, 5)

        profile.refresh_from_db()
        self.assertEqual(profile.daily_actions_remaining, 19)
        self.assertEqual(profile.current_time_label, "5:00 AM")

    def test_time_windows_support_daytime_and_overnight_steps(self):
        daytime_action = {"available_between": {"start": 5, "end": 18}}
        overnight_action = {"available_between": {"start": 20, "end": 5}}

        self.assertTrue(action_is_available(daytime_action, 5))
        self.assertFalse(action_is_available(daytime_action, 18))
        self.assertTrue(action_is_available(overnight_action, 23))
        self.assertTrue(action_is_available(overnight_action, 2))
        self.assertFalse(action_is_available(overnight_action, 12))
