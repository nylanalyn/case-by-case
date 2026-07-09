from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
        ("towns", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Case",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("summary", models.TextField()),
                ("outcome_text", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("starting_location", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="starting_cases", to="towns.location")),
                ("town", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="cases", to="towns.town")),
            ],
            options={
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="Clue",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.SlugField(max_length=80)),
                ("title", models.CharField(max_length=120)),
                ("text", models.TextField()),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                ("case", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="clues", to="cases.case")),
            ],
            options={
                "ordering": ["sort_order", "title"],
                "unique_together": {("case", "code")},
            },
        ),
        migrations.CreateModel(
            name="PlayerCaseProgress",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("not_started", "Not started"), ("active", "Active"), ("complete", "Complete")], default="active", max_length=20)),
                ("step", models.PositiveSmallIntegerField(default=0)),
                ("started_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("case", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="player_progress", to="cases.case")),
                ("player", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="case_progress", to="accounts.playerprofile")),
            ],
            options={
                "unique_together": {("player", "case")},
            },
        ),
        migrations.CreateModel(
            name="PlayerClue",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("acquired_at", models.DateTimeField(auto_now_add=True)),
                ("clue", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="player_clues", to="cases.clue")),
                ("player", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="player_clues", to="accounts.playerprofile")),
            ],
            options={
                "ordering": ["-acquired_at"],
                "unique_together": {("player", "clue")},
            },
        ),
    ]
