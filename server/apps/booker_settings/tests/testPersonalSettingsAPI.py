from apps.rooms.models.Room import Room
from apps.booking.views.booking import BookingCreate

from django.test.testcases import TestCase
from django.contrib.auth.models import User

from rest_framework.test import force_authenticate, APIRequestFactory

from apps.booker_settings.models.PersonSettings import PersonSettings


class PersonSettingsAPITest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.booker = User.objects.create_user(username='booker',
                                               email='booker@booker.com',
                                               password='booker')
        self.booker.save()

        self.admin = User.objects.create_user(username="admin",
                                              is_superuser=True)

        self.admin.save()
