import datetime

from django.db import models

from apps.booking.models.Booking import Booking
from apps.system_administration.models.system_settings import SystemSettings
from apps.util.ModelObserver import ModelObserver
from apps.notifications.apps import NotificationsConfig
from apps.booker_settings.models.EmailSettings import EmailSettings


class BookingReminderManager(models.Manager, ModelObserver):

    def create_reminder(self, booking, remind_time_delta_before=None):

        if remind_time_delta_before is None:
            settings = SystemSettings.get_settings()
            remind_time_delta_before = settings.default_time_to_notify_before_booking

        reminder = BookingReminder(booking=booking)

        reminder_time = datetime.datetime.combine(booking.date, booking.start_time) - remind_time_delta_before
        reminder.reminder_time = reminder_time

        reminder.save()

        return reminder

    def send_reminders(self):

        now = datetime.datetime.now()
        print(now)

        # lower bound prevents sending mass reminders if reminders are turned off for a while.
        # They would accumulate and get sent all at once when the feature is turned on.
        lower_bound = now - datetime.timedelta(minutes=NotificationsConfig.booking_reminder_interval_minutes + 1)
        print(lower_bound)
        reminders = self.filter(reminder_time__lte=now, reminder_time__gte=lower_bound)

        for reminder in reminders:
            reminder.send()

        old_reminders = self.filter(reminder_time__lt=lower_bound)
        for reminder in old_reminders:
            reminder.delete()

    def subject_created(self, subject):
        self.create_reminder(subject)

    def subject_updated(self, subject):
        pass

    def subject_deleted(self, subject):
        reminders_for_booking = self.filter(booking=subject)

        for reminder in reminders_for_booking:
            reminder.delete()


class BookingReminder(models.Model):

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)  # type: Booking
    reminder_time = models.DateTimeField()

    objects = BookingReminderManager()

    def send(self):

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
            email_settings = EmailSettings.objects.get_or_create(booker=user)[0]
            if email_settings.booking_reminder:
                greeting = "Hello {}".format(user.first_name)
                full_message = greeting + "\n\n" + message
                user.send_email(subject, full_message)

        self.delete()
