from django.db import models
from apps.accounts.models.Student import Student
from apps.booking.models.Booking import Booking
from django.db.models import Q

class CampOn(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return 'Campon: %d, Student: %s, Booking: %d, Start time: %s, End time: %s' % (self.id, self.student.student_id, self.booking.id, self.start_time, self.end_time)

    def validate_model(self):
        today = datetime.now().strftime("%Y-%m-%d").date()
        if (booking.date!=today):
            raise ValidationError("Camp-on can only be done for today.")
        elif CampOn.objects.filter(student=self.student,booking=self.booking).exists():
            raise ValidationError("Cannot camp-on the same Booking.")