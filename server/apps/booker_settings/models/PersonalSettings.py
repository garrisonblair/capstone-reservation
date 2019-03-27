from django.db import models
from apps.accounts.models.User import User
from django.core.exceptions import ValidationError
import re


class PersonalSettings(models.Model):
    booker = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    schedule_vertical = models.BooleanField(default=True)
    booking_color = models.CharField(default="#1F5465", max_length=7, blank=False, null=False)
    campon_color = models.CharField(default="#82220E", max_length=7, blank=False, null=False)
    passed_booking_color = models.CharField(default="#7F7F7F", max_length=7, blank=False, null=False)

    def save(self, *args, **kwargs):

        self.validate_model()
        this = super(PersonalSettings, self).save(*args, **kwargs)
        return this

    def validate_model(self):
        hex_pattern = re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")

        if not hex_pattern.match(self.booking_color):
            raise ValidationError("The format of booking color code is invalid.")

        if not hex_pattern.match(self.campon_color):
            raise ValidationError("The format of campon color code is invalid.")

        if not hex_pattern.match(self.passed_booking_color):
            raise ValidationError("The format of passed booking color code is invalid.")

    def update(self, data):
        if "schedule_vertical" in data:
            self.schedule_vertical = data["schedule_vertical"]

        if "booking_color" in data:
            self.booking_color = data["booking_color"]

        if "campon_color" in data:
            self.campon_color = data["campon_color"]

        if "passed_booking_color" in data:
            self.passed_booking_color = data["passed_booking_color"]

        self.save()
