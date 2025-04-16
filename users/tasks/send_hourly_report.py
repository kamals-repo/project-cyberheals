from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from users.models import Role
from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()

@shared_task
def send_user_statistics_email():
    
    total_users = User.objects.count() 
    role_counts = Role.objects.values('role').annotate(count=Count('role'))
    
    counts = {
        'admin': 0,
        'manager': 0,
        'staff': 0,
    }
    for item in role_counts:
        counts[item['role']] = item['count']
    
    email_body = (
        "User Statistics:\n\n"
        f"Total Users: {total_users}\n\n"
        "Counts by Role:\n"
        f"Admin: {counts.get('admin', 0)}\n"
        f"Manager: {counts.get('manager', 0)}\n"
        f"Staff: {counts.get('staff', 0)}\n"
    )
   
    admin_roles = Role.objects.filter(role='admin').select_related('user')
    admin_emails = [role.user.email for role in admin_roles if role.user.email]

    for email in admin_emails:
        send_mail(
            subject="Hourly User Statistics Report",
            message=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )