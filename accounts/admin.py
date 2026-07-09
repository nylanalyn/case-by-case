from django.contrib import admin

from .models import PlayerProfile
from .services import reset_daily_actions


@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "town", "daily_actions_remaining", "last_rollover_date")
    list_filter = ("town",)
    search_fields = ("user__username", "user__email")
    actions = ["reset_selected_daily_actions"]

    @admin.action(description="Reset selected players' daily actions")
    def reset_selected_daily_actions(self, request, queryset):
        for profile in queryset.select_related("user"):
            reset_daily_actions(profile)
            self.log_change(request, profile, "Reset daily actions from admin action.")
        self.message_user(request, f"Reset daily actions for {queryset.count()} player(s).")
