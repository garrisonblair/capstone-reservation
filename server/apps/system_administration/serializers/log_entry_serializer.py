from rest_framework.serializers import ModelSerializer
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType


class ContentTypeSerializer(ModelSerializer):

    class Meta:
        model = ContentType
        fields = '__all__'


class LogEntrySerializer(ModelSerializer):

    content_type = ContentTypeSerializer()

    class Meta:
        model = LogEntry
        fields = '__all__'
