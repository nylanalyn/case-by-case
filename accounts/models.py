from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="player_profile")
    town = models.ForeignKey("towns.Town", on_delete=models.PROTECT, related_name="players")
    daily_actions_remaining = models.PositiveSmallIntegerField(default=settings.DAILY_ACTION_ALLOWANCE)
    last_rollover_date = models.DateField(null=True, blank=True)
    stats = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    @property
    def current_hour(self):
        from turns.time import current_hour

        return current_hour(self)

    @property
    def current_time_label(self):
        from turns.time import format_hour

        return format_hour(self.current_hour)
