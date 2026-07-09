from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from accounts.services import ensure_player_profile

from .models import MessageBoardPost


@login_required
def delete_post(request, post_id):
    profile = ensure_player_profile(request.user)
    post = get_object_or_404(MessageBoardPost, id=post_id, town=profile.town)
    location_slug = post.location.slug
    if request.method != "POST":
        return redirect("location_detail", slug=location_slug)
    if post.player_id != profile.id and not request.user.is_staff:
        messages.error(request, "You can only remove your own notes.")
        return redirect("location_detail", slug=location_slug)
    post.delete()
    messages.success(request, "Your note was removed.")
    return redirect("location_detail", slug=location_slug)
