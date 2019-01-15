from django.contrib.auth.models import User as DjangoUser
from django.core import mail
from django.conf import settings

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

    def send_email(self, subject, message, send_to_primary=False):

        recipient_list = list()
        if self.bookerprofile.secondary_email and not send_to_primary:
            recipient_list.append(self.bookerprofile.secondary_email)
        else:
            recipient_list.append(self.email)

        mail.send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
