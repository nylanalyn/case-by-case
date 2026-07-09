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
    ("Mara Bell", "diner", "Diner worker", "Mara remembers every breakfast order and almost every lie."),
    ("Deputy Halden Price", "sheriffs-office", "Deputy", "Halden writes careful notes in a notebook with a cracked cover."),
    ("Iris Vale", "library", "Librarian", "Iris keeps the old town ledgers in better shape than the town keeps itself."),
    ("Nico Saye", "bus-depot", "Bus depot clerk", "Nico says buses arrive late, early, or wrong."),
    ("June Arlet", "cemetery", "Cemetery caretaker", "June trims the grass and refuses to discuss the north gate."),
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
