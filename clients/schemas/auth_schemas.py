from pydantic import BaseModel, EmailStr, Field, validator
from ninja.errors import HttpError

class CompteRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @validator('password')
    def validate_password_length(cls, v):
        if len(v) < 8:
            raise HttpError("Le mot de passe doit contenir au moins 8 caractères.", status_code=400)
        return v

    @validator('confirm_password')
    def validate_passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise HttpError("Les mots de passe ne correspondent pas.", status_code=400)
        return v

class CompteLoginSchema(BaseModel):
    email: EmailStr
    password: str

class CompteOutSchema(BaseModel):
    id: str
    email: str
    is_active: bool
    is_suspended: bool

 

class ResetPasswordSchema(BaseModel):
    email: EmailStr

class CompteUpdateSchema(BaseModel):
    old_password: str = Field(..., description="Ancien mot de passe")

    @validator('old_password')
    def validate_old_password_length(cls, v):
        if len(v) < 8:
            raise HttpError("L'ancien mot de passe doit contenir au moins 8 caractères.", status_code=400)
        return v

    new_password: str = Field(..., description="Nouveau mot de passe")

    @validator('new_password')
    def validate_new_password_length(cls, v):
        if len(v) < 8:
            raise HttpError("Le nouveau mot de passe doit contenir au moins 8 caractères.", status_code=400)
        return v

    is_active: bool = Field(None, description="Indique si le compte est actif")
    is_suspended: bool = Field(None, description="Indique si le compte est suspendu")
    ip_address: str = Field(None, description="Adresse IP de l'utilisateur")
