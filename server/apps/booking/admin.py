from django.contrib import admin
from .models.CampOn import CampOn
from .models.Booking import Booking, RecurringBooking


# Register your models here.
admin.site.register(Booking)
admin.site.register(CampOn)
admin.site.register(RecurringBooking)
