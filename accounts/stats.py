STAT_DEFINITIONS = {
    "town_trust": "Town Trust",
    "diner_trust": "Diner Trust",
    "library_trust": "Library Trust",
    "sheriff_trust": "Sheriff's Office Trust",
    "cemetery_trust": "Cemetery Trust",
    "bus_depot_trust": "Bus Depot Trust",
    "observatory_trust": "Observatory Trust",
    "river_trust": "River Walk Trust",
    "weirdness_tolerance": "Weirdness Tolerance",
    "skeptical": "Skeptical",
}


def display_stats(stats):
    stats = stats or {}
    return [
        {"key": key, "label": label, "value": stats.get(key, 0)}
        for key, label in STAT_DEFINITIONS.items()
        if stats.get(key, 0) != 0
    ]


def stat_label(key):
    return STAT_DEFINITIONS.get(key, key.replace("_", " ").title())
