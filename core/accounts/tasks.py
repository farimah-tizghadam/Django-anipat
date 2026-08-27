from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_activation_email(email, name, activation_url):
    send_mail(
        "accounts/email/activate_account.tpl",
        {
            "name": name,
            "activation_url": activation_url,
        },
        from_email=None,
        recipient_list=[email],
    )