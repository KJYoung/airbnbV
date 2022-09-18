from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/github/", views.github_login, name="github_login"),
    path("login/github/callback/", views.github_callback, name="github_callback"),
    path("login/kakao/", views.kakao_login, name="kakao_login"),
    path("login/kakao/callback/", views.kakao_callback, name="kakao_callback"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path(
        "verify/<str:email_key>/",
        views.complete_verification,
        name="complete_verification",
    ),
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),
    path("edit-profile/", views.EditProfileView.as_view(), name="edit_profile"),
    path("password-change/", views.UpdatePassword.as_view(), name="password_change"),
    path("switch-hosting/", views.switch_hosting_mode, name="switch-hosting"),
    path("switch-lang/", views.switch_lang, name="switch-lang"),
]
