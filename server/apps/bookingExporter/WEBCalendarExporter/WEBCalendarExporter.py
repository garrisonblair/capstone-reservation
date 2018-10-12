import requests as r

from ..BookingExporter import BookingExporter
from .ICSSerializer import ICSSerializer


class WEBCalendarExporter(BookingExporter):

    def __init__(self):
        self.__init__(r, ICSSerializer())

    def __init__(self, request_module, ics_serializer):
        self.requests = request_module
        self.serializer = ics_serializer
        self.logged_in = False

    def login(self):
        pass

    def export_file(self, file_content):
        pass

    #BookingExporter
    # TODO: Investigate if using threads here could improve performance
    def backup_booking(self, booking):
        if not self.logged_in:
            self.login()

        ics_file_content = self.serializer.serializeBooking(booking)

        self.export_file(ics_file_content)

    # ClassObserver

    def subject_saved(self, subject):
        self.backup_booking(subject)

    def subject_updated(self, subject):
        self.backup_booking(subject)

    def subject_deleted(self, subject):
        pass
