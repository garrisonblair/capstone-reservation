from django.db import models
from apps.accounts.models.User import User
from django.core.exceptions import ValidationError


class EmailSettings(models.Model):
    booker = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    when_booking = models.BooleanField(default=True)


    def __str__(self):
        return 'Booker ID:{}, when_booking: {}'.format(self.booker.id, self.when_booking)

    def save(self, *args, **kwargs):

        self.validate_model()
        this = super(EmailSettings, self).save(*args, **kwargs)
        return this

    def validate_model(self):
        if(not isinstance(self.when_booking, bool)):
            raise ValidationError("'when_booking' must be a boolean")


