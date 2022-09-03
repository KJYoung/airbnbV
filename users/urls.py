from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/github/", views.github_login, name="github_login"),
    path("login/github/callback/", views.github_callback, name="github_callback"),
    path("login/kakao/", views.github_login, name="kakao_login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path(
        "verify/<str:email_key>",
        views.complete_verification,
        name="complete_verification",
    ),
]
