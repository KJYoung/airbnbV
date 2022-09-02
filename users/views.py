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
