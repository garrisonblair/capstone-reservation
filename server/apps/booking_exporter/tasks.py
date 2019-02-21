from celery import shared_task

from .GmailImporter.GmailICSImporter import GmailICSImporter


@shared_task
def importGmailICSFiles():
    importer = GmailICSImporter()
    importer.import_unprocessed_bookings()
