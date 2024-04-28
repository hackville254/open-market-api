from ninja import Router, UploadedFile, Form, File
from typing import List
from ..models import Acce, Fichier, Livre, ProduitNumerique
from ..schemas import ModifyProduitDigitalSCHEMA, ProduitNumeriqueSchema, LivreSchema, AccesSchema
from typing import List, Optional

router = Router()

# PRODUIT NUMERIQUE
############
############
############

# Ajouter produit numerique


@router.post('produit_numerique')
def ajouter_produit_numerique(request, data: Form[ProduitNumeriqueSchema], image: UploadedFile, fichiers: List[UploadedFile]):
    token = request.headers.get("Authorization").split(" ")[1]
    produit = ProduitNumerique.objects.create(
        nom_produit=data.nom_produit,
        description=data.description,
        image_presentation=image,
        gratuit=data.gratuit,
        prix_produit=data.prix_produit,
        prix_produit_promotion=data.prix_produit_promotion,
        langue_produit=data.langue_produit,
        categorie_produit=data.categorie_produit,
        taille_Fichier=data.taille_Fichier,
        type=data.type
    )
    if fichiers:
        for f in fichiers:
            Fichier.objects.create(
                produit=produit,
                fichier=f
            )
    return 200

# Modifier un produit numérique


@router.post('/modifier_produit_numerique/{produit_id}')
def modifier_produit_numerique(request, produit_id: str, data: Form[ModifyProduitDigitalSCHEMA], fileId: Optional[List[str]] = None, image: UploadedFile = None, fichiers: List[UploadedFile] = None):
    # Récupérer le produit numérique à modifier par son identifiant
    # Si des données sont fournies, les mettre à jour
    produit = ProduitNumerique.objects.get(id=id)
    print(data)
    if data:
        # Parcourir tous les champs du modèle
        for attr, value in data.dict().items():
            # Vérifier si la nouvelle valeur est différente de la valeur existante et si elle n'est pas nulle
            if value is not None and getattr(produit, attr) != value:
                setattr(produit, attr, value)
    # Si une nouvelle image est fournie, la mettre à jour
    if image:
        produit.image_presentation = image

    # Enregistrer les modifications dans la base de données
    produit.save()

    # Si des nouveaux fichiers sont fournis, les associer au produit
    if fichiers:
        for fileId, f in zip(data.fileId, fichiers):
            if fileId:  # S'il existe un fileId, mettre à jour le fichier existant
                # Recherche du fichier existant par son fileId et l'associer au produit
                fichier_exist = Fichier.objects.get(id=fileId)
                fichier_exist.fichier = f
                fichier_exist.save()
            else:  # Sinon, créer un nouveau fichier et l'associer au produit
                Fichier.objects.create(produit=produit, fichier=f)

    # Retourner une réponse HTTP 200 OK
    return 200

# recuperer un produit numerique ave son <<id>>


@router.get('get_produit_numerique/{produit_id}')
def recuperer_produit_numerique(request, produit_id: str):
    produit = list(ProduitNumerique.objects.filter(
        id=produit_id, supprime=False).values())
    return produit

# supprimer un produit numerique ave son <<id>>


@router.delete('delete_produit_numerique/{produit_id}')
def supprimer_produit_numerique(request, produit_id: str):
    produit = ProduitNumerique.objects.get(id=produit_id)
    produit.supprime = True
    produit.save()
    return 200

