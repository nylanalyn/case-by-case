from django.db import models


class MessageBoardPost(models.Model):
    town = models.ForeignKey("towns.Town", on_delete=models.CASCADE, related_name="board_posts")
    location = models.ForeignKey("towns.Location", on_delete=models.CASCADE, related_name="board_posts")
    player = models.ForeignKey("accounts.PlayerProfile", on_delete=models.CASCADE, related_name="board_posts")
    content = models.CharField(max_length=280)
    is_hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.location}: {self.content[:32]}"
