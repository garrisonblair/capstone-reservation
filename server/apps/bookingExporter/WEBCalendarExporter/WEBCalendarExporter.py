import requests

from ..BookingExporter import BookingExporter
from .ICSSerializer import ICSSerializer


class WEBCalendarExporter(BookingExporter):

    BASE_URL = "https://capstone.encs.concordia.ca/"
    LOGIN_URL = BASE_URL + "login.php"
    IMPORT_HANDLER_URL = BASE_URL + "import_handler.php"

    NOT_AUTHORIZED_MESSAGE = "You are not authorized"

    USERNAME = "f_daigl"
    PASSWORD = "<PUT_PASSWORD_HERE>"

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
        response = self.session.post(self.LOGIN_URL, data={"login": self.USERNAME, "password": self.PASSWORD})

        if response.status_code is not 200:
            # TODO: handle login failure
            print("login failed")
            pass

        pass

    def export_file(self, booking, file_content):

        file = {"FileName": ("booking.ics", file_content)}
        data = {"ImportType": "ICAL",
                "exc_private": "1",
                "overwrite": "Y",
                "calUser": "_NUC_LAB_H961_04"}
        response = self.session.post(self.IMPORT_HANDLER_URL, files=file, data=data)

        print(response.text)

        if self.NOT_AUTHORIZED_MESSAGE in response.text:
            # TODO: handle request failure
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

    def subject_saved(self, subject):
        self.backup_booking(subject)

    def subject_updated(self, subject):
        self.backup_booking(subject)

    def subject_deleted(self, subject):
        pass
