from django.db import models


class SettingStatus(models.Model):
    setting_name = models.CharField(max_length=100, null=False, blank=False)
    field_name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    field_status = models.BooleanField()
