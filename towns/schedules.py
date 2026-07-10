import hashlib

from django.utils import timezone

from turns.time import action_is_available

from .models import NPC


TOWNSFOLK_LOCATION_SLUGS = (
    "town-square",
    "diner",
    "library",
    "sheriffs-office",
    "cemetery",
    "river-walk",
    "bus-depot",
    "observatory",
)

LOCATION_LINES = {
    "town-square": ("The clock is slow again. Or everyone else is early.", "They pause by the fountain, as if waiting for it to offer advice."),
    "diner": ("The coffee is stronger than it needs to be.", "They claim this is just a quick stop, with no real conviction."),
    "library": ("It is quieter in here than quiet ought to be.", "They return a book with a receipt tucked carefully inside."),
    "sheriffs-office": ("Nothing to report. That is usually worth reporting.", "They came in to ask a small question and got distracted by the rain."),
    "cemetery": ("The gate is wet again. It has been doing that all week.", "They keep to the path, even though nobody is watching."),
    "river-walk": ("The river looks higher than yesterday.", "They watch something move downstream, then decide it is only a branch."),
    "bus-depot": ("The posted time is more of a suggestion.", "They check the road twice, though there is no bus due yet."),
    "observatory": ("Cloud cover is not the same thing as an empty sky.", "They look down at town as if counting lit windows."),
}

TIME_LINES = {
    "morning": "Morning has not quite caught up with them.",
    "afternoon": "They seem to be stretching one errand into an afternoon.",
    "evening": "They say they should probably be heading home soon.",
    "night": "They lower their voice without saying why.",
}


def _choice_index(*parts, length):
    digest = hashlib.sha256(":".join(map(str, parts)).encode()).digest()
    return int.from_bytes(digest[:8], "big") % length


def _townsfolk_location_slug(npc, hour, today):
    # Four-hour blocks give residents enough time to feel present while the
    # town still changes over a day. The hash keeps a block stable for every
    # player in the same town, then reshuffles it tomorrow.
    block = hour // 4
    index = _choice_index(npc.town_id, npc.slug, today.isoformat(), block, length=len(TOWNSFOLK_LOCATION_SLUGS))
    return TOWNSFOLK_LOCATION_SLUGS[index]


def npc_location_slug(npc, hour, today=None):
    if npc.is_townsfolk:
        return _townsfolk_location_slug(npc, hour, today or timezone.localdate())
    if not npc.daily_schedule:
        return npc.home_location.slug
    for block in npc.daily_schedule:
        if action_is_available({"available_between": block}, hour):
            return block["location_slug"]
    return None


def npc_is_present(npc, location, hour, today=None):
    return npc_location_slug(npc, hour, today=today) == location.slug


def npcs_at_location(town, location, hour, today=None):
    return [
        npc
        for npc in NPC.objects.filter(town=town).select_related("home_location")
        if npc_is_present(npc, location, hour, today=today)
    ]


def npc_dialogue(npc, location, hour, today=None):
    """Return stable, incidental dialogue for a resident at this time and place."""
    if not npc.is_townsfolk:
        return npc.dialogue
    today = today or timezone.localdate()
    location_lines = LOCATION_LINES[location.slug]
    location_line = location_lines[_choice_index(npc.slug, location.slug, today.isoformat(), hour // 4, length=len(location_lines))]
    period = "morning" if hour < 12 else "afternoon" if hour < 17 else "evening" if hour < 22 else "night"
    return f"{location_line} {TIME_LINES[period]}"
