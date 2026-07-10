# Case by Case

A small Django prototype for a daily-turn mystery game set in the persistent town of Brindle Creek.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_initial_data
python manage.py runserver
```

Open http://127.0.0.1:8000 and create an account.

## Useful commands

```bash
python manage.py test
python manage.py rollover
python manage.py validate_case_definitions
```

## Time-gated case steps

Each action normally remains available all day. To limit an authored case step,
add an `available_between` window using 24-hour values. The start is inclusive
and the end is exclusive; an end before the start crosses midnight.

```python
"available_between": {"start": 20, "end": 5},
```

This example makes a step available from 8:00 PM through 4:59 AM.

To require a scheduled person, add their stable NPC slug to the step:

```python
"npc_slug": "mara-bell",
```

## Persistent Townsfolk

Generated townsfolk are stored permanently in one town and follow daily schedules.
They are opt-in while the town is being authored:

```bash
python manage.py generate_townsfolk brindle-creek --count 4
```
