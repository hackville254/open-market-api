# https://pypi.org/project/ninja-schema/
from typing import List,Optional
from ninja import ModelSchema,Schema,Field
from pydantic import BaseModel
from .models import Produit, ProduitNumerique, Livre, Acce
from datetime import datetime


class ProduitSchema(ModelSchema):
    class Meta:
        model = Produit
        exclude = ['id','slug', 'image_presentation', 'date_modification','entreprise','taille_Fichier','supprime', 'date','date_modification']


class ProduitNumeriqueSchema(ProduitSchema):
    type: str


class LivreSchema(ProduitSchema):
    #auteur: str
    nombre_page: Optional[int]
    #editeur: str


class AccesSchema(ProduitSchema):
    lien: str

# // SCHEMA POUR LA MODIFICATION DES ELEMENTS
#Optional[bool] = None
class ModifyProduitDigitalSCHEMA(BaseModel):
    nom_produit: Optional[str] = None
    description: Optional[str] = None
    gratuit: Optional[bool] = None
    prix_produit: Optional[float] = None
    prix_produit_promotion: Optional[float] = None
    langue_produit: Optional[str] = None
    categorie_produit: Optional[str] = None
    taille_Fichier: Optional[int] = None
    type: Optional[str] = None
    
    # Ajoutez d'autres champs selon vos besoins

class ModifyLivre(Schema):
    nom_produit: Optional[str]
    description: Optional[str]
    gratuit: Optional[bool]
    prix_produit: Optional[float]
    prix_produit_promotion: Optional[float]
    langue_produit: Optional[str]
    categorie_produit: Optional[str]
    nombre_page: Optional[int]
    # Ajoutez d'autres champs selon vos besoins

class ModifyAcces(Schema):
    nom_produit: Optional[str]
    description: Optional[str]
    gratuit: Optional[bool]
    prix_produit: Optional[float]
    prix_produit_promotion: Optional[float]
    langue_produit: Optional[str]
    categorie_produit: Optional[str]
    taille_Fichier: Optional[int]
    lien: Optional[str]
    delais: Optional[str]
    # Ajoutez d'autres champs selon vos besoins

class CHECKOUTSchema(Schema):
    nom_client : str
    devise_client: str
    id_operateur: int
    type: Optional[str]
    pays_client: str
    montant: float
    moyen_de_paiement: str
    numero: Optional[str]
    email: str
    codeOtp: Optional[str]
    
    
class MySoleaPay(Schema):
    operator : int
    customer_number : str
    amount:float
    