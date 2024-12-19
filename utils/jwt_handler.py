import jwt
import datetime
from django.conf import settings
from ninja.errors import HttpError

def create_jwt(user):
    payload = {
        'id': str(user.id),
        'email': user.email,
        'is_active': user.is_active,
        'is_suspended': user.is_suspended,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Expire dans 1 heure
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def decode_jwt(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise HttpError("Le token a expiré", status_code=401)
    except jwt.InvalidTokenError:
        raise HttpError("Token invalide", status_code=401)
