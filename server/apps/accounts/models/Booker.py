from django.db import models
from django.contrib.auth.models import User

from .PrivilegeCategory import PrivilegeCategory, PrivilegeMerger
from apps.util.AbstractBooker import AbstractBooker


class Booker(models.Model, AbstractBooker):

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, default=None, null=True)
    booker_id = models.CharField(max_length=8, blank=False, primary_key=True)
    privilege_categories = models.ManyToManyField(PrivilegeCategory)

    def get_privileges(self):

        if self.privilege_categories.all().count() is 0:
            return None

        return PrivilegeMerger(list(self.privilege_categories.all()))

    def __str__(self):
        return self.booker_id
