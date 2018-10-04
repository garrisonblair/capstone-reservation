from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, default=None, null=True)
    student_id = models.CharField(max_length=8, blank=False, primary_key=True)

    def __str__(self):
        return self.student_id
