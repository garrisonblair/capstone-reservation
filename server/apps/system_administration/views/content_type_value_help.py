from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.contenttypes.models import ContentType
from ..serializers.log_entry_serializer import ContentTypeSerializer


class ContentTypeValueHelp(APIView):

    exposed_models = [
        "booking",
        "campon",
        "recurringbooking",
    ]

    def get(self, request):
        content_types = ContentType.objects.filter(model__in=ContentTypeValueHelp.exposed_models)
        serializer = ContentTypeSerializer(content_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
