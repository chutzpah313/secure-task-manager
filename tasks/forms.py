"""
Task Forms - Secure Task Manager
================================
This module contains Django forms for task management.

OWASP Security Controls:
- Input validation (A03:2021 - Injection Prevention)
- XSS prevention via Django's automatic template escaping
- CSRF protection via Django middleware
- Form field whitelisting (only specified fields accepted)
"""

from django import forms
from django.utils import timezone
from .models import Task


class TaskForm(forms.ModelForm):
    """
    Form for creating and updating tasks.
    
    Security Features:
    - Only whitelisted fields are accepted (title, description, status, due_date)
    - Owner field is NOT included - prevents users from assigning to others
    - ModelForm validates against model constraints
    - Django templates auto-escape all rendered values
    
    OWASP Compliance:
    - A03:2021 (Injection): ORM handles SQL escaping
    - A07:2021 (XSS): Template auto-escaping enabled
    """
    
    class Meta:
        model = Task
        # SECURITY: Only allow these specific fields
        # The 'owner' field is NOT included to prevent unauthorized task assignment
        fields = ['title', 'description', 'status', 'due_date']
        
        # Custom widgets for better UX and consistent styling
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '200',
                'placeholder': 'Enter task title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter task description (optional)'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
    
    def clean_title(self):
        """
        Validate and sanitize the title field.
        
        Security:
        - Strips leading/trailing whitespace
        - Django auto-escapes on output (XSS prevention)
        """
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 1:
            raise forms.ValidationError("Title cannot be empty.")
        return title

    def clean_due_date(self):
        """
        Validate the due date field.
        
        Validation:
        - Due date cannot be in the past
        - Allows empty/null due dates (optional field)
        """
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now().date():
            raise forms.ValidationError("Date already passed. Please select today or a future date.")
        return due_date
