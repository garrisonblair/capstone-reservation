from django.db import models

from apps.accounts.models.User import User
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.util.AbstractBooker import AbstractBooker


class Group(models.Model, AbstractBooker):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(User, blank=True)
    is_verified = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_groups", default=None)
    privilege_category = models.ForeignKey(PrivilegeCategory, blank=True, null=True, on_delete=models.SET_NULL)

    def get_privileges(self):
        return self.privilege_category

    def get_bookings(self):
        return self.booking_set

    def __str__(self):
        return str(self.name)
