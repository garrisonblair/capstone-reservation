import json
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from .models.system_settings import SystemSettings
from .models.Announcement import Announcement
from .serializers.announcement import AnnouncementSerializer


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'content',
        'start_date',
        'end_date'
    )

    def log_addition(self, request, object, message):
        """
        Log that an object has been successfully added.
        The default implementation creates an admin LogEntry object.
        """
        from django.contrib.admin.models import LogEntry, ADDITION
        return LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=ContentType.objects.get_for_model(object).pk,
            object_id=object.pk,
            object_repr=json.dumps(AnnouncementSerializer(object).data),
            action_flag=ADDITION,
            change_message=message,
        )

    def log_change(self, request, object, message):
        """
        Log that an object has been successfully added.
        The default implementation creates an admin LogEntry object.
        """
        from django.contrib.admin.models import LogEntry, CHANGE
        return LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=ContentType.objects.get_for_model(object).pk,
            object_id=object.pk,
            object_repr=json.dumps(AnnouncementSerializer(object).data),
            action_flag=CHANGE,
            change_message=message,
        )

    def log_deletion(self, request, object, object_repr):
        """
        Log that an object will be deleted. Note that this method must be
        called before the deletion.
        The default implementation creates an admin LogEntry object.
        """
        from django.contrib.admin.models import LogEntry, DELETION
        return LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=ContentType.objects.get_for_model(object).pk,
            object_id=object.pk,
            object_repr=object_repr,
            action_flag=DELETION,
        )


admin.site.register(SystemSettings)
admin.site.register(LogEntry)
admin.site.register(Announcement, AnnouncementAdmin)
