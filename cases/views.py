from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.services import ensure_player_profile
from towns.models import Location
from turns.services import NotEnoughActions

from .models import Case, PlayerClue
from .services import (
    CaseLocked,
    CaseUnavailableAtThisTime,
    InvalidCaseResolution,
    WrongLocation,
    advance_case,
    available_case_action,
    case_card_for_player,
    case_cards_for_player,
    case_journal_for_player,
    get_or_start_case,
)


@login_required
def case_list(request):
    profile = ensure_player_profile(request.user)
    case_cards = case_cards_for_player(profile)
    return render(request, "cases/list.html", {"case_cards": case_cards, "profile": profile})


@login_required
def case_detail(request, case_id):
    profile = ensure_player_profile(request.user)
    case = get_object_or_404(Case, id=case_id, town=profile.town)
    card = case_card_for_player(profile, case)
    progress = card["progress"]
    if card["is_available"]:
        progress = get_or_start_case(profile, case)
    action = available_case_action(progress) if progress is not None else card["action"]
    clues = PlayerClue.objects.filter(player=profile, clue__case=case).select_related("clue")
    return render(
        request,
        "cases/detail.html",
        {"case": case, "progress": progress, "action": action, "clues": clues, "profile": profile, "card": card},
    )


@login_required
def advance_case_view(request, case_id):
    if request.method != "POST":
        return redirect("case_detail", case_id=case_id)
    profile = ensure_player_profile(request.user)
    case = get_object_or_404(Case, id=case_id, town=profile.town)
    location = None
    location_slug = request.POST.get("location_slug")
    if location_slug:
        location = get_object_or_404(Location, town=profile.town, slug=location_slug)
    try:
        _progress, clue = advance_case(
            profile,
            case,
            location=location,
            completion_key=request.POST.get("completion_key"),
        )
    except (CaseLocked, CaseUnavailableAtThisTime, InvalidCaseResolution, NotEnoughActions, WrongLocation) as exc:
        messages.error(request, str(exc))
    else:
        if clue:
            messages.success(request, f"New clue: {clue.title}")
    if location is not None:
        return redirect("location_detail", slug=location.slug)
    return redirect("case_detail", case_id=case.id)


@login_required
def clue_journal(request):
    profile = ensure_player_profile(request.user)
    case_records = case_journal_for_player(profile)
    clues = PlayerClue.objects.filter(player=profile).select_related("clue", "clue__case")
    return render(request, "cases/journal.html", {"case_records": case_records, "clues": clues, "profile": profile})
