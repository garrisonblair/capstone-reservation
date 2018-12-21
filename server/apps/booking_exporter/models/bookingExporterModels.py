from django.db import models

from apps.rooms.models.Room import Room


class ExternalRoomID(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    external_id = models.TextField()
