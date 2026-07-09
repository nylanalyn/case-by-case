from django.core.exceptions import ValidationError
from django.utils import timezone

from turns.services import spend_action
from towns.models import TownEvent

from .models import MessageBoardPost


class BoardCooldownError(Exception):
    pass


def create_post(player, location, content):
    content = content.strip()
    if not content:
        raise ValidationError("Post content cannot be empty.")
    last_post = MessageBoardPost.objects.filter(player=player).order_by("-created_at").first()
    if last_post and timezone.now() - last_post.created_at < timezone.timedelta(minutes=1):
        raise BoardCooldownError("Wait a minute before pinning another note.")
    spend_action(player, reason="leave a note")
    post = MessageBoardPost.objects.create(
        town=player.town,
        location=location,
        player=player,
        content=content,
    )
    TownEvent.objects.create(
        town=player.town,
        title=f"{player.user.username} left a note at {location.name}",
        body=content,
    )
    return post
