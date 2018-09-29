from django.contrib import admin
from .models.Student import Student
from .models.Room import Room
from .models.Booking import Booking

# Register your models here.
admin.site.register(Student)
admin.site.register(Room)
admin.site.register(Booking)
