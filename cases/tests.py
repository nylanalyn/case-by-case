from io import StringIO

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from accounts.services import ensure_player_profile
from cases.definitions import CASE_DEFINITIONS, case_definition_for_slug
from cases.models import Case, PlayerCaseProgress, PlayerClue
from cases.services import (
    CaseLocked,
    InvalidCaseResolution,
    WrongLocation,
    advance_case,
    case_cards_for_location,
    case_cards_for_player,
    case_journal_for_player,
    reset_case_progress,
)
from cases.validation import validate_case_definitions
from towns.models import Location, TownEvent


def card_for_title(cards, title):
    return next(card for card in cards if card["case"].title == title)


class CaseTests(TestCase):
    def test_all_authored_case_definitions_load_in_explicit_order(self):
        self.assertEqual(
            [definition["slug"] for definition in CASE_DEFINITIONS],
            ["missing-ledger", "cemetery-gate", "observatory-appointment"],
        )

    def test_case_definition_lookup_uses_stable_slug(self):
        definition = case_definition_for_slug("missing-ledger")

        self.assertEqual(definition["title"], "The Missing Ledger")
        self.assertEqual(case_definition_for_slug("not-a-case"), {})

    def test_case_definition_validation_passes_for_authored_cases(self):
        self.assertEqual(validate_case_definitions(CASE_DEFINITIONS), [])

    def test_case_definition_validation_reports_actionable_errors(self):
        definitions = [
            {
                "slug": "broken-case",
                "starting_location_slug": "not-a-place",
                "requirements": {"curiosity": 1},
                "completion_effects": {},
                "clues": [("same-clue", "First", "", 1), ("same-clue", "Second", "", 2)],
                "steps": [
                    {
                        "action": "start",
                        "location_slug": "diner",
                        "clue": "missing-clue",
                        "next_step": 4,
                        "completion_choices": [{"key": "", "completion_effects": {"also-unknown": 1}}],
                    }
                ],
            }
        ]

        errors = validate_case_definitions(definitions)

        self.assertIn("broken-case: unknown starting location 'not-a-place'.", errors)
        self.assertIn("broken-case: unknown stat 'curiosity' in requirements.", errors)
        self.assertIn("broken-case: duplicate clue code 'same-clue'.", errors)
        self.assertIn("broken-case: first step must be at the starting location.", errors)
        self.assertIn("broken-case: final step must use action 'finish'.", errors)
        self.assertIn("broken-case, step 1: unknown clue 'missing-clue'.", errors)
        self.assertIn("broken-case, step 1: next_step must be 1.", errors)
        self.assertIn("broken-case, step 1: completion choice is missing a key.", errors)
        self.assertIn("broken-case, step 1: completion choice '' is missing a label.", errors)
        self.assertIn("broken-case, step 1: completion choice '' is missing outcome text.", errors)
        self.assertIn("broken-case, step 1: unknown stat 'also-unknown' in completion choice effects.", errors)

    def test_case_definition_validation_rejects_duplicate_case_slugs(self):
        definitions = [
            {
                "slug": "duplicate-case",
                "starting_location_slug": "diner",
                "requirements": {},
                "completion_effects": {},
                "clues": [("first-clue", "First clue", "", 1)],
                "steps": [
                    {
                        "action": "finish",
                        "location_slug": "diner",
                        "clue": "first-clue",
                        "next_step": 1,
                    }
                ],
            },
            {
                "slug": "duplicate-case",
                "starting_location_slug": "library",
                "requirements": {},
                "completion_effects": {},
                "clues": [("second-clue", "Second clue", "", 1)],
                "steps": [
                    {
                        "action": "finish",
                        "location_slug": "library",
                        "clue": "second-clue",
                        "next_step": 1,
                    }
                ],
            },
        ]

        self.assertIn("duplicate-case: duplicate case slug.", validate_case_definitions(definitions))

    def test_validate_case_definitions_command(self):
        output = StringIO()

        call_command("validate_case_definitions", stdout=output)

        self.assertIn("Validated 3 case definitions.", output.getvalue())

    def test_authored_case_steps_reference_seeded_clues(self):
        for definition in CASE_DEFINITIONS:
            clue_codes = {clue[0] for clue in definition["clues"]}
            step_clues = {step["clue"] for step in definition["steps"]}

            self.assertTrue(step_clues.issubset(clue_codes), definition["slug"])

    def test_starter_case_can_be_completed(self):
        user = User.objects.create_user(username="nico", password="safe-password-123")
        profile = ensure_player_profile(user)
        case = Case.objects.get(slug="missing-ledger", town=profile.town)
        locations = [
            Location.objects.get(town=profile.town, slug="diner"),
            Location.objects.get(town=profile.town, slug="library"),
            Location.objects.get(town=profile.town, slug="sheriffs-office"),
            Location.objects.get(town=profile.town, slug="river-walk"),
        ]

        for location in locations[:-1]:
            progress, _clue = advance_case(profile, case, location=location)
        progress, _clue = advance_case(
            profile,
            case,
            location=locations[-1],
            completion_key="report-the-scheme",
        )

        self.assertEqual(progress.status, PlayerCaseProgress.COMPLETE)
        self.assertEqual(PlayerClue.objects.filter(player=profile, clue__case=case).count(), 4)
        self.assertEqual(TownEvent.objects.filter(town=profile.town, title__contains=case.title).count(), 1)
        profile.refresh_from_db()
        self.assertEqual(profile.daily_actions_remaining, 20)
        self.assertEqual(profile.stats["town_trust"], 1)
        self.assertEqual(profile.stats["diner_trust"], 1)
        self.assertEqual(profile.stats["sheriff_trust"], 1)

    def test_case_step_requires_correct_location(self):
        user = User.objects.create_user(username="mara", password="safe-password-123")
        profile = ensure_player_profile(user)
        case = Case.objects.get(slug="missing-ledger", town=profile.town)
        library = Location.objects.get(town=profile.town, slug="library")

        with self.assertRaises(WrongLocation):
            advance_case(profile, case, location=library)

    def test_reset_case_progress_clears_case_clues(self):
        user = User.objects.create_user(username="iris", password="safe-password-123")
        profile = ensure_player_profile(user)
        case = Case.objects.get(slug="missing-ledger", town=profile.town)
        diner = Location.objects.get(town=profile.town, slug="diner")
        progress, _clue = advance_case(profile, case, location=diner)

        reset_case_progress(progress)

        progress.refresh_from_db()
        self.assertEqual(progress.status, PlayerCaseProgress.ACTIVE)
        self.assertEqual(progress.step, 0)
        self.assertEqual(PlayerClue.objects.filter(player=profile, clue__case=case).count(), 0)

    def test_completed_case_does_not_crash_location_cards(self):
        user = User.objects.create_user(username="rumi", password="safe-password-123")
        profile = ensure_player_profile(user)
        case = Case.objects.get(slug="missing-ledger", town=profile.town)
        locations = [
            Location.objects.get(town=profile.town, slug="diner"),
            Location.objects.get(town=profile.town, slug="library"),
            Location.objects.get(town=profile.town, slug="sheriffs-office"),
            Location.objects.get(town=profile.town, slug="river-walk"),
        ]
        for location in locations[:-1]:
            advance_case(profile, case, location=location)
        advance_case(profile, case, location=locations[-1], completion_key="report-the-scheme")

        cards = case_cards_for_location(profile, locations[-1])

        self.assertEqual(cards, [])

    def test_case_cards_point_to_next_lead(self):
        user = User.objects.create_user(username="halden", password="safe-password-123")
        profile = ensure_player_profile(user)
        case = Case.objects.get(slug="missing-ledger", town=profile.town)

        card = card_for_title(case_cards_for_player(profile), "The Missing Ledger")
        self.assertEqual(card["status"], PlayerCaseProgress.NOT_STARTED)
        self.assertEqual(card["action"]["location_slug"], "diner")

        diner = Location.objects.get(town=profile.town, slug="diner")
        advance_case(profile, case, location=diner)

        card = card_for_title(case_cards_for_player(profile), "The Missing Ledger")
        self.assertEqual(card["status"], PlayerCaseProgress.ACTIVE)
        self.assertEqual(card["action"]["location_slug"], "library")

    def test_ledger_case_requires_a_resolution_without_spending_an_action(self):
        user = User.objects.create_user(username="elliot", password="safe-password-123")
        profile = ensure_player_profile(user)
        case = Case.objects.get(slug="missing-ledger", town=profile.town)
        locations = [
            Location.objects.get(town=profile.town, slug="diner"),
            Location.objects.get(town=profile.town, slug="library"),
            Location.objects.get(town=profile.town, slug="sheriffs-office"),
            Location.objects.get(town=profile.town, slug="river-walk"),
        ]

        for location in locations[:-1]:
            advance_case(profile, case, location=location)

        with self.assertRaises(InvalidCaseResolution):
            advance_case(profile, case, location=locations[-1])

        profile.refresh_from_db()
        progress = PlayerCaseProgress.objects.get(player=profile, case=case)
        self.assertEqual(profile.daily_actions_remaining, 21)
        self.assertEqual(progress.status, PlayerCaseProgress.ACTIVE)
        self.assertEqual(PlayerClue.objects.filter(player=profile, clue__case=case).count(), 3)
        self.client.force_login(user)
        response = self.client.get("/town/locations/river-walk/")
        self.assertContains(response, "Bring the receipt to Deputy Halden")
        self.assertContains(response, "Leave the receipt with Mara")

    def test_ledger_case_can_end_by_leaving_the_receipt_with_mara(self):
        user = User.objects.create_user(username="dana", password="safe-password-123")
        profile = ensure_player_profile(user)
        case = Case.objects.get(slug="missing-ledger", town=profile.town)
        locations = [
            Location.objects.get(town=profile.town, slug="diner"),
            Location.objects.get(town=profile.town, slug="library"),
            Location.objects.get(town=profile.town, slug="sheriffs-office"),
            Location.objects.get(town=profile.town, slug="river-walk"),
        ]

        for location in locations[:-1]:
            advance_case(profile, case, location=location)
        progress, _clue = advance_case(
            profile,
            case,
            location=locations[-1],
            completion_key="leave-it-with-mara",
        )

        profile.refresh_from_db()
        self.assertEqual(progress.completion_key, "leave-it-with-mara")
        self.assertEqual(profile.stats["diner_trust"], 2)
        self.assertEqual(profile.stats["town_trust"], -1)
        self.assertEqual(profile.stats["sheriff_trust"], -1)
        event = TownEvent.objects.get(town=profile.town, title__contains=case.title)
        self.assertIn("closes the books early", event.body)
        card = card_for_title(case_cards_for_player(profile), "The Missing Ledger")
        self.assertIn("closes the books early", card["outcome_text"])

    def test_second_case_has_its_own_route(self):
        user = User.objects.create_user(username="arlet", password="safe-password-123")
        profile = ensure_player_profile(user)
        case = Case.objects.get(slug="cemetery-gate", town=profile.town)
        locations = [
            Location.objects.get(town=profile.town, slug="cemetery"),
            Location.objects.get(town=profile.town, slug="library"),
            Location.objects.get(town=profile.town, slug="bus-depot"),
            Location.objects.get(town=profile.town, slug="cemetery"),
        ]

        for location in locations:
            progress, _clue = advance_case(profile, case, location=location)

        self.assertEqual(progress.status, PlayerCaseProgress.COMPLETE)
        self.assertEqual(PlayerClue.objects.filter(player=profile, clue__case=case).count(), 4)
        profile.refresh_from_db()
        self.assertEqual(profile.daily_actions_remaining, 20)
        self.assertEqual(profile.stats["weirdness_tolerance"], 1)
        self.assertEqual(profile.stats["cemetery_trust"], 1)

    def test_stat_gated_case_unlocks_after_required_stat(self):
        user = User.objects.create_user(username="vale", password="safe-password-123")
        profile = ensure_player_profile(user)
        observatory_case = Case.objects.get(slug="observatory-appointment", town=profile.town)
        observatory = Location.objects.get(town=profile.town, slug="observatory")

        card = card_for_title(case_cards_for_player(profile), "The Observatory Appointment")
        self.assertFalse(card["is_available"])
        self.assertEqual(card["requirements"], "Weirdness Tolerance 1+")
        self.assertIn("stranger than a scheduling error", card["lock_text"])
        with self.assertRaises(CaseLocked):
            advance_case(profile, observatory_case, location=observatory)

        self.client.force_login(user)
        response = self.client.get("/cases/")
        self.assertContains(response, "Iris will not put the observatory appointment in your hands")
        self.assertContains(response, "Needed: Weirdness Tolerance 1+")

        cemetery_case = Case.objects.get(slug="cemetery-gate", town=profile.town)
        cemetery_route = [
            Location.objects.get(town=profile.town, slug="cemetery"),
            Location.objects.get(town=profile.town, slug="library"),
            Location.objects.get(town=profile.town, slug="bus-depot"),
            Location.objects.get(town=profile.town, slug="cemetery"),
        ]
        for location in cemetery_route:
            advance_case(profile, cemetery_case, location=location)
        profile.refresh_from_db()

        card = card_for_title(case_cards_for_player(profile), "The Observatory Appointment")
        self.assertTrue(card["is_available"])
        self.assertEqual(card["action"]["location_slug"], "observatory")

    def test_case_pages_show_next_lead_link(self):
        user = User.objects.create_user(username="mara", password="safe-password-123")
        ensure_player_profile(user)

        self.client.force_login(user)
        response = self.client.get("/cases/")

        self.assertContains(response, "Next lead")
        self.assertContains(response, "/town/locations/diner/")

    def test_location_case_card_links_to_next_lead_after_action(self):
        user = User.objects.create_user(username="mara", password="safe-password-123")
        profile = ensure_player_profile(user)
        case = Case.objects.get(slug="missing-ledger", town=profile.town)
        diner = Location.objects.get(town=profile.town, slug="diner")
        advance_case(profile, case, location=diner)

        self.client.force_login(user)
        response = self.client.get("/town/locations/diner/")

        self.assertContains(response, "Next lead")
        self.assertContains(response, "/town/locations/library/")

    def test_location_displays_found_clue_until_the_case_is_closed(self):
        user = User.objects.create_user(username="mara", password="safe-password-123")
        profile = ensure_player_profile(user)
        case = Case.objects.get(slug="missing-ledger", town=profile.town)
        diner = Location.objects.get(town=profile.town, slug="diner")
        library = Location.objects.get(town=profile.town, slug="library")
        sheriff = Location.objects.get(town=profile.town, slug="sheriffs-office")
        river_walk = Location.objects.get(town=profile.town, slug="river-walk")

        advance_case(profile, case, location=diner)

        diner_card = card_for_title(case_cards_for_location(profile, diner), "The Missing Ledger")
        self.assertEqual(diner_card["found_clue"].clue.code, "counter-note")
        library_card = card_for_title(case_cards_for_location(profile, library), "The Missing Ledger")
        self.assertIsNone(library_card["found_clue"])
        self.client.force_login(user)
        response = self.client.get("/town/locations/diner/")
        self.assertContains(response, "A note under the counter")
        self.assertContains(response, "Mara found a damp note where the ledger should have been.")

        advance_case(profile, case, location=library)
        library_card = card_for_title(case_cards_for_location(profile, library), "The Missing Ledger")
        self.assertEqual(library_card["found_clue"].clue.code, "library-card")

        advance_case(profile, case, location=sheriff)
        advance_case(profile, case, location=river_walk, completion_key="report-the-scheme")
        diner_card = card_for_title(case_cards_for_location(profile, diner), "The Missing Ledger")
        self.assertIsNone(diner_card["found_clue"])

    def test_case_journal_groups_evidence_by_case(self):
        user = User.objects.create_user(username="june", password="safe-password-123")
        profile = ensure_player_profile(user)
        case = Case.objects.get(slug="missing-ledger", town=profile.town)
        diner = Location.objects.get(town=profile.town, slug="diner")

        advance_case(profile, case, location=diner)

        record = card_for_title(case_journal_for_player(profile), "The Missing Ledger")
        self.assertEqual(record["case"], case)
        self.assertEqual(len(record["clues"]), 1)
        self.assertEqual(record["action"]["location_slug"], "library")

    def test_journal_page_shows_cases_and_evidence(self):
        user = User.objects.create_user(username="nico", password="safe-password-123")
        profile = ensure_player_profile(user)
        case = Case.objects.get(slug="missing-ledger", town=profile.town)
        diner = Location.objects.get(town=profile.town, slug="diner")
        advance_case(profile, case, location=diner)

        self.client.force_login(user)
        response = self.client.get("/cases/journal/")

        self.assertContains(response, "Case Journal")
        self.assertContains(response, "The Missing Ledger")
        self.assertContains(response, "A note under the counter")
        self.assertContains(response, "/town/locations/library/")
