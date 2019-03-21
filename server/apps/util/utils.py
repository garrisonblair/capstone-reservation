import random
import string
import datetime

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

    log_entry.change_message = model_instance.json_serialize()
    log_entry.save()


def get_system_user(username="system_user"):

    try:
        user = User.objects.get(username=username)

    except User.DoesNotExist:

        password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))

        user = User.objects.create_user(username=username, password=password)

    return user


def get_rounded_time(minute):
    time = datetime.datetime.now().replace(microsecond=0)
    discard = datetime.timedelta(
        minutes=time.minute % minute,
        seconds=time.second,
        microseconds=time.microsecond
    )
    time -= discard
    if discard >= datetime.timedelta(minutes=minute/2):
        time += datetime.timedelta(minutes=minute)
    return time
