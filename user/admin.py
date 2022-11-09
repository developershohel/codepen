from django.contrib import admin
from .models import User, UserLogs


# Register your models here.
class UserList(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'is_superuser', 'is_staff', 'user_status', 'user_modified')


admin.site.register(User, UserList)
admin.site.register(UserLogs)
