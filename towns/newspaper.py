CLASSIFIEDS = [
    "Found: one brass key, warm to the touch. Ask at the diner, but not before lunch.",
    "For sale: rain barrel, nearly new, knows too much.",
    "Wanted: someone with steady hands to repaint the bus depot numbers.",
]

WEIRD_NOTICES = [
    "The north cemetery gate will remain closed until it apologizes.",
    "Residents are reminded not to feed the payphone behind the library.",
    "Anyone hearing bells from the river should count them and then forget the number.",
]


def current_rumor(events):
    for event in events:
        if "Rumor:" in event.body:
            return event.body.split("Rumor:", 1)[1].strip()
    return "Nothing official, which has never stopped anyone here."
