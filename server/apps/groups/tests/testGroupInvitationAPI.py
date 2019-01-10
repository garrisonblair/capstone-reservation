from django.test import TestCase

from django.contrib.auth.models import User

from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework import status

from apps.accounts.models.Booker import Booker
from ..models.GroupInvitation import GroupInvitation
from ..models.Group import Group
from ..views.group_invitations import GroupInvitationsList, AcceptInvitation, RejectInvitation, RevokeInvitation


class TestGroupInvitationAPI(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.user1 = User.objects.create_user(username="user1",
                                              email="coolemail@email.com",
                                              password='safePassw0rd',
                                              is_superuser=True)
        self.user1.save()

        self.user2 = User.objects.create_user(username="user2",
                                              email="user2@email.com",
                                              password="anotherPassword")
        self.user2.save()

        self.booker1 = Booker(booker_id="11111111")
        self.booker1.save()
        self.booker1.user = self.user1
        self.booker1.save()

        self.booker2 = Booker(booker_id="22222222")
        self.booker2.save()
        self.booker2.user = self.user2
        self.booker2.save()

        self.group = Group(name="My Group", owner=self.booker1)
        self.group.save()

        self.invitation1 = GroupInvitation(group=self.group, invited_booker=self.booker2)
        self.invitation1.save()

        self.invitation2 = GroupInvitation(group=self.group, invited_booker=self.booker1)
        self.invitation2.save()

    def testAcceptInvitationSuccess(self):

        request = self.factory.post("/group_invitation/1/accept")
        force_authenticate(request, self.user2)

        response = AcceptInvitation.as_view()(request, self.invitation1.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.booker2 in self.group.members.all())

        #  Check invitation was deleted
        try:
            self.invitation1.refresh_from_db()
        except GroupInvitation.DoesNotExist:
            self.assertTrue(True)
            return
        self.fail()

    def testAcceptInvitationForOtherUserFail(self):
        request = self.factory.post("/group_invitation/1/accept")
        force_authenticate(request, self.user1)

        response = AcceptInvitation.as_view()(request, self.invitation1.id)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def testAcceptNonExistantInvitation(self):
        request = self.factory.post("/group_invitation/3/accept")
        force_authenticate(request, self.user1)

        response = AcceptInvitation.as_view()(request, 3)

        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

    def testRejectInvitationSuccess(self):
        request = self.factory.post("/group_invitation/1/reject")
        force_authenticate(request, self.user2)

        response = RejectInvitation.as_view()(request, self.invitation1.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.booker2 not in self.group.members.all())

        #  Check invitation was deleted
        try:
            self.invitation1.refresh_from_db()
        except GroupInvitation.DoesNotExist:
            self.assertTrue(True)
            return
        self.fail()

    def testGetInvitationsAuthenticatedBooker(self):

        request = self.factory.get("/group_invitations")
        force_authenticate(request, self.user2)

        response = GroupInvitationsList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only the invitation for the authenticated booker is retrieved.

        invitation = response.data[0]
        self.assertEqual(invitation["group"]["id"], self.group.id)
        self.assertEqual(invitation["invited_booker"]["id"], self.booker2.id)

    def testGetInvitationsAuthenticatedAdmin(self):
        request = self.factory.get("/group_invitations")
        force_authenticate(request, self.user1)

        response = GroupInvitationsList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Admin can see all invitations

    def testGetInvitationsNotAuthenticated(self):
        request = self.factory.get("/group_invitations")

        response = GroupInvitationsList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def testRevokeInvitationOwner(self):
        request = self.factory.post("/group_invitation/1/revoke")
        force_authenticate(request, self.user1)

        response = RevokeInvitation.as_view()(request, self.invitation1.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.booker2 not in self.group.members.all())

        #  Check invitation was deleted
        try:
            self.invitation1.refresh_from_db()
        except GroupInvitation.DoesNotExist:
            self.assertTrue(True)
            return
        self.fail()

    def testRevokeInvitationNotOwner(self):
        request = self.factory.post("/group_invitation/1/revoke")
        force_authenticate(request, self.user2)

        response = RevokeInvitation.as_view()(request, self.invitation1.id)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(self.booker2 not in self.group.members.all())

        #  Check invitation was deleted
        try:
            self.invitation1.refresh_from_db()
        except GroupInvitation.DoesNotExist:
            self.fail()
            return
        self.assertTrue(True)
