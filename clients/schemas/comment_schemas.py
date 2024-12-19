# schemas.py
from pydantic import BaseModel
from uuid import UUID

class CommentaireCreation(BaseModel):
    produit_id: UUID
    entreprise_id: UUID
    utilisateur_id: UUID  # Ajoutez le champ utilisateur_id
    contenu: str

class CommentaireResponse(BaseModel):
    id: UUID
    produit_id: UUID
    entreprise_id: UUID
    utilisateur_id: UUID  # Ajoutez le champ utilisateur_id
    contenu: str
    est_cache: bool
    cree_a: str
    mis_a_jour_a: str
