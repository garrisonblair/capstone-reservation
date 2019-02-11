from django.test import TestCase
from apps.booking.models.Announcement import Announcement
from apps.rooms.models.Room import Room
from datetime import datetime, time, timedelta

from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.core.exceptions import ValidationError
from django.core.management import call_command

from apps.system_administration.models.system_settings import SystemSettings
from apps.accounts.models.User import User
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.accounts.exceptions import PrivilegeError

from apps.booking.views.announcement import AnnouncementCreate


class AnnouncementAPITest(TestCase):
    def setUp(self):

        # Setup an admin
        self.factory = APIRequestFactory()
        self. admin = User.objects.create_user(username="admin",
                                               is_superuser=True)
        self.admin.save()

        # Setup a regular booker
        self.normal_user = User.objects.create_user(username='user',
                                                    email='user@user.com',
                                                    password='user')
        self.normal_user.save()

        # Setup one Date
        self.today = datetime.now().date()
        self.tomorrow = datetime.now().date() + timedelta(days=1)
        self.title = "New Announment"
        self.content = "hello world"

    def testAnnouncementCreateSuccessful(self):
        request = self.factory.post("/announcement", {
                                        "title": self.title,
                                        "content": self.content,
                                        "begin_date": self.today,
                                        "end_date": self.tomorrow
                                    }, format="json")
        force_authenticate(request, user=self.admin)
        response = AnnouncementCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 1)
        created_ann = anns[0]
        self.assertEqual(created_ann.title, self.title)
        self.assertEqual(created_ann.content, self.content)
        self.assertEqual(created_ann.begin_date, self.today)
        self.assertEqual(created_ann.end_date, self.tomorrow)

    def testAnnouncementAPICreaationBeginDateLaterThanEndDate(self):
        request = self.factory.post("/announcement", {
                                        "title": self.title,
                                        "content": self.content,
                                        "begin_date": self.tomorrow,
                                        "end_date": self.today
                                    }, format="json")
        force_authenticate(request, user=self.admin)
        response = AnnouncementCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 0)

    def testAnnouncementAPICreateWithNormalUser(self):
        request = self.factory.post("/announcement", {
                                        "title": self.title,
                                        "content": self.content,
                                        "begin_date": self.tomorrow,
                                        "end_date": self.today
                                    }, format="json")
        force_authenticate(request, user=self.normal_user)
        response = AnnouncementCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 0)
