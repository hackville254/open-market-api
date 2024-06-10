import json
from ninja import Router, UploadedFile, Form, File
from typing import List
from ninja.errors import HttpError

from authentification.models import Entreprise
from authentification.token import verify_token
from ..models import Acce, Fichier, Livre, ProduitNumerique, Produit
from ..schemas import (
    ModifyProduitDigitalSCHEMA,
    ProduitNumeriqueSchema,
    LivreSchema,
    AccesSchema,
)
from typing import List, Optional
from django.http import JsonResponse

router = Router()


# GET ALL RECUPERER TOUT LES PRODUITS D'UNE ENTREPRISE
# POUR NE PAS AVOIR DE REDOMDANCE JE PREFERE ECRIRE ICI
###################################
@router.get("getAll")
def recuperer_tout_les_produits_une_entrepise(request):
    token = request.headers.get("Authorization").split(" ")[1]
    payload = verify_token(token)
    e = Entreprise.objects.get(id=payload.get("entreprise_id"))
    lists_produits = []
    produits = Produit.objects.filter(entreprise=e, supprime=False)
    for produit in produits:
        produit_info = {
            "id": produit.id,
            "nom": produit.nom_produit,
            "slug": produit.slug,
            "image": produit.image_presentation.url,
            "gratuit": produit.gratuit,
            "promotion": produit.promotion,
            "prix": produit.prix_produit,
            "status": produit.is_visible,
            "type": produit.categorie_produit,
            "lien": f"shop.op-markets.com/{e.slug}/{produit.slug}",
        }
        lists_produits.append(produit_info)
    return JsonResponse(lists_produits, safe=False)


#######GET BY SLUG RECUPERE UN PRODUIT VIA SON SLUG
@router.get("getby/{slug}")
def get_by_slug(request, slug: str):
    try:
        produit = list(Produit.objects.filter(slug=slug).values())
        if not produit:
            return HttpError(message="Produit non trouvé", status_code=404)
        return {"status": 200, "produit": produit}
    except Exception as e:
        return HttpError(message="Erreur interne du serveur", status_code=500)


#######GET BY SLUG RECUPERE UN PRODUIT VIA SON SLUG POUR LE CHECKOUT
@router.get("getby/{slug}/user", auth=None)
def get_by_slug_by(request, slug: str):
    try:
        token = request.headers
        produit = list(Produit.objects.filter(slug=slug).values())
        produit[0]['image_presentation'] = Produit.objects.get(slug=slug).image_presentation.url
        return {"status": 200, "produit": produit}
    except Exception as e:
        return HttpError(message="Erreur interne du serveur", status_code=500)





# PRODUIT NUMERIQUE
############
############
############

# Ajouter produit numerique


@router.post("produit_numerique")
def ajouter_produit_numerique(
    request,
    data: Form[ProduitNumeriqueSchema],
    image: UploadedFile,
    fichiers: List[UploadedFile],
):
    token = request.headers.get("Authorization").split(" ")[1]
    payload = verify_token(token)
    e = Entreprise.objects.get(id=payload.get("entreprise_id"))
    print("------------------------------------------------")
    print("------------------------------------------------")
    print("------------------------------------------------")
    print("------------------------------------------------")
    print("------------------------------------------------")
    print("------------------------------------------------")

    produit = ProduitNumerique.objects.create(
        nom_produit=data.nom_produit,
        entreprise=e,
        description=str(data.description),
        image_presentation=image,
        gratuit=data.gratuit,
        prix_produit=data.prix_produit,
        prix_produit_promotion=data.prix_produit_promotion,
        duree_promotion=data.duree_promotion,
        langue_produit=data.langue_produit,
        categorie_produit=data.categorie_produit,
        type=data.type,
        promotion=data.promotion,
        is_visible=data.is_visible,
    )
    if fichiers:
        for f in fichiers:
            print(f)
            produit.taille_Fichier = round(f.size / 1048576, 2)  # Mo
            produit.save()
            Fichier.objects.create(produit=produit, fichier=f)
    return 200


# Modifier un produit numérique


@router.post("/modifier_produit_numerique/{produit_id}")
def modifier_produit_numerique(
    request,
    produit_id: str,
    data: Form[ModifyProduitDigitalSCHEMA],
    fileId: Optional[List[str]] = None,
    image: UploadedFile = None,
    fichiers: List[UploadedFile] = None,
):
    try:
        # Récupérer le produit numérique à modifier par son identifiant
        # Si des données sont fournies, les mettre à jour
        produit = ProduitNumerique.objects.get(slug=produit_id)
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
    except ProduitNumerique.DoesNotExist:
        raise HttpError(404, "Produit numérique non trouvé.")
    except Exception as e:
        raise HttpError(
            500,
            "Une erreur s'est produite lors de la modification du produit numérique.",
        )


# recuperer un produit numerique ave son <<id>>


@router.get("get_produit_numerique/{produit_id}")
def recuperer_produit_numerique(request, produit_id: str):
    try:
        produit = list(
            ProduitNumerique.objects.filter(
                slug=produit_id, supprime=False, is_visible=True
            ).values()
        )
        pf = ProduitNumerique.objects.get(slug=produit_id)
        fichier = list(Fichier.objects.filter(produit=pf).values("fichier"))
        return produit + fichier
    except ProduitNumerique.DoesNotExist:
        raise HttpError(404, "Produit numérique non trouvé.")
    except Exception as e:
        raise HttpError(
            500,
            "Une erreur s'est produite lors de la récupération du produit numérique.",
        )


# supprimer un produit numerique ave son <<id>>


@router.delete("delete_produit_numerique/{produit_id}")
def supprimer_produit_numerique(request, produit_id: str):
    try:
        produit = ProduitNumerique.objects.get(slug=produit_id)
        print(produit)
        produit.supprime = True
        produit.save()
        return 200
    except ProduitNumerique.DoesNotExist:
        raise HttpError(404, "Produit numérique non trouvé.")
    except Exception as e:
        raise HttpError(
            500,
            "Une erreur s'est produite lors de la suppression du produit numérique.",
        )
