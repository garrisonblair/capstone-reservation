from django.db import models

from apps.accounts.models.Booker import Booker
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory


class Group(models.Model):
    name = models.CharField(max_length=50)
    bookers = models.ManyToManyField(Booker)
    is_verified = models.BooleanField(default=False)

    privilege_category = models.ForeignKey(PrivilegeCategory, blank=True, null=True, on_delete=models.SET_NULL)
