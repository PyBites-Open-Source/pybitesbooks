from django.contrib import admin

from .models import UserList


class UserListAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')


admin.site.register(UserList, UserListAdmin)
