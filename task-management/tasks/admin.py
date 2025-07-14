from django.contrib import admin

# Register your models here.

from tasks.models import Task, Employee, Project, TaskDetail


admin.site.register(Task)
admin.site.register(Employee)
admin.site.register(Project)
admin.site.register(TaskDetail)
