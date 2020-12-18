from django.contrib import admin

from todoapp.models import Task


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
    # list_display = ['username', 'email']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass

