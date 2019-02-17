from rest_framework.views import View

from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from apps.accounts.permissions.IsSuperUser import IsSuperUser
from apps.card_reader.models.card_reader import CardReader
from apps.card_reader.serializers.card_reader import ReadCardReaderSerializer, WriteCardReaderSerializer

from django.core.exceptions import ValidationError


class ListCardReaders(ListAPIView):

    queryset = CardReader.objects.all()
    permission_classes = (IsSuperUser,)
    serializer_class = ReadCardReaderSerializer

    def get_queryset(self):

        qs = CardReader.objects.all()

        room = self.request.GET.get('room')
        if room:
            qs = qs.filter(room=room)

        return qs


class CardReaderCreateView(CreateAPIView):

    permission_classes = (IsSuperUser,)
    serializer_class = WriteCardReaderSerializer


class CardReaderUpdateView(UpdateAPIView):
    queryset = CardReader.objects.all()
    permission_classes = (IsSuperUser,)
    serializer_class = WriteCardReaderSerializer


class CardReaderDeleteView(DestroyAPIView):

    queryset = CardReader.objects.all()
    permission_classes = (IsSuperUser,)
    serializer_class = WriteCardReaderSerializer


class CardReaderConfirmBookingView(APIView):

    def post(self, request, pk):
        try:
            CardReader.confirm_booking(self, request, pk)
        except ValidationError as e:
            return Response(e.message, status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
