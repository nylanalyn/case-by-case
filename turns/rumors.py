DAILY_RUMORS = [
    "Someone left a jar of buttons on the library steps. Nobody has claimed the blue ones.",
    "The diner clock lost eleven minutes overnight, but only above the counter.",
    "A bus ticket was found in the cemetery gate latch, dry despite the rain.",
    "The river carried a receipt upstream this morning. Mara said not to make a thing of it.",
    "The observatory light blinked twice after closing, then once more when everyone looked away.",
]


def rumor_for_date(day):
    return DAILY_RUMORS[day.toordinal() % len(DAILY_RUMORS)]
