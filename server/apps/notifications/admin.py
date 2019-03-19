from django.contrib import admin
from .models.Notification import Notification
from .models.BookingReminder import BookingReminder


class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'range_start', 'range_end', 'minimum_booking_time')


class BookingReminderAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking')


admin.site.register(Notification, NotificationsAdmin)
admin.site.register(BookingReminder, BookingReminderAdmin)
