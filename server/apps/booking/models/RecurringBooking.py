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

from apps.util import utils
from apps.system_administration.models.system_settings import SystemSettings
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
        self.evaluate_privilege()
        if self.id is None:
            is_create = True
        else:
            is_create = False
        self.validate_model(is_create)
        super(RecurringBooking, self).save(*args, **kwargs)

    def validate_model(self, is_create=False):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date can not be after End date.")
        elif self.end_date < self.start_date + timedelta(days=7):
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

    def edit_recurring_booking(self,
                               start_date,  # type: date
                               end_date,
                               booking_start_time,
                               booking_end_time,
                               skip_conflicts,
                               user=None):

        if start_date is None or end_date is None or booking_start_time is None or booking_end_time is None:
            raise ValidationError("Missing required parameters for start/end date and time.")

        from apps.booking.models.Booking import Booking

        now = datetime.now()
        today = datetime.today().date()
        settings = SystemSettings.get_settings()
        timeout = (now + settings.booking_edit_lock_timeout).time()
        all_conflicts = []
        non_conflicting_bookings = []

        # Gets all bookings associated to the indicated booking which happen after current date and current time
        all_associated_bookings = Booking.objects.all().filter(Q(Q(start_time__gt=now.time()) & Q(date__gt=today)) |
                                                               Q(Q(recurring_booking=self) &
                                                               Q(date__gte=today)))
        # Find the earliest booking in the list and use it to determine the offset of booking edits
        sorted_bookings = all_associated_bookings.order_by("date")
        sorted_bookings = list(sorted_bookings)
        bookings_to_delete = list()

        # remove bookings out of range
        for booking in sorted_bookings:
            if booking.date < start_date:
                bookings_to_delete.append(booking)
                sorted_bookings.remove(booking)
            else:
                break

        # if start_date is in past, move it to now
        while start_date < today:
            start_date = add_days_to_date(start_date, 7)

        first_booking_new_start = start_date

        while first_booking_new_start < sorted_bookings[0].date:
            first_booking_new_start = add_days_to_date(first_booking_new_start, 7)

        booking_offset = (first_booking_new_start - sorted_bookings[0].date).days

        # Iterates through associated bookings and makes the adjustments of start/end time and start/end date
        for associated_booking in sorted_bookings:
            # Will apply offset regardless, but if no offset, will add zero
            if booking_start_time:
                associated_booking.start_time = booking_start_time
            if booking_end_time:
                associated_booking.end_time = booking_end_time
            if start_date:
                # This applies the offset in case the start date has been moved earlier or later
                date_dt = datetime.combine(associated_booking.date, time(0, 0, 0))
                associated_booking.date = (date_dt + timedelta(days=booking_offset)).date()
            # Previously existing bookings should be validated and then appended to either conflicting items list
            # or non-conflicting items lists
            try:
                associated_booking.validate_model()
                non_conflicting_bookings.append(associated_booking)
            except ValidationError:
                all_conflicts.append(associated_booking.date)
                continue

        # create bookings at beginning if necessary
        while start_date < sorted_bookings[0].date:
            try:

                booking = Booking.objects.create_booking(
                    booker=self.booker,
                    group=self.group,
                    room=self.room,
                    date=start_date,
                    start_time=booking_start_time,
                    end_time=booking_end_time,
                    recurring_booking=self,
                    confirmed=False
                )
                booking.validate_model()
                non_conflicting_bookings.append(booking)
            except ValidationError as e:
                all_conflicts.append(booking.date)
                continue
            finally:
                start_date = add_days_to_date(start_date, 7)

        # delete bookings at end if necessary
        for booking in sorted_bookings:
            if booking.date > end_date:
                bookings_to_delete.append(booking)
                sorted_bookings.remove(booking)

        last_booking = sorted_bookings[len(sorted_bookings) - 1]
        # Get current end date and apply offset in case start date has changed (Ex. -2 + 9 = 7)

        current_end_date = last_booking.date + timedelta(days=booking_offset + 7)

        # Create new bookings if new end date has been extended and add to appropriate lists)
        while current_end_date < end_date:

            # New bookings should be validated and then appended to either conflicting items list
            # or non-conflicting items lists
            try:
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
                booking.validate_model()
                non_conflicting_bookings.append(booking)
            except ValidationError as e:
                all_conflicts.append(current_end_date)
                continue
            finally:
                current_end_date = add_days_to_date(current_end_date, 7)

        # If there are no conflicts, simply make adjustments accordingly
        if len(all_conflicts) == 0 or skip_conflicts:

            for non_conflicting in non_conflicting_bookings:
                non_conflicting.save()
                utils.log_model_change(non_conflicting, utils.CHANGE, user)

            for booking in bookings_to_delete:
                booking.delete_booking()

            # In case any bookings that were added as conflicts need to be deleted based on date range change
            for conflicting in all_conflicts:
                # Gets the booking object for the conflicting date and this RecurringBooking
                conflicting = Booking.objects.get(recurring_booking=self, date=conflicting)
                # If the booking was in the past, ignore this one (higher precedence than next case which would delete)
                if datetime.combine(conflicting.date, datetime.min.time()) < today \
                        or (conflicting.date == today.date()
                            and conflicting.start_time > timeout):
                    pass
                # Delete bookings which have not started or have passed but are before the new start date
                elif conflicting.date < start_date:
                    conflicting.delete()
                    utils.log_model_change(conflicting, utils.DELETION, user)
                # Delete bookings which were scheduled to occure after the new end date
                elif conflicting.date > end_date:
                    conflicting.delete()
                    utils.log_model_change(conflicting, utils.DELETION, user)

            # Set the new dates / times on the recurring booking and save it (start and end)
            self.booking_start_time = booking_start_time
            self.booking_end_time = booking_end_time
            self.start_date = start_date
            self.end_date = end_date
            self.save()
            utils.log_model_change(self, utils.CHANGE, user)
        else:
            # If there are any conflicts, return list of them
            return all_conflicts


def add_days_to_date(date, days):
    date_dt = datetime.combine(date, time(0, 0, 0))
    date_dt += timedelta(days=days)
    return date_dt.date()
