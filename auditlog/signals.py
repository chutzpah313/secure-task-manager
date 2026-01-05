from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .models import AuditLog

@receiver(user_logged_in)
def log_successful_login(sender, user, request, **kwargs):
    AuditLog.objects.create(
        user=user,
        action='LOGIN_SUCCESS',
        ip_address=request.META.get('REMOTE_ADDR'),
        details=f"Successful login via {request.META.get('HTTP_USER_AGENT', 'unknown')}"
    )

@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    username = credentials.get('username', 'unknown')
    AuditLog.objects.create(
        action='LOGIN_FAILED',
        ip_address=request.META.get('REMOTE_ADDR'),
        details=f"Failed login attempt for '{username}'"
    )

@receiver(user_logged_out)
def log_logout(sender, user, request, **kwargs):
    AuditLog.objects.create(
        user=user,
        action='LOGOUT',
        ip_address=request.META.get('REMOTE_ADDR'),
        details="User logged out"
    )