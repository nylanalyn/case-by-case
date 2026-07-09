from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.services import ensure_player_profile
from boards.forms import MessageBoardPostForm
from boards.models import MessageBoardPost
from boards.services import BoardCooldownError, create_post
from cases.services import case_cards_for_location, case_cards_for_player
from turns.services import NotEnoughActions

from .models import Location, TownEvent
from .newspaper import CLASSIFIEDS, WEIRD_NOTICES, current_rumor
from .seed import ensure_initial_town


def home(request):
    if request.user.is_authenticated:
        return redirect("town_home")
    ensure_initial_town()
    return render(request, "home.html")


@login_required
def town_home(request):
    profile = ensure_player_profile(request.user)
    locations = Location.objects.filter(town=profile.town, is_unlocked=True)
    events = TownEvent.objects.filter(town=profile.town)[:5]
    case_cards = case_cards_for_player(profile)
    return render(
        request,
        "towns/home.html",
        {"profile": profile, "locations": locations, "events": events, "case_cards": case_cards},
    )


@login_required
def town_history(request):
    profile = ensure_player_profile(request.user)
    events = TownEvent.objects.filter(town=profile.town)[:50]
    return render(request, "towns/history.html", {"profile": profile, "events": events})


@login_required
def newspaper(request):
    profile = ensure_player_profile(request.user)
    events = list(TownEvent.objects.filter(town=profile.town)[:20])
    solved_cases = [event for event in events if " closed " in event.title]
    return render(
        request,
        "towns/newspaper.html",
        {
            "profile": profile,
            "events": events[:5],
            "solved_cases": solved_cases[:5],
            "rumor": current_rumor(events),
            "classifieds": CLASSIFIEDS,
            "weird_notices": WEIRD_NOTICES,
        },
    )


@login_required
def location_detail(request, slug):
    profile = ensure_player_profile(request.user)
    location = get_object_or_404(Location, town=profile.town, slug=slug, is_unlocked=True)
    if request.method == "POST":
        form = MessageBoardPostForm(request.POST)
        if form.is_valid():
            try:
                create_post(profile, location, form.cleaned_data["content"])
            except (BoardCooldownError, NotEnoughActions) as exc:
                messages.error(request, str(exc))
            else:
                messages.success(request, "Your note is pinned to the board.")
            return redirect("location_detail", slug=location.slug)
    else:
        form = MessageBoardPostForm()

    posts = MessageBoardPost.objects.filter(town=profile.town, location=location, is_hidden=False).select_related("player__user")
    case_cards = case_cards_for_location(profile, location)
    return render(
        request,
        "towns/location_detail.html",
        {"profile": profile, "location": location, "form": form, "posts": posts, "case_cards": case_cards},
    )
