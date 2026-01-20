from django.views import View
from django.contrib import messages
from user.web.forms import LoginForm, SignupForm
from django.shortcuts import render, redirect
from user.controllers import UserController
from django.contrib.auth import login, authenticate


class LoginView(View):
    template_name = "user/login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect("home")  # Correct redirect to be determined
            else:
                messages.error(request, "Email ou mot de passe invalide.")

        return render(request, self.template_name, {"form": form})


class SignupView(View):
    template_name = "user/signup.html"

    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            UserController.create_user(email=form.cleaned_data["email"], pseudo=form.cleaned_data["pseudo"], password=form.cleaned_data["password"])
            messages.success(request, "Compte créé avec succès. Vous pouvez maintenant vous connecter.")
            return redirect("login")

        return render(request, self.template_name, {"form": form})


class HomeView(View):
    template_name = "user/home.html"

    def get(self, request):
        return render(request, self.template_name)
