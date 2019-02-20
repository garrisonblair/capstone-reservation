import datetime
from django.db import models
from rest_framework.exceptions import ValidationError
import pdb

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
        best_result = datetime.timedelta()
        for i in range(0, room_bookings_for_range.count() - 1):
            range_end = room_bookings_for_range[i + 1].start_time
            range_start = room_bookings_for_range[i].end_time
            free = datetime.datetime.combine(self.date, range_end) - datetime.datetime.combine(self.date, range_start)
            # pdb.set_trace()
            if free >= self.minimum_booking_time and free >= best_result:
                best_result = free
                start = range_start
                end = range_end
        if best_result == datetime.timedelta():
            return False
        return start, end
