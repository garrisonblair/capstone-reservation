import datetime

from django.test.testcases import TestCase
from apps.groups.models.PrivilegeRequest import PrivilegeRequest
from apps.groups.models.Group import Group
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.accounts.models.User import User
from apps.util.mock_datetime import mock_datetime


class PrivilegeRequestTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="f_daigl")
        self.owner.save()

        self.category = PrivilegeCategory(name="Category")
        self.category.save(bypass_validation=True)

        self.group = Group(name="Queen", is_verified=False, owner=self.owner)
        self.group.save()
        self.group.members.add(self.owner)
        self.group.save()

    def testPrivilegeRequestCreation(self):
        request = PrivilegeRequest(group=self.group, privilege_category=self.category)
        with mock_datetime(datetime.datetime(2018, 1, 1, 12, 30, 0, 0), datetime):
            request.save()

        self.assertEqual(PrivilegeRequest.objects.count(), 1)
        self.assertEqual(request.group, self.group)
        self.assertEqual(request.privilege_category, self.category)
        self.assertEqual(request.submission_date, datetime.date(2018, 1, 1))
        self.assertEqual(request.status, "Pending")
