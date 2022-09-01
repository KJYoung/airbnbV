from django import forms
from . import models


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     try:
    #         user = models.User.objects.get(username=email)
    #         return email
    #     except models.User.DoesNotExist:
    #         raise forms.ValidationError("Username(Email) does not exist.")

    # def clean_password(self):
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")
    #     try:
    #         user = models.User.objects.get(username=email)
    #         if user.check_password(password):
    #             return password
    #         else:
    #             raise forms.ValidationError("Wrong password.")
    #     except models.User.DoesNotExist:
    #         pass

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Wrong password."))
        except models.User.DoesNotExist:
            self.add_error(
                "email", forms.ValidationError("Username(Email) does not exist.")
            )


class SignUpForm(forms.Form):
    email = forms.EmailField()

    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=60)

    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password"
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            user = models.User.objects.get(email=email)
            raise forms.ValidationError("Email is already used.")
        except models.User.DoesNotExist:
            return email

    def clean_password_confirm(self):
        password_confirm = self.cleaned_data.get("password_confirm")
        password = self.cleaned_data.get("password")

        if password != password_confirm:
            raise forms.ValidationError("Two password are not same.")
        else:
            return password

    def save(self):
        email = self.cleaned_data.get("email")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        password = self.cleaned_data.get("password")

        new_user = models.User.objects.create_user(
            email, email=email, password=password
        )
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()
