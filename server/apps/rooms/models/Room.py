from django.db import models


class Room(models.Model):
    room_id = models.CharField(max_length=50, blank=False, unique=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    number_of_computers = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return '%s, Capacity: %d, Number of computers: %d' % (self.room_id, self.capacity, self.number_of_computers)
