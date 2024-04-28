from ninja import Router, UploadedFile, Form, File
from typing import List

from authentification.models import Entreprise
from authentification.token import verify_token
from ..models import Acce, Fichier, Livre
from ..schemas import LivreSchema, AccesSchema, ModifyLivre
from typing import List, Optional

router = Router()


@router.post('liens')
def ajouer_un_liens(request, data: Form[AccesSchema], image: UploadedFile):
    token = request.headers.get("Authorization").split(" ")[1]
    payload = verify_token(token)
    e = Entreprise.object.get(id = payload['entreprise_id'])
    lien = Acce.objects.create(
        nom_produit=data.nom_produit,
        entreprise = e,
        description=data.description,
        image_presentation=image,
        gratuit=data.gratuit,
        prix_produit=data.prix_produit,
        prix_produit_promotion=data.prix_produit_promotion,
        langue_produit=data.langue_produit,
        categorie_produit=data.categorie_produit,
        lien=data.lien,
        delais=data.delais,
    )
    return 200



@router.post('modifier_un_lien/{lien_id}')
def modifier_un_lien(request, lien_id: str, data: Form[AccesSchema], image: UploadedFile = None):
    # Si des données sont fournies, les mettre à jour
    lien = Acce.objects.get(id=lien_id)
    print(data)
    if data:
        # Parcourir tous les champs du modèle
        for attr, value in data.dict().items():
            # Vérifier si la nouvelle valeur est différente de la valeur existante et si elle n'est pas nulle
            if value is not None and getattr(lien, attr) != value:
                setattr(lien, attr, value)
    # Si une nouvelle image est fournie, la mettre à jour
    if image:
        lien.image_presentation = image

    # Enregistrer les modifications dans la base de données
    lien.save()

    # Retourner une réponse HTTP 200 OK
    return 200


@router.get('lien/{lien_id}')
def recuperer_un_lien(request, lien_id: str):
    lien = list(Livre.objects.filter(id=lien_id).values())
    return lien



# supprimer un livre ave son <<id>>

@router.delete('delete_lien_numerique/{lien_id}')
def supprimer_un_livre_numerique(request, lien_id: str):
    lien = Livre.objects.get(id=lien_id)
    lien.supprime = True
    lien.save()
    return 200


