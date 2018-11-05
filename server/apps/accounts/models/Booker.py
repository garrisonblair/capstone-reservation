from django.db import models
from django.contrib.auth.models import User

from .PrivilegeCategory import PrivilegeCategory


class Booker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, default=None, null=True)
    booker_id = models.CharField(max_length=8, blank=False, primary_key=True)
    privilege_category = models.ForeignKey(PrivilegeCategory, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.booker_id
