from django.apps import apps
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status

from apps.accounts.models.User import User
from apps.csv.views.csv import CsvView


class testCSVAPI(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='spongebob',
            email='spongebob@krustykrab.com',
            password='krabby patty'
        )
        self.user.is_superuser = True
        self.user.save()

    def tearDown(self):
        pass

    def testGetAllModels(self):
        request = self.factory.get("/csv")
        force_authenticate(request, user=self.user)
        response = CsvView.as_view()(request)
        models = apps.get_models()
        model_names = [model.__name__ for model in models]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, model_names)

    def testDownloadCSV(self):
        data = dict(
            model='User'
        )
        request = self.factory.post('/csv', data)
        force_authenticate(request, user=self.user)
        response = CsvView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
