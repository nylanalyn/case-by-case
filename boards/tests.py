from django.contrib.auth.models import User
from django.test import TestCase

from accounts.services import ensure_player_profile
from boards.models import MessageBoardPost
from boards.services import BoardCooldownError, create_post
from towns.models import Location, TownEvent


class BoardTests(TestCase):
    def test_posts_are_scoped_to_town_and_location(self):
        user = User.objects.create_user(username="june", password="safe-password-123")
        profile = ensure_player_profile(user)
        location = Location.objects.get(town=profile.town, slug="diner")

        create_post(profile, location, "The pie case is empty again.")

        self.assertEqual(MessageBoardPost.objects.filter(town=profile.town, location=location).count(), 1)
        self.assertEqual(TownEvent.objects.filter(town=profile.town, title__contains="left a note").count(), 1)
        profile.refresh_from_db()
        self.assertEqual(profile.daily_actions_remaining, 19)

    def test_player_can_delete_own_post(self):
        user = User.objects.create_user(username="mara", password="safe-password-123")
        profile = ensure_player_profile(user)
        location = Location.objects.get(town=profile.town, slug="diner")
        post = create_post(profile, location, "Back booth is sticky.")

        self.client.force_login(user)
        response = self.client.post(f"/boards/posts/{post.id}/delete/")

        self.assertRedirects(response, f"/town/locations/{location.slug}/")
        self.assertFalse(MessageBoardPost.objects.filter(id=post.id).exists())

    def test_player_cannot_delete_another_players_post(self):
        owner = User.objects.create_user(username="mara", password="safe-password-123")
        other = User.objects.create_user(username="halden", password="safe-password-123")
        owner_profile = ensure_player_profile(owner)
        ensure_player_profile(other)
        location = Location.objects.get(town=owner_profile.town, slug="diner")
        post = create_post(owner_profile, location, "Back booth is sticky.")

        self.client.force_login(other)
        response = self.client.post(f"/boards/posts/{post.id}/delete/")

        self.assertRedirects(response, f"/town/locations/{location.slug}/")
        self.assertTrue(MessageBoardPost.objects.filter(id=post.id).exists())

    def test_staff_can_delete_another_players_post(self):
        owner = User.objects.create_user(username="june", password="safe-password-123")
        staff = User.objects.create_user(username="operator", password="safe-password-123", is_staff=True)
        owner_profile = ensure_player_profile(owner)
        ensure_player_profile(staff)
        location = Location.objects.get(town=owner_profile.town, slug="diner")
        post = create_post(owner_profile, location, "This should come down.")

        self.client.force_login(staff)
        response = self.client.post(f"/boards/posts/{post.id}/delete/")

        self.assertRedirects(response, f"/town/locations/{location.slug}/")
        self.assertFalse(MessageBoardPost.objects.filter(id=post.id).exists())

    def test_posting_has_simple_cooldown(self):
        user = User.objects.create_user(username="iris", password="safe-password-123")
        profile = ensure_player_profile(user)
        location = Location.objects.get(town=profile.town, slug="library")

        create_post(profile, location, "Returned the atlas.")

        with self.assertRaises(BoardCooldownError):
            create_post(profile, location, "Forgot the bookmark.")

    def test_board_posts_do_not_leak_between_town_pods(self):
        first_user = User.objects.create_user(username="rumi", password="safe-password-123")
        first_profile = ensure_player_profile(first_user)
        first_profile.town.capacity = 1
        first_profile.town.save()
        second_user = User.objects.create_user(username="nico", password="safe-password-123")
        second_profile = ensure_player_profile(second_user)

        first_diner = Location.objects.get(town=first_profile.town, slug="diner")
        second_diner = Location.objects.get(town=second_profile.town, slug="diner")
        create_post(first_profile, first_diner, "Only the first town should see this.")

        self.assertEqual(MessageBoardPost.objects.filter(town=first_profile.town, location=first_diner).count(), 1)
        self.assertEqual(MessageBoardPost.objects.filter(town=second_profile.town, location=second_diner).count(), 0)
