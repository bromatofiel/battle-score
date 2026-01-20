from django import forms
from user.models import User
from django.utils.translation import gettext as _


class LoginForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "placeholder": _("votre@email.com"),
                "class": "form-input",
            }
        ),
    )
    password = forms.CharField(
        label=_("Mot de passe"),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "••••••••",
                "class": "form-input",
            }
        ),
    )


class SignupForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "placeholder": _("votre@email.com"),
                "class": "form-input",
            }
        ),
    )
    pseudo = forms.CharField(
        label=_("Pseudo"),
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Votre pseudo"),
                "class": "form-input",
            }
        ),
    )
    password = forms.CharField(
        label=_("Mot de passe"),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "••••••••",
                "class": "form-input",
            }
        ),
    )
    password_confirm = forms.CharField(
        label=_("Confirmer le mot de passe"),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "••••••••",
                "class": "form-input",
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Cet email est déjà utilisé."))
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", _("Les mots de passe ne correspondent pas."))

        return cleaned_data
