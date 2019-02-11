import json
import datetime

from django.db import models
from apps.accounts.models.User import User
from apps.groups.models.Group import Group
from apps.rooms.models.Room import Room
from ..models.RecurringBooking import RecurringBooking
from django.db.models import Q
from django.core.exceptions import ValidationError

from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.accounts.exceptions import PrivilegeError
from apps.system_administration.models.system_settings import SystemSettings

from apps.util.SubjectModel import SubjectModel
from apps.util.AbstractBooker import AbstractBooker
from apps.util import utils


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

    def get_first_booking_date(self):
        if self.count() == 0:
            return datetime.datetime.now().date()
        return self.order_by("date").first().date


class Booking(models.Model, SubjectModel):
    booker = models.ForeignKey(User,
                               on_delete=models.CASCADE)  # type: User
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              blank=True, null=True)  # type: Group
    room = models.ForeignKey(Room,
                             on_delete=models.CASCADE)
    note = models.CharField(max_length=255, blank=True, null=True)
    display_note = models.BooleanField(default=False)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    recurring_booking = models.ForeignKey(RecurringBooking,
                                          on_delete=models.CASCADE,
                                          blank=True,
                                          null=True)

    bypass_privileges = models.BooleanField(default=False)
    bypass_validation = models.BooleanField(default=False)

    objects = BookingManager()

    observers = list()

    def save(self, *args, **kwargs):
        if not self.bypass_validation:
            self.validate_model()

        is_create = False
        if self.id is None:
            is_create = True

        if not self.bypass_privileges:
            self.evaluate_privilege(is_create)

        this = super(Booking, self).save(*args, **kwargs)

        if is_create:
            self.object_created()
        else:
            self.object_updated()
        return this

    def __str__(self):
        return 'Booking: {}, Booker: {}, Room: {}, Date: {}, Start time: {}, End Time: {}, Recurring Booking: {}'\
            .format(self.id, self.booker.username, self.room.name, self.date, self.start_time, self.end_time,
                    self.recurring_booking)

    def validate_model(self):
        now = datetime.datetime.now()
        if not isinstance(self.start_time, datetime.time):
            self.start_time = datetime.datetime.strptime(self.start_time, "%H:%M").time()
        if not isinstance(self.end_time, datetime.time):
            self.end_time = datetime.datetime.strptime(self.end_time, "%H:%M").time()

        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be less than end time")

        if Booking.objects.filter(~Q(id=self.id),
                                  start_time__lt=self.end_time,
                                  end_time__gt=self.start_time,
                                  room=self.room,
                                  date=self.date).exists():
            raise ValidationError("Specified time is overlapped with other bookings.")

    def merge_with_neighbouring_bookings(self):
        settings = SystemSettings.get_settings()

        if settings.merge_adjacent_bookings is False:
            return

        threshold_minutes = settings.merge_threshold_minutes
        threshold_minutes = datetime.timedelta(minutes=threshold_minutes)

        start_time_max = (datetime.datetime.combine(datetime.date.today(), self.end_time) + threshold_minutes).time()
        end_time_min = (datetime.datetime.combine(datetime.date.today(), self.start_time) - threshold_minutes).time()

        possible_neighbours = Booking.objects.filter(room=self.room, booker=self.booker, date=self.date)
        neighbours = possible_neighbours.filter(Q(Q(start_time__lte=start_time_max)
                                                  & Q(start_time__gte=self.end_time)
                                                  | Q(end_time__gte=end_time_min)
                                                  & Q(end_time__lte=self.start_time)))

        for neighbour in neighbours:  # type: Booking

            if neighbour.end_time > self.end_time:
                self.end_time = neighbour.end_time
            if neighbour.start_time < self.start_time:
                self.start_time = neighbour.start_time

            neighbour.delete()
            utils.log_model_change(neighbour, utils.DELETION)

    def evaluate_privilege(self, is_create):

        if self.group is not None:
            booker_entity = self.group  # type: AbstractBooker
        else:
            booker_entity = self.booker

        # no checks if no category assigned
        if booker_entity.get_privileges() is None:
            return

        p_c = booker_entity.get_privileges()  # type: PrivilegeCategory

        max_days_until_booking = p_c.get_parameter("max_days_until_booking")
        max_num_days_with_bookings = p_c.get_parameter("max_num_days_with_bookings")
        max_num_bookings_for_date = p_c.get_parameter("max_num_bookings_for_date")
        start_time = p_c.get_parameter("booking_start_time")
        end_time = p_c.get_parameter("booking_end_time")

        if is_create:
            # max_days_until_booking
            today = datetime.date.today()
            day_delta = self.date - today
            if day_delta.days > max_days_until_booking and self.recurring_booking is None:
                raise PrivilegeError(p_c.get_error_text("max_days_until_booking"))

            # max_num_days_with_bookings
            num_days_with_bookings = booker_entity.get_days_with_active_bookings().count()

            if num_days_with_bookings >= max_num_days_with_bookings and \
                    not booker_entity.get_days_with_active_bookings().filter(date=self.date).exists():
                # check that the new booking is in day that already has booking
                raise PrivilegeError(p_c.get_error_text("max_num_days_with_bookings"))

            # max_num_bookings_for_date
            num_bookings_for_date = booker_entity.get_non_recurring_bookings_for_date(self.date).count()

            if num_bookings_for_date >= max_num_bookings_for_date:
                raise PrivilegeError(p_c.get_error_text("max_num_bookings_for_date"))

        # booking_start_time
        if self.start_time < start_time:
            raise PrivilegeError(p_c.get_error_text("booking_start_time"))

        # booking_end_time
        if self.end_time > end_time:
            raise PrivilegeError(p_c.get_error_text("booking_end_time"))

    def get_observers(self):
        return Booking.observers

    def json_serialize(self):
        from ..serializers.booking import BookingSerializer
        return json.dumps(BookingSerializer(self).data)

    def get_duration(self):
        return (datetime.datetime.combine(date=datetime.date.today(), time=self.end_time)
                - datetime.datetime.combine(date=datetime.date.today(), time=self.start_time))
