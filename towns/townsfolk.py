from .models import NPC
from .seed import ensure_town_content


def create_townsfolk(town, count):
    """Compatibility helper for the old management command.

    Townsfolk are now a fixed, art-directed roster.  `count` is retained only
    for command compatibility and can never create anonymous extra residents.
    """
    existing_ids = set(NPC.objects.filter(town=town, is_townsfolk=True).values_list("id", flat=True))
    ensure_town_content(town)
    roster = NPC.objects.filter(town=town, is_townsfolk=True).exclude(id__in=existing_ids).order_by("name")
    return list(roster[:count])
