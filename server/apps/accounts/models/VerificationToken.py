import binascii
import os
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from datetime import timedelta


class VerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, default=None, null=True)
    token = models.CharField(max_length=40, blank=True, primary_key=True)
    expiration = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_key()

        self.expiration = timezone.now() + timedelta(hours=1)
        print(self.expiration)
        return super(VerificationToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.token

    @receiver(pre_save, sender=User)
    def user_updated(sender, **kwargs):
        user = kwargs.get('instance', None)
        if user:
            new_password = user.password
            try:
                old_password = User.objects.get(pk=user.pk).password
            except User.DoesNotExist:
                old_password = None
            if new_password != old_password:
                if VerificationToken.objects.filter(user=user).exists():
                    token = VerificationToken.objects.get(user=user)
                    token.delete()
