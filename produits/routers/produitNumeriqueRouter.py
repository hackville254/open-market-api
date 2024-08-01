from django.db.models.functions import TruncMonth
import json
from ninja import Router, UploadedFile, Form, File
from typing import List
from ninja.errors import HttpError
from datetime import datetime, timedelta
from django.db.models import Count, Sum
from authentification.models import Entreprise
from authentification.token import verify_token
from ..models import Acce, Fichier, Livre, ProduitNumerique, Produit, CHECKOUT
from ..schemas import (
    ModifyProduitDigitalSCHEMA,
    ProduitNumeriqueSchema,
    LivreSchema,
    AccesSchema,
)
from typing import List, Optional
from django.http import JsonResponse
from utils.get_ip_client import *
from utils.get_geo_data import *

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
        client_ip = get_client_ip(request)
        geo_data = get_geo_data(client_ip)
        print(geo_data)
        token = request.headers
        produit = list(Produit.objects.filter(slug=slug , is_visible = True , supprime = False).values())
        p = Produit.objects.get(slug=slug)
        produit[0]['image_presentation'] = p.image_presentation.url
        entreprise = Entreprise.objects.get(nom_entreprise = p.entreprise)
        # Vérifiez si une visite avec la même IP existe déjà pour l'entreprise
        #if not Visite.objects.filter(
        #    entreprise=entreprise, ip_client=client_ip , produit = p
        #).exists():
        #   Visite.objects.create(
        #        entreprise=entreprise,
        #       ip_client=client_ip,
        #        produit=p,
        #       region=geo_data["region"],
        #        pays=geo_data["country"],
        #       ville=geo_data["city"],
        #    )
        return {"status": 200, "produit": produit}
    except Exception as e:
        return HttpError(message="Erreur interne du serveur", status_code=500)


# VISITE
##############
###########
######
""" @router.get("/monthly_stats")
def get_monthly_stats(request):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        payload = verify_token(token)
        entreprise_id = payload.get("entreprise_id")
        entreprise = Entreprise.objects.get(id=entreprise_id)

        # Déterminer les dates du mois courant
        today = datetime.today()
        first_day_of_month = today.replace(day=1)
        current_day_of_month = today.day

        # Récupérer les visites et les ventes du mois jusqu'à aujourd'hui
        visits = Visite.objects.filter(
            date__range=[first_day_of_month, today], entreprise=entreprise
        )
        sales = CHECKOUT.objects.filter(
            date__range=[first_day_of_month, today],
            entreprise=entreprise,
            status="Reussi",
        )

        # Calculer les statistiques de visites par jour
        visit_stats = (
            visits.extra({"day": "date(date)"})
            .values("day")
            .annotate(count=Count("id"))
        )

        # Calculer les statistiques de ventes par jour
        sales_stats = sales.values("date__date").annotate(
            sum=Sum("produit__prix_produit")
        )  # Utilisation de 'produit__prix_produit'

        # Préparer les données pour chaque jour du mois jusqu'à aujourd'hui
        stats = []
        for day in range(1, current_day_of_month + 1):
            date = first_day_of_month + timedelta(days=day - 1)
            day_str = date.strftime("%Y-%m-%d")
            day_visits = next(
                (v["count"] for v in visit_stats if v["day"] == day_str), 0
            )
            day_sales = next(
                (
                    s["sum"]
                    for s in sales_stats
                    if s["date__date"].strftime("%Y-%m-%d") == day_str
                ),
                0,
            )
            stats.append({"day": str(day), "sales": day_sales, "visits": day_visits})

        return {"status": 200, "data": stats}
    except Entreprise.DoesNotExist:
        return {"status": 404, "message": "Entreprise non trouvée"}
    except Exception as e:
        return {"status": 500, "message": f"Erreur interne du serveur: {str(e)}"}
 """
