from django.db import models

# from django.db.models import Q

# Add room #21
# Modify Room #22
# Delete Room #23


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

#    def save(self):
#        is_create = False
#        if self.id is None:
#            is_create = True
#
#        this = super(Room, self).save(*args, **kwargs)
#
#        if is_create:
#            self.object_created()
#        else:
#            self.object_updated()
#
#        return this

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
