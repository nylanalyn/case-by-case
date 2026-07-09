from django.contrib import admin

from .models import MessageBoardPost


@admin.register(MessageBoardPost)
class MessageBoardPostAdmin(admin.ModelAdmin):
    list_display = ("player", "town", "location", "created_at", "is_hidden")
    list_filter = ("town", "location", "is_hidden")
    search_fields = ("content", "player__user__username")
    actions = ["hide_selected_posts", "unhide_selected_posts"]

    @admin.action(description="Hide selected board posts")
    def hide_selected_posts(self, request, queryset):
        updated = queryset.update(is_hidden=True)
        for post in queryset:
            self.log_change(request, post, "Hid board post from admin action.")
        self.message_user(request, f"Hid {updated} post(s).")

    @admin.action(description="Unhide selected board posts")
    def unhide_selected_posts(self, request, queryset):
        updated = queryset.update(is_hidden=False)
        for post in queryset:
            self.log_change(request, post, "Unhid board post from admin action.")
        self.message_user(request, f"Unhid {updated} post(s).")
