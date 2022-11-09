import os
from django.db import models
from user.models import User
from datetime import date


def upload_path(instance, filename):
    today = date.today()
    year = str(today.strftime("%Y"))
    month = str(today.strftime("%m"))
    name = instance.user.username
    return f'users/{name}/{year}/{month}/{filename}'


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    birth = models.DateField(auto_now_add=False, auto_now=False, null=False, blank=False)
    profile_img = models.ImageField(upload_to=upload_path, null=True, blank=True)
    banner_img = models.ImageField(upload_to=upload_path, null=True, blank=True)
    bio = models.TextField(max_length=1500, null=True, blank=True)
    screen_name = models.CharField(max_length=255, blank=False, null=False)
    country = models.CharField(max_length=132, blank=False, null=False)
    address = models.CharField(max_length=255, blank=False, null=False)
    street = models.CharField(max_length=64, blank=False, null=False)
    phone = models.CharField(max_length=15, blank=False, null=False)
    organization = models.CharField(max_length=255, blank=True, null=True)
    profile_links = models.JSONField()
    profile_register = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    profile_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def username(self):
        return self.user.username

    def user_email(self):
        return self.user.email

    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def __str__(self):
        return f'{self.screen_name}'

    def delete(self, *args, **kwargs):
        self.profile_img.storage.delete(self.profile_img.name)
        self.banner_img.storage.delete(self.banner_img.name)
        super().delete(*args, **kwargs)
