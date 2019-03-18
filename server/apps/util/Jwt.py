import jwt
import time
import os


def generateToken(user):
    now = int(time.time())
    token={
        "iat": now,
        "exp": now + 10, #3600 * 2,  # 2 hours
        "user_id": user.id
    }
    secret_key = os.environ.get('SECRET_KEY')
    token = jwt.encode(token, secret_key, algorithm="HS256")

    return token

