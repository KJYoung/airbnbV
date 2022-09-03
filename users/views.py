import os
import requests
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import FormView
from django.core.files.base import ContentFile
from django.contrib.auth.forms import UserCreationForm
from . import forms, models


class LoginView(FormView):
    template_name: str = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    initial = {"email": "jykim157@snu.ac.kr"}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


# class LoginView(View):
#     def get(self, request):
#         form = forms.LoginForm(initial={"email": "jykim157@snu.ac.kr"})
#         return render(request, "users/login.html", {"form": form})

#     def post(self, request):
#         form = forms.LoginForm(request.POST)

#         # Validation.
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse("core:home"))
#         else:
#             print("is not valid")
#         return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name: str = "users/signup.html"
    form_class = forms.SignUpForm
    # form_class = UserCreationForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "Junyoung",
        "last_name": "Kim",
        "email": "jy@na.com",
    }

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


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback/"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


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
                raise GithubException("There was an error.")
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
                        else:
                            raise GithubException(
                                f"The email [{email}] is already used."
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
        print(f"GithubException. MSG : {str(e)}")
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
            raise KakaoException("There was an error with token_request.")
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
                    raise KakaoException("You should check the email options.")
            else:
                # email = "no_email_kakao@kakao.error"
                raise KakaoException("You should check the email options.")

            nickname = properties.get("nickname")
            profile_image = properties.get("profile_image", None)

            try:
                user = models.User.objects.get(email=email)
                if user.login_method == models.User.LOGIN_KAKAO:
                    # trying to login.
                    login(request, user)
                else:
                    raise KakaoException(f"The email [{email}] is already used.")

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
        print(f"KakaoException. MSG : {str(e)}")
        return redirect(reverse("users:login"))


# json 버전 {'access_token': 'dw6ihvYs0xfHd72ki8Pfs00KGQP7H_2UWMfBV_cpCj11WwAAAYMDW8uE', 'token_type': 'bearer', 'refresh_token': 'MzwzwfY41RdrWxeLX-w-mPKn77Ca0j1TDY4jLlT-Cj11WwAAAYMDW8uD', 'expires_in': 21599, 'scope': 'account_email profile_image profile_nickname', 'refresh_token_expires_in': 5183999}
# json 버전
temp = {
    "id": 2415334006,
    "connected_at": "2022-09-03T12:38:11Z",
    "properties": {
        "nickname": "김준영",
        "profile_image": "http://k.kakaocdn.net/dn/eN6TtK/btrGDLWw99Q/hYWJmqH3np4IDZveAuu3ok/img_640x640.jpg",
        "thumbnail_image": "http://k.kakaocdn.net/dn/eN6TtK/btrGDLWw99Q/hYWJmqH3np4IDZveAuu3ok/img_110x110.jpg",
    },
    "kakao_account": {
        "profile_nickname_needs_agreement": False,
        "profile_image_needs_agreement": False,
        "profile": {
            "nickname": "김준영",
            "thumbnail_image_url": "http://k.kakaocdn.net/dn/eN6TtK/btrGDLWw99Q/hYWJmqH3np4IDZveAuu3ok/img_110x110.jpg",
            "profile_image_url": "http://k.kakaocdn.net/dn/eN6TtK/btrGDLWw99Q/hYWJmqH3np4IDZveAuu3ok/img_640x640.jpg",
            "is_default_image": False,
        },
        "has_email": True,
        "email_needs_agreement": False,
        "is_email_valid": True,
        "is_email_verified": True,
        "email": "jykim157@naver.com",
    },
}
