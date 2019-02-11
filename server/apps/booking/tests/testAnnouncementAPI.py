import json
from django.test import TestCase
from apps.booking.models.Announcement import Announcement
from datetime import datetime, timedelta
from django.contrib.admin.models import LogEntry, ContentType, ADDITION, CHANGE, DELETION

from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.test import Client

from apps.accounts.models.User import User
from apps.booking.serializers.announcement import AnnouncementSerializer

from apps.booking.views.announcement import AnnouncementCreate, AnnouncementDelete, AnnouncementUpdate, AnnouncementList


class AnnouncementAPITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        client = Client()

        # Setup an admin
        self. admin = User.objects.create_user(username="admin",
                                               password="admin",
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

        # LogEntry test
        latest_log = LogEntry.objects.last()  # type: LogEntry
        self.assertEqual(latest_log.action_flag, ADDITION)
        self.assertEqual(latest_log.object_id, str(created_ann.id))
        self.assertEqual(latest_log.user, self.admin)
        self.assertEqual(latest_log.object_repr, json.dumps(AnnouncementSerializer(created_ann).data))

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

    def testAnnouncementAPIDeleteSuccessful(self):

        announcement = Announcement(title=self.title,
                                    content=self.content,
                                    begin_date=self.today,
                                    end_date=self.tomorrow)
        announcement.save()

        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 1)
        request = self.factory.delete("/announcement", {}, format="json")
        force_authenticate(request, user=self.admin)
        response = AnnouncementDelete.as_view()(request, 1)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 0)

        # LogEntry test
        latest_log = LogEntry.objects.last()  # type: LogEntry
        self.assertEqual(latest_log.action_flag, DELETION)
        self.assertEqual(latest_log.object_id, "1")
        self.assertEqual(latest_log.user, self.admin)

    def testAnnouncementAPIDeleteWithNormalUser(self):

        announcement = Announcement(title=self.title,
                                    content=self.content,
                                    begin_date=self.today,
                                    end_date=self.tomorrow)
        announcement.save()

        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 1)
        request = self.factory.delete("/announcement", {}, format="json")
        force_authenticate(request, user=self.normal_user)
        response = AnnouncementDelete.as_view()(request, 1)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 1)

    def testAnnouncementAPIDeleteWithId9999(self):

        announcement = Announcement(title=self.title,
                                    content=self.content,
                                    begin_date=self.today,
                                    end_date=self.tomorrow)
        announcement.save()

        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 1)
        request = self.factory.delete("/announcement", {}, format="json")
        force_authenticate(request, user=self.admin)
        response = AnnouncementDelete.as_view()(request, 9999)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 1)

    def testAnnouncementAPIUpdateSuccessful(self):

        announcement = Announcement(title=self.title,
                                    content=self.content,
                                    begin_date=self.today,
                                    end_date=self.tomorrow)
        announcement.save()

        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 1)

        request = self.factory.patch("/announcement", {
                                        "title": self.title,
                                        "content": "new content",
                                        "begin_date": self.today,
                                        "end_date": self.tomorrow
                                    }, format="json")
        force_authenticate(request, user=self.admin)
        response = AnnouncementUpdate.as_view()(request, 1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 1)

        ann = anns[0]
        self.assertEqual(ann.title, self.title)
        self.assertEqual(ann.content, "new content")
        self.assertEqual(ann.begin_date, self.today)
        self.assertEqual(ann.end_date, self.tomorrow)

        # LogEntry test
        latest_log = LogEntry.objects.last()  # type: LogEntry
        self.assertEqual(latest_log.action_flag, CHANGE)
        self.assertEqual(latest_log.object_id, str(ann.id))
        self.assertEqual(latest_log.user, self.admin)
        self.assertEqual(latest_log.object_repr, json.dumps(AnnouncementSerializer(ann).data))

    def testAnnouncementAPIUpdateBeginDatelaterThanEndDate(self):

        announcement = Announcement(title=self.title,
                                    content=self.content,
                                    begin_date=self.today,
                                    end_date=self.tomorrow)
        announcement.save()

        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 1)

        request = self.factory.patch("/announcement", {
                                        "title": self.title,
                                        "content": "new content",
                                        "begin_date": self.tomorrow,
                                        "end_date": self.today
                                    }, format="json")
        force_authenticate(request, user=self.admin)
        response = AnnouncementUpdate.as_view()(request, 1)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 1)

        ann = anns[0]
        self.assertEqual(ann.title, self.title)
        self.assertEqual(ann.content, self.content)
        self.assertEqual(ann.begin_date, self.today)
        self.assertEqual(ann.end_date, self.tomorrow)

    def testAnnouncementAPIUpdateForbiddenUser(self):

        announcement = Announcement(title=self.title,
                                    content=self.content,
                                    begin_date=self.today,
                                    end_date=self.tomorrow)
        announcement.save()

        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 1)

        request = self.factory.patch("/announcement", {
                                        "title": self.title,
                                        "content": "new content",
                                        "begin_date": self.today,
                                        "end_date": self.tomorrow
                                    }, format="json")
        force_authenticate(request, user=self.normal_user)
        response = AnnouncementUpdate.as_view()(request, 1)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 1)

        ann = anns[0]
        self.assertEqual(ann.title, self.title)
        self.assertEqual(ann.content, self.content)
        self.assertEqual(ann.begin_date, self.today)
        self.assertEqual(ann.end_date, self.tomorrow)

    def testAnnouncementAPIUpdateWithIdNotFound(self):

        announcement = Announcement(title=self.title,
                                    content=self.content,
                                    begin_date=self.today,
                                    end_date=self.tomorrow)
        announcement.save()

        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 1)

        request = self.factory.patch("/announcement", {
                                        "title": self.title,
                                        "content": "new content",
                                        "begin_date": self.today,
                                        "end_date": self.tomorrow
                                    }, format="json")
        force_authenticate(request, user=self.admin)
        response = AnnouncementUpdate.as_view()(request, 9999)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 1)

        ann = anns[0]
        self.assertEqual(ann.title, self.title)
        self.assertEqual(ann.content, self.content)
        self.assertEqual(ann.begin_date, self.today)
        self.assertEqual(ann.end_date, self.tomorrow)

    def testAnnouncementAPIGetAll(self):

        announcement = Announcement(title=self.title,
                                    content=self.content,
                                    begin_date=self.today,
                                    end_date=self.tomorrow)
        announcement.save()

        announcement = Announcement(title="a2",
                                    content="new content",
                                    begin_date=self.today,
                                    end_date=self.today)
        announcement.save()

        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 2)

        request = self.factory.get("/announcement", {}, format="json")
        response = AnnouncementList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def testAnnouncementAPIGetOneDay(self):

        announcement = Announcement(title=self.title,
                                    content=self.content,
                                    begin_date=self.today,
                                    end_date=self.tomorrow)
        announcement.save()

        announcement = Announcement(title="a2",
                                    content="new content",
                                    begin_date=self.today,
                                    end_date=self.today)
        announcement.save()

        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 2)

        request = self.factory.get("/announcement", {
                                        "date": self.tomorrow
                                    }, format="json")
        response = AnnouncementList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def testAnnouncementAPIGetOneDay(self):

        announcement = Announcement(title=self.title,
                                    content=self.content,
                                    begin_date=self.today,
                                    end_date=self.tomorrow)
        announcement.save()

        announcement = Announcement(title="a2",
                                    content="new content",
                                    begin_date=self.today,
                                    end_date=self.today)
        announcement.save()

        anns = Announcement.objects.all()
        self.assertEqual(len(anns), 2)

        yesterday = datetime.now().date() - timedelta(days=1)
        request = self.factory.get("/announcement", {
                                        "date": yesterday
                                    }, format="json")
        response = AnnouncementList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def testGetAllUrl(self):
        response = self.client.get('/announcements')
        self.assertEqual(response.status_code, 200)

    def testGetADayUrl(self):
        response = self.client.get('/announcements', {'date':self.today})
        self.assertEqual(response.status_code, 200)

    def testCreateUrl(self):
        self.client.post('/login', {'username': 'admin', 'password': 'admin'})

        data = dict(
            title=self.title,
            content=self.content,
            begin_date=self.today,
            end_date=self.tomorrow
        )
        response = self.client.post('/announcement', data)
        self.assertEqual(response.status_code, 201)

    def testUpdateUrl(self):
        self.client.post('/login', {'username': 'admin', 'password': 'admin'})

        announcement = Announcement(title=self.title,
                                    content=self.content,
                                    begin_date=self.today,
                                    end_date=self.tomorrow)
        announcement.save()

        response = self.client.patch('/announcement/1',
                                {
                                    "title": self.title,
                                    "content": "new content",
                                    "begin_date": self.today,
                                    "end_date": self.tomorrow
                                }, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def testDeleteUrl(self):
        self.client.post('/login', {'username': 'admin', 'password': 'admin'})

        announcement = Announcement(title=self.title,
                                    content=self.content,
                                    begin_date=self.today,
                                    end_date=self.tomorrow)
        announcement.save()
        response = self.client.delete('/announcement/delete/1')
        self.assertEqual(response.status_code, 204)
