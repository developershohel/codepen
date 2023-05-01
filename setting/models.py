from django.db import models

from user.models import User


class Setting(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    setting_name = models.CharField(max_length=100, blank=False, null=False)
    auto_run = models.BooleanField(blank=True, null=True, default=False)
    auto_save = models.BooleanField(blank=True, null=True, default=False)
    auto_format = models.BooleanField(blank=True, null=True, default=False)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} {self.setting_name} {self.auto_run} {self.auto_save}'
