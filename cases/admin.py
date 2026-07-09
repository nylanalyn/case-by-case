from django.contrib import admin

from .models import Case, Clue, PlayerCaseProgress, PlayerClue


class ClueInline(admin.TabularInline):
    model = Clue
    extra = 0


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ("title", "town", "starting_location", "is_active")
    list_filter = ("town", "is_active")
    inlines = [ClueInline]


@admin.register(PlayerCaseProgress)
class PlayerCaseProgressAdmin(admin.ModelAdmin):
    list_display = ("player", "case", "status", "step", "updated_at")
    list_filter = ("status", "case")


@admin.register(PlayerClue)
class PlayerClueAdmin(admin.ModelAdmin):
    list_display = ("player", "clue", "acquired_at")
