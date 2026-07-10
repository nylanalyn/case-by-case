from django.db import migrations, models
from django.utils.text import slugify


def populate_npc_slugs(apps, schema_editor):
    NPC = apps.get_model("towns", "NPC")
    for npc in NPC.objects.all().order_by("town_id", "id"):
        base_slug = slugify(npc.name)
        slug = base_slug
        suffix = 2
        while NPC.objects.filter(town_id=npc.town_id, slug=slug).exclude(id=npc.id).exists():
            slug = f"{base_slug}-{suffix}"
            suffix += 1
        npc.slug = slug
        npc.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [("towns", "0001_initial")]

    operations = [
        migrations.AddField(model_name="npc", name="slug", field=models.SlugField(default="", max_length=80), preserve_default=False),
        migrations.AddField(model_name="npc", name="daily_schedule", field=models.JSONField(blank=True, default=list)),
        migrations.AddField(model_name="npc", name="is_townsfolk", field=models.BooleanField(default=False)),
        migrations.RunPython(populate_npc_slugs, migrations.RunPython.noop),
        migrations.AlterUniqueTogether(name="npc", unique_together={("town", "slug")}),
    ]
