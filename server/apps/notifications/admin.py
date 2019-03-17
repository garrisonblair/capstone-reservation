from django.contrib import admin
from .models.Notification import Notification


class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'range_start', 'range_end', 'minimum_booking_time')


admin.site.register(Notification, NotificationsAdmin)
