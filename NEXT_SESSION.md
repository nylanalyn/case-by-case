# Next Session Notes

## Current State

Case by Case is a Django + SQLite daily-turn mystery prototype set in Brindle Creek.

The playable loop currently supports:

* local accounts and sessions
* town/pod assignment with Brindle Creek pods
* locations, NPCs, message boards, town history, and newspaper
* daily actions and rollover rumors
* authored cases with location-based leads
* clue journal and case evidence
* player stats with a defined vocabulary
* stat-gated cases
* Django admin/operator controls

The working tree was clean before this note was added. The test suite was green after the last implementation pass.

## Recent Direction

We decided main cases should stay authored for quality and tone.

Longer term, procedural or generated content should probably be used for filler/micro-cases, rumors, flavor, and side mysteries, not as the core source of major cases until the authored case loop is strong.

The case data was centralized in `cases/definitions.py` so adding authored cases is cheaper and less error-prone.

Cases are now keyed by a stable `slug` (unique per town), not by title. Every definition in `cases/definitions.py` must include a `slug`, and all definition lookups go through `case_definition_for_slug`. Titles are display-only and may clash — this is deliberate, since future generated cases will collide on names by luck. Migration `cases/0002_case_slug` backfilled existing rows.

Two security fixes also landed: startup now fails loudly if `DEBUG` is off without a real `SECRET_KEY`, and board posts no longer copy their content into public `TownEvent` bodies (so hiding/deleting a note actually removes it from history/newspaper, and players can't inject fake "Rumor:" lines).

## Design Intent

Keep the town persistent, grounded, odd, and local.

Daily actions should make choices feel intentional. Posting on a board costs 1 action and should stay that way unless playtesting proves it is too punishing.

Stats should stay meaningful. Do not add a new stat for every case. Use the defined vocabulary in `accounts/stats.py`, especially:

* town trust
* zone trust
* weirdness tolerance
* skeptical

Future bad or mixed endings can lower trust or shift stats.

## Recommended Next Steps

1. Add one more authored case using `cases/definitions.py` to prove the new structure is pleasant.
2. Consider adding simple branching endings for one existing case, with different stat effects.
3. Improve locked-case UI if it feels too mechanical.
4. Add a light “case authoring checklist” to docs once the next case confirms the pattern.
5. Only after that, sketch procedural filler case templates.

## Useful Commands

```bash
source .venv/bin/activate
python manage.py test
python manage.py seed_initial_data
python manage.py runserver
```

## Last Known Good Tests

Full suite passed with 34 tests after moving cases to slug-based identity.
