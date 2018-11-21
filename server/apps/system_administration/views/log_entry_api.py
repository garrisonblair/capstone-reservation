from datetime import datetime
from dateutil import parser as date_parser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.admin.models import LogEntry
from django.db.models.query import QuerySet

from ..serializers.log_entry_serializer import LogEntrySerializer


class LogEntryView(APIView):

    def get(self, request):

        # Get query params
        start_datetime = request.GET.get("from")  # Datetime string
        end_datetime = request.GET.get("to")  # Datetime string

        model_id = request.GET.get("content_type_id")  # model content type id
        object_id = request.GET.get("object_id")  # object id
        user_id = request.GET.get("user_id")  # user id

        log_entries = LogEntry.objects.all()  # type: QuerySet

        if start_datetime is not None:
            start_datetime = date_parser.parse(start_datetime, dayfirst=True)
            log_entries = log_entries.filter(action_time__gte=start_datetime)

        if end_datetime is not None:
            end_datetime = date_parser.parse(end_datetime, dayfirst=True)
            log_entries = log_entries.filter(action_time_lte=end_datetime)

        if model_id is not None:
            log_entries = log_entries.filter(content_type=model_id)

        if object_id is not None:
            log_entries = log_entries.filter(object_id=object_id)

        if user_id is not None:
            log_entries = log_entries.filter(user=user_id)

        serializer = LogEntrySerializer(log_entries, many=True)

        return Response(serializer.data)
