from django.contrib import admin
from .models.Booking import Booking
from .models.CampOn import CampOn

# Register your models here.
admin.site.register(Booking)
admin.site.register(CampOn)
