from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models.Student import Student
from apps.accounts.models.Room import Room

class Booking(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return 'Student: %s, Room: %r, Date: %d, Start time: %st, End Time: %et' % (self.student, self.room, self.date, self.start_time, self.end_time)
		