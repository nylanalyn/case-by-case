from django.conf import settings

from towns.seed import assign_town_for_new_player

from .models import PlayerProfile


def ensure_player_profile(user):
    profile = PlayerProfile.objects.filter(user=user).first()
    if profile is not None:
        return profile
    profile = PlayerProfile.objects.create(
        user=user,
        town=assign_town_for_new_player(),
        daily_actions_remaining=settings.DAILY_ACTION_ALLOWANCE,
    )
    return profile


def reset_daily_actions(profile):
    profile.daily_actions_remaining = settings.DAILY_ACTION_ALLOWANCE
    profile.save(update_fields=["daily_actions_remaining"])
    return profile
