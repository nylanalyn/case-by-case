from django.contrib import admin

from .models import Case, Clue, PlayerCaseProgress, PlayerClue
from .services import reset_case_progress


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
    search_fields = ("player__user__username", "case__title")
    actions = ["reset_selected_case_progress"]

    @admin.action(description="Reset selected case progress")
    def reset_selected_case_progress(self, request, queryset):
        for progress in queryset.select_related("player__user", "case"):
            reset_case_progress(progress)
            self.log_change(request, progress, "Reset case progress from admin action.")
        self.message_user(request, f"Reset {queryset.count()} case progress record(s).")


@admin.register(PlayerClue)
class PlayerClueAdmin(admin.ModelAdmin):
    list_display = ("player", "clue", "acquired_at")
    list_filter = ("clue__case",)
    search_fields = ("player__user__username", "clue__title", "clue__case__title")
