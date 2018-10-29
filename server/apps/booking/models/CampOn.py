from django.db import models
from apps.accounts.models.Student import Student
from apps.booking.models.Booking import Booking
from django.db.models import Q
from datetime import datetime
from django.core.exceptions import ValidationError


class CampOnMangager(models.Manager):
    def create_camp_on(self, student, booking, start_time, end_time):
        pass


class CampOn(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    camped_on_booking = models.ForeignKey(Booking,
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          related_name="camp_ons")

    generated_booking = models.ForeignKey(Booking,
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          related_name="generator_camp_on")
    start_time = models.TimeField()
    end_time = models.TimeField()

    def save(self, *args, **kwargs):
        self.validate_model()
        super(CampOn, self).save(*args, **kwargs)

    def __str__(self):
        return 'Campon: {}, Student: {}, Booking: {}, Start time: {}, End time: {},'.format(self.id,
                                                                                            self.student.student_id,
                                                                                            self.camped_on_booking.id,
                                                                                            self.start_time,
                                                                                            self.end_time)

    def validate_model(self):
        today = datetime.now().strftime("%Y-%m-%d")
        invalid_start_time = datetime.strptime("8:00", "%H:%M").time()
        invalid_end_time = datetime.strptime("23:00", "%H:%M").time()

        if str(self.camped_on_booking.date) != today:
            raise ValidationError("Camp-on can only be done for today.")

        elif self.start_time < self.camped_on_booking.start_time:
            raise ValidationError("Start time has to be in between the selected Booking period.")

        elif self.start_time >= self.camped_on_booking.end_time:
            raise ValidationError("Start time has to be in between the selected Booking period.")

        elif self.end_time < invalid_start_time:
            raise ValidationError("End time cannot be earlier than 8:00.")

        elif self.end_time > invalid_end_time:
            raise ValidationError("End time cannot be later than 23:00.")

        elif self.start_time >= self.end_time:
            raise ValidationError("End time must be later than the start time")

        elif CampOn.objects.filter(student=self.student, booking=self.camped_on_booking).exists():
            raise ValidationError("Cannot camp-on the same Booking.")
