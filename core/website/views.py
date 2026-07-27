from django.views.generic import CreateView
from django.views.generic import TemplateView
from .models import Contact
from .forms import ContactForm
from django.contrib import messages
from django.urls import reverse_lazy


class IndexView(TemplateView):
    template_name = "website/index.html"


class AboutView(TemplateView):
    template_name = "website/about.html"


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "website/contact.html"
    success_url = reverse_lazy("website:contact")

    def form_valid(self, form):
        messages.success(self.request, "Your message has been sent successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "please correct the errors below.")
        return super().form_invalid(form)
