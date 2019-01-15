from django.db import models
from django.contrib.auth.models import User as DjangoUser

from apps.accounts.models.User import User

from .PrivilegeCategory import PrivilegeCategory, PrivilegeMerger
from apps.util.AbstractBooker import AbstractBooker

from django.db.models.signals import post_save
from django.dispatch import receiver


class BookerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, default=None, null=True)
    booker_id = models.CharField(max_length=8, blank=True, unique=True, null=True)
    privilege_categories = models.ManyToManyField(PrivilegeCategory)
    secondary_email = models.EmailField(blank=True, default=None, null=True)

    def __str__(self):
        return self.user.username + " profile"


@receiver(post_save, sender=User)
def create_booker_profile(sender, instance, created, **kwargs):
    if created:
        BookerProfile.objects.create(user=instance)


@receiver(post_save, sender=DjangoUser)
def create_booker_profile_alt(sender, instance, created, **kwargs):
    if created:
        BookerProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_booker_profile(sender, instance, **kwargs):
    instance.bookerprofile.save()


@receiver(post_save, sender=DjangoUser)
def save_booker_profile(sender, instance, **kwargs):
    instance = User.cast_django_user(instance)
    instance.bookerprofile.save()
