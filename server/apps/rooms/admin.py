from django.contrib import admin
from .models.Room import Room
from .models.RoomUnavailability import RoomUnavailability


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'capacity', 'number_of_computers', 'available',
                    'unavailable_start_time', 'unavailable_end_time')


admin.site.register(Room, RoomAdmin)
admin.site.register(RoomUnavailability)
