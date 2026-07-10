from django.conf import settings

from towns.seed import assign_town_for_new_player, ensure_town_content

from .models import PlayerProfile
from .stats import STAT_DEFINITIONS


def ensure_player_profile(user):
    profile = PlayerProfile.objects.filter(user=user).first()
    if profile is not None:
        # Keep towns created before new authored content in sync as the game
        # grows. The seeder uses get_or_create, so this is safe on each visit.
        ensure_town_content(profile.town)
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


def apply_stat_changes(profile, changes):
    if not changes:
        return profile
    stats = dict(profile.stats or {})
    for key, delta in changes.items():
        if key not in STAT_DEFINITIONS:
            raise ValueError(f"Unknown player stat: {key}")
        stats[key] = stats.get(key, 0) + delta
    profile.stats = stats
    profile.save(update_fields=["stats"])
    return profile
