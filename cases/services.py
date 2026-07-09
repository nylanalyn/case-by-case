from django.utils import timezone

from accounts.services import apply_stat_changes
from accounts.stats import stat_label
from turns.services import spend_action
from towns.models import TownEvent

from .models import Clue, PlayerCaseProgress, PlayerClue


CASE_STEPS = {
    "The Missing Ledger": [
        {
            "action": "start",
            "label": "Ask about the missing ledger",
            "location_slug": "diner",
            "location_name": "Diner",
            "clue": "counter-note",
            "next_step": 1,
        },
        {
            "action": "library",
            "label": "Check the library records",
            "location_slug": "library",
            "location_name": "Library",
            "clue": "library-card",
            "next_step": 2,
        },
        {
            "action": "sheriff",
            "label": "Compare notes at the sheriff's office",
            "location_slug": "sheriffs-office",
            "location_name": "Sheriff's Office",
            "clue": "sheriff-copy",
            "next_step": 3,
        },
        {
            "action": "finish",
            "label": "Close the ledger case",
            "location_slug": "river-walk",
            "location_name": "River Walk",
            "clue": "river-receipt",
            "next_step": 4,
        },
    ],
    "The Cemetery Gate": [
        {
            "action": "start",
            "label": "Ask June about the wet gate",
            "location_slug": "cemetery",
            "location_name": "Cemetery",
            "clue": "wet-lock",
            "next_step": 1,
        },
        {
            "action": "library",
            "label": "Compare the old burial map",
            "location_slug": "library",
            "location_name": "Library",
            "clue": "north-row-map",
            "next_step": 2,
        },
        {
            "action": "depot",
            "label": "Check the late bus schedule",
            "location_slug": "bus-depot",
            "location_name": "Bus Depot",
            "clue": "folded-ticket",
            "next_step": 3,
        },
        {
            "action": "finish",
            "label": "Close the cemetery gate case",
            "location_slug": "cemetery",
            "location_name": "Cemetery",
            "clue": "cleaned-hinge",
            "next_step": 4,
        },
    ],
    "The Observatory Appointment": [
        {
            "action": "start",
            "label": "Ask about the missed appointment",
            "location_slug": "observatory",
            "location_name": "Observatory",
            "clue": "missed-appointment",
            "next_step": 1,
        },
        {
            "action": "library",
            "label": "Read the old star chart",
            "location_slug": "library",
            "location_name": "Library",
            "clue": "wrong-star-chart",
            "next_step": 2,
        },
        {
            "action": "river",
            "label": "Follow the reflected light",
            "location_slug": "river-walk",
            "location_name": "River Walk",
            "clue": "river-reflection",
            "next_step": 3,
        },
        {
            "action": "finish",
            "label": "Close the observatory appointment",
            "location_slug": "observatory",
            "location_name": "Observatory",
            "clue": "empty-calendar",
            "next_step": 4,
        },
    ],
}

CASE_STAT_REQUIREMENTS = {
    "The Observatory Appointment": {
        "weirdness_tolerance": 1,
    },
}

CASE_COMPLETION_EFFECTS = {
    "The Missing Ledger": {
        "town_trust": 1,
        "diner_trust": 1,
        "sheriff_trust": 1,
    },
    "The Cemetery Gate": {
        "weirdness_tolerance": 1,
        "cemetery_trust": 1,
        "bus_depot_trust": 1,
        "skeptical": -1,
    },
    "The Observatory Appointment": {
        "weirdness_tolerance": 1,
        "observatory_trust": 1,
        "river_trust": 1,
        "town_trust": -1,
    },
}


class WrongLocation(Exception):
    pass


class CaseLocked(Exception):
    pass


def steps_for_case(case):
    return CASE_STEPS.get(case.title, [])


def unmet_case_requirements(player, case):
    requirements = CASE_STAT_REQUIREMENTS.get(case.title, {})
    stats = player.stats or {}
    unmet = {}
    for stat, minimum in requirements.items():
        if stats.get(stat, 0) < minimum:
            unmet[stat] = minimum
    return unmet


def format_requirements(requirements):
    return ", ".join(f"{stat_label(stat)} {minimum}+" for stat, minimum in requirements.items())


