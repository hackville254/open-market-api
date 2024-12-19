from uuid import UUID
from django.shortcuts import get_object_or_404
from ninja import Router
from typing import List
from ninja.errors import HttpError
from authentification.models import Entreprise
from authentification.token import verify_token
from marketing.models import FacebookPixel
from marketing.schemas import FacebookPixelIn, FacebookPixelOut
from produits.models import Produit

router = Router()

# POST: Créer un FacebookPixel


@router.post("{produit_id}/create")
def create_facebook_pixel(request, produit_id: UUID, pixel_data: FacebookPixelIn):

    # Récupérer le token depuis les headers
    token = request.headers.get("Authorization").split(" ")[1]

    # Vérifier et décoder le token
    decoded_token = verify_token(token)

    # Récupérer l'entreprise à partir du token
    entreprise = Entreprise.objects.get(id=decoded_token.get('entreprise_id'))

    # Récupérer le produit
    produit = get_object_or_404(Produit, id=produit_id)
    # Vérifier si un FacebookPixel avec ce pixel_id existe déjà pour le même produit et entreprise
    existing_pixel = FacebookPixel.objects.filter(
        pixel_id=pixel_data.pixel_id
    ).first()

    if existing_pixel:
        # Lever une exception HttpError si le pixel existe déjà
        raise HttpError(
            status_code=400,
            message="Un pixel avec ce pixel_id existe déja."
        )

    # Créer un FacebookPixel
    pixel = FacebookPixel.objects.create(
        entreprise=entreprise,
        produit=produit,
        pixel_id=pixel_data.pixel_id
    )

    # Retourner le pixel créé
    return {
        "pixel_id": pixel.pixel_id
    }

# GET ALL: Récupérer tous les pixels


@router.get("all")
def get_all_pixels(request):
    pixels = FacebookPixel.objects.all()
    return [
        {
            "product_id": pixel.produit.id,
            "produit": pixel.produit.nom_produit,
            "pixel_id": pixel.pixel_id,
        }
        for pixel in pixels
    ]

# GET: Récupérer un pixel spécifique par ID

@router.get("{produit_id}", response={200: dict}, auth = None)
def get_pixel(request, produit_id: UUID):
    # Récupérer l'objet FacebookPixel en fonction du produit_id
    produit = Produit.objects.filter(id = produit_id).first()
    pixel = get_object_or_404(FacebookPixel, produit=produit)
    
    print(pixel.pixel_id)
    # Retourner l'ID du pixel dans un dictionnaire
    return { "pixel_id": pixel.pixel_id }

# DELETE: Supprimer un pixel par ID


@router.delete("{pixel_id}/delete", response={204: None})
def delete_pixel(request, pixel_id: str):
    pixel = get_object_or_404(FacebookPixel, pixel_id=pixel_id)
    pixel.delete()
    return 204
