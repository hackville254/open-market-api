from ninja import Router, UploadedFile, Form, File
from typing import List
from ninja.errors import HttpError

from authentification.models import Entreprise
from authentification.token import verify_token
from ..models import Acce
from ..schemas import LivreSchema, AccesSchema, ModifyLivre
from typing import List, Optional

router = Router()


@router.post('liens')
def ajouer_un_liens(request, data: Form[AccesSchema], image: UploadedFile):
    token = request.headers.get("Authorization").split(" ")[1]
    payload = verify_token(token)
    e = Entreprise.objects.get(id = payload.get('entreprise_id'))
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
        duree_promotion = data.duree_promotion,
        promotion = data.promotion,
        is_visible = data.is_visible,
    )
    return 200



@router.post('modifier_un_lien/{lien_id}')
def modifier_un_lien(request, lien_id: str, data: Form[AccesSchema], image: UploadedFile = None):
    try:
        # Si des données sont fournies, les mettre à jour
        lien = Acce.objects.get(slug=lien_id)
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
    except Acce.DoesNotExist:
        raise HttpError(404, "Lien non trouvé.")
    except Exception as e:
        raise HttpError(500, "Une erreur s'est produite lors de la modification du lien.")


@router.get('get_lien/{lien_id}')
def recuperer_un_lien(request, lien_id: str):
    try:
        lien = list(Acce.objects.filter(slug=lien_id, supprime=False , is_visible = True).values())
        return lien
    except Acce.DoesNotExist:
        raise HttpError(404, "Lien non trouvé.")
    except Exception as e:
        raise HttpError(500, "Une erreur s'est produite lors de la récupération du lien.")


# supprimer un lien ave son <<id>>

@router.delete('delete_lien_numerique/{lien_id}')
def supprimer_un_livre_numerique(request, lien_id: str):
    try:
        lien = Acce.objects.get(slug=lien_id)
        lien.supprime = True
        lien.save()
        return 200
    except Acce.DoesNotExist:
        raise HttpError(404, "Lien non trouvé.")
    except Exception as e:
        raise HttpError(500, "Une erreur s'est produite lors de la suppression du lien.")

