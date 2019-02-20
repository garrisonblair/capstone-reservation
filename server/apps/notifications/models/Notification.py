import datetime
from django.db import models
from rest_framework.exceptions import ValidationError

from apps.accounts.models.User import User
from apps.rooms.models.Room import Room


class Notification(models.Model):
    booker = models.ForeignKey(User, on_delete=models.CASCADE)  # type: User
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
            start_time__lte=self.range_end, end_time__gte=self.range_start).order_by('start_time')
        return room_bookings_for_range

    def check_room_availability(self, room):
        room_bookings_for_range = self.get_room_bookings_for_range(room)
        best_result = datetime.timedelta()
        start = None
        end = None
        for i in range(0, room_bookings_for_range.count() - 1):
            range_end = room_bookings_for_range[i + 1].start_time
            range_start = room_bookings_for_range[i].end_time
            free = datetime.datetime.combine(self.date, range_end) - datetime.datetime.combine(self.date, range_start)
            if free >= self.minimum_booking_time and free >= best_result:
                best_result = free
                start = range_start
                end = range_end
        if best_result == datetime.timedelta():
            return False
        return start, end

    def check_all_room_availability(self):
        best_room = None
        best_start = self.range_end
        best_end = self.range_start
        for room in self.rooms.all():
            result = self.check_room_availability(room)
            if not result:
                continue

            start = result[0]
            end = result[1]
            current = datetime.datetime.combine(self.date, end) - datetime.datetime.combine(self.date, start)
            best = datetime.datetime.combine(self.date, best_end) - datetime.datetime.combine(self.date, best_start)

            if current > best:
                best_room = room
                best_start = start
                best_end = end

        if best_room is None:
            return False
        return best_room, best_start, best_end
