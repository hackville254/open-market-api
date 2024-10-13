from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from ninja.errors import HttpError
from pydantic import ValidationError

from clients.models import Compte
from clients.schemas.auth_schemas import CompteRegisterSchema, CompteUpdateSchema
from django.contrib.auth.models import User


class AuthService:

    @staticmethod
    def register(data: CompteRegisterSchema, ip_address: str):
        global_user = User.objects.filter(username=data.email).exists()
        
        if global_user:
            raise HttpError(
                message=f"{data.email} existe déjà. Merci de changer",status_code=404)
            
        if data.password != data.confirm_password:
            raise HttpError(
                message="Les mots de passe ne correspondent pas", status_code=400)

        # Vérifie si un utilisateur avec cet email existe déjà
        if Compte.objects.filter(email=data.email).exists():
            raise HttpError(
                message=f"{data.email} existe déjà. Merci de changer",status_code=400)

        if Compte.objects.filter(username=data.email).exists():
            raise HttpError(
                message="Un utilisateur avec ce nom d'utilisateur existe déjà", status_code=400)

        try:
            user = Compte.objects.create_user(
                email=data.email,
                username=data.email,  # Utilisation de l'email comme nom d'utilisateur
                password=data.password,
                ip_address=ip_address
            )
        except:
            raise HttpError(
                message=f"Erreur lors de la création de l'utilisateur", status_code=400)

        return user

    @staticmethod
    def login(email: str, password: str):
        # Vérifier si l'utilisateur avec cet email existe
        user = Compte.objects.filter(email=email).first()

        if user is None:
            # L'utilisateur avec cet email n'existe pas
            raise HttpError(
                message="L'adresse e-mail saisie n'est associée à aucun compte. Veuillez vérifier et réessayer.", status_code=401)

        # Vérifier si l'utilisateur est actif
        if not user.is_active:
            # L'utilisateur est inactif
            raise HttpError(
                message="Votre compte est désactivé. Veuillez contacter le support pour assistance.", status_code=401)

        # Vérifier le mot de passe
        if not user.check_password(password):
            raise HttpError(
                message="Le mot de passe saisi est incorrect. Veuillez réessayer.",
                status_code=401)
            # L'utilisateur est authentifié avec succès
        return user

    @staticmethod
    def reset_password(email: str):
        user = Compte.objects.filter(email=email).first()
        if not user:
            raise HttpError("Utilisateur non trouvé", status_code=404)
        new_password = get_random_string(12)
        user.set_password(new_password)
        user.save()

        send_mail(
            'Réinitialisation du mot de passe',
            f'Votre nouveau mot de passe est : {new_password}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return user

    @staticmethod
    def update_user(user: Compte, data: CompteUpdateSchema):
        # Vérifier l'ancien mot de passe
        if not user.check_password(data.old_password):
            raise HttpError("Ancien mot de passe incorrect", status_code=400)

        # Mettre à jour les informations de l'utilisateur
        if data.is_active is not None:
            user.is_active = data.is_active
        if data.is_suspended is not None:
            user.is_suspended = data.is_suspended
        if data.ip_address:
            user.ip_address = data.ip_address

        # Mettre à jour le mot de passe
        user.set_password(data.new_password)

        user.save()
        return user
