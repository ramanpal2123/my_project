from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display  = ('title', 'user', 'priority', 'completed', 'created_at')
    list_filter   = ('priority', 'completed')
    search_fields = ('title', 'user__username')