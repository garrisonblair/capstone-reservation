import datetime
from django.db import models
from django.core.exceptions import ValidationError


class RoomManager(models.Manager):
    def create_room(self,
                    name,
                    capacity,
                    number_of_computers,
                    available=True,
                    unavailable_start_time=None,
                    unavailable_end_time=None):
        room = self.create(
            name=name,
            capacity=capacity,
            number_of_computers=number_of_computers,
            available=available,
            unavailable_start_time=unavailable_start_time,
            unavailable_end_time=unavailable_end_time,
        )

        return room


class Room(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    capacity = models.PositiveIntegerField(blank=False, null=False, default=0)
    number_of_computers = models.PositiveIntegerField(blank=False, null=False, default=0)
    available = models.BooleanField(default=True)
    unavailable_start_time = models.DateTimeField(blank=True, null=True)
    unavailable_end_time = models.DateTimeField(blank=True, null=True)
    objects = RoomManager()

    observers = list()

    def __str__(self):
        return '{}, ' \
               'Capacity: {}, ' \
               'Number of computers: {}, ' \
               'Available: {}, ' \
               'Unavailable start time: {}, ' \
               'Unavailable end time: {}'\
            .format(self.name, self.capacity, self.number_of_computers,
                    self.available, self.unavailable_start_time, self.unavailable_end_time)

    def save(self, *args, **kwargs):

        self.validate_model()
        this = super(Room, self).save(*args, **kwargs)
        return this

    def validate_model(self):

        name = self.name
        capacity = self.capacity
        number_of_computers = self.number_of_computers
        id = self.id

        if self.unavailable_start_time:
            if not isinstance(self.unavailable_start_time, datetime.datetime):
                self.unavailable_start_time = \
                    datetime.datetime.strptime(self.unavailable_start_time, "%Y-%m-%d %H:%M")
        if self.unavailable_end_time:
            if not isinstance(self.unavailable_end_time, datetime.datetime):
                self.unavailable_end_time = \
                    datetime.datetime.strptime(self.unavailable_end_time, "%Y-%m-%d %H:%M")

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

        if not self.unavailable_start_time and self.unavailable_end_time:
            raise ValidationError("Unavailable start time must have a corresponding end time")

        if not self.unavailable_end_time and self.unavailable_start_time:
            raise ValidationError("Unavailable end time must have a corresponding start time")

        if self.unavailable_start_time and self.unavailable_end_time and self.available is True:
                raise ValidationError("Unavailable period is not needed if the room is available")

        if self.unavailable_start_time and self.unavailable_end_time:
            if self.unavailable_start_time >= self.unavailable_end_time:
                raise ValidationError("Unavailable start time must be less than end time")

    def get_observers(self):
        return Room.observers

    def get_bookings(self, start_date=None, end_date=None):
        bookings = self.booking_set
        if start_date is not None:
            bookings = bookings.filter(date__gte=start_date)
        if end_date is not None:
            bookings = bookings.filter(date__lte=end_date)
        return bookings
