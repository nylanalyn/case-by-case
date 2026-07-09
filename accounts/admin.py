from django.contrib import admin

from .models import PlayerProfile


@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "town", "daily_actions_remaining", "last_rollover_date")
    list_filter = ("town",)
    search_fields = ("user__username", "user__email")
