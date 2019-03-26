from django.contrib import admin
from .models.EmailSettings import EmailSettings
from .models.PersonalSettings import PersonalSettings


class EmailSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'when_booking')


admin.site.register(EmailSettings, EmailSettingsAdmin)
admin.site.register(PersonalSettings)
