from django.contrib.auth.models import User
from django.test import TestCase

from accounts.services import ensure_player_profile
from boards.models import MessageBoardPost
from boards.services import BoardCooldownError, create_post
from towns.models import Location


class BoardTests(TestCase):
    def test_posts_are_scoped_to_town_and_location(self):
        user = User.objects.create_user(username="june", password="safe-password-123")
        profile = ensure_player_profile(user)
        location = Location.objects.get(town=profile.town, slug="diner")

        create_post(profile, location, "The pie case is empty again.")

        self.assertEqual(MessageBoardPost.objects.filter(town=profile.town, location=location).count(), 1)
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

    def test_posting_has_simple_cooldown(self):
        user = User.objects.create_user(username="iris", password="safe-password-123")
        profile = ensure_player_profile(user)
        location = Location.objects.get(town=profile.town, slug="library")

        create_post(profile, location, "Returned the atlas.")

        with self.assertRaises(BoardCooldownError):
            create_post(profile, location, "Forgot the bookmark.")
