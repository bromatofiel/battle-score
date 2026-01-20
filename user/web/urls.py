from django.urls import path
from user.web.views import HomeView, LoginView, LogoutView, SignupView, DashboardView, AccountSettingsView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("settings/", AccountSettingsView.as_view(), name="settings"),
]
