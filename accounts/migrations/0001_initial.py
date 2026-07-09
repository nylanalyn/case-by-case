from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("towns", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlayerProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("daily_actions_remaining", models.PositiveSmallIntegerField(default=20)),
                ("last_rollover_date", models.DateField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("town", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="players", to="towns.town")),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="player_profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
