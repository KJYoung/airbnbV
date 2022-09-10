import os
import requests
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.core.files.base import ContentFile
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins


class LoginView(mixins.AnnonymousOnlyView, FormView):
    template_name: str = "users/login.html"
    form_class = forms.LoginForm
    # success_url = reverse_lazy("core:home")
    # initial = {"email": "jykim157@snu.ac.kr"}
    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Welcome back {user.first_name}!")
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    messages.info(request, f"Logged out successfully.")
    return redirect(reverse("core:home"))


class SignUpView(mixins.AnnonymousOnlyView, FormView):
    template_name: str = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    # initial = {
    #     "first_name": "Junyoung",
    #     "last_name": "Kim",
    #     "email": "jy@na.com",
    # }

    def form_valid(self, form):
        form.save()

        # new_user login
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.email_verification()
        return super().form_valid(form)


def complete_verification(request, email_key):
    try:
        user = models.User.objects.get(email_key=email_key)
        user.email_verified = True
        user.email_key = ""
        user.save()
        # TODO.. Add Success msg.
    except models.User.DoesNotExist:
        pass  # TODO.. Some times.. Error msg.
    return redirect(reverse("core:home"))


class EditProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = "users/edit_profile.html"
    fields = (
        "first_name",
        "last_name",
        "avatar",
        "gender",
        "bio",
        "birth",
        "language",
        "currency",
    )
    success_message = "Profile updated successfully!"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["birth"].widget.attrs = {"placeholder": "Birthdate"}
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last name"}
        return form

    def form_valid(self, form):
        # I will not allow email modification.
        # email = form.cleaned_data.get("email")
        # self.object.username = email
        # self.object.save()
        return super().form_valid(form)


class UpdatePassword(
    mixins.EmailUserOnlyView,
    mixins.LoggedInOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):
    template_name = "users/change_password.html"
    success_message = "Password changed successfully!"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current Passoword"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New Password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "New Password Again"
        }
        return form

    def get_success_url(self) -> str:
        return self.request.user.get_absolute_url()


class GithubException(Exception):
    pass


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback/"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


def github_callback(request):
    try:
        callback_code = request.GET.get("code")
        client_id = os.environ.get("GH_ID")
        client_pw = os.environ.get("GH_SECRET")
        if callback_code is not None:
            access_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_pw}&code={callback_code}",
                headers={"Accept": "application/json"},
            )
            result_json = access_request.json()
            error = result_json.get("error", None)
            if error is not None:
                raise GithubException("Error with authorization.")
            else:
                access_token = result_json.get("access_token")
                progile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = progile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    bio = "" if bio is None else bio
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method == models.User.LOGIN_GITHUB:
                            # trying to login.
                            login(request, user)
                            messages.success(
                                request, f"Welcome back {user.first_name}!"
                            )
                        else:
                            raise GithubException(
                                f"Please log in with: {user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        new_user = models.User.objects.create(
                            username=email,
                            first_name=name,
                            bio=bio,
                            email=email,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        new_user.set_unusable_password()
                        new_user.save()
                        login(request, new_user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Username is None.")
        else:
            raise GithubException("Callback_code is None.")
    except GithubException as e:
        messages.error(request, str(e))
        return redirect(reverse("users:login"))
    except:
        print("UnknownException")
        return redirect(reverse("users:login"))


class KakaoException(Exception):
    pass


def kakao_login(request):
    rest_api_key = os.environ.get("KAKAO_KEY")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback/"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
    )


def kakao_callback(request):
    try:
        rest_api_key = os.environ.get("KAKAO_KEY")
        kakao_admin_key = os.environ.get("KAKAO_ADMIN_KEY")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback/"
        code = request.GET.get("code")
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}",
            headers={"Content-type": "application/x-www-form-urlencoded;charset=utf-8"},
        )
        response_json = token_request.json()
        error = response_json.get("error", None)
        if error is not None:
            raise KakaoException("Error with authorization.")
        else:
            access_token = response_json.get("access_token")
            profile_request = requests.get(
                f"https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            profile_json = profile_request.json()
            kakao_account = profile_json.get("kakao_account")
            properties = profile_json.get("properties")

            has_email = kakao_account.get("has_email")
            if has_email:
                email = kakao_account.get("email", None)
                if email is None:
                    raise KakaoException("Please give us the email.")
            else:
                # email = "no_email_kakao@kakao.error"
                raise KakaoException("Please give us the email.")

            nickname = properties.get("nickname")
            profile_image = properties.get("profile_image", None)

            try:
                user = models.User.objects.get(email=email)
                if user.login_method == models.User.LOGIN_KAKAO:
                    # trying to login.
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}!")
                else:
                    raise KakaoException(f"Please log in with: {user.login_method}")

            except models.User.DoesNotExist:
                new_user = models.User.objects.create(
                    username=email,
                    first_name=nickname,
                    email=email,
                    login_method=models.User.LOGIN_KAKAO,
                    email_verified=True,
                )
                new_user.set_unusable_password()
                new_user.save()
                if profile_image is not None and profile_image != "":
                    photo_request = requests.get(profile_image)
                    email_wo_at = email.replace("@", "_")
                    new_user.avatar.save(
                        f"{email_wo_at}-avatar.jpg", ContentFile(photo_request.content)
                    )
                    new_user.save()
                login(request, new_user)
            return redirect(reverse("core:home"))
    except KakaoException as e:
        # print(f"KakaoException. MSG : {str(e)}")
        messages.error(request, str(e))
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    model = models.User
    context_object_name = "user_profile"
