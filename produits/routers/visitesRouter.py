""" from ninja import Router
from ninja.errors import HttpError

from authentification.models import Entreprise
from authentification.token import verify_token
from datetime import datetime, timedelta
from django.db.models import Sum
from ..models import Produit, VisiteProduitNumerique,VisiteAcces,VisiteLivre,Acce,ProduitNumerique,Livre



router = Router()

@router.post('enregister_visite', auth=None)
def enregister_Visite(request , id : str):
    print(id)
    acces = Acce.objects.filter(id = id).first()
    livre = Livre.objects.filter(id = id).first()
    produitnumerique = ProduitNumerique.objects.filter(id = id).first()
    
    # Vérifie et enregistre la visite en conséquence
    if acces:
        VisiteAcces.objects.create(produit=acces)
        return {"message": "Visite d'accès enregistrée avec succès." , "status":200}
    elif livre:
        VisiteLivre.objects.create(produit=livre)
        return {"message": "Visite de livre enregistrée avec succès." , "status":200}
    elif produitnumerique:
        VisiteProduitNumerique.objects.create(produit=produitnumerique)
        return {"message": "Visite de produit numérique enregistrée avec succès." , "status":200}
    else:
        return {"message": "Produit non trouvé." , "status":404}



@router.get('recupere_les_visite')
def recupere_les_Visite(request):
    token = request.headers.get("Authorization").split(" ")[1]
    payload = verify_token(token)
    entreprise = Entreprise.objects.get(id = payload.get('entreprise_id'))
    acces = Acce.objects.filter(entreprise = entreprise).first()
    livre = Livre.objects.filter(entreprise = entreprise).first()
    print(livre)
    produitnumerique = ProduitNumerique.objects.filter(entreprise = entreprise).first()

    

    # Obtenir la date actuelle et le début du mois
    today = datetime.now().date()
    start_of_month = today.replace(day=1)

    # Préparer une liste pour stocker les résultats
    results = []

    # Boucle pour chaque jour du mois
    for day in range(1, today.day + 1):
        current_date = start_of_month + timedelta(days=day - 1)
        
        # Calculer les visites pour les Livres
        visites_livres = VisiteLivre.objects.filter(
            produit=livre,
            date=current_date
        ).aggregate(total_visites=Sum('visite'))['total_visites'] or 0

        # Calculer les visites pour les Acces
        visites_acces = VisiteAcces.objects.filter(
            produit=acces,
            date=current_date
        ).aggregate(total_visites=Sum('visite'))['total_visites'] or 0

        # Calculer les visites pour les Produits Numeriques
        visites_numeriques = VisiteProduitNumerique.objects.filter(
            produit=produitnumerique,
            date=current_date
        ).aggregate(total_visites=Sum('visite'))['total_visites'] or 0

        # Calculer le total des visites
        total_visites = visites_livres + visites_acces + visites_numeriques

        # Ajout des données du jour aux résultats
        results.append({
            "day": str(day),
            "visits": total_visites
        })

    return results
 """