from django.utils import timezone

from accounts.services import apply_stat_changes
from accounts.stats import stat_label
from turns.services import spend_action
from turns.time import action_is_available, current_hour, format_availability
from towns.models import NPC, TownEvent
from towns.schedules import npc_location_slug

from .definitions import case_definition_for_slug
from .models import Clue, PlayerCaseProgress, PlayerClue


class WrongLocation(Exception):
    pass


class CaseLocked(Exception):
    pass


class InvalidCaseResolution(Exception):
    pass


class CaseUnavailableAtThisTime(Exception):
    pass


def steps_for_case(case):
    return case_definition_for_slug(case.slug).get("steps", [])


def unmet_case_requirements(player, case):
    requirements = case_definition_for_slug(case.slug).get("requirements", {})
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


def action_is_available_for_player(player, action):
    return action_unavailability_reason(player, action) == ""


def action_unavailability_reason(player, action):
    if action is None:
        return ""
    if not action_is_available(action, current_hour(player)):
        return format_availability(action)
    npc_slug = action.get("npc_slug")
    if not npc_slug:
        return ""
    npc = NPC.objects.filter(town=player.town, slug=npc_slug).select_related("home_location").first()
    if npc is None or npc_location_slug(npc, current_hour(player)) != action["location_slug"]:
        return "The person you need is not here right now."
    return ""


def latest_case_clue_for_location(player, case, location):
    clue_codes = [
        step["clue"]
        for step in steps_for_case(case)
        if step["location_slug"] == location.slug
    ]
    if not clue_codes:
        return None
    return (
        PlayerClue.objects.filter(player=player, clue__case=case, clue__code__in=clue_codes)
        .select_related("clue")
        .first()
    )


def completion_choice(action, completion_key):
    choices = action.get("completion_choices", [])
    if not choices:
        return None
    for choice in choices:
        if choice["key"] == completion_key:
            return choice
    raise InvalidCaseResolution("Choose how to close this case.")


def outcome_text_for_progress(progress):
    if not progress.completion_key:
        return progress.case.outcome_text
    for step in steps_for_case(progress.case):
        for choice in step.get("completion_choices", []):
            if choice["key"] == progress.completion_key:
                return choice["outcome_text"]
    return progress.case.outcome_text


def advance_case(player, case, location=None, completion_key=None):
    progress = PlayerCaseProgress.objects.filter(player=player, case=case).first()
    if progress is None:
        progress = get_or_start_case(player, case)
    action = available_case_action(progress)
    if action is None:
        return progress, None
    if location is not None and not action_matches_location(action, location):
        raise WrongLocation(f"That lead belongs at {action['location_name']}.")
    if not action_is_available_for_player(player, action):
        raise CaseUnavailableAtThisTime(action_unavailability_reason(player, action))

    choice = completion_choice(action, completion_key) if action["action"] == "finish" else None
    spend_action(player, reason=action["label"].lower())
    clue = Clue.objects.get(case=case, code=action["clue"])
    PlayerClue.objects.get_or_create(player=player, clue=clue)
    progress.step = action["next_step"]
    if action["action"] == "finish":
        progress.status = PlayerCaseProgress.COMPLETE
        progress.completed_at = timezone.now()
        progress.completion_key = choice["key"] if choice else ""
        effects = choice["completion_effects"] if choice else case_definition_for_slug(case.slug).get("completion_effects", {})
        apply_stat_changes(player, effects)
        TownEvent.objects.create(
            town=player.town,
            title=f"{player.user.username} closed {case.title}",
            body=choice["outcome_text"] if choice else case.outcome_text,
        )
    progress.save()
    return progress, clue


def reset_case_progress(progress):
    PlayerClue.objects.filter(player=progress.player, clue__case=progress.case).delete()
    progress.status = PlayerCaseProgress.ACTIVE
    progress.step = 0
    progress.completed_at = None
    progress.completion_key = ""
    progress.save(update_fields=["status", "step", "completed_at", "completion_key", "updated_at"])
    return progress


def case_card_for_player(player, case, progress=None):
    if progress is None:
        progress = PlayerCaseProgress.objects.filter(player=player, case=case).first()
    definition = case_definition_for_slug(case.slug)
    requirements = unmet_case_requirements(player, case) if progress is None else {}
    if progress is None:
        steps = definition.get("steps", [])
        action = None if requirements else steps[0] if steps else None
        unavailable_reason = action_unavailability_reason(player, action)
        return {
            "case": case,
            "progress": None,
            "status": PlayerCaseProgress.NOT_STARTED,
            "action": action,
            "action_is_available": not unavailable_reason,
            "action_time_label": unavailable_reason,
            "is_available": not requirements,
            "requirements": format_requirements(requirements),
            "lock_text": definition.get("lock_text", ""),
        }
    action = available_case_action(progress)
    unavailable_reason = action_unavailability_reason(player, action)
    return {
        "case": case,
        "progress": progress,
        "status": progress.status,
        "action": action,
        "action_is_available": not unavailable_reason,
        "action_time_label": unavailable_reason,
        "is_available": True,
        "requirements": "",
        "lock_text": "",
        "outcome_text": outcome_text_for_progress(progress) if progress.status == PlayerCaseProgress.COMPLETE else "",
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
        found_clue = None
        if progress is not None and progress.status != PlayerCaseProgress.COMPLETE:
            found_clue = latest_case_clue_for_location(player, case, location)
        if case.starting_location_id == location.id or action_matches_location(action, location) or found_clue:
            cards.append(
                {
                    **case_card_for_player(player, case, progress),
                    "action": action,
                    "found_clue": None if action_matches_location(action, location) else found_clue,
                }
            )
    return cards
