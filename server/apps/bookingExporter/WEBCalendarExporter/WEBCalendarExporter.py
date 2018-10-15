import requests

from ..BookingExporter import BookingExporter
from .ICSSerializer import ICSSerializer

from apps.calendar_administration.models.system_settings import SystemSettings


class WEBCalendarExporter(BookingExporter):

    BASE_URL = "https://capstone.encs.concordia.ca/"
    LOGIN_URL = BASE_URL + "login.php"
    IMPORT_HANDLER_URL = BASE_URL + "import_handler.php"

    # These messages are extremely dependent on WEBCalendar, but the system should
    # not be updated during a transition phase
    LOGIN_FAILED_MESSAGE = "Error: Invalid login"
    NOT_AUTHORIZED_MESSAGE = "You are not authorized"

    def __init__(self, request_session=None, ics_serializer=None):

        if not request_session:
            request_session = requests.Session()
        self.session = request_session

        if not ics_serializer:
            ics_serializer = ICSSerializer()
        self.serializer = ics_serializer

        self.logged_in = False

    # Gets authorization Cookies
    def login(self):
        settings = SystemSettings.get_settings()
        username = settings.webcalendar_username
        password = settings.webcalendar_password

        response = self.session.post(self.LOGIN_URL, data={"login": username, "password": password})

        if self.LOGIN_FAILED_MESSAGE in response.text:
            # TODO: handle login failure (Log it)
            print("login failed")
            pass

        pass

    def export_file(self, booking, file_content):

        file = {"FileName": ("booking.ics", file_content)}
        data = {"ImportType": "ICAL",
                "exc_private": "1",
                "overwrite": "Y",
                "calUser": booking.room.externalroomid.external_id}
        response = self.session.post(self.IMPORT_HANDLER_URL, files=file, data=data)

        print(response.text)

        if self.NOT_AUTHORIZED_MESSAGE in response.text:
            # TODO: handle request failure (Log it)
            print("Not Authorized")
            pass

    # BookingExporter
    # TODO: Investigate if using threads here could improve performance
    def backup_booking(self, booking):
        if not self.logged_in:
            self.login()

        ics_file_content = self.serializer.serialize_booking(booking)
        self.export_file(booking, ics_file_content)

    # ClassObserver

    def subject_created(self, subject):
        self.backup_booking(subject)

    def subject_updated(self, subject):
        self.backup_booking(subject)

    def subject_deleted(self, subject):
        pass
