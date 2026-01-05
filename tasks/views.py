from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from .models import Task
from auditlog.models import AuditLog  # <-- Added for logging


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(owner=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'status', 'due_date']
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)

        # Log task creation
        AuditLog.objects.create(
            user=self.request.user,
            action='TASK_CREATE',
            details=f"Created task: '{self.object.title}' (ID: {self.object.id})"
        )
        return response


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'status', 'due_date']
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.owner or self.request.user.is_staff

    def form_valid(self, form):
        response = super().form_valid(form)

        # Log task update
        AuditLog.objects.create(
            user=self.request.user,
            action='TASK_UPDATE',
            details=f"Updated task: '{self.object.title}' (ID: {self.object.id})"
        )
        return response


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.owner or self.request.user.is_staff

    def form_valid(self, form):
        task_title = self.object.title
        task_id = self.object.id
        response = super().form_valid(form)

        # Log task deletion
        AuditLog.objects.create(
            user=self.request.user,
            action='TASK_DELETE',
            details=f"Deleted task: '{task_title}' (ID: {task_id})"
        )
        return response
    
    
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from auditlog.models import AuditLog

@method_decorator(staff_member_required, name='dispatch')
class AuditLogListView(LoginRequiredMixin, ListView):
    model = AuditLog
    template_name = 'auditlog/audit_log.html'
    context_object_name = 'logs'
    paginate_by = 25
    ordering = ['-timestamp']