from django.contrib import admin

from .models import MessageBoardPost


@admin.register(MessageBoardPost)
class MessageBoardPostAdmin(admin.ModelAdmin):
    list_display = ("player", "town", "location", "created_at", "is_hidden")
    list_filter = ("town", "location", "is_hidden")
    search_fields = ("content", "player__user__username")
