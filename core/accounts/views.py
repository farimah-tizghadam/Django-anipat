from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views import View

from .forms import CustomUserCreationForm, LoginForm
from .tasks import send_activation_email
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse

from django.contrib import messages
from django.contrib.auth import get_user_model

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from accounts.forms import (
    UserEditForm, 
    ProfileEditForm, 
    PasswordChangeCustomForm,
    ResendActivationForm,
)
from .models import Profile

# Create your views here.

# getting custom user
User = get_user_model()


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CustomLoginView(LoginView):
    """
    a custom login view with a decorator to ensure that a view sets a CSRF cookie
    """

    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse("blog:post-list")


class RegisterPageView(CreateView):
    """
    a class for register user and generates uid and token, pass them to
    the existed task then sends activation/verification email
    """

    template_name = "accounts/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        activation_path = reverse(
            "accounts:activate",
            kwargs={"uidb64": uid, "token": token},
        )

        activation_url = self.request.build_absolute_uri(activation_path)

        send_activation_email.delay(
            user.email,
            activation_url,
        )
        messages.success(self.request, "activation/verification email has been sent.")

        self.object = user
        return redirect(self.success_url)


class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("accounts:login")


def activate_account(request, uidb64, token):
    """
    Activates a user's account by validating the user ID and activation token.
    If valid, marks the user as active and verified, then redirects to login.
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_verified = True
        user.save(update_fields=["is_active", "is_verified"])

        messages.success(
            request, "Your account has been activated. You can now log in."
        )

        messages.error(request, "The activation link is invalid or has expired.")

        return redirect("accounts:login")

    messages.error(
        request,
        "This activation link is invalid or has expired. "
        "Please request a new activation email.",
    )

    return redirect("accounts:resend-activation")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_profile(self):
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["user_form"] = UserEditForm(instance=self.request.user)

        context["profile_form"] = ProfileEditForm(instance=self.get_profile())

        context["password_form"] = PasswordChangeCustomForm()

        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        profile = self.get_profile()

        user_form = UserEditForm(
            request.POST,
            instance=user,
        )

        profile_form = ProfileEditForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        password_form = PasswordChangeCustomForm(request.POST)

        if "change_password" in request.POST:

            if password_form.is_valid():

                current_password = password_form.cleaned_data["current_password"]

                new_password = password_form.cleaned_data["new_password1"]

                if not user.check_password(current_password):

                    password_form.add_error(
                        "current_password",
                        "Your current password is incorrect.",
                    )

                else:
                    user.set_password(new_password)
                    user.save()

                    update_session_auth_hash(
                        request,
                        user,
                    )

                    messages.success(
                        request,
                        "Your password was changed successfully.",
                    )

                    return redirect("accounts:profile")

        elif "save_profile" in request.POST:

            if user_form.is_valid() and profile_form.is_valid():

                user_form.save()
                profile_form.save()

                messages.success(
                    request,
                    "Profile edited successfully.",
                )

                return redirect("accounts:profile")

        context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "password_form": password_form,
        }

        return self.render_to_response(context)


def resend_activation(request):
    if request.method == "POST":
        form = ResendActivationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                user = None

            if user is not None and not user.is_active:

                uid = urlsafe_base64_encode(
                    force_bytes(user.pk)
                )

                token = default_token_generator.make_token(user)

                activation_path = reverse(
                    "accounts:activate",
                    kwargs={
                        "uidb64": uid,
                        "token": token,
                    },
                )

                activation_url = request.build_absolute_uri(
                    activation_path
                )

                send_activation_email.delay(
                    user.email,
                    activation_url,
                )

            messages.success(
                request,
                "If an inactive account exists with that email address, "
                "a new activation link has been sent.",
            )

            return redirect("accounts:login")

    else:
        form = ResendActivationForm()

    return render(
        request,
        "accounts/resend_activation.html",
        {
            "form": form,
        },
    )