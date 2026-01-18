"""
Task Model - Secure Task Manager
================================
This module defines the Task model for the task management application.

Security Features:
- Owner-based access control (ForeignKey to User)
- No direct object references exposed
- Uses Django ORM for SQL injection prevention
"""

from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """
    Task model representing a user's task.
    
    Attributes:
        title: Task title (max 200 characters)
        description: Optional detailed description
        status: Current status (TODO, IN_PROGRESS, DONE)
        due_date: Optional deadline
        owner: Foreign key to User (for RBAC)
        created_at: Auto-set creation timestamp
    
    Security:
        - Owner field ensures tasks belong to specific users
        - CASCADE deletion prevents orphaned records
    """
    
    # Status choices for dropdown validation
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]
    
    title = models.CharField(
        max_length=200,
        help_text="Task title (required)"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional task description"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='TODO',
        help_text="Current task status"
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        help_text="Optional due date"
    )
    # SECURITY: ForeignKey ensures owner-based access control
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        help_text="Task owner (for access control)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Auto-set creation timestamp"
    )

    def __str__(self):
        """String representation for admin and debugging."""
        return f"{self.title} - {self.owner.username}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
