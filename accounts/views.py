from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import RegistrationForm
from .services import ensure_player_profile
from .stats import display_stats


def register(request):
    if request.user.is_authenticated:
        return redirect("town_home")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            ensure_player_profile(user)
            login(request, user)
            return redirect("town_home")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


class ProfileCreatingLoginView(LoginView):
    authentication_form = AuthenticationForm
    template_name = "accounts/login.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        ensure_player_profile(self.request.user)
        return response


login_view = ProfileCreatingLoginView.as_view()


@login_required
def account(request):
    profile = ensure_player_profile(request.user)
    return render(request, "accounts/account.html", {"profile": profile, "display_stats": display_stats(profile.stats)})
