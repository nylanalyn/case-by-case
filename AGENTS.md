# AGENTS.md

# Agent Instructions

This project is a web-based daily-turn mystery game set in a persistent small town.

When working on this codebase, prioritize simple, maintainable foundations over clever abstractions.

## Core Rule

Build the smallest useful version first.

Do not turn every system into a framework unless the current game needs it.

## Project Priorities

In order:

1. Make the game playable.
2. Keep the code understandable.
3. Preserve town persistence.
4. Make future expansion easy.
5. Add polish only after the loop works.

## Design Philosophy

The game is about returning to the same town every day.

Do not treat locations, NPCs, or player traces as disposable unless explicitly required.

Persistent details matter.

## Auth

Use simple local authentication first.

Requirements:

* username
* password
* optional email
* hashed passwords
* secure session cookies

Do not implement OAuth unless specifically asked.

Do not store plaintext passwords.

## Data Model Expectations

Most game tables should include `town_id` where appropriate.

The project may begin with one town, but the schema should not make multiple towns difficult later.

Likely core entities:

* users
* towns
* players
* locations
* npcs
* cases
* clues
* inventory_items
* player_case_progress
* daily_state
* message_board_posts
* town_events

## Daily Actions

Daily actions are central to the game.

Keep this system simple:

* player has a daily action allowance
* actions decrement when used
* daily rollover restores actions
* rollover may update town state

Do not create a complex energy/stamina/resource system until the basic action loop is working.

## Message Boards

Location message boards are an early social feature.

They should be:

* persistent
* scoped by town
* scoped by location
* rate-limited eventually
* easy to moderate later

Do not build real-time chat for the first version.

## NPC Portraits

NPC portraits may use layered PNG assets.

Store portrait recipes as data, not as regenerated images.

Example fields:

* body
* head
* hair
* hat
* glasses
* outfit
* accessory
* background

The same NPC should look the same every time unless changed intentionally.

## Case System

Cases should be data-friendly but not overengineered.

Every case has a stable `slug` that is its identity. The slug links database
rows to their authored definition in `cases/definitions.py` and is unique per
town. Titles are display-only and may clash (especially once generated cases
exist) — never look up a case or its definition by title.

A case should support:

* slug (stable identity, unique per town)
* title (display only)
* description
* starting location
* progress state
* clues
* required actions
* completion conditions
* outcome text

Avoid building a huge generic mystery scripting language before the first case works.

## Frontend

Prefer boring, readable UI.

Server-rendered pages, light JavaScript, or HTMX are acceptable.

The UI should support:

* logging in
* seeing current actions
* navigating locations
* reading location descriptions
* interacting with NPCs
* working a case
* viewing clues
* posting to a board

Do not start with a complex SPA unless specifically requested.

## Database

SQLite is preferred for early development.

Use migrations.

Keep schema readable.

Avoid premature sharding, queues, distributed systems, or heavy infrastructure.

## Code Style

Prefer:

* clear names
* small functions
* explicit behavior
* boring dependencies
* simple database queries
* tests for game rules

Avoid:

* magical abstractions
* hidden global state
* excessive metaprogramming
* complicated build steps
* speculative plugin systems

## Testing Priorities

Test game rules first:

* account creation
* login
* action spending
* action reset
* case progress
* clue acquisition
* town scoping
* message board scoping

## Security Basics

Always handle:

* password hashing
* session security
* input validation
* SQL injection prevention
* rate limits for posting
* basic moderation hooks

Do not trust user-submitted text.

## First Milestone

The first milestone is not “the full game.”

The first milestone is:

A player can create an account, log in, enter one town, visit locations, spend daily actions, progress through one case, leave a note on one location board, and return after rollover.

## Do Not Build Yet

Unless specifically asked, do not begin with:

* OAuth
* live chat
* trading
* guilds
* complex economy
* procedural map generation
* AI content generation
* admin dashboards
* mobile app
* large asset pipelines

## Tone Reminder

The game should feel grounded, local, odd, and persistent.

It is not epic fantasy.

It is not pure cosmic horror.

It is a small town where the diner coffee is bad, the cemetery gate is always wet, and somebody keeps leaving notes about ducks.
<!-- grove:start -->
## Code navigation: grove for structure, shell for the rest

**grove** is a tree-sitter engine for *structural* code questions — byte-precise,
token-cheap (languages: python). Its tools are **deferred** MCP tools; load them in
one ToolSearch when a code question lands (don't default to a search agent or grep):
`mcp__grove__outline`, `mcp__grove__symbols`, `mcp__grove__source`, `mcp__grove__callers`, `mcp__grove__definition`, `mcp__grove__map`, `mcp__grove__check`.

**Use grove for named symbols and relationships** (every result carries a stable
`symbol-id`, `<lang>:<relpath>#<name>@<row>`, to pass forward; lines 1-based):
- What's in a file (skeleton, not the whole file) → `mcp__grove__outline` (`detail:0` if > 500 lines).
- Where a fn / type / struct / macro is defined → `mcp__grove__symbols` with `name` → `mcp__grove__source` with the id.
- One symbol's exact body → `mcp__grove__source`.
- Who calls it → `mcp__grove__callers`.
- Go-to-def from a usage (scope-aware, follows imports cross-file) → `mcp__grove__definition` with `at` (file:line:col).
- How a directory connects → `mcp__grove__map` (one call; prefer over many `mcp__grove__source`).
- Syntax after an edit → `mcp__grove__check`.

**Use the shell — the right tool, not a fallback — when grove can't see the target:**
- Text, not a symbol (a string, log / error message, config key, a macro's *value*,
  a constant, a flag, a TODO) → `grep -rn` / `rg`. grove finds definitions, not text.
- Non-code files (Makefiles, configs, data, docs) → `grep` / `read`.
- A quick fact (path exists, `ls`, `wc -l`, `find`, read a small file) → shell.

**Combine** (same 1-based lines, same bytes): `grep` a literal's line → `mcp__grove__definition`
`at` to resolve its symbol · `mcp__grove__outline` → bounded `read` (`offset`/`limit`) for
adjacent symbols · `mcp__grove__map` / `mcp__grove__symbols` to locate → `grep` a constant inside.

Rule of thumb: want a **symbol** → grove first (don't `grep` / `read` for it). Want
**text or a quick fact** → shell. Combining is fine.
<!-- grove:end -->
