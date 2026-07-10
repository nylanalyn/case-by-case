from django.contrib.auth.models import User
from django.test import TestCase

from accounts.services import ensure_player_profile
from cases.models import Case
from cases.services import action_is_available_for_player, advance_case
from towns.models import Location, NPC, TownEvent
from towns.schedules import npc_dialogue, npc_location_slug, npcs_at_location
from towns.seed import ensure_town_content
from turns.services import pass_time


class TownHistoryTests(TestCase):
    def test_scheduled_npc_moves_between_locations_and_can_be_required_by_a_case_step(self):
        user = User.objects.create_user(username="mara", password="safe-password-123")
        profile = ensure_player_profile(user)
        diner = Location.objects.get(town=profile.town, slug="diner")
        depot = Location.objects.get(town=profile.town, slug="bus-depot")
        npc = NPC.objects.create(
            town=profile.town,
            slug="mara-bell-test",
            name="Mara Bell Test",
            home_location=diner,
            role="Diner worker",
            dialogue="Not now.",
            daily_schedule=[
                {"start": 5, "end": 17, "location_slug": "diner"},
                {"start": 17, "end": 18, "location_slug": "bus-depot"},
            ],
        )

        self.assertIsNone(npc_location_slug(npc, 2))
        self.assertEqual(npc_location_slug(npc, 17), "bus-depot")
        pass_time(profile, 17)
        self.assertIn(npc, npcs_at_location(profile.town, depot, profile.current_hour))
        action = {"location_slug": "bus-depot", "npc_slug": npc.slug}
        self.assertTrue(action_is_available_for_player(profile, action))
        self.assertFalse(action_is_available_for_player(profile, {**action, "location_slug": "diner"}))

    def test_named_townsfolk_are_seeded_and_have_stable_daily_locations(self):
        user = User.objects.create_user(username="nico", password="safe-password-123")
        profile = ensure_player_profile(user)
        townsfolk = NPC.objects.filter(town=profile.town, is_townsfolk=True)

        self.assertEqual(townsfolk.count(), 10)
        beverly = townsfolk.get(slug="beverly-kett")
        location_slug = npc_location_slug(beverly, 9)

        self.assertEqual(location_slug, npc_location_slug(beverly, 9))
        self.assertIn(location_slug, {location.slug for location in profile.town.locations.all()})

    def test_townsfolk_dialogue_responds_to_their_current_location_and_time(self):
        user = User.objects.create_user(username="darlene", password="safe-password-123")
        profile = ensure_player_profile(user)
        townsperson = NPC.objects.get(town=profile.town, slug="darlene-mott")
        location = Location.objects.get(town=profile.town, slug=npc_location_slug(townsperson, 8))

        dialogue = npc_dialogue(townsperson, location, 8)

        self.assertIn("Morning", dialogue)
        self.assertNotEqual(dialogue, townsperson.dialogue)

    def test_seed_normalizes_legacy_halden_without_creating_a_duplicate(self):
        user = User.objects.create_user(username="legacy", password="safe-password-123")
        profile = ensure_player_profile(user)
        canonical = NPC.objects.get(town=profile.town, slug="halden-price")
        home_location = canonical.home_location
        canonical.delete()
        NPC.objects.create(
            town=profile.town,
            slug="deputy-halden-price",
            name="Deputy Halden Price",
            home_location=home_location,
            role="Deputy",
            dialogue="Not now.",
        )

        ensure_town_content(profile.town)

        haldens = NPC.objects.filter(town=profile.town, name="Deputy Halden Price")
        self.assertEqual(haldens.count(), 1)
        self.assertEqual(haldens.get().slug, "halden-price")

    def test_player_can_pass_multiple_hours_from_town_home(self):
        user = User.objects.create_user(username="iris", password="safe-password-123")
        profile = ensure_player_profile(user)

        self.client.force_login(user)
        response = self.client.post("/town/pass-time/", {"hours": 5})

        self.assertRedirects(response, "/town/")
        profile.refresh_from_db()
        self.assertEqual(profile.daily_actions_remaining, 19)
        self.assertEqual(profile.current_time_label, "5:00 AM")

    def test_town_home_shows_current_leads(self):
        user = User.objects.create_user(username="halden", password="safe-password-123")
        profile = ensure_player_profile(user)
        case = Case.objects.get(slug="missing-ledger", town=profile.town)
        diner = Location.objects.get(town=profile.town, slug="diner")
        advance_case(profile, case, location=diner)

        self.client.force_login(user)
        response = self.client.get("/town/")

        self.assertContains(response, "Current leads")
        self.assertContains(response, "The Missing Ledger")
        self.assertContains(response, "/town/locations/library/")

    def test_history_page_shows_town_events(self):
        user = User.objects.create_user(username="rumi", password="safe-password-123")
        profile = ensure_player_profile(user)
        TownEvent.objects.create(
            town=profile.town,
            title="The square clock skipped twice",
            body="Nobody agreed on which hour was missing.",
        )

        self.client.force_login(user)
        response = self.client.get("/town/history/")

        self.assertContains(response, "Brindle Creek History")
        self.assertContains(response, "The square clock skipped twice")
        self.assertContains(response, "Nobody agreed on which hour was missing.")

    def test_newspaper_page_summarizes_town_events(self):
        user = User.objects.create_user(username="mara", password="safe-password-123")
        profile = ensure_player_profile(user)
        TownEvent.objects.create(
            town=profile.town,
            title="A new day settles over town",
            body="Actions have refreshed. Rumor: The diner clock lost eleven minutes overnight.",
        )
        TownEvent.objects.create(
            town=profile.town,
            title="mara closed The Missing Ledger",
            body="The ledger was hidden behind the coffee tins.",
        )

        self.client.force_login(user)
        response = self.client.get("/town/newspaper/")

        self.assertContains(response, "The Brindle Creek Register")
        self.assertContains(response, "The diner clock lost eleven minutes overnight.")
        self.assertContains(response, "Closed Cases")
        self.assertContains(response, "mara closed The Missing Ledger")
        self.assertContains(response, "Classifieds")
