import json
import datetime

from django.db import models
from apps.accounts.models.Booker import Booker
from apps.groups.models.Group import Group
from apps.rooms.models.Room import Room
from apps.booking.models.RecurringBooking import RecurringBooking
from django.db.models import Q
from django.core.exceptions import ValidationError

from apps.util.SubjectModel import SubjectModel
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.accounts.exceptions import PrivilegeError

from apps.util.AbstractBooker import AbstractBooker


class BookingManager(models.Manager):
    def create_booking(self, booker, group, room, date, start_time, end_time, recurring_booking):
        booking = self.create(
            booker=booker,
            group=group,
            room=room,
            date=date,
            start_time=start_time,
            end_time=end_time,
            recurring_booking=recurring_booking
        )

        return booking


class Booking(models.Model, SubjectModel):
    booker = models.ForeignKey(Booker,
                               on_delete=models.CASCADE)  # type: Booker
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              blank=True, null=True)  # type: Group
    room = models.ForeignKey(Room,
                             on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    recurring_booking = models.ForeignKey(RecurringBooking,
                                          on_delete=models.CASCADE,
                                          blank=True,
                                          null=True)

    objects = BookingManager()

    observers = list()

    def save(self, *args, **kwargs):
        self.evaluate_privilege()
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
            self.id, self.booker.booker_id, self.room.name, self.date, self.start_time, self.end_time
        )

    def validate_model(self):

        if not isinstance(self.start_time, datetime.time):
            self.start_time = datetime.datetime.strptime(self.start_time, "%H:%M").time()
        if not isinstance(self.end_time, datetime.time):
            self.end_time = datetime.datetime.strptime(self.end_time, "%H:%M").time()

        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be less than end time")

        elif Booking.objects.filter(~Q(start_time=self.end_time),
                                    ~Q(id=self.id),
                                    room=self.room,
                                    date=self.date,
                                    start_time__range=(self.start_time, self.end_time)).exists():
            raise ValidationError("Specified time is overlapped with other bookings.")

        elif Booking.objects.filter(~Q(end_time=self.start_time),
                                    ~Q(id=self.id),
                                    room=self.room,
                                    date=self.date,
                                    end_time__range=(self.start_time, self.end_time)).exists():
            raise ValidationError("Specified time is overlapped with other bookings.")

    def get_active_daily_bookings(self, booker_entity, current_date, current_time):
        return booker_entity.booking_set.filter(Q(Q(date=current_date) & Q(end_time__gte=current_time))
                                                | Q(date__gt=current_date))

    def get_active_daily_non_recurring_bookings(self, booker_entity, selected_date, selected_time):
        return self.get_active_daily_bookings(booker_entity, selected_date, selected_time
                                              ).filter(recurring_booking=None)

    def get_active_overall_non_recurring_bookings(self, booker_entity):
        return booker_entity.booking_set.filter(recurring_booking=None)

    def evaluate_privilege(self):

        if self.group is not None:
            booker_entity = self.group  # type: AbstractBooker
        else:
            booker_entity = self.booker

        # no checks if no category assigned
        if booker_entity.get_privileges() is None:
            return

        p_c = booker_entity.get_privileges()  # type: PrivilegeCategory

        max_days_until_booking = p_c.get_parameter("max_days_until_booking")
        max_overall_bookings = p_c.get_parameter("max_overall_bookings")
        max_daily_bookings = p_c.get_parameter("max_daily_bookings")
        start_time = p_c.get_parameter("booking_start_time")
        end_time = p_c.get_parameter("booking_end_time")

        # max_days_until_booking
        today = datetime.date.today()

        day_delta = self.date - today
        if day_delta.days > max_days_until_booking and self.recurring_booking is None:
            raise PrivilegeError(p_c.get_error_text("max_days_until_booking"))

        # max_overall_bookings
        num_overall_bookings = self.get_active_overall_non_recurring_bookings(booker_entity)\
                                   .values_list('date').distinct().count()

        if num_overall_bookings > max_overall_bookings:
            raise PrivilegeError(p_c.get_error_text("max_overall_bookings"))

        # max_daily_bookings
        num_daily_bookings = self.get_active_daily_non_recurring_bookings(booker_entity, self.date, self.start_time
                                                                          ).count()

        if num_daily_bookings > max_daily_bookings:
            raise PrivilegeError(p_c.get_error_text("max_daily_bookings"))

        # booking_start_time
        if self.start_time < start_time:
            raise PrivilegeError(p_c.get_error_text("booking_start_time"))

        # booking_end_time
        if self.end_time > end_time:
            raise PrivilegeError(p_c.get_error_text("booking_end_time"))

    def get_observers(self):
        return Booking.observers
