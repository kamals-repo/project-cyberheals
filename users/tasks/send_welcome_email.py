from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

@shared_task
def send_welcome_email(user_id):
    User = get_user_model()
    user = User.objects.get(id=user_id)
    send_mail(
        subject="Welcome to Cyber Heals!",
        message=f"Hi {user.username}, welcome to Cyber Heals!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
