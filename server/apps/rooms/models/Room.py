import datetime
from django.db import models
from django.core.exceptions import ValidationError


class RoomManager(models.Manager):
    def create_room(self,
                    name,
                    capacity,
                    number_of_computers,
                    has_tv=False,
                    has_windows=False):
        room = self.create(
            name=name,
            capacity=capacity,
            number_of_computers=number_of_computers,
            has_tv=has_tv,
            has_windows=has_windows,
        )

        return room


class Room(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    capacity = models.PositiveIntegerField(blank=False, null=False, default=0)
    number_of_computers = models.PositiveIntegerField(blank=False, null=False, default=0)
    has_tv = models.BooleanField(default=False)
    has_windows = models.BooleanField(default=False)
    max_booking_duration = models.IntegerField(blank=True, null=True)
    max_recurring_booking_duration = models.IntegerField(blank=True, null=True)

    objects = RoomManager()

    observers = list()

    def __str__(self):
        return '{}, ' \
               'Capacity: {}, ' \
               'Number of computers: {}'.format(self.name, self.capacity, self.number_of_computers)

    def save(self, *args, **kwargs):

        self.validate_model()
        this = super(Room, self).save(*args, **kwargs)
        return this

    def validate_model(self):

        name = self.name
        capacity = self.capacity
        number_of_computers = self.number_of_computers
        id = self.id

        if name is '':
            raise ValidationError("Room id cannot be empty. Please enter room id")

        if not isinstance(capacity, int):
            raise ValidationError("Invalid capacity. Please enter a positive integer value or zero")

        if not isinstance(number_of_computers, int):
            raise ValidationError("Invalid number of computers. Please enter a positive integer value or zero")

        if capacity < 0:
            raise ValidationError("Invalid capacity. Please enter a positive integer value or zero")

        if (capacity % 1) != 0:
            raise ValidationError("Invalid capacity. Please enter a positive integer value or zero")

        if int(number_of_computers) < 0:
            raise ValidationError("Invalid number of computers. Please enter a positive integer value or zero")

        if (number_of_computers % 1) != 0:
            raise ValidationError("Invalid Number of computers. Please enter a positive integer value or zero")

    def get_observers(self):
        return Room.observers

    def get_bookings(self, start_date=None, end_date=None):
        bookings = self.booking_set
        if start_date is not None:
            bookings = bookings.filter(date__gte=start_date)
        if end_date is not None:
            bookings = bookings.filter(date__lte=end_date)
        return bookings

    def is_available(self, date, start, end):
        if self.booking_set.filter(date=date, start_time__lt=end, end_time__gt=start).exists():
            return False
        return True
