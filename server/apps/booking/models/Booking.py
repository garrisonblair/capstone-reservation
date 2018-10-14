from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models.Student import Student
from apps.rooms.models.Room import Room
from django.db.models import Q
from django.core.exceptions import ValidationError

from apps.util.SubjectModel import SubjectModel


class Booking(models.Model, SubjectModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

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
        return 'Booking: %d, Student: %s, Room: %s, Date: %s, Start time: %s, End Time: %s' % (self.id, self.student.student_id, self.room.room_id, self.date, self.start_time, self.end_time)

    def validate_model(self):

        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be less than end time")

        if Booking.objects.filter(~Q(start_time=self.end_time), room=self.room, date=self.date, start_time__range=(self.start_time, self.end_time)).exists():
            raise ValidationError("Specified time is overlapped with other bookings.")
        elif Booking.objects.filter(~Q(end_time=self.start_time), room=self.room, date=self.date, end_time__range=(self.start_time, self.end_time)).exists():
            raise ValidationError("Specified time is overlapped with other bookings.")

    def get_observers(self):
        return Booking.observers
