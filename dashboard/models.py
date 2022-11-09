from django.db import models

# Create your models here.
from codepen.functions import upload_path
from user.models import User


class Media(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_title = models.CharField(max_length=100, null=False, blank=False)
    file_description = models.TextField()
    file_name = models.CharField(max_length=100, null=False, blank=False)
    file_url = models.FileField(null=False, blank=False, upload_to=upload_path, unique=True, max_length=200)
    file_size = models.BigIntegerField(null=False, blank=False)
    mime_type = models.CharField(max_length=100, null=False, blank=False)
    uploaded_date = models.DateTimeField(auto_now=True)
    uploaded_modified = models.DateTimeField(auto_now_add=True)
