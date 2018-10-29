from django.db import models
from apps.accounts.models.Student import Student
from apps.booking.models.Booking import Booking
from django.core.exceptions import ValidationError


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
        if self.start_time < self.camped_on_booking.start_time:
            raise ValidationError("Start time has to be in between the selected Booking period.")

        elif self.start_time >= self.camped_on_booking.end_time:
            raise ValidationError("Start time has to be in between the selected Booking period.")

        elif self.start_time >= self.end_time:
            raise ValidationError("End time must be later than the start time")

        elif self.end_time > self.camped_on_booking.end_time:
            found_bookings = Booking.objects.filter(
                start_time__range=(self.camped_on_booking.end_time, self.end_time))
            if found_bookings is not None:
                raise ValidationError("Camp-on can not end after another booking has started")

        elif CampOn.objects.filter(student=self.student, camped_on_booking=self.camped_on_booking).exists():
            raise ValidationError("Cannot camp-on the same Booking.")
