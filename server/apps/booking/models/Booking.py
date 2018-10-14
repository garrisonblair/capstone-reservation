from django.db import models
from apps.accounts.models.Student import Student
from apps.groups.models.StudentGroup import StudentGroup
from apps.rooms.models.Room import Room
from apps.booking.models.RecurringBooking import RecurringBooking
from django.db.models import Q
from django.core.exceptions import ValidationError


class BookingManager(models.Manager):
    def create_booking(self, student, student_group, room, date, start_time, end_time, recurring_booking):
        booking = self.create(
            student=student,
            student_group=student_group,
            room=room,
            date=date,
            start_time=start_time,
            end_time=end_time,
            recurring_booking=recurring_booking
        )

        return booking


class Booking(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    recurring_booking = models.ForeignKey(RecurringBooking, on_delete=models.CASCADE, null=True)

    objects = BookingManager()

    def save(self, *args, **kwargs):
        self.validate_model()
        super(Booking, self).save(*args, **kwargs)

    def __str__(self):
        return 'Booking: %d, Student: %s, Room: %s, Date: %s, Start time: %s, End Time: %s' % (self.id, self.student.student_id, self.room.room_id, self.date, self.start_time, self.end_time)

    def validate_model(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be less than end time")
        if Booking.objects.filter(~Q(start_time=self.end_time), room=self.room, date=self.date, start_time__range=(
                self.start_time, self.end_time)).exists():
            raise ValidationError("Specified time is overlapped with other bookings.")
        elif Booking.objects.filter(~Q(end_time=self.start_time), room=self.room, date=self.date, end_time__range=(
                self.start_time, self.end_time)).exists():
            raise ValidationError("Specified time is overlapped with other bookings.")
