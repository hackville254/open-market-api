import jwt
from datetime import datetime, timedelta, timezone
from ninja.errors import HttpError

from authentification.models import Entreprise
from banque.models import CompteBancaire

# Secret key for signing and verifying tokens
SECRET_KEY = "$ 9@^!Q#7Xp&v$%*+0q1z2m3n4L5K6J7H8G9F0E1D2C3B4A5a6b7c8d9e0f1g2h3i4j5k6l7M8N9O0P!@#$%^&*()"






def create_token(user_id):
    try:
        # Set the expiration time for the token
        

        # Create the payload containing the user ID, user type, and expiration time
        payload = {
            'user_id': user_id,
        }

        # Check if the user is an enterprise
        try:
            entreprise = Entreprise.objects.get(user_id=user_id)
            payload['is_enterprise'] = True
            payload['entreprise_id'] = str(entreprise.id)
            payload['entreprise_name'] = entreprise.nom_entreprise
            # Include additional information about the user's bank account
            compte_bancaire = CompteBancaire.objects.get(entreprise=entreprise)
            payload['compte_bancaire_id'] = str(compte_bancaire.id)
            payload['numero_compte'] = compte_bancaire.numero_compte
            # Add any other necessary information from the CompteBancaire model
            payload['exp'] = datetime.now(timezone.utc) + timedelta(days=1)
        except Entreprise.DoesNotExist:
            payload['is_enterprise'] = False
            payload['exp'] = datetime.now(timezone.utc) + timedelta(days=30)
            

        # Generate the token using the payload and secret key
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return token

    except Exception as e:
        # Handle any exceptions that occur during token creation
        raise HttpError(status_code=500, detail=f"Erreur lors de la création du jeton : {e}")

def verify_token(token):
    try:
        # Verify and decode the token using the secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        return payload

    except jwt.ExpiredSignatureError:
        # Handle the case where the token has expired
        raise HttpError(status_code=401, detail="Le jeton a expiré")
    except jwt.InvalidTokenError:
        # Handle the case where the token is invalid
        raise HttpError(status_code=401, detail="Jeton invalide")
    except Exception as e:
        # Handle any other exceptions that occur during token verification
        raise HttpError(status_code=500, detail=f"Erreur lors de la vérification du jeton : {e}")

