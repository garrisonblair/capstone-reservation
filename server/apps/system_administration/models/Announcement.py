import json
from django.db import models
from django.core.exceptions import ValidationError


class Announcement(models.Model):

    title = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)

    def save(self, *args, **kwargs):
        self.validate_model()
        super(Announcement, self).save(*args, **kwargs)

    def validate_model(self):
        if self.start_date > self.end_date:
            raise ValidationError("Begin date must be earlier then end date.")

    def json_serialize(self):
        from ..serializers.announcement import AnnouncementSerializer
        return json.dumps(AnnouncementSerializer(self).data)
