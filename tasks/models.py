from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('TODO', 'To Do'),
            ('IN_PROGRESS', 'In Progress'),
            ('DONE', 'Done'),
        ],
        default='TODO'
    )
    due_date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.owner.username}"

    class Meta:
        ordering = ['-created_at']