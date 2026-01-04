from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'due_date', 'created_at')
    list_filter = ('status', 'owner')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)

admin.site.register(Task, TaskAdmin)