from ninja import Router, UploadedFile, Form, File
from typing import List
from ..models import Acce, Fichier, Livre
from ..schemas import LivreSchema, AccesSchema, ModifyLivre
from typing import List, Optional

router = Router()


@router.post('livres')
def ajouer_un_livre(request, data: Form[LivreSchema], image: UploadedFile, fichiers: List[UploadedFile]):
    livre = Livre.objects.create(
        nom_produit=data.nom_produit,
        description=data.description,
        image_presentation=image,
        gratuit=data.gratuit,
        prix_produit=data.prix_produit,
        prix_produit_promotion=data.prix_produit_promotion,
        langue_produit=data.langue_produit,
        categorie_produit=data.categorie_produit,
        taille_Fichier=data.taille_Fichier,
        nombre_page=data.nombre_page,
    )
    if fichiers:
        for f in fichiers:
            Fichier.objects.create(
                produit=livre,
                fichier=f
            )
    return 200


@router.post('modifier_un_livre/{livre_id}')
def modifier_un_livre(request, livre_id: str, data: Form[ModifyLivre], image: UploadedFile = None, fichiers: List[UploadedFile] = None):
    # Si des données sont fournies, les mettre à jour
    livre = Livre.objects.get(id=livre_id)
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
                fichier_exist = Fichier.objects.get(id=fileId)
                fichier_exist.fichier = f
                fichier_exist.save()
            else:  # Sinon, créer un nouveau fichier et l'associer au livre
                Fichier.objects.create(produit=livre, fichier=f)

    # Retourner une réponse HTTP 200 OK
    return 200


@router.get('livres/{livre_id}')
def recuperer_un_livre(request, livre_id: str):
    livre = list(Livre.objects.filter(id=livre_id).values())
    return livre

# supprimer un livre ave son <<id>>


@router.delete('delete_livre_numerique/{livre_id}')
def supprimer_un_livre_numerique(request, livre_id: str):
    livre = Livre.objects.get(id=livre_id)
    livre.supprime = True
    livre.save()
    return 200


