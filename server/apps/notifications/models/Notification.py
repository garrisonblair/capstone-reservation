import datetime
from django.db import models
from rest_framework.exceptions import ValidationError

from apps.rooms.models.Room import Room


class Notification(models.Model):
    rooms = models.ManyToManyField(to=Room, related_name='notifications')
    date = models.DateField()
    range_start = models.TimeField()
    range_end = models.TimeField()
    minimum_booking_time = models.DurationField()

    def save(self, *args, **kwargs):
        self.validate_model()
        this = super(Notification, self).save(*args, **kwargs)
        return this

    def validate_model(self):
        if self.range_start >= self.range_end:
            raise ValidationError("Start of range must be before end of range")

    def get_room_bookings_for_range(self, room):
        room_bookings_for_range = room.get_bookings(start_date=self.date, end_date=self.date).filter(
            start_time__lt=self.range_end, end_time__gt=self.range_start).order_by('start_time')
        return room_bookings_for_range

    def check_room_availability(self, room):
        room_bookings_for_range = self.get_room_bookings_for_range(room)
        for i in range(0, room_bookings_for_range.count()):
            start = room_bookings_for_range[i+1].start_time
            end = room_bookings_for_range[i].end_time
            available_range = end - start
            if available_range >= self.minimum_booking_time:
                return start, end
        return False
