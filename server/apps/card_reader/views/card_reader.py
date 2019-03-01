from rest_framework.views import View

from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from apps.accounts.models.User import User
from apps.accounts.permissions.IsSuperUser import IsSuperUser
from apps.booking.models.Booking import Booking
from apps.card_reader.models.card_reader import CardReader
from apps.card_reader.serializers.card_reader import ReadCardReaderSerializer, WriteCardReaderSerializer
from apps.system_administration.models.system_settings import SystemSettings
import datetime

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
    permission_classes = ()

    def post(self, request):
        try:

            settings = SystemSettings.get_settings()

            data = request.data
            secret_key = data['device_id']
            student_id = data['card_id']

            card_reader = CardReader.objects.get(secret_key=secret_key)
            room = card_reader.room

            booker = User.objects.get(bookerprofile__booker_id=student_id)

            if not settings.check_for_expired_bookings_active:
                return
            else:
                # Required parameters to find bookings for a booker/room/card-reader combination for a specific day
                today = datetime.date.today()
                now = datetime.datetime.now()

                # Get all bookings for room corresponding to the card reader for current day and booker who scans card
                bookings = Booking.objects.filter(room=room, booker=booker, date=today)

                # Filter out bookings to find current booking in case user has multiple bookings in same room in one day
                # Ensures booking start is before current time, booking end / booking expiration are after current time
                for booking in bookings:
                    if (booking.end_time > now > booking.start_time) and booking.get_expiration() > now:
                        booking.set_to_confirmed()

                    if settings.campons_refutable and booking.confirmed:
                        for campon in booking.campons:
                            campon.delete()

        except ValidationError as e:
            return Response(e.message, status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
