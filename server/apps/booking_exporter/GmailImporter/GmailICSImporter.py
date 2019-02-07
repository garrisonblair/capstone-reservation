from __future__ import print_function
import pickle
import os.path
import base64
from ics import Calendar, Event
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


from ..models.EmailId import EmailId

from apps.accounts.models.User import User
from apps.booking.models.Booking import Booking
from apps.rooms.models.Room import Room

from apps.util import utils
from apps.util import Logging

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

logger = Logging.get_logger()


class GmailICSImporter:

    def __init__(self):

        self.service = self.get_service()

    def import_unprocessed_bookings(self):

        message_ids = self.get_unprocessed_message_ids()

        for message_id in message_ids:
            self.create_booking_from_message(message_id)

        logger.debug("ICS Webcalender bookings updated.")

    def create_booking_from_message(self, message_id):
        try:
            message = self.get_message(message_id)

            ics_file = self.get_message_ICS_attachment(message)
            room_name = self.get_room_from_message(message)
            username = self.get_username_from_message(message)

            calendar = Calendar(ics_file)
            event = calendar.events[0]  # type: Event

            start_time = event.begin.datetime.replace(tzinfo=None)
            end_time = event.end.datetime.replace(tzinfo=None)

            booker = utils.get_system_user("WebCalendar User")

            room = Room.objects.get(name=room_name)

            booking = Booking(room=room,
                              booker=booker,
                              date=start_time.date(),
                              start_time=start_time.time(),
                              end_time=end_time.time(),
                              note=username,
                              display_note=True)

            booking.save()
            utils.log_model_change(booking, utils.ADDITION)
            logger.info("Booking {} imported from ICS file.".format(booking.id))

        except Exception as error:
            logger.warn("A booking failed to import from ICS file. Error :" + str(error))

    def get_service(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'apps/booking_exporter/GmailImporter/credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('gmail', 'v1', credentials=creds)

        return service

    def list_messages(self):
        results = self.service.users().messages().list(userId='me', q="*CAPSTONE*").execute()
        return results.get('messages', [])

    def get_unprocessed_message_ids(self):
        messages = self.list_messages()

        unprocessed_messages = list()
        for message in messages:
            try:
                EmailId.objects.get(email_id=message["id"])
            except EmailId.DoesNotExist:
                unprocessed_messages.append(message["id"])
                email_id = EmailId(email_id=message["id"])
                email_id.save()

        return unprocessed_messages

    def get_message(self, id):
        response = self.service.users().messages().get(userId='me', id=id).execute()

        return response

    def get_message_ICS_attachment(self, message):

        for part in message['payload']['parts']:
            if 'filename' in part and part['filename'] == 'WebCalendar.ics':
                attachment_id = part['body']['attachmentId']
                break

        attachment = self.service.users().messages().attachments().get(userId='me', messageId=id, id=attachment_id)\
            .execute()

        file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))

        return file_data.decode('UTF-8')

    def get_room_from_message(self, message):
        body_encoded = message['payload']['parts'][0]['body']['data']
        email_text = base64.urlsafe_b64decode(body_encoded.encode('UTF-8')).decode('UTF-8')  # type: str
        first_line = email_text.split('\r')[0]
        room_name = first_line.split(' ')[1]

        return room_name

    def get_username_from_message(self, message):
        for header in message["headers"]:

            if header["name"] == "From":
                username = header["value"]

        return username
