from django.db import models
from django.contrib.auth.models import User

from .PrivilegeCategory import PrivilegeCategory


class Booker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, default=None, null=True)
    booker_id = models.CharField(max_length=8, blank=False, primary_key=True)
    privilege_category = models.ForeignKey(PrivilegeCategory, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.booker_id
