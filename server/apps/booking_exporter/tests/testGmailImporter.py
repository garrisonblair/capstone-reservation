from django.test.testcases import TestCase
from ..GmailImporter.GmailICSImporter import GmailICSImporter


class GmailImporterTest(TestCase):

    def testGmailImporter(self):
        importer = GmailICSImporter()

        # print(importer.get_message_ICS_attachment('16877e6911c03044'))
