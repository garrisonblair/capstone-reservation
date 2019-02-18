from rest_framework.views import View

from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from apps.accounts.permissions.IsSuperUser import IsSuperUser
from apps.booking.models.Booking import Booking
from apps.card_reader.models.card_reader import CardReader
from apps.card_reader.serializers.card_reader import ReadCardReaderSerializer, WriteCardReaderSerializer
from apps.system_administration.models.system_settings import SystemSettings
from datetime import datetime

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

            settings = SystemSettings.get_settings()

            data = request.data
            secret_key = data['secret_key']
            card_reader = CardReader.objects.get(secret_key=secret_key)
            room = card_reader.room
            # TODO: Figure out best way to get booker based on studentID
            booker = User.objects.get(pk=pk)

            if settings.check_for_expired_bookings_active is False or secret_key != self.secret_key:
                return
            else:
                # Required parameters to find bookings for a booker/room/card-reader combination for a specific day
                today = datetime.date.today()
                now = datetime.datetime.now()

                # Get all bookings for room corresponding to the card reader for current day and booker who scans card
                bookings = Booking.objects.filter(room=room, booker=booker, date=today)

                # Filter out bookings to find current booking in case user has multiple bookings in same room in one day
                # Ensures booking start is before current time, booking end and booking expiration are after current time
                for booking in bookings:
                    if (booking.end_time > now > booking.start_time) and booking.expiration > now:
                        booking.set_to_confirmed()

        except ValidationError as e:
            return Response(e.message, status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
