"""
Audit Log Signals - Secure Task Manager
=======================================
This module contains Django signals for automatic audit logging.

OWASP ASVS V7 Compliance:
- Automatically logs authentication events
- Captures failed login attempts for security monitoring
- Records IP addresses for forensic analysis
- No sensitive data logged (passwords, tokens)

Usage:
    These signals are automatically connected when the app is ready.
    See auditlog/apps.py for signal registration.
"""

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .models import AuditLog


@receiver(user_logged_in)
def log_successful_login(sender, user, request, **kwargs):
    """
    Log successful login attempts.
    
    Captures:
    - User who logged in
    - Client IP address
    - User agent (browser info)
    
    Security:
    - Helps identify legitimate access patterns
    - Enables detection of account takeover
    """
    AuditLog.objects.create(
        user=user,
        action='LOGIN_SUCCESS',
        ip_address=request.META.get('REMOTE_ADDR'),
        details=f"Successful login via {request.META.get('HTTP_USER_AGENT', 'unknown')}"
    )


@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    """
    Log failed login attempts.
    
    Captures:
    - Attempted username (not password - security)
    - Client IP address
    
    Security:
    - Enables brute force detection
    - Supports rate limiting decisions
    - No password logged (OWASP compliance)
    """
    # SECURITY: Only log username, never the password
    username = credentials.get('username', 'unknown')
    AuditLog.objects.create(
        user=None,  # No user for failed attempts
        action='LOGIN_FAILED',
        ip_address=request.META.get('REMOTE_ADDR'),
        details=f"Failed login attempt for username: '{username}'"
    )


@receiver(user_logged_out)
def log_logout(sender, user, request, **kwargs):
    """
    Log user logout events.
    
    Captures:
    - User who logged out
    - Client IP address
    
    Security:
    - Helps verify session termination
    - Supports compliance auditing
    """
    AuditLog.objects.create(
        user=user,
        action='LOGOUT',
        ip_address=request.META.get('REMOTE_ADDR'),
        details="User logged out"
    )
