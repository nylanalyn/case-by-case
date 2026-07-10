from django.db import models


class Case(models.Model):
    # Stable key linking this row to its authored definition in
    # cases/definitions.py. Titles are display-only and may clash.
    slug = models.SlugField(max_length=80)
    title = models.CharField(max_length=120)
    summary = models.TextField()
    town = models.ForeignKey("towns.Town", on_delete=models.CASCADE, related_name="cases")
    starting_location = models.ForeignKey("towns.Location", on_delete=models.PROTECT, related_name="starting_cases")
    outcome_text = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("town", "slug")
        ordering = ["title"]

    def __str__(self):
        return self.title


class Clue(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="clues")
    code = models.SlugField(max_length=80)
    title = models.CharField(max_length=120)
    text = models.TextField()
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ("case", "code")
        ordering = ["sort_order", "title"]

    def __str__(self):
        return self.title


class PlayerCaseProgress(models.Model):
    NOT_STARTED = "not_started"
    ACTIVE = "active"
    COMPLETE = "complete"
    STATUS_CHOICES = [
        (NOT_STARTED, "Not started"),
        (ACTIVE, "Active"),
        (COMPLETE, "Complete"),
    ]

    player = models.ForeignKey("accounts.PlayerProfile", on_delete=models.CASCADE, related_name="case_progress")
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="player_progress")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)
    step = models.PositiveSmallIntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    completion_key = models.SlugField(max_length=80, blank=True)

    class Meta:
        unique_together = ("player", "case")

    def __str__(self):
        return f"{self.player} - {self.case}"


class PlayerClue(models.Model):
    player = models.ForeignKey("accounts.PlayerProfile", on_delete=models.CASCADE, related_name="player_clues")
    clue = models.ForeignKey(Clue, on_delete=models.CASCADE, related_name="player_clues")
    acquired_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("player", "clue")
        ordering = ["-acquired_at"]

    def __str__(self):
        return f"{self.player}: {self.clue}"
