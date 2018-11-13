from django.contrib import admin
from .models.Room import Room


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_id', 'capacity', 'number_of_computers')

admin.site.register(Room, RoomAdmin)
