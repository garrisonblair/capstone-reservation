import binascii
import datetime
import os
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class VerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, default=None, null=True)
    token = models.CharField(max_length=40, blank=True, primary_key=True)
    expiration = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_key()

        # Set token expiration to 1 hour
        if not self.expiration:
            self.expiration = timezone.now() + datetime.timedelta(hours=1)

        return super(VerificationToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.token

    @receiver(post_save, sender=User)
    def delete_token(sender, instance, **kwargs):
        if VerificationToken.objects.filter(user=instance).exists():
            token = VerificationToken.objects.get(user=instance)
            token.delete()
