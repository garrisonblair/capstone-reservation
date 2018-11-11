from django.db import models
from django.core.exceptions import ValidationError


class RoomManager(models.Manager):
    def create_room(self, room_id, capacity, number_of_computers):
        room = self.create(
            room_id=room_id,
            capacity=capacity,
            number_of_computers=number_of_computers
        )

        return room


class Room(models.Model):
    room_id = models.CharField(max_length=50, blank=False, unique=True)
    capacity = models.PositiveIntegerField(blank=False, null=False, default=0)
    number_of_computers = models.PositiveIntegerField(blank=False, null=False, default=0)

    objects = RoomManager()

    observers = list()

    def __str__(self):
        return '{}, Capacity: {}, Number of computers: {}'.format(
            self.room_id, self.capacity, self.number_of_computers
        )

    def save(self, *args, **kwargs):

        self.validate_model()
        this = super(Room, self).save(*args, **kwargs)
        return this

    def validate_model(self):

        room_id = self.room_id
        capacity = self.capacity
        number_of_computers = self.number_of_computers

        if room_id is '':
            raise ValidationError("Room id cannot be empty. Please enter room id")

        elif not isinstance(capacity, int):
            raise ValidationError("Invalid capacity. Please enter a positive integer value or zero")

        elif not isinstance(number_of_computers, int):
            raise ValidationError("Invalid number of computers. Please enter a positive integer value or zero")

        elif capacity < 0:
            raise ValidationError("Invalid capacity. Please enter a positive integer value or zero")

        elif (capacity % 1) != 0:
            raise ValidationError("Invalid capacity. Please enter a positive integer value or zero")

        elif int(number_of_computers) < 0:
            raise ValidationError("Invalid number of computers. Please enter a positive integer value or zero")

        elif (number_of_computers % 1) != 0:
            raise ValidationError("Invalid Number of computers. Please enter a positive integer value or zero")

    def get_observers(self):
        return Room.observers
