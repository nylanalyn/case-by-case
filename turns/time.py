from django.conf import settings


def current_hour(player):
    return max(0, settings.DAILY_ACTION_ALLOWANCE - player.daily_actions_remaining) % 24


def format_hour(hour):
    suffix = "AM" if hour < 12 else "PM"
    display_hour = hour % 12 or 12
    return f"{display_hour}:00 {suffix}"


def action_is_available(action, hour):
    window = action.get("available_between")
    if window is None:
        return True
    start, end = window["start"], window["end"]
    if start == end:
        return True
    if start < end:
        return start <= hour < end
    return hour >= start or hour < end


def format_availability(action):
    window = action.get("available_between")
    if window is None:
        return ""
    return f"Available {format_hour(window['start'])} to {format_hour(window['end'])}."
