# routers.py
from ninja import Router
from uuid import UUID
from ninja.errors import HttpError

from authentification.models import Entreprise
from authentification.token import verify_token
from clients.schemas.comment_schemas import CommentaireCreation, CommentaireResponse
from clients.services.comment_service import CommentaireService
from utils.jwt_handler import decode_jwt

router = Router()

@router.post('/commentaires/', response_model=CommentaireResponse)
def creer_commentaire(request, commentaire_data: CommentaireCreation):
    # Récupérer le token des cookies
    token = request.COOKIES.get('token')
    if not token:
        raise HttpError(message="Token non fourni", status_code=401)

    user_data = decode_jwt(token)  # Décode le token pour obtenir les données utilisateur

    # Vérifiez que l'utilisateur est actif
    if not user_data.get("is_active"):
        raise HttpError(message="Utilisateur inactif", status_code=403)

    commentaire = CommentaireService.creer_commentaire(commentaire_data, user_data)
    return commentaire

@router.patch('/commentaires/{commentaire_id}/cacher', response_model=CommentaireResponse)
def cacher_commentaire(request, commentaire_id: UUID):
    # Récupérer le token des cookies
    token = request.headers.get("Authorization").split(" ")[1]
    if not token:
        raise HttpError(message="Token non fourni", status_code=401)

    payload = verify_token(token)
    entreprise_id = payload.get("entreprise_id")
    entreprise = Entreprise.objects.filter(id=entreprise_id).exists()
    if not entreprise:
        raise HttpError(message="Utilisateur inactif", status_code=403)

    commentaire = CommentaireService.cacher_commentaire(commentaire_id)
    return commentaire

@router.get('/commentaires/produit/{produit_id}/', response_model=list[CommentaireResponse])
def obtenir_commentaires(request, produit_id: UUID):
    # Pas besoin de vérification du token ici, car nous ne modifions pas l'état
    commentaires = CommentaireService.obtenir_commentaires_pour_produit(produit_id)
    return commentaires
