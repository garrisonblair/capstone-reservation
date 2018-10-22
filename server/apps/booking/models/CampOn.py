from django.db import models
from apps.accounts.models.Student import Student
from apps.booking.models.Booking import Booking
from django.db.models import Q
from datetime import datetime
from django.core.exceptions import ValidationError

class CampOn(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    start_time = models.TimeField(default=datetime.now().strftime("%H:%M"))
    end_time = models.TimeField()

    def save(self, *args, **kwargs):
        self.validate_model()
        super(CampOn, self).save(*args, **kwargs)

    def __str__(self):
        return 'Campon: %d, Student: %s, Booking: %d, Start time: %s, End time: %s' % (self.id, self.student.student_id, self.booking.id, self.start_time, self.end_time)

    def validate_model(self):
        today = datetime.now().strftime("%Y-%m-%d")
        if (self.booking.date!=today):
            raise ValidationError("Camp-on can only be done for today.")
        elif self.start_time >= self.end_time:
            raise ValidationError("End time must be later than the start time")
        elif CampOn.objects.filter(student=self.student,booking=self.booking).exists():
            raise ValidationError("Cannot camp-on the same Booking.")