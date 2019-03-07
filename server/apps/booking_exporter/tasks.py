from celery import shared_task

from .GmailImporter.GmailICSImporter import GmailICSImporter


@shared_task
def importGmailICSFiles():
    importer = GmailICSImporter()
    importer.import_unprocessed_bookings()


@shared_task
def exportICSFile(booking_id):
    from .WEBCalendarExporter.WEBCalendarExporter import WEBCalendarExporter
    from apps.booking.models.Booking import Booking

    exporter = WEBCalendarExporter()
    booking = Booking.objects.get(pk=booking_id)
    exporter.backup_booking(booking)
