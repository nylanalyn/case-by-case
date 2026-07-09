from django.db import migrations, models
from django.utils.text import slugify


TITLE_TO_SLUG = {
    "The Missing Ledger": "missing-ledger",
    "The Cemetery Gate": "cemetery-gate",
    "The Observatory Appointment": "observatory-appointment",
}


def populate_slugs(apps, schema_editor):
    Case = apps.get_model("cases", "Case")
    for case in Case.objects.all():
        case.slug = TITLE_TO_SLUG.get(case.title) or slugify(case.title)
        case.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="case",
            name="slug",
            field=models.SlugField(default="", max_length=80),
            preserve_default=False,
        ),
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
        migrations.AlterUniqueTogether(
            name="case",
            unique_together={("town", "slug")},
        ),
    ]
