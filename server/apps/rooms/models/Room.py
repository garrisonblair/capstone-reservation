from django.db import models


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
