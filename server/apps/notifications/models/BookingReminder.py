import datetime

from django.db import models

from apps.booking.models.Booking import Booking


class BookingReminderManager(models.Manager):

    def create_reminder(self, booking, remind_time_delta_before):
        reminder = BookingReminder(booking=booking)

        reminder_time = datetime.datetime.combine(booking.date, booking.start_time) - remind_time_delta_before
        reminder.reminder_time = reminder_time

        reminder.save()

        return reminder


class BookingReminder(models.Model):

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)  # type: Booking
    reminder_time = models.DateTimeField()

    objects = BookingReminderManager()

    def remind(self):

        users = list()

        if self.booking.group:
            users = self.booking.group.members
        else:
            users.append(self.booking.booker)

        subject = "Booking Reminder"
        message = "This is a reminder that you have a booking on {} at {} in room {}.".format(self.booking.date,
                                                                                              self.booking.start_time,
                                                                                              self.booking.room.name)

        for user in users:
            greeting = "Hello {}".format(user.first_name)

            full_message = greeting + "\n\n" + message

            user.send_email(subject, full_message)
