from django.contrib import admin
from .models import *


class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'target_date', 'project', 'complete')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_editable = ('complete', )
    list_filter = ('title', 'target_date', 'complete')


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title', )


admin.site.register(Tasks, TasksAdmin)
admin.site.register(Projects, ProjectsAdmin)
