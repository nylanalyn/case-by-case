from django.db import migrations, models


def preserve_spent_hours(apps, schema_editor):
    PlayerProfile = apps.get_model("accounts", "PlayerProfile")
    for profile in PlayerProfile.objects.all():
        profile.daily_actions_remaining += 4
        profile.save(update_fields=["daily_actions_remaining"])


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_playerprofile_stats"),
    ]

    operations = [
        migrations.AlterField(
            model_name="playerprofile",
            name="daily_actions_remaining",
            field=models.PositiveSmallIntegerField(default=24),
        ),
        migrations.RunPython(preserve_spent_hours, migrations.RunPython.noop),
    ]
