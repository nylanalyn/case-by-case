from django.db import models


class Town(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    capacity = models.PositiveSmallIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    town = models.ForeignKey(Town, on_delete=models.CASCADE, related_name="locations")
    name = models.CharField(max_length=120)
    slug = models.SlugField()
    description = models.TextField()
    atmosphere_tags = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_unlocked = models.BooleanField(default=True)

    class Meta:
        unique_together = ("town", "slug")
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class NPC(models.Model):
    town = models.ForeignKey(Town, on_delete=models.CASCADE, related_name="npcs")
    name = models.CharField(max_length=120)
    home_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="npcs")
    role = models.CharField(max_length=120)
    personality_tags = models.CharField(max_length=200, blank=True)
    dialogue = models.TextField()
    portrait_recipe = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class TownEvent(models.Model):
    town = models.ForeignKey(Town, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=160)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
