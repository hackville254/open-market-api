# services.py
from uuid import UUID
from clients.models import Commentaire
from clients.schemas.comment_schemas import CommentaireCreation


class CommentaireService:
    @staticmethod
    def creer_commentaire(commentaire_data: CommentaireCreation):
        commentaire = Commentaire.objects.create(
            produit_id=commentaire_data.produit_id,
            entreprise_id=commentaire_data.entreprise_id,
            utilisateur_id=commentaire_data.utilisateur_id,  # L'utilisateur est associé ici
            contenu=commentaire_data.contenu,
        )
        return commentaire

    @staticmethod
    def cacher_commentaire(commentaire_id: UUID):
        commentaire = Commentaire.objects.get(id=commentaire_id)
        commentaire.est_cache = True
        commentaire.save()
        return commentaire

    @staticmethod
    def obtenir_commentaires_pour_produit(produit_id: UUID):
        return Commentaire.objects.filter(produit_id=produit_id, est_cache=False).all()
