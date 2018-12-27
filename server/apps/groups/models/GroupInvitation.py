from datetime import datetime

from django.db import models
from apps.accounts.models.Booker import Booker
from .Group import Group


class GroupInvitation(models.Model):

    invited_booker = models.ForeignKey(Booker, related_name="group_invitations")
    group = models.ForeignKey(Group, related_name="invitations")
    timestamp = models.DateTimeField()

    def save(self, *args, **kwargs):

        self.timestamp = datetime.now()
        return super(GroupInvitation, self).save(*args, **kwargs)
