from django.db import models
from apps.accounts.models.Booker import Booker
from apps.groups.models.StudentGroup import StudentGroup
from apps.rooms.models.Room import Room
from apps.booking.models.RecurringBooking import RecurringBooking
from django.db.models import Q
from django.core.exceptions import ValidationError
import datetime

from apps.util.SubjectModel import SubjectModel


class BookingManager(models.Manager):
    def create_booking(self, booker, student_group, room, date, start_time, end_time, recurring_booking):
        booking = self.create(
            booker=booker,
            student_group=student_group,
            room=room,
            date=date,
            start_time=start_time,
            end_time=end_time,
            recurring_booking=recurring_booking
        )

        return booking


class Booking(models.Model, SubjectModel):
    booker = models.ForeignKey(Booker, on_delete=models.CASCADE)
    student_group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    recurring_booking = models.ForeignKey(RecurringBooking, on_delete=models.CASCADE, blank=True, null=True)

    objects = BookingManager()

    observers = list()

    def save(self, *args, **kwargs):
        self.validate_model()
        is_create = False
        if self.id is None:
            is_create = True

        this = super(Booking, self).save(*args, **kwargs)

        if is_create:
            self.object_created()
        else:
            self.object_updated()

        return this

    def __str__(self):
        return 'Booking: {}, Booker: {}, Room: {}, Date: {}, Start time: {}, End Time: {}'.format(
            self.id, self.booker.booker_id, self.room.room_id, self.date, self.start_time, self.end_time
        )

    def validate_model(self):
        invalid_start_time = datetime.time(8, 0)
        invalid_end_time = datetime.time(23, 0)

        if not isinstance(self.start_time, datetime.time):
            self.start_time = datetime.datetime.strptime(self.start_time, "%H:%M").time()
        if not isinstance(self.end_time, datetime.time):
            self.end_time = datetime.datetime.strptime(self.end_time, "%H:%M").time()

        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be less than end time")

        elif self.end_time < invalid_start_time:
            raise ValidationError("End time cannot be earlier than 8:00.")

        elif self.end_time > invalid_end_time:
            raise ValidationError("End time cannot be later than 23:00.")

        elif self.start_time < invalid_start_time:
            raise ValidationError("Start time cannot be earlier than 8:00.")

        elif self.start_time > invalid_end_time:
            raise ValidationError("Start time cannot be later than 23:00.")

        elif Booking.objects.filter(~Q(start_time=self.end_time),
                                    room=self.room,
                                    date=self.date,
                                    start_time__range=(self.start_time, self.end_time)).exists():
            raise ValidationError("Specified time is overlapped with other bookings.")

        elif Booking.objects.filter(~Q(end_time=self.start_time), room=self.room, date=self.date, end_time__range=(
                self.start_time, self.end_time)).exists():
            raise ValidationError("Specified time is overlapped with other bookings.")

    def get_observers(self):
        return Booking.observers
