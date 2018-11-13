from django.contrib import admin
from .models.Room import Room


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'capacity', 'number_of_computers')

admin.site.register(Room, RoomAdmin)
