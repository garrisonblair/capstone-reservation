from __future__ import print_function
import pickle
import os.path
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from ..models.EmailId import EmailId

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailICSImporter:

    def __init__(self):

        self.service = self.get_service()

    def import_unprocessed_bookings(self):

        message_ids = self.get_unprocessed_message_ids()

        ics_files = list()

        for message_id in message_ids:
            self.create_booking_from_ics(self.get_message_ICS_attachment(message_id))

    def create_booking_from_ics(self, ics_file):
        pass

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
                EmailId.objects.get(email_id=message.id)
            except EmailId.DoesNotExist:
                unprocessed_messages.append(message.id)
                email_id = EmailId(email_id=message.id)
                email_id.save()

        return unprocessed_messages

    def get_message(self, id):
        response = self.service.users().messages().get(userId='me', id=id).execute()

        return response

    def get_message_ICS_attachment(self, id):

        message = self.get_message(id)

        for part in message['payload']['parts']:
            if 'filename' in part and part['filename'] == 'WebCalendar.ics':
                attachment_id = part['body']['attachmentId']
                break

        attachment = self.service.users().messages().attachments().get(userId='me', messageId=id, id=attachment_id)\
            .execute()

        file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
