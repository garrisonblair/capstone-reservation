from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from apps.rooms.models.Room import Room
from apps.accounts.models.Booker import Booker
from apps.groups.models.Group import Group
from datetime import timedelta


class RecurringBookingManager(models.Manager):
    def create_recurring_booking(self, start_date, end_date, start_time, end_time, room, group,
                                 booker, skip_conflicts):
        recurring_booking = self.create(
            start_date=start_date,
            end_date=end_date,
            booking_start_time=start_time,
            booking_end_time=end_time,
            room=room,
            group=group,
            booker=booker,
            skip_conflicts=skip_conflicts
        )

        from . import Booking
        date = recurring_booking.start_date
        conflicts = list()
        while date <= recurring_booking.end_date:
            try:
                booking = Booking.objects.create_booking(
                    booker=recurring_booking.booker,
                    group=recurring_booking.group,
                    room=recurring_booking.room,
                    date=date,
                    start_time=recurring_booking.booking_start_time,
                    end_time=recurring_booking.booking_end_time,
                    recurring_booking=recurring_booking
                )
                recurring_booking.booking_set.add(booking)
            except ValidationError:
                if skip_conflicts:
                    conflicts.append(date)
                    date += timedelta(days=7)
                    continue
            date += timedelta(days=7)

        return recurring_booking, conflicts


class RecurringBooking(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    booking_start_time = models.TimeField()
    booking_end_time = models.TimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    booker = models.ForeignKey(Booker, on_delete=models.CASCADE)
    skip_conflicts = models.BooleanField(default=False)

    objects = RecurringBookingManager()

    def save(self, *args, **kwargs):
        self.validate_model()
        super(RecurringBooking, self).save(*args, **kwargs)

    def validate_model(self):
        if not self.group.is_verified:
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
            bookings = 0
            while date <= self.end_date:
                if Booking.objects.filter(~Q(start_time=self.booking_end_time), room=self.room, date=date,
                                          start_time__range=(self.booking_start_time, self.booking_end_time)).exists():
                    if self.skip_conflicts:
                        bookings += 1
                    else:
                        raise ValidationError("Recurring booking at specified time overlaps with another booking.")
                elif Booking.objects.filter(~Q(end_time=self.booking_start_time), room=self.room, date=date,
                                            end_time__range=(self.booking_start_time, self.booking_end_time)).exists():
                    if self.skip_conflicts:
                        bookings += 1
                    else:
                        raise ValidationError("Recurring booking at specified time overlaps with another booking.")
                else:
                    bookings += 1
                date += timedelta(days=7)
            if self.skip_conflicts and bookings == 0:
                raise ValidationError("Recurring booking at specified time overlaps with another booking every week.")
