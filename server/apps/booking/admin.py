from django.contrib import admin
from .models.Booking import Booking, RecurringBooking

# Register your models here.
admin.site.register(Booking)
admin.site.register(RecurringBooking)
