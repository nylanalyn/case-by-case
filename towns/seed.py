from .models import Location, NPC, Town


LOCATION_DATA = [
    ("town-square", "Town Square", "The square has a dry fountain, a crooked clock, and benches nobody admits fixing."),
    ("diner", "Diner", "Coffee burns on the warmer. The regulars know exactly which stool is unlucky."),
    ("library", "Library", "The town library smells like dust, raincoats, and copier toner."),
    ("sheriffs-office", "Sheriff's Office", "A quiet office with a dented filing cabinet and too many missing pens."),
    ("cemetery", "Cemetery", "The cemetery gate is wet even on dry days."),
    ("river-walk", "River Walk", "The river moves slowly here, carrying bottle caps, leaves, and rumors."),
    ("bus-depot", "Bus Depot", "The schedule board is handwritten where the plastic letters ran out."),
    ("observatory", "Observatory", "The hilltop observatory is closed more often than it is open."),
]

NPC_DATA = [
    ("Mara Bell", "diner", "Diner worker", "Mara remembers every breakfast order and almost every lie."),
    ("Deputy Halden Price", "sheriffs-office", "Deputy", "Halden writes careful notes in a notebook with a cracked cover."),
    ("Iris Vale", "library", "Librarian", "Iris keeps the old town ledgers in better shape than the town keeps itself."),
    ("Nico Saye", "bus-depot", "Bus depot clerk", "Nico says buses arrive late, early, or wrong."),
    ("June Arlet", "cemetery", "Cemetery caretaker", "June trims the grass and refuses to discuss the north gate."),
]


def ensure_initial_town():
    town, _created = Town.objects.get_or_create(
        slug="deep-archive",
        defaults={"name": "Deep Archive", "capacity": 100},
    )
    locations = {}
    for index, (slug, name, description) in enumerate(LOCATION_DATA):
        location, _created = Location.objects.get_or_create(
            town=town,
            slug=slug,
            defaults={
                "name": name,
                "description": description,
                "atmosphere_tags": "local, odd, persistent",
                "sort_order": index,
            },
        )
        locations[slug] = location
    for name, location_slug, role, dialogue in NPC_DATA:
        NPC.objects.get_or_create(
            town=town,
            name=name,
            defaults={
                "home_location": locations[location_slug],
                "role": role,
                "dialogue": dialogue,
                "personality_tags": "grounded, observant",
            },
        )
    ensure_starter_case(town, locations)
    return town


def ensure_starter_case(town, locations):
    from cases.models import Case, Clue

    case, _created = Case.objects.get_or_create(
        town=town,
        title="The Missing Ledger",
        defaults={
            "summary": "The diner ledger vanished overnight. Mara says it is just bookkeeping, but the last page was copied by hand.",
            "starting_location": locations["diner"],
            "outcome_text": "The ledger was hidden to cover a petty cash scheme. The receipt from River Walk does not fit the story.",
        },
    )
    clues = [
        ("counter-note", "A note under the counter", "Mara found a damp note where the ledger should have been.", 1),
        ("library-card", "A misfiled library card", "The ledger's borrower line matches an old library account that should be closed.", 2),
        ("sheriff-copy", "A copied ledger page", "The sheriff's office has a copy with one line scratched out too neatly.", 3),
        ("river-receipt", "A river-stained receipt", "The receipt proves the ledger was near River Walk after midnight.", 4),
    ]
    for code, title, text, order in clues:
        Clue.objects.get_or_create(
            case=case,
            code=code,
            defaults={"title": title, "text": text, "sort_order": order},
        )
