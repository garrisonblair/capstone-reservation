from django.core.exceptions import ValidationError
from django.core import serializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.rooms.models.Room import Room


class RoomView(APIView):

    def get(self, request):

        data = serializers.serialize("json", Room.objects.all())

        try:
            return Response(data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)
