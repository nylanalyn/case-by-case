from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="playerprofile",
            name="stats",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
