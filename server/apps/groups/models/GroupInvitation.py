from datetime import datetime

from django.utils.timezone import make_aware
from django.db import models
from apps.accounts.models.Booker import Booker
from .Group import Group


class GroupInvitation(models.Model):

    invited_booker = models.ForeignKey(Booker, related_name="group_invitations", on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name="invitations", on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    def save(self, *args, **kwargs):

        self.timestamp = make_aware(datetime.now())
        return super(GroupInvitation, self).save(*args, **kwargs)
