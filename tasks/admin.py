from django.contrib import admin

from tasks.models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'status', 'owner', "created_at", "updated_at")
    list_filter = ('status',)
    actions = ['mark_archived']
    def mark_archived(self, request, queryset):
        queryset.update(status='ARCHIVED')
    mark_archived.short_description = 'Mark selected tasks as archived'

# admin.site.register(Task, TaskAdmin)
