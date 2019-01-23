from django.test.testcases import TestCase
from ..GmailImporter.GmailICSImporter import GmailICSImporter


class GmailImporterTest(TestCase):

    def testGmailImporter(self):
        importer = GmailICSImporter()

        print(importer.get_message_ICS_attachment('1687760a9899c4bc'))
