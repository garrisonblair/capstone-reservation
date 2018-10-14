from django.db import models
from apps.accounts.models.Student import Student
from apps.booking.models.Booking import Booking
from django.db.models import Q

class CampOn(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    start_time = models.TimeField()

    def __str__(self):
        return 'Campon: %d, Student: %s, Booking: %d, Start time: %s' % (self.id, self.student.student_id, self.booking.id, self.start_time)
