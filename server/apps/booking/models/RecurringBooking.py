from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from apps.rooms.models.Room import Room
from apps.accounts.models.Student import Student
from apps.groups.models.StudentGroup import StudentGroup
from datetime import timedelta


class RecurringBookingManager(models.Manager):
    def create_recurring_booking(self, start_date, end_date, start_time, end_time, room, student_group, student):
        recurring_booking = self.create(
            start_date=start_date,
            end_date=end_date,
            booking_start_time=start_time,
            booking_end_time=end_time,
            room=room,
            student_group=student_group,
            student=student
        )

        from . import Booking
        date = recurring_booking.start_date
        while date <= recurring_booking.end_date:
            booking = Booking.objects.create_booking(
                student=recurring_booking.student,
                student_group=recurring_booking.student_group,
                room=recurring_booking.room,
                date=date,
                start_time=recurring_booking.booking_start_time,
                end_time=recurring_booking.booking_end_time,
                recurring_booking=recurring_booking
            )
            recurring_booking.booking_set.add(booking)
            date += timedelta(days=7)

        return recurring_booking


class RecurringBooking(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    booking_start_time = models.TimeField()
    booking_end_time = models.TimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    student_group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    objects = RecurringBookingManager()

    def save(self, *args, **kwargs):
        self.validate_model()
        super(RecurringBooking, self).save(*args, **kwargs)

    def validate_model(self):
        if not self.student_group.is_verified:
            raise ValidationError("You must book as part of a verified group to create a recurring booking")
        elif self.start_date >= self.end_date:
            raise ValidationError("Start date can not be after End date.")
        elif self.end_date < self.start_date + timedelta(days=7):
            raise ValidationError("You must book for at least two consecutive weeks.")
        elif self.booking_start_time >= self.booking_end_time:
            raise ValidationError("Start time can not be after End time.")
        else:
            from . import Booking
            date = self.start_date
            while date <= self.end_date:
                if Booking.objects.filter(~Q(start_time=self.booking_end_time), room=self.room, date=date,
                                          start_time__range=(self.booking_start_time, self.booking_end_time)).exists():
                    raise ValidationError("Recurring booking at specified time overlaps with another booking.")
                elif Booking.objects.filter(~Q(end_time=self.booking_start_time), room=self.room, date=date,
                                            end_time__range=(self.booking_start_time, self.booking_end_time)).exists():
                    raise ValidationError("Recurring booking at specified time overlaps with another booking.")
                date += timedelta(days=7)
