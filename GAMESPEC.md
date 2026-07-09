# GAMESPEC.md

# Project Overview

This is a web-based daily-turn mystery game set in a persistent small town.

Players create an account, enter a town, spend a limited number of daily actions investigating cases, talking to NPCs, collecting clues, reading local messages, and slowly uncovering strange events.

The game should feel cozy, weird, social, and persistent. The town is not a disposable map. It is the heart of the game.

## Core Inspirations

* Kingdom of Loathing style daily turns
* Legend of the Green Dragon style recurring browser play
* Small-town mystery fiction
* Light social persistence through town boards and player traces
* Strange-but-grounded atmosphere

## Core Design Principle

The player should always have one more interesting thing to check before logging off.

Not fifty things. One more thing.

## Tone

The game should mostly feel like a normal small town with odd edges.

Most cases are grounded:

* missing items
* strange neighbors
* petty crimes
* fraud
* local legends
* suspicious accidents

Occasionally, something has no clean explanation.

The horror should be quiet. The weirdness should arrive sideways.

## Player Loop

Each day, a player receives a fixed number of actions.

Players spend actions to:

* visit locations
* investigate scenes
* interview NPCs
* search for clues
* work cases
* read notices
* perform side activities
* recover resources
* interact with town systems

At daily rollover:

* actions refresh
* certain cases advance
* rumors update
* town events may change
* bulletin boards remain persistent
* NPCs may move or change availability

## Accounts

Initial account system should be simple.

Required:

* username
* password

Optional:

* email address

Email is not required to play. If provided, it may later support password resets or notifications.

OAuth is not required for the first version.

Passwords must be securely hashed. Never store plaintext passwords.

## Towns / Pods

Players belong to a town.

Each town is a semi-private shared instance with a limited population, such as 100 players.

All players in the same town see:

* the same location boards
* the same local events
* the same town history
* the same public player traces

If the game grows, new players can be assigned to towns automatically.

The town model should be included early, even if only one town exists at launch.

## Locations

The town is mapped, not fully randomized.

Each location should have:

* name
* description
* available actions
* NPCs
* possible cases
* message board or local note system
* atmosphere tags
* unlock conditions, if any

Example locations:

* Town Square
* Sheriff’s Office
* Diner
* Library
* Cemetery
* Bus Depot
* Apartments
* River Walk
* Observatory
* Forgotten Alley

## NPCs

NPCs may be hand-authored, generated, or hybrid.

NPCs should persist once created.

NPCs can have:

* name
* portrait recipe
* home location
* role
* personality tags
* dialogue
* case involvement
* relationship state with the player
* public town state

NPC portraits may be generated from layered PNG parts.

A portrait recipe should store selected asset IDs rather than generating a new image every time.

Example:

```json
{
  "body": "body_03",
  "head": "head_08",
  "hair": "hair_black_messy",
  "glasses": "round_gold",
  "hat": null,
  "coat": "raincoat_green",
  "background": "diner_booth"
}
```

## Cases

Cases are structured investigations.

A case may include:

* title
* summary
* starting location
* involved NPCs
* clue list
* required actions
* branching outcomes
* rewards
* failure or delay states
* public town consequences

Cases should be data-driven where practical, but not so abstract that development stalls.

The engine exists to support the town, not the other way around.

## Clues

Clues are pieces of information, objects, testimony, contradictions, or observations.

Clues may be:

* found at locations
* gained through interviews
* unlocked by items
* produced by comparing other clues
* tied to case progress

Clues should be readable and flavorful, not just mechanical tokens.

## Social Features

Initial social features should be small and location-based.

Each location may have a message board where players can leave notes.

Message board requirements:

* tied to town_id
* tied to location_id
* character limit
* rate limit
* moderation tools
* report/hide functionality eventually
* no private messaging required at first

Player messages should make the town feel lived-in, not chaotic.

## Admin and Operator Controls

The game needs basic trusted-operator controls early, before broader playtesting.

Initial admin controls should use Django staff/admin permissions rather than a custom dashboard.

Admins should be able to:

* reset a player's daily actions
* run or trigger daily rollover
* reset a player's case progress
* remove or hide message board posts
* review basic player, town, case, and board state

Admin actions should be logged where practical.

Do not expose destructive controls to normal players.

Do not build a large custom admin console before the core game loop is stable.

## Daily Newspaper

Eventually, the town may have a daily newspaper.

The newspaper can include:

* recent solved cases
* player achievements
* town rumors
* weather
* strange notices
* classified ads
* seasonal announcements
* selected bulletin board quotes

This is not required for the first prototype, but the data model should allow public town events to be logged.

## First Playable Prototype

The first playable version should include:

* account creation
* login/logout
* one town
* daily action counter
* several fixed locations
* one simple case
* persistent NPCs
* one location message board
* basic inventory or clue list
* daily rollover

The prototype is successful if a player can:

1. log in
2. spend actions
3. make progress on a case
4. run out of actions
5. return after rollover
6. continue playing

## Technical Preference

Recommended stack:

* Backend: FastAPI, Django, Axum, or similar
* Database: SQLite first
* Frontend: server-rendered HTML plus light JavaScript or HTMX
* Auth: local username/password sessions
* Deployment: small VPS
* Daily rollover: cron or systemd timer

Avoid overbuilding early.

## Non-Goals for Version 1

Do not build these first:

* complex OAuth
* real-time chat
* large economy
* trading
* guilds
* combat system
* procedural world generation
* mobile app
* complex admin dashboard
* AI-generated live content

## Long-Term Ideas

Possible later systems:

* multiple towns / pods
* seasonal town events
* public town history
* newspapers
* mayor or town roles
* player reputation
* mail
* collectible portraits
* expandable wardrobe assets
* case authoring tools
* town-specific procedural details
* shared mysteries across towns
* limited inter-town events

## Guiding Vibe

A player should feel like they live in a peculiar little town where most days are normal, some days are strange, and once in a while everyone quietly agrees not to talk about what happened near the river.
