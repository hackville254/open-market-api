from ninja import Router, UploadedFile, Form, File
from typing import List
from ninja.errors import HttpError

from authentification.models import Entreprise
from authentification.token import verify_token
from ..models import Acce, Fichier, Livre
from ..schemas import LivreSchema, AccesSchema, ModifyLivre
from typing import List, Optional

router = Router()


@router.post('livres')
def ajouer_un_livre(request, data: Form[LivreSchema], image: UploadedFile, fichiers: List[UploadedFile]):
    token = request.headers.get("Authorization").split(" ")[1]
    payload = verify_token(token)
    e = Entreprise.objects.get(id = payload.get('entreprise_id'))
    livre = Livre.objects.create(
        nom_produit=data.nom_produit,
        entreprise = e,
        description=data.description,
        image_presentation=image,
        gratuit=data.gratuit,
        prix_produit=data.prix_produit,
        prix_produit_promotion=data.prix_produit_promotion,
        langue_produit=data.langue_produit,
        categorie_produit=data.categorie_produit,
        duree_promotion = data.duree_promotion,
        promotion = data.promotion,
        is_visible = data.is_visible,
    )
    if fichiers:
        for f in fichiers:
            livre.taille_Fichier = round(f.size/1048576,2) #Mo
            Fichier.objects.create(
                produit=livre,
                fichier=f
            )
    return 200


@router.post('modifier_un_livre/{livre_id}')
def modifier_un_livre(request, livre_id: str, data: Form[ModifyLivre], image: UploadedFile = None, fichiers: List[UploadedFile] = None):
    # Si des données sont fournies, les mettre à jour
    livre = Livre.objects.get(slug=livre_id)
    print(data)
    if data:
        # Parcourir tous les champs du modèle
        for attr, value in data.dict().items():
            # Vérifier si la nouvelle valeur est différente de la valeur existante et si elle n'est pas nulle
            if value is not None and getattr(livre, attr) != value:
                setattr(livre, attr, value)
    # Si une nouvelle image est fournie, la mettre à jour
    if image:
        livre.image_presentation = image

    # Enregistrer les modifications dans la base de données
    livre.save()

    # Si des nouveaux fichiers sont fournis, les associer au livre
    if fichiers:
        for fileId, f in zip(data.fileId, fichiers):
            if fileId:  # S'il existe un fileId, mettre à jour le fichier existant
                # Recherche du fichier existant par son fileId et l'associer au livre
                livre.taille_Fichier = round(f.size/1048576,2) #Mo
                fichier_exist = Fichier.objects.get(id=fileId)
                fichier_exist.fichier = f
                fichier_exist.save()
            else:  # Sinon, créer un nouveau fichier et l'associer au livre
                Fichier.objects.create(produit=livre, fichier=f)

    # Retourner une réponse HTTP 200 OK
    return 200


@router.get('get_produit_livre/{livre_id}')
def recuperer_un_livre(request, livre_id: str):
    livre = list(Livre.objects.filter(slug=livre_id , supprime=False).values())
    pf = Livre.objects.get(slug = livre_id)
    fichier = list(Fichier.objects.filter(produit = pf).values("fichier"))
    return livre+fichier

# supprimer un livre ave son <<id>>


@router.delete('delete_livre_numerique/{livre_id}')
def supprimer_un_livre_numerique(request, livre_id: str):
    livre = Livre.objects.get(slug=livre_id)
    livre.supprime = True
    livre.save()
    return 200


