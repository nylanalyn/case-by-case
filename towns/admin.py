from django.contrib import admin

from .models import Location, NPC, Town, TownEvent


@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "capacity", "created_at")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "town", "slug", "sort_order", "is_unlocked")
    list_filter = ("town", "is_unlocked")


@admin.register(NPC)
class NPCAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "town", "home_location", "role", "is_townsfolk")
    list_filter = ("town", "home_location", "is_townsfolk")


@admin.register(TownEvent)
class TownEventAdmin(admin.ModelAdmin):
    list_display = ("town", "title", "created_at")
    list_filter = ("town",)
