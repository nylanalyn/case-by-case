from accounts.stats import STAT_DEFINITIONS
from towns.seed import LOCATION_DATA, NPC_DATA


LOCATION_SLUGS = {location[0] for location in LOCATION_DATA}
AUTHORED_NPC_SLUGS = {npc[0] for npc in NPC_DATA}


def validate_case_definitions(definitions, location_slugs=LOCATION_SLUGS):
    errors = []
    case_slugs = set()

    for definition in definitions:
        slug = definition.get("slug", "")
        if not slug:
            errors.append("Case is missing a slug.")
        elif slug in case_slugs:
            errors.append(f"{slug}: duplicate case slug.")
        case_slugs.add(slug)

        prefix = slug or "Unnamed case"
        starting_location = definition.get("starting_location_slug")
        if starting_location not in location_slugs:
            errors.append(f"{prefix}: unknown starting location '{starting_location}'.")
        _validate_stat_keys(errors, prefix, "requirements", definition.get("requirements", {}))
        _validate_stat_keys(errors, prefix, "completion_effects", definition.get("completion_effects", {}))

        clues = definition.get("clues", [])
        clue_codes = [clue[0] for clue in clues]
        duplicate_clue_codes = {code for code in clue_codes if clue_codes.count(code) > 1}
        for code in duplicate_clue_codes:
            errors.append(f"{prefix}: duplicate clue code '{code}'.")

        steps = definition.get("steps", [])
        if not steps:
            errors.append(f"{prefix}: needs at least one step.")
            continue
        if steps[0].get("location_slug") != starting_location:
            errors.append(f"{prefix}: first step must be at the starting location.")
        if steps[-1].get("action") != "finish":
            errors.append(f"{prefix}: final step must use action 'finish'.")

        for index, step in enumerate(steps):
            step_prefix = f"{prefix}, step {index + 1}"
            location_slug = step.get("location_slug")
            if location_slug not in location_slugs:
                errors.append(f"{step_prefix}: unknown location '{location_slug}'.")
            if step.get("clue") not in clue_codes:
                errors.append(f"{step_prefix}: unknown clue '{step.get('clue')}'.")
            if step.get("next_step") != index + 1:
                errors.append(f"{step_prefix}: next_step must be {index + 1}.")
            _validate_time_window(errors, step_prefix, step.get("available_between"))
            if step.get("npc_slug") and step["npc_slug"] not in AUTHORED_NPC_SLUGS:
                errors.append(f"{step_prefix}: unknown NPC '{step['npc_slug']}'.")
            choices = step.get("completion_choices", [])
            if choices and index != len(steps) - 1:
                errors.append(f"{step_prefix}: completion choices belong on the final step.")
            _validate_completion_choices(errors, step_prefix, choices)

    return errors


def _validate_stat_keys(errors, prefix, field_name, changes):
    for stat in changes:
        if stat not in STAT_DEFINITIONS:
            errors.append(f"{prefix}: unknown stat '{stat}' in {field_name}.")


def _validate_completion_choices(errors, prefix, choices):
    choice_keys = set()
    for choice in choices:
        key = choice.get("key", "")
        if not key:
            errors.append(f"{prefix}: completion choice is missing a key.")
        elif key in choice_keys:
            errors.append(f"{prefix}: duplicate completion choice key '{key}'.")
        choice_keys.add(key)
        if not choice.get("label"):
            errors.append(f"{prefix}: completion choice '{key}' is missing a label.")
        if not choice.get("outcome_text"):
            errors.append(f"{prefix}: completion choice '{key}' is missing outcome text.")
        _validate_stat_keys(errors, prefix, "completion choice effects", choice.get("completion_effects", {}))


def _validate_time_window(errors, prefix, window):
    if window is None:
        return
    if not isinstance(window, dict) or set(window) != {"start", "end"}:
        errors.append(f"{prefix}: available_between needs start and end hours.")
        return
    if not all(isinstance(window[hour], int) and 0 <= window[hour] <= 23 for hour in ("start", "end")):
        errors.append(f"{prefix}: available_between hours must be between 0 and 23.")
