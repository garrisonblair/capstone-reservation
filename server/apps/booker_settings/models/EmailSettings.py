from django.db import models
from apps.accounts.models.User import User


class EmailSettings(models.Model):
    booker = models.ForeignKey(User, on_delete=models.CASCADE)
    when_booking = models.BooleanField(default=True)
