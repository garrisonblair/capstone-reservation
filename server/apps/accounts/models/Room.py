from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Room(models.Model):
    room_id = models.CharField(max_length=50, blank=False, primary_key=True)
    capacity = models.PositiveIntegerField()
    number_of_computers = models.PositiveIntegerField()
    is_active = models.BooleanField()

    def __str__(self):
        return self
