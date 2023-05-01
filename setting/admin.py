from django.contrib import admin

from setting.models import Setting


class SettingList(admin.ModelAdmin):
    list_display = ('get_setting_username', 'setting_name', 'auto_save', 'auto_run', 'auto_format')

    def get_setting_username(self, obj):
        return obj.user.username

    get_setting_username.short_description = 'User'


admin.site.register(Setting, SettingList)
