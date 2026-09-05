from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import Profile
from django.contrib.auth.password_validation import validate_password

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

    def clean(self):
        print("CUSTOM LOGIN CLEAN IS RUNNING")

        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if email and password:
            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                user = None

            if user is not None and not user.is_active:
                if user.check_password(password):
                    raise forms.ValidationError(
                        _(
                            "Your account is not activated yet. "
                            "Please check your email and click the activation link."
                        ),
                        code="inactive",
                    )

        return super().clean()


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "email",
        ]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "image",
        ]


class PasswordChangeCustomForm(forms.Form):
    current_password = forms.CharField(
        label="Current password",
        widget=forms.PasswordInput,
    )

    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput,
    )

    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput,
    )

    def clean_new_password1(self):
        password = self.cleaned_data["new_password1"]

        validate_password(password)

        return password

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            self.add_error(
                "new_password2",
                "The two passwords do not match.",
            )

        return cleaned_data


class ResendActivationForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "name@example.com",
                "class": "form-control",
            }
        ),
    )
