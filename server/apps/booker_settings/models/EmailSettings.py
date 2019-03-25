from django.db import models
from apps.accounts.models.User import User
from django.core.exceptions import ValidationError


class EmailSettings(models.Model):
    booker = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    when_booking = models.BooleanField(default=True)
    when_invitation = models.BooleanField(default=True)
    booking_reminder = models.BooleanField(default=True)
    when_camp_on_booking = models.BooleanField(default=True)


    def __str__(self):
        return 'Booker ID:{}, when_booking: {}'.format(self.booker.id, self.when_booking)

    def save(self, *args, **kwargs):

        self.validate_model()
        this = super(EmailSettings, self).save(*args, **kwargs)
        return this

    def validate_model(self):
        if not isinstance(self.when_booking, bool):
            raise ValidationError("'when_booking' must be a boolean")

        if not isinstance(self.when_invitation, bool):
            raise ValidationError("'when_invitation' must be a boolean")

        if not isinstance(self.booking_reminder, bool):
            raise ValidationError("'booking_reminder' must be a boolean")

        if not isinstance(self.when_camp_on_booking, bool):
            raise ValidationError("'when_camp_on_booking' must be a boolean")

    def update(self, data):
        if "when_booking" in data:
            self.when_booking = data["when_booking"]

        if "when_invitation" in data:
            self.when_invitation = data["when_invitation"]

        if "booking_reminder" in data:
            self.booking_reminder = data["booking_reminder"]

        if "when_camp_on_booking" in data:
            self.when_camp_on_booking = data["when_camp_on_booking"]

        self.save()


