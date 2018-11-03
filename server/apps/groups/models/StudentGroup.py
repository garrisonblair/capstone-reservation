from django.db import models
from apps.accounts.models.Booker import Booker


class StudentGroup(models.Model):
    name = models.CharField(max_length=50)
    students = models.ManyToManyField(Booker)
    is_verified = models.BooleanField(default=False)
