from django.db import models

from apps.accounts.models.Booker import Booker
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.util.AbstractBooker import AbstractBooker


class Group(models.Model, AbstractBooker):
    name = models.CharField(max_length=50)
    bookers = models.ManyToManyField(Booker)
    is_verified = models.BooleanField(default=False)

    privilege_category = models.ForeignKey(PrivilegeCategory, null=True, on_delete=models.SET_NULL)

    def get_privileges(self):
        return self.privilege_category
