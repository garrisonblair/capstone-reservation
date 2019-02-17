import datetime

from django.db import models
from uuid import uuid4

from apps.rooms.models.Room import Room
from apps.booking.models.Booking import Booking
from apps.system_administration.models.system_settings import SystemSettings


class CardReader(models.Model):

    secret_key = models.UUIDField(default=uuid4)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def confirm_booking(self, secret_key_param, student_id_param):

        settings = SystemSettings.get_settings()

        if settings.check_for_expired_bookings_active is False or secret_key_param != self.secret_key:
            return
        else:
            # Required parameters to find bookings for a booker/room/card-reader combination for a specific day
            booker = student_id_param
            today = datetime.date.today()
            now = datetime.datetime.now()

            # Get all bookings for room corresponding to the card reader for current day and booker who scans card
            bookings = Booking.objects.filter(room=self.room, booker=booker, date=today)

            # Filter out bookings to find current booking in case user has multiple bookings in same room in one day
            # Ensures booking start is before current time, booking end and booking expiration are after current time
            for booking in bookings:
                if (booking.end_time > now > booking.start_time) and booking.expiration > now:
                    booking.set_to_confirmed()
