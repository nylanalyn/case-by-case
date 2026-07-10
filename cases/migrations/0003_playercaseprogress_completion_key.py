from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0002_case_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="playercaseprogress",
            name="completion_key",
            field=models.SlugField(blank=True, max_length=80),
        ),
    ]
