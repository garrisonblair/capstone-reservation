from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status

from apps.accounts.models.User import User
from apps.card_reader.models.card_reader import CardReader
from apps.rooms.models.Room import Room

from apps.card_reader.views.card_reader import CardReaderCreateView, CardReaderDeleteView, ListCardReaders


class TestCardReaderManagementAPI(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.admin = User.objects.create(username="admin", is_superuser=True)
        self.user = User.objects.create(username="regular_user")

        self.card_reader1 = CardReader()
        self.card_reader1.save()

        self.room1 = Room(name="Room 1")
        self.room1.save()

    def testListCardReader(self):
        request = self.factory.get("/card_readers")

        force_authenticate(request, self.admin)
        response = ListCardReaders.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        card_reader = response.data[0]

        self.assertEqual(card_reader["id"], self.card_reader1.id)
        self.assertEqual(card_reader["room"], None)
        self.assertEqual(card_reader["secret_key"], str(self.card_reader1.secret_key))

    def testCreateCardReader(self):
        request = self.factory.post("/card_reader",
                                    {
                                        "room": self.room1.id
                                    })

        force_authenticate(request, self.admin)
        response = CardReaderCreateView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_reader = CardReader.objects.all().filter(room=self.room1.id)[0]

        self.assertEqual(created_reader.room, self.room1)

    def testDeleteCardReader(self):
        request = self.factory.delete("/card_reader/" + str(self.card_reader1.id) + "/delete")

        force_authenticate(request, self.admin)
        response = CardReaderDeleteView.as_view()(request, pk=self.card_reader1.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        try:
            CardReader.objects.get(id=self.card_reader1.id)
        except CardReader.DoesNotExist:
            self.assertTrue(True)
            return

        self.fail()

    def testOnlyAdminCanAccessList(self):
        request = self.factory.get("/card_readers")

        force_authenticate(request, self.user)
        response = ListCardReaders.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def testOnlyAdminCanCreate(self):
        request = self.factory.post("/card_reader",
                                    {
                                        "room": self.room1.id
                                    })

        force_authenticate(request, self.user)
        response = CardReaderCreateView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def testOnlyAdminCanDelete(self):
        request = self.factory.delete("/card_reader/" + str(self.card_reader1.id) + "/delete")

        force_authenticate(request, self.user)
        response = CardReaderDeleteView.as_view()(request, pk=self.card_reader1.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
