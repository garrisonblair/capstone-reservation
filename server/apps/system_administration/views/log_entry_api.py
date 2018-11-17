from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.admin.models import LogEntry

from ..serializers.log_entry_serializer import LogEntrySerializer


class LogEntryView(APIView):

    def get(self, request):
        log_entries = LogEntry.objects.all()

        serializer = LogEntrySerializer(log_entries, many=True)

        return Response(serializer.data)
