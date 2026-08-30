from celery import shared_task
from django.conf import settings
from mail_templated import send_mail


@shared_task
def send_activation_email(email, name, activation_url):
    """
    this task maintenance email context
    """
    send_mail(
        "email/activation.tpl",
        {
            "name": name,
            "activation_url": activation_url,
        },
        from_email=None,
        recipient_list=[email],
    )
