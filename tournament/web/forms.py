from django import forms
from tournament.models import Tournament


class TournamentForm(forms.ModelForm):
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date", "class": "form-input"}))
    time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time", "class": "form-input", "step": "60"}))

    class Meta:
        model = Tournament
        fields = ["name", "sport", "description", "nb_teams", "nb_players_per_team", "location"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input", "x-model": "name"}),
            "sport": forms.HiddenInput(attrs={"x-model": "sport"}),
            "description": forms.Textarea(attrs={"class": "form-input leading-relaxed", "rows": 3}),
            "location": forms.TextInput(attrs={"class": "form-input"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")

        if date and time:
            import datetime

            from django.utils import timezone

            combined_datetime = timezone.make_aware(datetime.datetime.combine(date, time))
            cleaned_data["datetime"] = combined_datetime

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.datetime = self.cleaned_data.get("datetime")
        if commit:
            instance.save()
        return instance
