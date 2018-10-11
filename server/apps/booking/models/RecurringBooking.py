from django.db import models
from apps.rooms.models.Room import Room
from apps.groups.models.StudentGroup import StudentGroup
from datetime import timedelta


class RecurringBookingManager(models.Manager):
    def create_recurring_booking(self, start_date, end_date, start_time, end_time, room, student_group):
        recurring_booking = RecurringBooking(
            start_date=start_date,
            end_date=end_date,
            booking_start_time=start_time,
            booking_end_time=end_time,
            room=room,
            student_group=student_group
        )
        recurring_booking.save()

        from . import Booking
        date = recurring_booking.start_date
        while date <= recurring_booking.end_date:
            booking = Booking.objects.create_booking(
                student=student_group.students.first(),
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

    objects = RecurringBookingManager()