###########
""" @router.get("/yearly_stats")
def get_yearly_stats(request):
    try:
        # Récupérer le token et valider l'entreprise associée
        token = request.headers.get("Authorization").split(" ")[1]
        payload = verify_token(token)
        entreprise_id = payload.get("entreprise_id")
        entreprise = Entreprise.objects.get(id=entreprise_id)

        # Déterminer les dates de début de l'année courante et du jour actuel
        today = datetime.today()
        first_day_of_year = datetime(today.year, 1, 1)
        current_month = today.month

        # Récupérer les visites et les ventes de l'année courante jusqu'au mois actuel inclus
        visits = Visite.objects.filter(
            date__range=[first_day_of_year, today], entreprise=entreprise
        )
        sales = CHECKOUT.objects.filter(
            date__range=[first_day_of_year, today],
            entreprise=entreprise,
            status="Reussi",
        )

        # Calculer les statistiques de visites par mois
        visit_stats = (
            visits.annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(count=Count("id"))
            .values("month", "count")
        )

        # Calculer les statistiques de ventes par mois
        sales_stats = (
            sales.annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(sum=Sum("produit__prix_produit"))
            .values("month", "sum")
        )

        # Préparer les noms des mois pour l'affichage
        month_names = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]

        # Préparer les données pour chaque mois jusqu'au mois actuel inclus
        stats = []
        for month in range(1, current_month + 1):
            month_str = f"{today.year}-{month:02d}"
            month_visits = next(
                (
                    v["count"]
                    for v in visit_stats
                    if v["month"].strftime("%Y-%m") == month_str
                ),
                0,
            )
            month_sales = next(
                (
                    s["sum"]
                    for s in sales_stats
                    if s["month"].strftime("%Y-%m") == month_str
                ),
                0,
            )
            stats.append(
                {
                    "month": month_names[month - 1],
                    "sales": month_sales,
                    "visits": month_visits,
                }
            )

        return {"status": 200, "data": stats}
    except Entreprise.DoesNotExist:
        return {"status": 404, "message": "Entreprise non trouvée"}
    except Exception as e:
        return {"status": 500, "message": f"Erreur interne du serveur: {str(e)}"} """

#############
@router.get("/sales_evolution")
def get_sales_evolution(request):
    try:
        # Récupérer le token et valider l'entreprise associée
        token = request.headers.get("Authorization").split(" ")[1]
        payload = verify_token(token)
        entreprise_id = payload.get("entreprise_id")
        entreprise = Entreprise.objects.get(id=entreprise_id)

        # Déterminer les dates de début de l'année courante et du jour actuel
        today = datetime.today()
        first_day_of_year = datetime(today.year, 1, 1)
        current_month = today.month

        # Récupérer les ventes de l'année courante jusqu'au mois actuel inclus
        sales = CHECKOUT.objects.filter(
            date__range=[first_day_of_year, today],
            entreprise=entreprise,
            status="Reussi",
        )

        # Calculer les statistiques de ventes par mois
        sales_stats = (
            sales.annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(sum=Sum("produit__prix_produit"))
            .values("month", "sum")
        )

        # Préparer les noms des mois pour l'affichage
        month_names = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]

        # Préparer les données pour chaque mois jusqu'au mois actuel inclus
        stats = []
        for month in range(1, current_month + 1):
            month_str = f"{today.year}-{month:02d}"
            month_sales = next(
                (
                    s["sum"]
                    for s in sales_stats
                    if s["month"].strftime("%Y-%m") == month_str
                ),
                0,
            )
            stats.append(
                {
                    "month": month_names[month - 1],
                    "sales": month_sales,
                }
            )

        return {"status": 200, "data": stats}
    except Entreprise.DoesNotExist:
        return {"status": 404, "message": "Entreprise non trouvée"}
    except Exception as e:
        return {"status": 500, "message": f"Erreur interne du serveur: {str(e)}"}
###################
@router.get("/top_selling_products")
def get_top_selling_products(request):
    try:
        # Récupérer le token et valider l'entreprise associée
        token = request.headers.get("Authorization").split(" ")[1]
        payload = verify_token(token)
        entreprise_id = payload.get("entreprise_id")
        entreprise = Entreprise.objects.get(id=entreprise_id)

        # Récupérer les ventes par produit pour l'entreprise
        product_sales = (
            CHECKOUT.objects.filter(entreprise=entreprise, status="Reussi")
            .values("produit__nom_produit")
            .annotate(total_sales=Sum("produit__prix_produit"))
            .order_by("-total_sales")
        )

        # Limiter les résultats aux 11 produits les plus vendus
        top_products = product_sales[:11]

        # Préparer les données dans le format requis
        data = [
            {"product": item["produit__nom_produit"], "sales": item["total_sales"]}
            for item in top_products
        ]

        return {"status": 200, "data": data}
    except Entreprise.DoesNotExist:
        return {"status": 404, "message": "Entreprise non trouvée"}
    except Exception as e:
        return {"status": 500, "message": f"Erreur interne du serveur: {str(e)}"}


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
