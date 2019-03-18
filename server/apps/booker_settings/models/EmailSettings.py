from django.db import models
from apps.accounts.models.User import User
from django.core.exceptions import ValidationError


class EmailSettings(models.Model):
    booker = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    when_booking = models.BooleanField(default=True)
    when_recurring_booking = models.BooleanField(default=True)
    when_delete_booking = models.BooleanField(default=True)
    when_delete_recurring_booking = models.BooleanField(default=True)
    when_camp_on_booking = models.BooleanField(default=True)


    def __str__(self):
        return 'Booker ID:{}, when_booking: {}'.format(self.booker.id, self.when_booking)

    def save(self, *args, **kwargs):

        self.validate_model()
        this = super(EmailSettings, self).save(*args, **kwargs)
        return this

    def validate_model(self):
        if(not isinstance(self.when_booking, bool)):
            raise ValidationError("'when_booking' must be a boolean")

        if(not isinstance(self.when_recurring_booking, bool)):
            raise ValidationError("'when_recurring_booking' must be a boolean")

        if(not isinstance(self.when_delete_booking, bool)):
            raise ValidationError("'when_delete_booking' must be a boolean")

        if(not isinstance(self.when_delete_recurring_booking, bool)):
            raise ValidationError("'when_delete_recurring_booking' must be a boolean")

        if(not isinstance(self.when_camp_on_booking, bool)):
            raise ValidationError("'when_camp_on_booking' must be a boolean")

    def update(self, data):
        if "when_booking" in data:
            self.when_booking = data["when_booking"]

        if "when_recurring_booking" in data:
            self.when_recurring_booking = data["when_recurring_booking"]

        if "when_delete_booking" in data:
            self.when_delete_booking = data["when_delete_booking"]

        if "when_delete_recurring_booking" in data:
            self.when_delete_recurring_booking = data["when_delete_recurring_booking"]

        if "when_camp_on_booking" in data:
            self.when_camp_on_booking = data["when_camp_on_booking"]

        self.save()


