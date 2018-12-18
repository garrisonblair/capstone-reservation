from datetime import datetime
from dateutil import parser as date_parser

from django.test import TestCase
from django.core.management import call_command

from rest_framework.test import APIRequestFactory, force_authenticate

from django.contrib.admin.models import LogEntry
from ..views.log_entry_api import LogEntryView
from django.contrib.auth.models import User


class TestLogEntryAPI(TestCase):

    def setUp(self):
        call_command("loaddata", "apps/accounts/fixtures/users.json")
        call_command("loaddata", "./../fixtures/LogEntry.json")

        self.factory = APIRequestFactory()

    def tearDown(self):
        pass

    def testGetAllLogEntries(self):

        request = self.factory.get("/logentries")
        force_authenticate(request, User.objects.get(username="admin"))
        response = LogEntryView.as_view()(request)

        # retrieved all LogEntries
        self.assertEqual(len(response.data), LogEntry.objects.all().count())

    def testFilterByStartDate(self):
        start_datetime = datetime(2018, 11, 23)

        request = self.factory.get("/logentries", {"from": str(start_datetime)})
        force_authenticate(request, User.objects.get(username="admin"))
        response = LogEntryView.as_view()(request)

        for log_entry in response.data:
            log_entry_time = date_parser.parse(log_entry["action_time"], dayfirst=True)  # type: datetime
            log_entry_time = log_entry_time.replace(tzinfo=None)
            self.assertGreaterEqual(log_entry_time, start_datetime)

    def testFilterByEndDate(self):
        end_datetime = datetime(2018, 11, 23)

        request = self.factory.get("/logentries", {"to": str(end_datetime)})
        force_authenticate(request, User.objects.get(username="admin"))
        response = LogEntryView.as_view()(request)

        for log_entry in response.data:
            log_entry_time = date_parser.parse(log_entry["action_time"], dayfirst=True)  # type: datetime
            log_entry_time = log_entry_time.replace(tzinfo=None)
            self.assertLessEqual(log_entry_time, end_datetime)

    def testFilterByContentType(self):
        request = self.factory.get("/logentries", {"content_type_id": 2})
        force_authenticate(request, User.objects.get(username="admin"))
        response = LogEntryView.as_view()(request)

        for log_entry in response.data:
            self.assertEqual(log_entry["content_type"]["id"], 2)

    def testFilterByObjectID(self):
        request = self.factory.get("/logentries", {"object_id": 3})
        force_authenticate(request, User.objects.get(username="admin"))
        response = LogEntryView.as_view()(request)

        for log_entry in response.data:
            self.assertEqual(log_entry["object_id"], "3")

    def testFilterByUserID(self):
        request = self.factory.get("/logentries", {"user_id": 3})
        force_authenticate(request, User.objects.get(username="admin"))
        response = LogEntryView.as_view()(request)

        for log_entry in response.data:
            self.assertEqual(log_entry["user"]["id"], 3)
