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
    capacity = models.PositiveIntegerField(blank=True, null=True)
    number_of_computers = models.PositiveIntegerField(blank=True, null=True)

    def modify_room_id(self, room_id):
        self.room_id = room_id
        self.save()

    def modify_capacity(self, capacity):
        self.capacity = capacity
        self.save()

    def modify_number_of_computers(self, number_of_computers):
        self.number_of_computers = number_of_computers
        self.save()

    def __str__(self):
        return '{}, Capacity: {}, Number of computers: {}'.format(
            self.room_id, self.capacity, self.number_of_computers
        )

    def modify_room_id(self, room_id):
        self.room_id = room_id

    def modify_capacity(self, capacity):
        self.capacity = capacity

    def modify_number_of_computers(self, number_of_computers):
        self.number_of_computers = number_of_computers

    def delete_room(self):
        self.delete()

    def validate_model(self):

        room_id = self.room_id,
        capacity = self.capacity,
        number_of_computers = self.number_of_computers

        if room_id is '':
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
