from celery import shared_task
from django.conf import settings
from mail_templated import send_mail


@shared_task
def send_activation_email(email, activation_url):
    """
    Send account activation email.
    """
    send_mail(
        "email/activation.tpl",
        {
            "email": email,
            "activation_url": activation_url,
        },
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
