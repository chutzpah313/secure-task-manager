"""
Task Views - Secure Task Manager
=================================
This module contains all views for task management with OWASP security controls.

Security Features Implemented:
- Authentication: LoginRequiredMixin on all views
- Authorization: UserPassesTestMixin for owner/admin checks (RBAC)
- CSRF: Automatically handled by Django forms
- Input Validation: Django form validation
- Audit Logging: All CRUD operations logged
- No IDOR: Owner verification before access
"""

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from .models import Task
from auditlog.models import AuditLog


# =============================================================================
# AUTHENTICATION VIEWS
# =============================================================================

class CustomLoginView(LoginView):
    """
    Custom login view with security enhancements.
    
    Security:
    - CSRF protection (Django default)
    - Rate limiting via django-axes (5 attempts, 2min lockout)
    - Redirects authenticated users away from login page
    """
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class RegisterView(CreateView):
    """
    User registration view with automatic login.
    
    Security:
    - Password validation via AUTH_PASSWORD_VALIDATORS
    - CSRF protection on form
    - Auto-login after registration
    """
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        """Save user and auto-login after successful registration."""
        response = super().form_valid(form)
        # Auto-login the newly registered user
        login(self.request, self.object)
        return response


# =============================================================================
# TASK CRUD VIEWS
# =============================================================================

class TaskListView(LoginRequiredMixin, ListView):
    """
    Display list of tasks based on user role.
    
    Security (RBAC):
    - Regular users: See only their own tasks
    - Admin users (is_staff): See all tasks
    - LoginRequiredMixin: Redirects unauthenticated users to login
    """
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        """
        Filter tasks based on user role (RBAC implementation).
        
        Returns:
            QuerySet: All tasks for admin, user's tasks for regular users
        """
        if self.request.user.is_staff:
            # Admin can see all tasks
            return Task.objects.all()
        # Regular users see only their own tasks (prevents IDOR)
        return Task.objects.filter(owner=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new task with automatic owner assignment.
    
    Security:
    - LoginRequiredMixin: Must be authenticated
    - Auto-assigns owner: Prevents task creation for other users
    - Audit logging: Records task creation
    - CSRF: Protected by Django form
    """
    model = Task
    fields = ['title', 'description', 'status', 'due_date']
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        """
        Set the owner to current user and log the action.
        
        Security: Owner is set server-side, not from user input.
        """
        # SECURITY: Set owner server-side (prevents tampering)
        form.instance.owner = self.request.user
        response = super().form_valid(form)

        # AUDIT: Log task creation for security monitoring
        AuditLog.objects.create(
            user=self.request.user,
            action='TASK_CREATE',
            details=f"Created task: '{self.object.title}' (ID: {self.object.id})"
        )
        return response


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update an existing task with ownership verification.
    
    Security:
    - LoginRequiredMixin: Must be authenticated
    - UserPassesTestMixin: Verifies ownership or admin role (RBAC)
    - Prevents IDOR: Cannot edit other users' tasks
    - Audit logging: Records task updates
    """
    model = Task
    fields = ['title', 'description', 'status', 'due_date']
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def test_func(self):
        """
        RBAC check: Only owner or admin can update.
        
        Returns:
            bool: True if user is owner or admin, False otherwise
        """
        task = self.get_object()
        return self.request.user == task.owner or self.request.user.is_staff

    def form_valid(self, form):
        """Save updates and log the action."""
        response = super().form_valid(form)

        # AUDIT: Log task update
        AuditLog.objects.create(
            user=self.request.user,
            action='TASK_UPDATE',
            details=f"Updated task: '{self.object.title}' (ID: {self.object.id})"
        )
        return response


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a task with ownership verification.
    
    Security:
    - LoginRequiredMixin: Must be authenticated
    - UserPassesTestMixin: Verifies ownership or admin role (RBAC)
    - Confirmation required: Prevents accidental deletion
    - Audit logging: Records task deletion
    """
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def test_func(self):
        """
        RBAC check: Only owner or admin can delete.
        
        Returns:
            bool: True if user is owner or admin, False otherwise
        """
        task = self.get_object()
        return self.request.user == task.owner or self.request.user.is_staff

    def form_valid(self, form):
        """Capture task info before deletion for audit log."""
        # Store info before deletion
        task_title = self.object.title
        task_id = self.object.id
        response = super().form_valid(form)

        # AUDIT: Log task deletion
        AuditLog.objects.create(
            user=self.request.user,
            action='TASK_DELETE',
            details=f"Deleted task: '{task_title}' (ID: {task_id})"
        )
        return response


# =============================================================================
# USER PROFILE VIEW
# =============================================================================

class ProfileView(LoginRequiredMixin, TemplateView):
    """
    User profile page showing account info and task statistics.
    
    Security:
    - LoginRequiredMixin: Must be authenticated
    - Shows only current user's data (no IDOR)
    """
    template_name = 'tasks/profile.html'

    def get_context_data(self, **kwargs):
        """Add user statistics to context."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get only the current user's tasks (prevents IDOR)
        user_tasks = Task.objects.filter(owner=user)
        
        # Calculate task statistics
        context['total_tasks'] = user_tasks.count()
        context['todo_tasks'] = user_tasks.filter(status='TODO').count()
        context['in_progress_tasks'] = user_tasks.filter(status='IN_PROGRESS').count()
        context['done_tasks'] = user_tasks.filter(status='DONE').count()
        
        return context


# =============================================================================
# ADMIN-ONLY VIEWS
# =============================================================================

@method_decorator(staff_member_required, name='dispatch')
class AuditLogListView(LoginRequiredMixin, ListView):
    """
    Admin-only view for audit logs (OWASP ASVS V7).
    
    Security:
    - staff_member_required: Only admin users can access
    - LoginRequiredMixin: Must be authenticated
    - Paginated: Prevents memory issues with large logs
    
    Displays:
    - Login attempts (success/failed)
    - Task CRUD operations
    - User actions with timestamps and IP addresses
    """
    model = AuditLog
    template_name = 'auditlog/audit_log.html'
    context_object_name = 'logs'
    paginate_by = 25
