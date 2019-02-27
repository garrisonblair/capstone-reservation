from dateutil import parser as date_parser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView
from django.contrib.admin.models import LogEntry
from django.db.models.query import QuerySet

from apps.util.AbstractPaginatedView import AbstractPaginatedView
from rest_framework.pagination import LimitOffsetPagination
from ..serializers.log_entry_serializer import LogEntrySerializer


@permission_classes((IsAuthenticated,))
class LogEntryView(ListAPIView):

    pagination_class = LimitOffsetPagination
    serializer_class = LogEntrySerializer

    def get_queryset(self):
        # Get query params
        start_datetime = self.request.GET.get("from")  # Datetime string
        end_datetime = self.request.GET.get("to")  # Datetime string

        model_id = self.request.GET.get("content_type_id")  # model content type id
        object_id = self.request.GET.get("object_id")  # object id
        user_id = self.request.GET.get("user_id")  # user id

        log_entries = LogEntry.objects.all()  # type: QuerySet

        try:
            if start_datetime is not None:
                start_datetime = date_parser.parse(start_datetime, dayfirst=True)
                log_entries = log_entries.filter(action_time__gte=start_datetime)

            if end_datetime is not None:
                end_datetime = date_parser.parse(end_datetime, dayfirst=True)
                log_entries = log_entries.filter(action_time__lte=end_datetime)

            if model_id is not None:
                log_entries = log_entries.filter(content_type=model_id)

            if object_id is not None:
                log_entries = log_entries.filter(object_id=object_id)

            if user_id is not None:
                log_entries = log_entries.filter(user=user_id)

            log_entries.order_by("action_time")
        except Exception as exception:
            return Response(exception.message, status=status.HTTP_400_BAD_REQUEST)

        return log_entries
