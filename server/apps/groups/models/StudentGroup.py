from django.db import models

from apps.accounts.models.Booker import Booker
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory


class StudentGroup(models.Model):
    name = models.CharField(max_length=50)
    students = models.ManyToManyField(Booker)
    is_verified = models.BooleanField(default=False)

    privilege_category = models.ForeignKey(PrivilegeCategory, on_delete=models.DO_NOTHING)
