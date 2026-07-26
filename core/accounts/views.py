from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm, LoginForm

# Create your views here.


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("blog:post-list")


class RegisterPageView(CreateView):
    template_name = "accounts/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")