def get_or_start_case(player, case):
    if unmet_case_requirements(player, case):
        raise CaseLocked(f"This case is not open to you yet. Needed: {format_requirements(unmet_case_requirements(player, case))}.")
    progress, _created = PlayerCaseProgress.objects.get_or_create(
        player=player,
        case=case,
        defaults={"status": PlayerCaseProgress.ACTIVE, "step": 0},
    )
    return progress


def available_case_action(progress):
    steps = steps_for_case(progress.case)
    if progress.status == PlayerCaseProgress.COMPLETE:
        return None
    if progress.step >= len(steps):
        return None
    return steps[progress.step]


def action_matches_location(action, location):
    return action is not None and location is not None and action["location_slug"] == location.slug


def advance_case(player, case, location=None):
    progress = PlayerCaseProgress.objects.filter(player=player, case=case).first()
    if progress is None:
        progress = get_or_start_case(player, case)
    action = available_case_action(progress)
    if action is None:
        return progress, None
    if location is not None and not action_matches_location(action, location):
        raise WrongLocation(f"That lead belongs at {action['location_name']}.")

    spend_action(player, reason=action["label"].lower())
    clue = Clue.objects.get(case=case, code=action["clue"])
    PlayerClue.objects.get_or_create(player=player, clue=clue)
    progress.step = action["next_step"]
    if action["action"] == "finish":
        progress.status = PlayerCaseProgress.COMPLETE
        progress.completed_at = timezone.now()
        apply_stat_changes(player, CASE_COMPLETION_EFFECTS.get(case.title, {}))
        TownEvent.objects.create(
            town=player.town,
            title=f"{player.user.username} closed {case.title}",
            body=case.outcome_text,
        )
    progress.save()
    return progress, clue


def reset_case_progress(progress):
    PlayerClue.objects.filter(player=progress.player, clue__case=progress.case).delete()
    progress.status = PlayerCaseProgress.ACTIVE
    progress.step = 0
    progress.completed_at = None
    progress.save(update_fields=["status", "step", "completed_at", "updated_at"])
    return progress


def case_card_for_player(player, case, progress=None):
    if progress is None:
        progress = PlayerCaseProgress.objects.filter(player=player, case=case).first()
    requirements = unmet_case_requirements(player, case) if progress is None else {}
    if progress is None:
        steps = steps_for_case(case)
        return {
            "case": case,
            "progress": None,
            "status": PlayerCaseProgress.NOT_STARTED,
            "action": None if requirements else steps[0] if steps else None,
            "is_available": not requirements,
            "requirements": format_requirements(requirements),
        }
    return {
        "case": case,
        "progress": progress,
        "status": progress.status,
        "action": available_case_action(progress),
        "is_available": True,
        "requirements": "",
    }


def case_cards_for_player(player):
    cases = list(player.town.cases.filter(is_active=True).select_related("starting_location"))
    progress_by_case = {
        progress.case_id: progress
        for progress in PlayerCaseProgress.objects.filter(player=player, case__in=cases)
    }
    return [case_card_for_player(player, case, progress_by_case.get(case.id)) for case in cases]


def case_journal_for_player(player):
    cards = case_cards_for_player(player)
    clues = PlayerClue.objects.filter(player=player).select_related("clue", "clue__case")
    clues_by_case_id = {}
    for player_clue in clues:
        clues_by_case_id.setdefault(player_clue.clue.case_id, []).append(player_clue)
    records = []
    for card in cards:
        records.append({**card, "clues": clues_by_case_id.get(card["case"].id, [])})
    return records


def case_cards_for_location(player, location):
    cases = list(player.town.cases.filter(is_active=True).select_related("starting_location"))
    progress_by_case = {
        progress.case_id: progress
        for progress in PlayerCaseProgress.objects.filter(player=player, case__in=cases)
    }
    cards = []
    for case in cases:
        progress = progress_by_case.get(case.id)
        if progress is None and case.starting_location_id != location.id:
            continue
        if progress is None:
            card = case_card_for_player(player, case)
            action = card["action"]
        else:
            action = available_case_action(progress)
        if case.starting_location_id == location.id or action_matches_location(action, location):
            cards.append({**case_card_for_player(player, case, progress), "action": action})
    return cards
