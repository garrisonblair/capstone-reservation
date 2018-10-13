import binascii
import datetime
import os
from django.db import models
from django.contrib.auth.models import User


class VerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, default=None, null=True)
    verification_token = models.CharField(max_length=40, blank=True, primary_key=True)
    expiration = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.verification_token:
            self.verification_token = self.generate_key()

        # Set token expiration to 1 hour
        if not self.expiration:
            self.expiration = datetime.datetime.now() + datetime.timedelta(hours=1)

        return super(VerificationToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.verification_token
