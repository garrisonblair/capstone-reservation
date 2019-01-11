from django.db import models
from django.contrib.auth.models import User as DjangoUser

from apps.accounts.models.User import User

from .PrivilegeCategory import PrivilegeCategory, PrivilegeMerger
from apps.util.AbstractBooker import AbstractBooker

from django.db.models.signals import post_save
from django.dispatch import receiver


class BookerProfile(models.Model, AbstractBooker):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, default=None, null=True)
    booker_id = models.CharField(max_length=8, blank=True, unique=True, null=True)
    privilege_categories = models.ManyToManyField(PrivilegeCategory)

    def get_privileges(self):

        if self.privilege_categories.all().count() is 0:
            return None

        return PrivilegeMerger(list(self.privilege_categories.all()))

    def get_bookings(self):
        return self.booking_set

    def __str__(self):
        return self.user.username + " profile"


@receiver(post_save, sender=DjangoUser)
def create_booker_profile(sender, instance, created, **kwargs):
    if created:
        BookerProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_booker_profile(sender, instance, **kwargs):
    instance.bookerprofile.save()
