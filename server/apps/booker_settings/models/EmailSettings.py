from django.db import models
from apps.accounts.models.User import User


class EmailSettings(models.Model):
    booker = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    when_booking = models.BooleanField(default=True)


    def __str__(self):
        return 'Booker ID:{}, when_booking: {}'.format(self.booker.id, self.when_booking)
