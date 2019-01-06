from django.test import TestCase

from django.contrib.auth.models import User

from apps.accounts.models.Booker import Booker
from ..models.GroupInvitation import GroupInvitation
from ..models.Group import Group


class TestGroupInvitationAPI(TestCase):

    def setUp(self):

        self.user1 = User.objects.create_user(username="user1",
                                              email="coolemail@email.com",
                                              password='safePassw0rd')

        self.user1.save()

        self.user2 = User.objects.create_user(username="user2",
                                              email="user2@email.com",
                                              password='anotherPassword')
        self.user2.save()
