from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Town",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("slug", models.SlugField(unique=True)),
                ("capacity", models.PositiveSmallIntegerField(default=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("slug", models.SlugField()),
                ("description", models.TextField()),
                ("atmosphere_tags", models.CharField(blank=True, max_length=200)),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                ("is_unlocked", models.BooleanField(default=True)),
                ("town", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="locations", to="towns.town")),
            ],
            options={
                "ordering": ["sort_order", "name"],
                "unique_together": {("town", "slug")},
            },
        ),
        migrations.CreateModel(
            name="NPC",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("role", models.CharField(max_length=120)),
                ("personality_tags", models.CharField(blank=True, max_length=200)),
                ("dialogue", models.TextField()),
                ("portrait_recipe", models.JSONField(blank=True, default=dict)),
                ("home_location", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="npcs", to="towns.location")),
                ("town", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="npcs", to="towns.town")),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="TownEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("body", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("town", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="events", to="towns.town")),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
