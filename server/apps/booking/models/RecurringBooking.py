import json

from django.core.exceptions import ValidationError
from apps.accounts.exceptions import PrivilegeError
from django.db import models

from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.rooms.models.Room import Room
from apps.accounts.models.User import User
from apps.groups.models.Group import Group
from apps.util.AbstractBooker import AbstractBooker

from datetime import timedelta, datetime, date, time


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

        from apps.booking.models.Booking import Booking
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
                    recurring_booking=recurring_booking,
                    confirmed=False
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
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    booker = models.ForeignKey(User, on_delete=models.CASCADE)
    skip_conflicts = models.BooleanField(default=False)

    objects = RecurringBookingManager()

    def save(self, *args, **kwargs):
        if self.id is None:
            is_create = True
            self.evaluate_privilege()
        else:
            is_create = False
        self.validate_model(is_create)
        super(RecurringBooking, self).save(*args, **kwargs)

    def validate_model(self, is_create=False):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date can not be after End date.")
        elif self.end_date < self.start_date + timedelta(days=7) and is_create:
            raise ValidationError("You must book for at least two consecutive weeks.")
        elif self.booking_start_time >= self.booking_end_time:
            raise ValidationError("Start time can not be after End time.")
        else:
            from apps.booking.models.Booking import Booking

            # Check room rule
            today = date.today()
            duration = datetime.combine(today, self.booking_end_time) - datetime.combine(today, self.booking_start_time)

            if self.room.max_recurring_booking_duration:
                if duration.seconds > self.room.max_booking_duration * 60 * 60:
                    raise ValidationError("This room can't be booked for more than {} hours for recurring bookings."
                                          .format(self.room.max_booking_duration))

            current_date = self.start_date
            bookings = 0
            conflicts = ''

            if is_create:
                while current_date <= self.end_date:
                    if Booking.objects.filter(start_time__lt=self.booking_end_time,
                                              end_time__gt=self.booking_start_time,
                                              room=self.room,
                                              date=current_date).exists():
                        if self.skip_conflicts:
                            bookings += 1
                        else:
                            conflict = current_date.strftime('%x')
                            conflicts += ", {}".format(conflict)
                    current_date += timedelta(days=7)

            if conflicts != '':
                raise ValidationError(conflicts[2:])

            if self.skip_conflicts and bookings == 0:
                raise ValidationError("Recurring booking at specified time overlaps with another booking every week.")

    def get_active_recurring_bookings(self, booker_entity):
        today = datetime.now().date()
        active_recurring_bookings = booker_entity.recurringbooking_set.filter(end_date__gt=today)
        # This will exclude any recurring bookings that don't contain any bookings as they shouldn't count towards
        # the active recurring bookings count, because they are essentially deleted
        for r_booking in active_recurring_bookings:
            if r_booking.booking_set.count() == 0:
                active_recurring_bookings = active_recurring_bookings.exclude(id=r_booking.id)
        return active_recurring_bookings

    def evaluate_privilege(self):
        if self.group is not None:
            booker_entity = self.group  # type: AbstractBooker
        else:
            booker_entity = self.booker

        # no checks if no category assigned
        if booker_entity.get_privileges() is None:
            return

        p_c = booker_entity.get_privileges()  # type: PrivilegeCategory

        can_make_recurring_booking = p_c.get_parameter("can_make_recurring_booking")
        max_recurring_bookings = p_c.get_parameter("max_recurring_bookings")
        start_time = p_c.get_parameter("booking_start_time")
        end_time = p_c.get_parameter("booking_end_time")

        if not can_make_recurring_booking:
            raise PrivilegeError(p_c.get_error_text("can_make_recurring_booking"))

        # max_recurring_bookings
        num_recurring_bookings = self.get_active_recurring_bookings(booker_entity).count()

        if num_recurring_bookings >= max_recurring_bookings:
            raise PrivilegeError(p_c.get_error_text("max_recurring_bookings"))

        # booking_start_time
        if self.booking_start_time < start_time:
            raise PrivilegeError(p_c.get_error_text("booking_start_time"))

        # booking_end_time
        if self.booking_end_time > end_time:
            raise PrivilegeError(p_c.get_error_text("booking_end_time"))

    def json_serialize(self):
        from ..serializers.recurring_booking import LogRecurringBookingSerializer
        return json.dumps(LogRecurringBookingSerializer(self).data)


def add_days_to_date(date, days):
    date_dt = datetime.combine(date, time(0, 0, 0))
    date_dt += timedelta(days=days)
    return date_dt.date()
