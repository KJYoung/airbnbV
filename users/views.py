import os
import requests
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import FormView
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
