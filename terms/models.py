from django.db import models
from user.models import User


# Create your models here.
class Categories(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.CharField(max_length=255, null=False, blank=False)
    cats_register = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    cats_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name
