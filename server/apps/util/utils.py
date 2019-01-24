from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from apps.accounts.models.User import User


def log_model_change(model_instance, action, user=None):

    if user is None:
        user = get_system_user()

    log_entry = LogEntry.objects.log_action(
        user_id=user.id,
        content_type_id=ContentType.objects.get_for_model(model_instance).pk,
        object_id=model_instance.id,
        object_repr="",
        action_flag=action
    )
    # log_action cuts the object_repr to 200 chars, need to set seperately

    log_entry.object_repr = model_instance.json_serialize()
    log_entry.save()


def get_system_user():
    try:
        user = User.objects.get(username="system_user")

    except User.DoesNotExist:
        user = User.objects.create_user(username="system_user", password="system_user")

    return user
