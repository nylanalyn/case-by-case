CASE_DEFINITIONS = [
    {
        "slug": "missing-ledger",
        "title": "The Missing Ledger",
        "summary": "The diner ledger vanished overnight. Mara says it is just bookkeeping, but the last page was copied by hand.",
        "starting_location_slug": "diner",
        "outcome_text": "The ledger was hidden to cover a petty cash scheme. The receipt from River Walk does not fit the story.",
        "requirements": {},
        "completion_effects": {
            "town_trust": 1,
            "diner_trust": 1,
            "sheriff_trust": 1,
        },
        "steps": [
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
                "label": "Decide what to do with the receipt",
                "location_slug": "river-walk",
                "location_name": "River Walk",
                "clue": "river-receipt",
                "next_step": 4,
                "completion_choices": [
                    {
                        "key": "report-the-scheme",
                        "label": "Bring the receipt to Deputy Halden",
                        "outcome_text": "Halden opens a quiet investigation into the petty cash scheme. Mara keeps serving bad coffee, but she stops asking who saw the ledger first.",
                        "completion_effects": {
                            "town_trust": 1,
                            "diner_trust": 1,
                            "sheriff_trust": 1,
                        },
                    },
                    {
                        "key": "leave-it-with-mara",
                        "label": "Leave the receipt with Mara",
                        "outcome_text": "Mara settles the missing cash before anyone files a report. The diner closes the books early for a week, and the river receipt is never mentioned again.",
                        "completion_effects": {
                            "diner_trust": 2,
                            "town_trust": -1,
                            "sheriff_trust": -1,
                        },
                    },
                ],
            },
        ],
        "clues": [
            ("counter-note", "A note under the counter", "Mara found a damp note where the ledger should have been.", 1),
            ("library-card", "A misfiled library card", "The ledger's borrower line matches an old library account that should be closed.", 2),
            ("sheriff-copy", "A copied ledger page", "The sheriff's office has a copy with one line scratched out too neatly.", 3),
            ("river-receipt", "A river-stained receipt", "The receipt proves the ledger was near River Walk after midnight.", 4),
        ],
    },
    {
        "slug": "cemetery-gate",
        "title": "The Cemetery Gate",
        "summary": "The cemetery's north gate keeps turning up wet, unlocked, and facing the wrong way by morning.",
        "starting_location_slug": "cemetery",
        "outcome_text": "June was hiding a late-night shortcut for the bus depot clerk. The hinge was cleaned with river water, for reasons nobody explains.",
        "requirements": {},
        "completion_effects": {
            "weirdness_tolerance": 1,
            "cemetery_trust": 1,
            "bus_depot_trust": 1,
            "skeptical": -1,
        },
        "steps": [
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
        "clues": [
            ("wet-lock", "A wet lock", "The north gate lock is damp inside, though the rest of the iron is dry.", 1),
            ("north-row-map", "The north row map", "An old library map shows a service path from the cemetery toward the depot.", 2),
            ("folded-ticket", "A folded bus ticket", "The ticket is punched after midnight and tucked into the wrong schedule slot.", 3),
            ("cleaned-hinge", "A cleaned hinge", "The hinge was scrubbed with river water and a strip of diner towel.", 4),
        ],
    },
    {
        "slug": "observatory-appointment",
        "title": "The Observatory Appointment",
        "summary": "An appointment appears on the observatory calendar every Thursday, signed by nobody and already crossed out.",
        "starting_location_slug": "observatory",
        "outcome_text": "The appointment was copied from a star chart margin, not scheduled by a person. The telescope was aimed at the river anyway.",
        "requirements": {
            "weirdness_tolerance": 1,
        },
        "lock_text": "Iris will not put the observatory appointment in your hands until you have seen Brindle Creek be stranger than a scheduling error.",
        "completion_effects": {
            "weirdness_tolerance": 1,
            "observatory_trust": 1,
            "river_trust": 1,
            "town_trust": -1,
        },
        "steps": [
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
        "clues": [
            ("missed-appointment", "A missed appointment", "The calendar entry is written in pencil that leaves no dust when rubbed.", 1),
            ("wrong-star-chart", "The wrong star chart", "The library chart marks a Thursday that never happened in the town records.", 2),
            ("river-reflection", "A river reflection", "The observatory dome appears in the river reflection even when the hill is behind you.", 3),
            ("empty-calendar", "An empty calendar square", "The appointment vanishes after the telescope is turned away from the water.", 4),
        ],
    },
]

CASE_DEFINITION_BY_SLUG = {definition["slug"]: definition for definition in CASE_DEFINITIONS}


def case_definition_for_slug(slug):
    return CASE_DEFINITION_BY_SLUG.get(slug, {})
