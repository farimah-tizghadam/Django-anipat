from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views import View

from .forms import CustomUserCreationForm, LoginForm
from .tasks import send_welcome_email
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.



@method_decorator(ensure_csrf_cookie, name="dispatch")
class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("blog:post-list")

    def get_redirect_url(self):
        return ""

class RegisterPageView(CreateView):
    template_name = "accounts/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        response = super().form_valid(form)

        user = self.object

        send_welcome_email.delay(
            user.email,
            user.first_name,
        )

        return response

class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("accounts:login")