from django.contrib import admin
from .models.EmailSettings import EmailSettings


class EmailSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'when_booking')


admin.site.register(EmailSettings, EmailSettingsAdmin)
