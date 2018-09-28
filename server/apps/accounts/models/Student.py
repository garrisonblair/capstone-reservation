from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, default=None, null=True)
    student_id = models.TextField(max_length=8, blank=False, primary_key=True)


