from authentification.models import Entreprise
from authentification.token import verify_token
from produits.models import Visite, VisiteMultiple
from produits.schemas import VisiteData
from django.db.models import Q, F, Count
from ninja import Router

router = Router()

@router.get("/visites/unique")
def get_visites(request):
    # Vérification du token d'authentification
    token = request.headers.get("Authorization").split(" ")[1]
    payload = verify_token(token)
    entreprise_id = payload.get("entreprise_id")

    # Récupération de l'entreprise associée au token
    entreprise = Entreprise.objects.get(id=entreprise_id)

    # Récupération des visites pour l'entreprise
    visites = Visite.objects.filter(entreprise=entreprise).order_by('date')


    # Regroupement des visites par produit, date, ville, région et pays
    visites_groupées =  visites.values('produit__nom_produit', 'date', 'ville','region', 'pays').annotate(unique_visits=Count('id', distinct=True))


    # Sérialisation des données en utilisant le modèle VisiteData
    data = []
    for visite in visites_groupées:
        data.append(VisiteData(
            product=visite['produit__nom_produit'],
            uniqueVisits=visite['unique_visits'],
            region=visite['region'],
            country=visite['pays'],
            city=visite['ville'],
            date=visite['date'].isoformat()
        ))

    return data




@router.get("/visites/multiple")
def get_visites_multiple(request):
    # Vérification du token d'authentification
    token = request.headers.get("Authorization").split(" ")[1]
    payload = verify_token(token)
    entreprise_id = payload.get("entreprise_id")

    # Récupération de l'entreprise associée au token
    entreprise = Entreprise.objects.get(id=entreprise_id)

    # Récupération des visites pour l'entreprise, regroupées par produit, ville, région, pays et date
    visites = VisiteMultiple.objects.filter(entreprise=entreprise) \
       .values('produit__nom_produit', 'produit', 'ville','region', 'pays', 'date__date') \
       .annotate(multiple_visits=Count('id')) \
       .order_by('date__date')

    # Sérialisation des données en utilisant le modèle VisiteData
    data = []
    for visite in visites:
        data.append(VisiteData(
            product=visite['produit__nom_produit'],
            uniqueVisits=visite['multiple_visits'],
            region=visite['region'],
            country=visite['pays'],
            city=visite['ville'],
            date=visite['date__date'].isoformat()
        ))

    return data
