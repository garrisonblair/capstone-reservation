from django.test import TestCase
from uuid import uuid4

from apps.card_reader.models.card_reader import CardReader


class TestCardReader(TestCase):

    def testCreateCardReader(self):
        card_reader = CardReader()

        self.assertTrue(card_reader.secret_key is not None)
