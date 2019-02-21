import datetime
from django.db import models
from rest_framework.exceptions import ValidationError

from apps.accounts.models.User import User
from apps.rooms.models.Room import Room


class NotificationManager(models.Manager):
    def notify(self, date, room):
        notifications_for_date = self.filter(date=date)
        for notification in notifications_for_date:
            notification.check_and_notify(room)


class Notification(models.Model):
    booker = models.ForeignKey(User, on_delete=models.CASCADE)  # type: User
    rooms = models.ManyToManyField(to=Room, related_name='notifications')
    date = models.DateField()
    range_start = models.TimeField()
    range_end = models.TimeField()
    minimum_booking_time = models.DurationField()

    objects = NotificationManager()

    def save(self, *args, **kwargs):
        self.validate_model()
        this = super(Notification, self).save(*args, **kwargs)
        return this

    def validate_model(self):
        if self.range_start >= self.range_end:
            raise ValidationError("Start of range must be before end of range")
        start = datetime.datetime.combine(self.date, self.range_start)
        end = datetime.datetime.combine(self.date, self.range_end)
        range_duration = end - start
        if range_duration < self.minimum_booking_time:
            raise ValidationError("Minimum booking duration can not be longer than duration range")

    def get_room_bookings_for_range(self, room):
        room_bookings_for_range = room.get_bookings(start_date=self.date, end_date=self.date).filter(
            start_time__lte=self.range_end, end_time__gte=self.range_start).order_by('start_time')
        return room_bookings_for_range

    def check_room_availability(self, room):
        room_bookings_for_range = self.get_room_bookings_for_range(room)
        best_result = datetime.timedelta()
        start = None
        end = None
        # For each slot with no bookings, check if it is longer than the minimum range required to book
        for i in range(0, room_bookings_for_range.count() - 1):
            range_end = room_bookings_for_range[i + 1].start_time
            range_start = room_bookings_for_range[i].end_time
            free = datetime.datetime.combine(self.date, range_end) - datetime.datetime.combine(self.date, range_start)
            # If there are multiple solutions, we take the longest one
            if free >= self.minimum_booking_time and free >= best_result:
                best_result = free
                start = range_start
                end = range_end
        if best_result == datetime.timedelta():
            return False
        available = dict()
        available["start_time"] = start
        available["end_time"] = end
        return available

    def check_all_room_availability(self):
        best_room = None
        best_start = self.range_end
        best_end = self.range_start
        # For each room we check if it has an available slot
        # If there is more than one room with a slot, we take the one with the longest slot
        for room in self.rooms.all():
            result = self.check_room_availability(room)
            if not result:
                continue

            start = result["start_time"]
            end = result["end_time"]
            current = datetime.datetime.combine(self.date, end) - datetime.datetime.combine(self.date, start)
            best = datetime.datetime.combine(self.date, best_end) - datetime.datetime.combine(self.date, best_start)

            if current > best:
                best_room = room
                best_start = start
                best_end = end

        if best_room is None:
            return False

        available_room = dict()
        available_room["room"] = best_room.id
        available_room["start_time"] = best_start
        available_room["end_time"] = best_end

        return available_room

    def check_and_notify(self, room):
        if room not in self.rooms.all():
            return

        result = self.check_room_availability(room)
        if not result:
            return

        start_time = result["start_time"]
        end_time = result["end_time"]
        subject = "Room available to book!"
        message = "Hello {}!\n" \
                  "Room {} has become available to book on {} from to {} to {}.\n" \
                  "Visit the calendar to make a booking.".format(self.booker.username,
                                                                 room.name,
                                                                 self.date.strftime("%A, %B %d %Y"),
                                                                 start_time.strftime("%H:%M"),
                                                                 end_time.strftime("%H:%M")
                                                                 )
        self.booker.send_email(subject, message)
