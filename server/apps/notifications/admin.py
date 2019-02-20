from django.contrib import admin
from .models.Notification import Notification


class NotificationsAdmin(admin.ModelAdmin):
    # list_display = ('id', 'name', 'capacity', 'number_of_computers')


admin.site.register(Notification, NotificationsAdmin)
