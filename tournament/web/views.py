import random

from core.constants import COUNTRIES
from django.contrib import messages
from django.shortcuts import redirect
from tournament.models import Team, Tournament
from django.views.generic import FormView
from tournament.web.forms import TournamentForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin


class TournamentCreateView(LoginRequiredMixin, FormView):
    template_name = "tournament/create.html"
    form_class = TournamentForm

    def form_valid(self, form):
        tournament = form.save(commit=False)
        tournament.admin = self.request.user
        tournament.save()

        # Generate initial teams
        available_names = [capital for _, capital in COUNTRIES]
        random.shuffle(available_names)

        nb_teams = form.cleaned_data.get("nb_teams")
        for i in range(1, int(nb_teams) + 1):
            team_name = available_names.pop() if available_names else f"Equipe {i}"
            Team.objects.create(tournament=tournament, name=team_name, number=i)

        messages.success(self.request, _("Tournoi créé avec succès !"))
        return redirect("dashboard")

    def form_invalid(self, form):
        messages.error(self.request, _("Veuillez corriger les erreurs ci-dessous."))
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sport_choices"] = Tournament.SPORTS
        return context
