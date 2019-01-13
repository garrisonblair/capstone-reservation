from django.contrib.auth.models import User as DjangoUser
from apps.util.AbstractBooker import AbstractBooker

from apps.accounts.models.PrivilegeCategory import PrivilegeMerger


class User(DjangoUser, AbstractBooker):

    class Meta:
        proxy = True

    @staticmethod
    def cast_django_user(django_user):
        return User.objects.get(id=django_user.id)

    def get_privileges(self):

        if self.bookerprofile.privilege_categories.all().count() is 0:
            return None

        return PrivilegeMerger(list(self.bookerprofile.privilege_categories.all()))

    def get_bookings(self):
        return self.booking_set
