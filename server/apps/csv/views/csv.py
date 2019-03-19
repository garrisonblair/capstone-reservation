import csv
from django.apps import apps
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions.IsSuperUser import IsSuperUser


class CsvView(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)

    def get(self, request):
        models = apps.get_models()
        response = [model.__name__ for model in models]
        return Response(response)

    def post(self, request):
        model = ''
        if 'model' in request.data:
            model = request.data['model']
        models = apps.get_models()
        model_instance = [instance for instance in models if instance.__name__ == model][0]
        meta = model_instance._meta
        fields = [field.name for field in meta.fields]  # CSV headers

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(model)

        writer = csv.writer(response)
        writer.writerow(fields)

        for instance in model_instance.objects.all():
            row = [getattr(instance, field) for field in fields]
            writer.writerow(row)
        return response
