from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views import View

from .forms import CustomUserCreationForm, LoginForm
from .tasks import send_activation_email
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse

from django.contrib import messages
from django.contrib.auth import get_user_model

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
        return reverse_lazy("blog:post-list")

    def get_redirect_url(self):
        return ""


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
            user.first_name,
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

        return redirect("accounts:login")

    messages.error(request, "The activation link is invalid or has expired.")

    return redirect("accounts:login")
