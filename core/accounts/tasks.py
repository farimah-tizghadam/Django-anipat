from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_welcome_email(email, first_name):
    send_mail(
        subject="Welcome!",
        message=f"Hello {first_name}, welcome to our website!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
