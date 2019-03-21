from django.contrib.auth.models import User as DjangoUser
from django.conf import settings

from apps.util.Jwt import generateToken

import apps.accounts.tasks as tasks

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

    def send_email(self, subject, message, send_to_primary=False, ics_data=None):
        recipient_list = list()
        if self.bookerprofile.secondary_email and not send_to_primary:
            recipient_list.append(self.bookerprofile.secondary_email)
        else:
            recipient_list.append(self.email)
        token = generateToken(self)
        message = message + "\n\n\nClick on link below to unsubscribe from emails\n" + "{}://{}/#/email_settings/{}".format(settings.ROOT_PROTOCOL,settings.ROOT_URL, token)
        tasks.send_email.delay(subject, message, recipient_list, ics_data)

