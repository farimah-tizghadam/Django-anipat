from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

# get user model object
User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    creating custom user form
    """

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class LoginForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        required=True,
    )

    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        required=True,
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(
                self.request,
                email=email,
                password=password,
            )

            if self.user_cache is None:
                raise forms.ValidationError(_("Invalid email or password."))

            if not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))

        return cleaned_data

    def get_user(self):
        return self.user_cache
