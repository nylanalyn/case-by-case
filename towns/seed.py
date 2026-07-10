from django.db import models
from django.utils.text import slugify

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
    ("mara-bell", "Mara Bell", "diner", "Diner worker", "Mara remembers every breakfast order and almost every lie."),
    ("halden-price", "Deputy Halden Price", "sheriffs-office", "Deputy", "Halden writes careful notes in a notebook with a cracked cover."),
    ("iris-vale", "Iris Vale", "library", "Librarian", "Iris keeps the old town ledgers in better shape than the town keeps itself."),
    ("nico-saye", "Nico Saye", "bus-depot", "Bus depot clerk", "Nico says buses arrive late, early, or wrong."),
    ("june-arlet", "June Arlet", "cemetery", "Cemetery caretaker", "June trims the grass and refuses to discuss the north gate."),
]

# These are ordinary, recognizable Brindle Creek residents.  They are not case
# contacts yet; their locations and incidental dialogue are supplied by
# towns.schedules so they can make the town feel lived in without authoring a
# schedule for every person.
TOWNSFOLK_DATA = [
    ("beverly-kett", "Beverly Kett", "town-square", "Retired postal clerk", "Keeps an eye on the weather and everyone else's business."),
    ("colin-voss", "Colin Voss", "river-walk", "Dock repairer", "Usually smells faintly of river water and machine oil."),
    ("darlene-mott", "Darlene Mott", "diner", "School bus driver", "Knows which streets flood before the town does."),
    ("elliot-ward", "Elliot Ward", "library", "Night-shift stocker", "Sleeps at unusual hours and notices empty shelves."),
    ("frances-pell", "Frances Pell", "cemetery", "Florist", "Carries an umbrella only when she remembers."),
    ("gabriel-shaw", "Gabriel Shaw", "bus-depot", "Appliance repairer", "Always seems to be between one errand and another."),
    ("helen-rook", "Helen Rook", "observatory", "Former science teacher", "Still points out constellations through the clouds."),
    ("jasper-quill", "Jasper Quill", "town-square", "Handyman", "Has paint on his cuffs and a theory about every loose board."),
    ("lila-barnes", "Lila Barnes", "library", "Bakery assistant", "Gets up before the town and is never quite over it."),
    ("martin-crowe", "Martin Crowe", "sheriffs-office", "Volunteer firekeeper", "Speaks softly, except when discussing faulty wiring."),
]


def ensure_initial_town():
    town = Town.objects.filter(slug="brindle-creek").first()
    old_town = Town.objects.filter(slug="deep-archive").first()
    if town is None and old_town is not None:
        old_town.slug = "brindle-creek"
        old_town.name = "Brindle Creek"
        old_town.save(update_fields=["slug", "name"])
        town = old_town
    elif town is not None and town.name != "Brindle Creek":
        town.name = "Brindle Creek"
        town.save(update_fields=["name"])
    if town is None:
        town = Town.objects.create(slug="brindle-creek", name="Brindle Creek", capacity=100)
    ensure_town_content(town)
    return town


def assign_town_for_new_player():
    ensure_initial_town()
    town = (
        Town.objects.annotate(player_count=models.Count("players"))
        .filter(player_count__lt=models.F("capacity"))
        .order_by("created_at", "id")
        .first()
    )
    if town is None:
        town = create_town_pod()
    ensure_town_content(town)
    return town


def create_town_pod():
    next_number = Town.objects.count() + 1
    while True:
        name = f"Brindle Creek {next_number}"
        slug = slugify(name)
        if not Town.objects.filter(slug=slug).exists():
            town = Town.objects.create(slug=slug, name=name, capacity=100)
            ensure_town_content(town)
            return town
        next_number += 1


def ensure_town_content(town):
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
    for slug, name, location_slug, role, dialogue in NPC_DATA:
        npc = NPC.objects.filter(town=town, slug=slug).first()
        legacy_npcs = NPC.objects.filter(town=town, name=name)
        if npc is None:
            # Before stable slugs, the deputy was stored as
            # "deputy-halden-price" from their display name. Reuse that row
            # rather than creating a second Halden.
            npc = legacy_npcs.first()
            if npc is not None:
                npc.slug = slug
                npc.save(update_fields=["slug"])
        if npc is None:
            npc = NPC.objects.create(
                town=town,
                slug=slug,
                name=name,
                home_location=locations[location_slug],
                role=role,
                dialogue=dialogue,
                personality_tags="grounded, observant",
            )
        elif not npc.name:
            # Repair rows created by the first stable-slug seed pass, which
            # supplied a slug but accidentally omitted the display name.
            npc.name = name
            npc.save(update_fields=["name"])

        # If the first stable-slug pass already created a canonical row, the
        # legacy display-name row is now redundant. NPCs are not referenced by
        # foreign keys, so removing it cannot orphan game progress.
        legacy_npcs.exclude(pk=npc.pk).delete()
    for slug, name, location_slug, role, description in TOWNSFOLK_DATA:
        NPC.objects.get_or_create(
            town=town,
            slug=slug,
            defaults={
                "name": name,
                "home_location": locations[location_slug],
                "role": role,
                "dialogue": description,
                "personality_tags": "local, passing through",
                "portrait_recipe": {"portrait": slug},
                "is_townsfolk": True,
            },
        )
    ensure_cases(town, locations)


def ensure_cases(town, locations):
    from cases.definitions import CASE_DEFINITIONS
    from cases.models import Case, Clue

    for data in CASE_DEFINITIONS:
        case, _created = Case.objects.get_or_create(
            town=town,
            slug=data["slug"],
            defaults={
                "title": data["title"],
                "summary": data["summary"],
                "starting_location": locations[data["starting_location_slug"]],
                "outcome_text": data["outcome_text"],
            },
        )
        for code, title, text, order in data["clues"]:
            Clue.objects.get_or_create(
                case=case,
                code=code,
                defaults={"title": title, "text": text, "sort_order": order},
            )
