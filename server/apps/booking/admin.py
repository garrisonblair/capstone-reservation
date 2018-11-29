from django.contrib import admin
from .models.CampOn import CampOn
from .models.Booking import Booking, RecurringBooking


class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'date', 'start_time', 'end_time', 'booker', 'group', 'recurring_booking')


class CampOnAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time', 'camped_on_booking', 'generated_booking', 'booker')


class RecurringBookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'start_date',
        'end_date',
        'booking_start_time',
        'booking_end_time',
        'room',
        'booker',
        'group',
        'skip_conflicts'
    )


admin.site.register(Booking, BookingAdmin)
admin.site.register(CampOn, CampOnAdmin)
admin.site.register(RecurringBooking, RecurringBookingAdmin)
