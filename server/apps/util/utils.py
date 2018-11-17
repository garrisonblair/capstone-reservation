from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType


def log_model_change(model_instance, action, user):
    LogEntry.objects.log_action(
        user_id=user.id,
        content_type_id=ContentType.objects.get_for_model(model_instance).pk,
        object_id=model_instance.id,
        object_repr=model_instance.__str__(),
        action_flag=action
    )
