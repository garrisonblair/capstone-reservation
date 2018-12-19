import datetime
from django.db import models

from apps.groups.models.Group import Group
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory


class PrivilegeRequest(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    privilege_category = models.ForeignKey(PrivilegeCategory, on_delete=models.CASCADE)
    submission_date = models.DateField()
    STATUS_CHOICES = (
        ('PE', "Pending"),
        ('DE', "Denied"),
        ('AP', "Approved")
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='PE'
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.submission_date = datetime.datetime.now().date()
            return super(PrivilegeRequest, self).save(*args, **kwargs)
