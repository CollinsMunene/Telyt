from django.contrib import admin
from .models import Projects, Files, ProjectUsers,Profile

# Register your models here.
admin.site.register(Projects)
admin.site.register(Files)
admin.site.register(Profile)
class CurrentProjectUserView(admin.ModelAdmin):
    list_display = ('project', 'user')
admin.site.register(ProjectUsers,CurrentProjectUserView)