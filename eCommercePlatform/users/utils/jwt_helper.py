import jwt
import datetime
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY

def generate_jwt(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=0, minutes=0, seconds=10),
        'iat': datetime.datetime.now()
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
