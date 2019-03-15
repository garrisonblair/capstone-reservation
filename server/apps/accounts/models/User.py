from django.contrib.auth.models import User as DjangoUser
from django.core import mail
from django.conf import settings

import jwt
import time
import os

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

    def send_email(self, subject, message, send_to_primary=False):
        recipient_list = list()
        if self.bookerprofile.secondary_email and not send_to_primary:
            recipient_list.append(self.bookerprofile.secondary_email)
        else:
            recipient_list.append(self.email)
        token = self.generateToken(self)
        # TODO: create URL
        message = message + "\n\n\nClick on link below to unsubscribe from emails\n" + "{}://{}/#/email_settings/{}".format(settings.ROOT_PROTOCOL,settings.ROOT_URL, token)
        print(message)
        tasks.send_email.delay(subject, message, recipient_list)

    def generateToken(self, user):
        now = int(time.time())
        token={
            "iat": now,
            "exp": now + 10, #3600 * 2,  # 2 hours
            "user_id": user.id
        }
        secret_key = os.environ.get('SECRET_KEY')
        token = jwt.encode(token, secret_key, algorithm="HS256")

        return token

