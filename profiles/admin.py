from django.contrib import admin
from profiles.models import Profile


class ProfileList(admin.ModelAdmin):
    list_display = ('username', 'user_email', 'full_name', 'screen_name')


admin.site.register(Profile, ProfileList)
