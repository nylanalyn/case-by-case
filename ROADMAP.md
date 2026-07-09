# ROADMAP.md

# Development Roadmap

This roadmap is intentionally staged. The goal is to build a playable foundation first, then expand the town outward.

## Phase 0: Project Setup

Goal: create a clean, runnable project skeleton.

Tasks:

* Choose backend stack.
* Create repository structure.
* Add basic app configuration.
* Add SQLite database setup.
* Add migrations.
* Add development startup instructions.
* Add basic test runner.
* Add linting or formatting if useful.
* Add placeholder home page.

Done when:

* The app runs locally.
* The database initializes cleanly.
* A developer can start the project from the README.

## Phase 1: Accounts and Sessions

Goal: allow players to create accounts and log in.

Tasks:

* Add user model.
* Add username/password registration.
* Add optional email field.
* Hash passwords securely.
* Add login.
* Add logout.
* Add session cookies.
* Add basic auth guards for game pages.
* Add simple account page.

Done when:

* A player can register.
* A player can log in and out.
* Protected pages require login.

## Phase 2: Town Foundation

Goal: establish the persistent town structure.

Tasks:

* Add town model.
* Add player profile model.
* Assign new players to a default town.
* Add location model.
* Seed initial locations.
* Add town-scoped queries.
* Add basic town landing page.
* Add location detail pages.

Initial locations:

* Town Square
* Sheriff’s Office
* Diner
* Library
* Cemetery
* River Walk
* Bus Depot
* Observatory

Done when:

* A logged-in player belongs to a town.
* The player can view a map or location list.
* The player can visit individual locations.

## Phase 3: Daily Actions

Goal: implement the core daily-turn loop.

Tasks:

* Add daily action allowance.
* Show remaining actions in the UI.
* Add action spending helper.
* Prevent actions when the player has none left.
* Add manual admin/dev rollover command.
* Add automated daily rollover script.
* Add tests for action spending and reset.

Initial rule:

* Each player receives 20 actions per day.

Done when:

* A player can spend actions.
* Actions run out.
* Rollover restores actions.

## Phase 4: First Case

Goal: make the game playable as a mystery game.

Tasks:

* Add case model.
* Add player case progress model.
* Add clue model.
* Add player clue acquisition.
* Create one simple starter case.
* Add case start action.
* Add investigate action.
* Add interview/search actions as needed.
* Add case completion.
* Add reward or completion text.

Starter case idea:

* “The Missing Ledger”
* Begins at the Diner.
* Leads to the Library and Sheriff’s Office.
* Uses 3–5 clues.
* Ends with a grounded explanation and one odd loose thread.

Done when:

* A player can start a case.
* A player can spend actions to progress.
* A player can collect clues.
* A player can complete the case.

## Phase 5: NPCs

Goal: add persistent people to the town.

Tasks:

* Add NPC model.
* Seed initial NPCs.
* Place NPCs at locations.
* Add NPC detail/interview page.
* Add simple dialogue blocks.
* Connect NPCs to the starter case.
* Add relationship or familiarity field only if needed.

Initial NPCs:

* Diner worker
* Sheriff or deputy
* Librarian
* Bus depot clerk
* Cemetery caretaker

Done when:

* NPCs persist in the town.
* Players can talk to NPCs.
* NPCs can provide clues or case text.

## Phase 6: Location Message Boards

Goal: add the first social feature.

Tasks:

* Add message board post model.
* Scope posts by town and location.
* Add post form to location pages.
* Add character limit.
* Add delete-own-post support.
* Add basic moderation/admin delete hook.
* Add rate-limit placeholder or simple cooldown.

Done when:

* Players in the same town can leave notes at locations.
* Notes persist.
* Notes do not appear across other towns.

## Phase 7: Inventory and Evidence

Goal: give players a clear record of what they have.

Tasks:

* Add evidence/clue journal page.
* Add simple inventory item model if needed.
* Display active cases.
* Display collected clues.
* Display completed cases.
* Add case history page.

Done when:

* A player can understand what they know and what they are working on.

## Phase 8: Portrait System

Goal: support layered NPC portraits.

Tasks:

* Add static asset folders for portrait parts.
* Add portrait recipe field to NPCs.
* Render portrait layers in the frontend.
* Add fallback portrait.
* Add simple generator for new NPC portrait recipes.
* Store generated recipes persistently.

Layer slots:

* background
* body
* head
* hair
* outfit
* glasses
* hat
* accessory

Done when:

* NPCs can display stable layered portraits.
* The same NPC looks the same on repeat visits.

## Phase 9: Town Events and Logs

Goal: allow the town to remember public events.

Tasks:

* Add town_event model.
* Log case completions.
* Log notable player milestones.
* Log system events.
* Show recent town events on town page.
* Keep events scoped by town.

Done when:

* The town has a visible recent history.

## Phase 10: Newspaper Prototype

Goal: create a daily town summary.

Tasks:

* Add newspaper page.
* Pull from recent town events.
* Add fake classifieds.
* Add current rumors.
* Add recent solved cases.
* Add weird notice section.
* Generate once per rollover or on demand.

Done when:

* Players can read a daily newspaper that reflects some town activity.

## Phase 11: Multiple Towns / Pods

Goal: prepare for growth without changing the core design.

Tasks:

* Add town capacity setting.
* Assign new players to towns under capacity.
* Create new town when needed.
* Ensure message boards, events, NPCs, and cases are town-scoped.
* Add tests for town separation.

Default:

* 100 players per town.

Done when:

* New players can be assigned across towns automatically.
* Town data does not leak between towns.

## Phase 12: More Content

Goal: make the town worth returning to.

Tasks:

* Add more cases.
* Add side activities.
* Add more NPC dialogue.
* Add more clues and items.
* Add more message board flavor.
* Add location-specific actions.
* Add daily rumors.

Possible cases:

* The Missing Ledger
* The Cemetery Gate
* The Bus That Arrived Empty
* The Library Book Nobody Wrote
* The Dog That Keeps Reporting Crimes
* The Lights Under River Walk
* The Observatory Appointment

Done when:

* A player has multiple days of meaningful things to do.

## Phase 13: Moderation and Safety

Goal: make public player text manageable.

Tasks:

* Add report post button.
* Add admin moderation view.
* Add post hiding.
* Add user mute/suspension fields.
* Add rate limits.
* Add simple content filters if needed.
* Add audit log for moderation actions.

Done when:

* The game can safely support public notes from real players.

## Phase 14: Polish

Goal: improve the feel without changing the foundation.

Tasks:

* Improve layout.
* Add town map styling.
* Add location art.
* Add better typography.
* Add mobile-friendly views.
* Add small animations only where useful.
* Improve empty states.
* Improve error messages.
* Add flavor text variation.

Done when:

* The game feels pleasant to use, not just technically functional.

## First True Milestone

The first real milestone is reached when:

* Players can register and log in.
* Players belong to a town.
* Players can visit locations.
* Players have daily actions.
* Players can complete one case.
* Players can talk to NPCs.
* Players can leave messages at one location.
* Rollover restores actions.

This is the minimum version worth showing to another person.

## Guiding Constraint

Whenever tempted to build a generic engine, ask:

Would one more interesting town location be more useful right now?

If yes, build the location.
