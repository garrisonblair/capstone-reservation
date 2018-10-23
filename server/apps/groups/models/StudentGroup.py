from django.db import models
from apps.accounts.models.Student import Student


class StudentGroup(models.Model):
    name = models.CharField(max_length=50)
    students = models.ManyToManyField(Student)
    is_verified = models.BooleanField(default=False)
