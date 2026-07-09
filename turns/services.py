from django.db import transaction


class NotEnoughActions(Exception):
    pass


@transaction.atomic
def spend_action(player, amount=1, reason="act"):
    locked = type(player).objects.select_for_update().get(pk=player.pk)
    if locked.daily_actions_remaining < amount:
        raise NotEnoughActions(f"You do not have enough actions left to {reason}.")
    locked.daily_actions_remaining -= amount
    locked.save(update_fields=["daily_actions_remaining"])
    player.daily_actions_remaining = locked.daily_actions_remaining
    return locked.daily_actions_remaining
