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
```
