from django.urls import path
from .views import index, about, contact

app_name = "website"


urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("contact/", contact, name="contact"),
]
