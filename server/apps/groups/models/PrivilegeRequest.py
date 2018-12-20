import datetime
from django.db import models

from apps.groups.models.Group import Group
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory


class PrivilegeRequest(models.Model):
    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE)
    privilege_category = models.ForeignKey(PrivilegeCategory, null=True, on_delete=models.CASCADE)
    submission_date = models.DateField(null=True, blank=True)

    PE = 'Pending'
    DE = 'Denied'
    AP = 'Approved'
    STATUS_CHOICES = (
        (PE, 'Pending'),
        (DE, 'Denied'),
        (AP, 'Approved')
    )
    status = models.CharField(
        max_length=8,
        choices=STATUS_CHOICES,
        default=PE
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.submission_date = datetime.datetime.now().date()
            self.status = PrivilegeRequest.PE
        return super(PrivilegeRequest, self).save(*args, **kwargs)
