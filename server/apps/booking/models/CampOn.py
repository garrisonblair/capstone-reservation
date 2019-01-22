import json

from django.db import models
from apps.accounts.models.User import User
from apps.booking.models.Booking import Booking
from datetime import datetime
from django.core.exceptions import ValidationError


from apps.accounts.exceptions import PrivilegeError
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory


class CampOn(models.Model):
    booker = models.ForeignKey(User, on_delete=models.CASCADE)
    camped_on_booking = models.ForeignKey(Booking,
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          related_name="camp_ons")

    generated_booking = models.ForeignKey(Booking,
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          blank=True,
                                          related_name="generator_camp_on")
    start_time = models.TimeField()
    end_time = models.TimeField()

    def save(self, *args, **kwargs):
        self.evaluate_privilege()
        self.validate_model()
        super(CampOn, self).save(*args, **kwargs)

    def __str__(self):
        booking_id = ""
        if self.camped_on_booking:
            booking_id = self.camped_on_booking_id
        return 'Campon: {}, Student: {}, Booking: {}, Start time: {}, End time: {},'.format(self.id,
                                                                                            self.booker.username,
                                                                                            booking_id,
                                                                                            self.start_time,
                                                                                            self.end_time)

    def validate_model(self):
        today = datetime.now().today().date()

        if self.camped_on_booking.date != today:
            raise ValidationError("Camp-on can only be done for today.")

        if self.start_time < self.camped_on_booking.start_time or self.start_time >= self.camped_on_booking.end_time:
            raise ValidationError("You can only camp on to an ongoing booking.")

        if self.start_time >= self.end_time:
            raise ValidationError("End time must be later than the start time")

        if self.end_time > self.camped_on_booking.end_time:
            found_bookings = Booking.objects.filter(
                start_time__range=(self.camped_on_booking.end_time, self.end_time)
            )
            if found_bookings is not None:
                raise ValidationError("Camp-on can not end after another booking has started")

        other_campons = CampOn.objects.filter(booker=self.booker, camped_on_booking=self.camped_on_booking)

        if other_campons.count() > 1 or (other_campons.count() is 1 and other_campons[0].id is not self.id):
            raise ValidationError("Cannot camp-on the same Booking more than once.")

    def evaluate_privilege(self):

        # no checks if no category assigned
        if self.booker.get_privileges() is None:
            return

        p_c = self.booker.get_privileges()  # type: PrivilegeCategory

        start_time = p_c.get_parameter("booking_start_time")
        end_time = p_c.get_parameter("booking_end_time")

        # booking_start_time
        if self.start_time < start_time:
            raise PrivilegeError(p_c.get_error_text("booking_start_time"))

        # booking_end_time
        if self.end_time > end_time:
            raise PrivilegeError(p_c.get_error_text("booking_end_time"))

    def json_serialize(self):
        from ..serializers.campon import CampOnSerializer
        return json.dumps(CampOnSerializer(self).data)
