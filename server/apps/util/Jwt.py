import jwt
import json
import time
import os
from rest_framework.exceptions import PermissionDenied
from django.conf import settings


def generateToken(user):
    now = int(time.time())
    token={
        "iss": "{}://{}".format(settings.ROOT_PROTOCOL,settings.ROOT_URL),
        "iat": now,
        "exp": now + 86400 , # 1 day
        "user_id": user.id
    }
    secret_key = os.environ.get('SECRET_KEY')
    token = jwt.encode(token, secret_key, algorithm="HS256")
    token = token.decode("utf8")
    return token


def getUserFromToken(token):
    from apps.accounts.models.User import User
    secret_key = os.environ.get('SECRET_KEY')
    try:
        decoded = jwt.decode(token, secret_key)
    except jwt.ExpiredSignatureError:
        raise PermissionDenied('URL expired. Please log in again.')
    except jwt.InvalidTokenError:
        raise PermissionDenied('Invalid token. We cannot find you in the system.')

    user = User.objects.get(id=decoded['user_id'])

    return user
