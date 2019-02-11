import json
from django.db import models
from django.core.exceptions import ValidationError


class Announcement(models.Model):

    title = models.CharField(max_length=255)
    content = models.TextField()
    begin_date = models.DateField()
    end_date = models.DateField()

    def save(self, *args, **kwargs):
        self.validate_model()
        super(Announcement, self).save(*args, **kwargs)

    def validate_model(self):
        if self.begin_date > self.end_date:
            raise ValidationError("Begin date must be earlier then end date.")
