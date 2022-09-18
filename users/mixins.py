from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy
from django.contrib import messages


class AnnonymousOnlyView(UserPassesTestMixin):
    permission_denied_message = "Page not found"

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, _("Can't go there!"))
        return redirect(reverse("core:home"))


class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")

    def test_func(self):
        return self.request.user.is_authenticated


class EmailUserOnlyView(UserPassesTestMixin):
    permission_denied_message = "Page not found"

    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, _("Can't go there!"))
        return redirect(reverse("core:home"))
