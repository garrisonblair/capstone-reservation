from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User

from apps.accounts.models.Booker import Booker


class PrivilegeCategoriesManagerAPITest(TestCase):

    def setUp(self):

    def testCreateBookingSuccess(self):
