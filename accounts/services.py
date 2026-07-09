from django.conf import settings

from towns.seed import ensure_initial_town

from .models import PlayerProfile


def ensure_player_profile(user):
    town = ensure_initial_town()
    profile, _created = PlayerProfile.objects.get_or_create(
        user=user,
        defaults={
            "town": town,
            "daily_actions_remaining": settings.DAILY_ACTION_ALLOWANCE,
        },
    )
    return profile


def reset_daily_actions(profile):
    profile.daily_actions_remaining = settings.DAILY_ACTION_ALLOWANCE
    profile.save(update_fields=["daily_actions_remaining"])
    return profile
