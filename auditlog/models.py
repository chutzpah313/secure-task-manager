"""
Audit Log Model - Secure Task Manager
=====================================
This module defines the AuditLog model for security monitoring and compliance.

OWASP ASVS V7 Compliance:
- Logs authentication events (login success/failure, logout)
- Logs data modification events (CRUD operations)
- Captures IP addresses for forensic analysis
- No sensitive data in logs (passwords, tokens)
"""

from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):
    """
    Audit log entry for security monitoring.
    
    Tracks:
    - Authentication events (login, logout, failed attempts)
    - Task CRUD operations
    - User actions with timestamps
    - Client IP addresses
    
    Security:
    - SET_NULL on user deletion preserves log integrity
    - No sensitive data stored (passwords, tokens, etc.)
    - Ordered by timestamp for chronological analysis
    """
    
    # Action type choices for categorization
    ACTION_CHOICES = [
        ('LOGIN_SUCCESS', 'Login Success'),
        ('LOGIN_FAILED', 'Login Failed'),
        ('LOGOUT', 'Logout'),
        ('TASK_CREATE', 'Task Created'),
        ('TASK_UPDATE', 'Task Updated'),
        ('TASK_DELETE', 'Task Deleted'),
    ]

    # SECURITY: SET_NULL preserves audit trail even if user is deleted
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User who performed the action (null for failed logins)"
    )
    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
        help_text="Type of action performed"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="When the action occurred"
    )
    details = models.TextField(
        blank=True,
        help_text="Additional details (no sensitive data)"
    )
    # SECURITY: IP address for forensic analysis
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="Client IP address"
    )

    def __str__(self):
        """String representation for admin and debugging."""
        username = self.user.username if self.user else 'Anonymous'
        return f"{self.timestamp} - {username} - {self.action}"

    class Meta:
        ordering = ['-timestamp']  # Most recent first
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
