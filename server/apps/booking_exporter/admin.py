from django.contrib import admin
from .models.bookingExporterModels import ExternalRoomID
from .models.EmailId import EmailId

admin.site.register(ExternalRoomID)
admin.site.register(EmailId)
