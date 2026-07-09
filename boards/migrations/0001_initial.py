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
            name="MessageBoardPost",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content", models.CharField(max_length=280)),
                ("is_hidden", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("location", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="board_posts", to="towns.location")),
                ("player", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="board_posts", to="accounts.playerprofile")),
                ("town", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="board_posts", to="towns.town")),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
