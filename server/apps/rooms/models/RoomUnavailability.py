import datetime
from django.db import models
from ..models.Room import Room
from django.core.exceptions import ValidationError


class RoomUnavailability(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField(blank=False, null=False)
    end_time = models.DateTimeField(blank=False, null=False)

    def save(self, *args, **kwargs):

        self.validate_model()
        this = super(RoomUnavailability, self).save(*args, **kwargs)
        return this

    def validate_model(self):

        if self.start_time:
            if not isinstance(self.start_time, datetime.datetime):
                self.start_time = \
                    datetime.datetime.strptime(self.start_time, "%Y-%m-%d %H:%M")
        if self.end_time:
            if not isinstance(self.end_time, datetime.datetime):
                self.end_time = \
                    datetime.datetime.strptime(self.end_time, "%Y-%m-%d %H:%M")

        if not self.start_time:
            raise ValidationError("Unavailable start time cannot be empty.")

        if not self.end_time:
            raise ValidationError("Unavailable end time cannot be empty.")

        if self.start_time >= self.end_time:
            raise ValidationError("Unavailable start time must be less than end time")
