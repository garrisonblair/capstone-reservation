from django.test import TestCase
from django.core.management import call_command


class TestLogEntryAPI(TestCase):

    def setUp(self):
        call_command("loaddata", "apps/accounts/fixtures/users.json")
        call_command("loaddata", "./../fixtures/LogEntry.json")
        pass

    def tearDown(self):
        pass

    def test1(self):
        self.assertTrue(True)
