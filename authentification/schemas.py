from ninja import Schema
from pydantic import validator
from ninja.errors import HttpError
import re
from ninja import ModelSchema

from .models import Entreprise
email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'


class RegisterSchemas(Schema):
    nom: str
    username: str
    motPasse: str
    CmotPasse: str

    @validator('username')
    def validate_email(cls, username):
        if not re.match(email_regex, username):
            raise HttpError(status_code=400,
                            message="L'adresse e-mail n'est pas valide.")
        return username

    @validator('motPasse')
    def validate_motPasse(cls, motPasse):
        if len(motPasse) < 5:
            raise HttpError(
                status_code=400, message="Le mot de passe doit contenir au moins 5 caractères.")
        if not any(char.isupper() for char in motPasse) or not any(char.islower() for char in motPasse):
            raise HttpError(
                status_code=400, message="Le mot de passe doit contenir des caractères en majuscules et en minuscules.")
        return motPasse

    @validator('CmotPasse')
    def validate_CmotPasse(cls, CmotPasse, values, **kwargs):
        if 'motPasse' in values and CmotPasse != values['motPasse']:
            raise HttpError(status_code=400,
                            message="Les mots de passe ne correspondent pas.")
        return CmotPasse


class LoginSchemas(Schema):
    username: str
    motPasse: str


class EntrepriseSchema(ModelSchema):
    email: str
    class Meta:
        model = Entreprise
        exclude = ['id', 'user', 'supprime','devise','slug','date_modification', 'date', 'logo','is_activate','is_private']
    @validator('email')
    def validate_email(cls, email):
        if not re.match(email_regex, email):
            raise HttpError(status_code=400,
                            message="L'adresse e-mail n'est pas valide.")
        return email



class LicenceSchemas(Schema):
    type : str
    prix : str
    periode:str