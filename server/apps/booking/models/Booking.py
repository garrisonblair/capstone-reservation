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
from apps.accounts.permissions.IsOwnerOrAdmin import IsOwnerOrAdmin
from apps.accounts.permissions.IsBooker import IsBooker
from apps.accounts.exceptions import PrivilegeError

from apps.system_administration.models.system_settings import SystemSettings

from apps.util.SubjectModel import SubjectModel
from apps.util.AbstractBooker import AbstractBooker
from apps.util import utils

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


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

    note = models.CharField(max_length=255, blank=True, null=True)
    display_note = models.BooleanField(default=False)
    show_note_on_calendar = models.BooleanField(default=False)

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

    def delete_booking(self, request, pk):

        from apps.booking.models.CampOn import CampOn
        from apps.booking.serializers.booking import BookingSerializer

        permission_classes = (IsAuthenticated, IsOwnerOrAdmin, IsBooker)
        serializer_class = BookingSerializer

        # Ensure that booking to be canceled exists
        try:
            booking = Booking.objects.get(id=pk)
        except Booking.DoesNotExist:
            raise ValidationError("Selected booking to cancel does not exist")

        # Check user permissions
        self.check_object_permissions(request, booking.booker)

        # Check if Booking has ended and if it has, disable booking from being canceled
        now = datetime.datetime.now()
        booking_end = booking.end_time
        timeout = now.time()

        if now.date() > booking.date or (now.date() == booking.date and timeout >= booking_end):
            raise ValidationError("Selected booking cannot be canceled as booking has started")

        # Get all campons for this booking
        booking_id = booking.id
        booking_campons = list(CampOn.objects.filter(camped_on_booking__id=booking_id))

        # Remove any campons that have endtimes before current time
        for campon in booking_campons:
            if campon.end_time < timeout:
                booking_campons.remove(campon)

        # Checks to see if booking to cancel has any campons otherwise simply deletes the booking
        if len(booking_campons) <= 0:
            utils.log_model_change(booking, utils.DELETION, request.user)
            booking.delete()

        # Otherwise handles turning campons of original booking into campons for new booking and bookings if required
        else:
            # Sort list of campons by campon.id
            booking_campons.sort(key=booking_key, reverse=False)
            # Set first campon in list to first campon created
            first_campon = booking_campons[0]

            # Turn first campon (which should be first created) into a booking
            new_booking = Booking(booker=first_campon.booker,
                                  group=None,
                                  room=booking.room,
                                  date=now.date(),
                                  start_time=first_campon.start_time,
                                  end_time=first_campon.end_time)

            # Delete previous booking in order to then save new_booking derived from first campon,
            # then delete first campon
            booking.delete()
            new_booking.save()
            previous_campon = first_campon

            # Adding to see if I can iterate over all the rest without checking condition
            booking_campons.remove(first_campon)

            for campon in booking_campons:
                # Change associated booking of all other campons to booking id of new booking
                campon.camped_on_booking = new_booking
                # Creates booking for difference (Assuming current campon does not go into another booking)
                if (campon.end_time.hour > previous_campon.end_time.hour) \
                        or (campon.end_time.hour == previous_campon.end_time.hour and
                            (campon.end_time.minute - previous_campon.end_time.minute) > 10):
                    difference_booking = Booking(
                        booker=campon.booker,
                        group=None,
                        room=booking.room,
                        date=new_booking.date,
                        start_time=previous_campon.end_time,
                        end_time=campon.end_time)
                    difference_booking.save()
                    campon.end_time = difference_booking.start_time
                else:
                    campon.end_time = previous_campon.end_time
                campon.save()
                previous_campon = campon
            # Finally delete the first campon as it is now a new booking
            first_campon.delete()

        return


def booking_key(val):
    return val.id
