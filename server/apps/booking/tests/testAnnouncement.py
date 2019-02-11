from django.test import TestCase
from apps.booking.models.Announcement import Announcement
from datetime import datetime, timedelta

from django.core.exceptions import ValidationError


class TestAnnouncement(TestCase):
    def setUp(self):
        # Setup basic info for creation
        self.today = datetime.now().date()
        self.tomorrow = datetime.now().date() + timedelta(days=1)
        self.title = "New Announment"
        self.content = "hello world"

    def testAnnouncementCreation(self):
        announcement = Announcement(title=self.title,
                                    content=self.content,
                                    begin_date=self.today,
                                    end_date=self.tomorrow)
        announcement.save()
        Created_announcement = Announcement.objects.last()
        self.assertEqual(Created_announcement, announcement)
        self.assertEqual(len(Announcement.objects.all()), 1)

    def testAnnouncementCreationFailed(self):
        announcement = Announcement(title=self.title,
                                    content=self.content,
                                    begin_date=self.tomorrow,
                                    end_date=self.today)

        with self.assertRaises(ValidationError):
            announcement.save()
            print(len(Announcement.objects.all()))
            self.assertEqual(len(Announcement.objects.all()), 0)
