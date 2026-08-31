from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import Profile

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


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "name@example.com",
                "autofocus": True,
            }
        ),
    )

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter your password",
            }
        ),
    )


class UserEditForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        help_text="Leave blank if you do not want to change your password.",
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "email",
        ]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "last_name",
            "image",
        ]