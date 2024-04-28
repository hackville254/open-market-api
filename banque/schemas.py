from ninja import ModelSchema
from pydantic import BaseModel,Field

from .models import CompteBancaire, Transaction

class CompteBancaireShema(ModelSchema):
    class Meta:
        model = CompteBancaire
        fields = ['numero_operateur']
        
        
class TransactionSchema(BaseModel):
    montant : float = Field(..., description="Le montant de la transaction")
    numero_compte_source : str = Field(..., description="L'identifiant du compte qui envoie")
    numero_compte_destination : str = Field(..., description="L'identifiant du compte qui recois")