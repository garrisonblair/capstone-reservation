from django.db import models


class Room(models.Model):
    room_id = models.CharField(max_length=50, blank=False, unique=True)
    capacity = models.PositiveIntegerField()
    number_of_computers = models.PositiveIntegerField()

    def __str__(self):
        return '{}, Capacity: {}, Number of computers: {}'.format(
            self.room_id, self.capacity, self.number_of_computers
        )
