from django.db import models
from uuid import uuid4

from apps.rooms.models.Room import Room


class CardReader(models.Model):

    secret_key = models.UUIDField(default=uuid4)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True, default=None)
