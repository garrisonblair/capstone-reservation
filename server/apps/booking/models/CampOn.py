from django.db import models
from apps.accounts.models.Booker import Booker
from apps.booking.models.Booking import Booking
from datetime import datetime
from django.core.exceptions import ValidationError


class CampOn(models.Model):
    booker = models.ForeignKey(Booker, on_delete=models.CASCADE)
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
                                                                                            self.booker.booker_id,
                                                                                            self.camped_on_booking.id,
                                                                                            self.start_time,
                                                                                            self.end_time)

    def validate_model(self):
        today = datetime.now().today().date()
        invalid_start_time = datetime.strptime("8:00", "%H:%M").time()
        invalid_end_time = datetime.strptime("23:00", "%H:%M").time()

        if self.camped_on_booking.date != today:
            raise ValidationError("Camp-on can only be done for today.")

        elif self.start_time < self.camped_on_booking.start_time or self.start_time >= self.camped_on_booking.end_time:
            raise ValidationError("You can only camp on to an ongoing booking.")

        elif self.end_time < invalid_start_time:
            raise ValidationError("End time cannot be earlier than 8:00.")

        elif self.end_time > invalid_end_time:
            raise ValidationError("End time cannot be later than 23:00.")

        elif self.start_time >= self.end_time:
            raise ValidationError("End time must be later than the start time")

        elif self.end_time > self.camped_on_booking.end_time:
            found_bookings = Booking.objects.filter(
                start_time__range=(self.camped_on_booking.end_time, self.end_time))
            if found_bookings is not None:
                raise ValidationError("Camp-on can not end after another booking has started")

        elif CampOn.objects.filter(booker=self.booker, camped_on_booking=self.camped_on_booking).exists():
            raise ValidationError("Cannot camp-on the same Booking.")
