from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="player_profile")
    town = models.ForeignKey("towns.Town", on_delete=models.PROTECT, related_name="players")
    daily_actions_remaining = models.PositiveSmallIntegerField(default=settings.DAILY_ACTION_ALLOWANCE)
    last_rollover_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
