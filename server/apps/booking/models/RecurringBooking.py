import json

from django.core.exceptions import ValidationError
from apps.accounts.exceptions import PrivilegeError
from django.db import models
from django.db.models import Q

from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.rooms.models.Room import Room
from apps.accounts.models.User import User
from apps.groups.models.Group import Group
from apps.util.AbstractBooker import AbstractBooker
from datetime import timedelta, datetime
from apps.util import utils


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
        self.evaluate_privilege()
        self.validate_model()
        super(RecurringBooking, self).save(*args, **kwargs)

    def validate_model(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date can not be after End date.")
        elif self.end_date < self.start_date + timedelta(days=7):
            raise ValidationError("You must book for at least two consecutive weeks.")
        elif self.booking_start_time >= self.booking_end_time:
            raise ValidationError("Start time can not be after End time.")
        else:
            from apps.booking.models.Booking import Booking

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

    def edit_recurring_booking(self,
                               start_date,
                               end_date,
                               booking_start_time,
                               booking_end_time,
                               skip_conflicts,
                               user=None):

        from apps.booking.models.Booking import Booking

        now = datetime.now()
        all_conflicts = []
        non_conflicting_bookings = []

        # Gets all bookings associated to the indicated booking which happen after current date
        all_associated_booking_instances = Booking.objects.all().filter(recurring_booking=self, date__gte=now)

        # Find the earliest booking in the list
        earliest_booking = all_associated_booking_instances[0]
        for booking in all_associated_booking_instances:
            if booking.date < earliest_booking.date:
                earliest_booking = booking

        # Determine offset based on earliest booking
        if start_date is not None:
            booking_offset = earliest_booking.date - start_date
        else:
            booking_offset = 0

        # Get current end date and apply offset in case start date has changed
        current_end_date = self.end_date + timedelta(days=booking_offset)

        # Create new bookings if new end date has been extended and add to appropriate lists
        if end_date is not None:
            while current_end_date < end_date:
                # Sets the next booking in series
                current_end_date = current_end_date + timedelta(days=7)
                if current_end_date < end_date:
                    booking = Booking.objects.create_booking(
                        booker=self.booker,
                        group=self.group,
                        room=self.room,
                        date=current_end_date,
                        start_time=booking_start_time,
                        end_time=booking_end_time,
                        recurring_booking=self,
                        confirmed=False
                    )
                    try:
                        booking.validate_model()
                        non_conflicting_bookings.append(booking)
                    except ValidationError:
                            all_conflicts.append(booking)
                            continue

        # Iterates through associated bookings and makes the adjustment
        for associated_booking in all_associated_booking_instances:
            # Will apply offset regardless, but if no offset, will add zero
            if booking_start_time:
                associated_booking.start_time = booking_start_time
            if associated_booking.end_time:
                associated_booking.end_time = booking_end_time
            if start_date:
                associated_booking.date = associated_booking.date + booking_offset
            try:
                associated_booking.validate_model()
                non_conflicting_bookings.append(associated_booking)
            except ValidationError:
                all_conflicts.append(associated_booking)
                continue

        # If there are no conflicts, simply make adjustments accordingly
        if len(all_conflicts) == 0 or skip_conflicts:
            for non_conflicting in non_conflicting_bookings:
                # Make sure bookings are in range and have not ended before modifying. Past bookings checked by filter
                if start_date is not None and end_date is not None and start_date <= non_conflicting.date <= end_date:
                    non_conflicting.save()
                    utils.log_model_change(non_conflicting, utils.CHANGE, user)
                # Make sure bookings are in range and have not ended before deleting. Past bookings checked by filter
                elif start_date is not None and non_conflicting.date >= start_date:
                    non_conflicting.delete()
        else:
            # If there are any conflicts, return list of them
            return all_conflicts
