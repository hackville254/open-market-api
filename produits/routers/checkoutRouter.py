from ninja import Router
from authentification.models import Entreprise
from banque.models import (
    PaiementEchoue,
    CompteBancaire,
    PaiementReussi,
    Retrait,
    Historique,
)
from ..models import Acce, Fichier, Livre, ProduitNumerique, Produit, CHECKOUT
from ..schemas import CHECKOUTSchema, MySoleaPay
from decouple import config
import requests
import json
from authentification.token import verify_token
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta,datetime
from utils.send_email import send_emailB

router = Router()

# BASE_URL = "https://soleaspay.com/api/agent/sandbox"
BASE_URL = "https://soleaspay.com/api/"


@router.get("paiement")
def getPayement(request):
    token = request.headers.get("Authorization").split(" ")[1]
    payload = verify_token(token)
    e = Entreprise.objects.get(id=payload.get("entreprise_id"))
    c = list(
        CHECKOUT.objects.filter(entreprise=e).values(
            "produit__nom_produit",
            "nom_client",
            "status",
            "email",
            "type",
            "pays_client",
            "date",
        )
    )
    return {"status": 200, "data": c}


@router.post("checkout/user/{entreprise_slug}/{slug}", auth=None)
def checkout_produit(request, entreprise_slug: str, slug: str, data: CHECKOUTSchema):
    print("debut requette")
    entreprise = Entreprise.objects.get(slug=entreprise_slug)
    produit = Produit.objects.get(slug=slug)
    checkout = CHECKOUT.objects.create(
        produit=produit,
        entreprise=entreprise,
        nom_client=data.nom_client,
        devise_client=data.devise_client,
        pays_client=data.pays_client,
        moyen_de_paiement=data.moyen_de_paiement,
        numero=data.numero,
        email=data.email,
        codeOtp=data.codeOtp,
        orderId=data.orderId,
    )
    url = f"{BASE_URL}agent/bills"
    #url = f"{BASE_URL}"
    order_id = data.orderId

    headers = {
        "x-api-key": config("X-API-KEY"),
        "operation": "2",
        "service": str(data.id_operateur),
        "Content-Type": "application/json",
        "otp": data.codeOtp,
    }

    if data.numero:
        wallet = data.numero
    else:
        wallet = data.email

    payload = {
        "wallet": wallet,
        "amount": float(data.montant),
        "currency": data.devise_client,
        "order_id": order_id,
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.text)
    response_data = json.loads(response.text)
    response_data["order_id"] = order_id
    print("-------------------------------")
    print("-------------------------------")
    print("-------------------------------")
    if response_data.get("success") == False:
        checkout.status = "Echec"
        checkout.save()
        token = response_data.get("payToken") or response_data.get("message")
        PaiementEchoue.objects.create(token=token, checkout=checkout)
        return {
            "status": 400,
            "message": "Votre paiement a échoué. Merci de réessayer.",
        }
    if response_data["data"]["payLink"]:
        payUrl = response_data["data"]["payLink"]
        print(payUrl)
        return {"status": 201, "url": payUrl}
    return {"status": 200}


verify_url = "https://soleaspay.com/api/agent/verif-pay"


@router.get("verify_payment/{orderId}", auth=None)
def verify_payment_router(request, orderId: str):
    checkhout = CHECKOUT.objects.get(orderId=orderId)
    if checkhout.status == "Reussi":
        PaiementReussi.objects.create(checkout=checkhout)
        return {"status": 200, "message": "votre produit a ete envoyer par email"}
    else:
        return {"status": 403}


@router.get("donwload/{orderId}", auth=None)
def donwloadFile(request, orderId: str):
    data = []
    checkhout = CHECKOUT.objects.get(orderId=orderId)
    produit = checkhout.produit
    if produit.categorie_produit != "lien":
        files = Fichier.objects.filter(produit=produit.id)
        for file in files:
            data.append({"fichier": file.fichier.url})
        print("url du produit", data)
        return {"type": "produit_digital", "data": data}
    else:
        liens = Acce.objects.filter(slug=produit.slug).first()
        print(liens)
        return {"type": "lien", "data": liens.lien}
    return 200


@router.post("callback/payin", auth=None)
def callbackPayin(request):
    # Récupérer le header
    header = request.headers
    key = header.get("X-Private-Key")
    print(header)
    if key == config("PAYOUT_KEY"):
        # Récupérer le contenu brut (Raw Content)
        raw_content = json.loads(request.body)
        print("status = ",raw_content.get("status"))
        if raw_content.get("status") == "SUCCESS":
            print("CALLBACK-------------------------------")
            order_id = raw_content.get("externalRef")
            checkout = CHECKOUT.objects.filter(orderId=order_id).first()
            produit = checkout.produit
            checkout.status = "Reussi"
            checkout.reference = raw_content.get("internalRef")
            checkout.save()
            Historique.objects.create(
                montant=raw_content.get("amount"),
                devise=raw_content.get("currency"),
                operation=raw_content.get("operation"),
            )
            entreprise = Entreprise.objects.get(id=checkout.entreprise.id)
            compte = CompteBancaire.objects.get(entreprise=entreprise)
            if produit.gratuit:
                compte.solde += 0
            elif produit.promotion: 
                compte.solde += float(produit.prix_produit_promotion)
                compte.save()
            else:
                compte.solde += float(produit.prix_produit)
                compte.save()
            # send email
            url_produit = f"https://shop.op-markets.com/download/{checkout.id}/{order_id}"

            subject = "Confirmation de votre achat sur Open Market"
            username = checkout.nom_client
            nom_produit = produit.nom_produit
            recipient = checkout.email
            vendeur_contact = "https://wa.me/"+checkout.entreprise.numero
            send_emailB(subject, username, nom_produit, recipient , url_produit ,vendeur_contact)
            print('email envoyer')
            # Traitez les données du webhook ici en utilisant le header et le contenu brut
            """
            {'Content-Length': '123', 'Content-Type': 'application/json', 'Host': '1665-129-0-189-44.ngrok-free.app', 'User-Agent': 'Symfony HttpClient/Curl', 'Accept': '*/*', 'Accept-Encoding': 'gzip', 'X-Forwarded-For': '209.159.155.171', 'X-Forwarded-Host': '1665-129-0-189-44.ngrok-free.app', 'X-Forwarded-Proto': 'https', 'X-Private-Key': 'nPPODj6dkvVzDBLOON1ck09JRBC8zvX33OfwMWFouiY'}
            
            {"status":"SUCCESS","internalRef":"MLS3969B","externalRef":"m6pv3uf7","amount":110,"currency":"XAF","operation":"PURCHASE"}
            """
            # Retournez une réponse appropriée au service de webhook
            return {"message": "Webhook reçu avec succès"}


@router.post("payOut")
def payOut(request, data: MySoleaPay):
    token = request.headers.get("Authorization").split(" ")[1]
    payload = verify_token(token)
    e = Entreprise.objects.get(id=payload.get("entreprise_id"))
    compte = CompteBancaire.objects.get(entreprise=e)
    amount = data.amount
    solde = compte.solde
    is_look = compte.bloque
    print(data)
    print("amount", amount)
    if amount < 1000:
        return {"status": 403, "message": "Le montant minimum à retirer est de 1000."}
    if is_look:
        return {
            "status": 403,
            "message": "Votre compte est bloqué. Contactez le service client.",
        }
    print("somme du compte , = ", compte.solde)
    if solde > 1000 and amount <= solde:
        if data.operator in [1, 2]:
            devise = "XAF"
        else:
            devise = "XOF"
        print(devise)
        compte.solde -= float(amount)
        compte.save()
        Retrait.objects.create(compte=compte, montant=amount)

        url = f"{BASE_URL}action/auth"
        payload = {
            "public_apikey": config("X-API-KEY"),
            "private_secretkey": config("PRIVATE_SECRET_KEY"),
        }

        response = requests.request("POST", url, json=payload)

        response_data = json.loads(response.text)
        if "access_token" in response_data:
            url = "https://soleaspay.com/api/action/account/withdraw"

            headers = {
                "operation": "4",
                "service": str(data.operator),
                "Authorization": "Bearer " + response_data["access_token"],
                "Content-Type": "application/json",
            }
            data = {
                "amount": float(data.amount),
                "wallet": data.customer_number,
                "currency": str(devise),
            }

            response = requests.post(url, headers=headers, data=json.dumps(data))
            result = response.json()
            print(result)
            if result.get("code") == 200:
                return {
                    "status": result.get("code"),
                    "message": str(amount)
                    + " "
                    + devise
                    + " ont été retirés de votre compte. Merci de faire confiance à Open Market.",
                }
            else:
                return {
                    "status": result.get("code"),
                    "message": result.get("message", "Erreur lors du retrait."),
                }
        else:
            return {
                "status": 401,
                "message": "Échec de l'authentification avec le service externe.",
            }
    else:
        if solde <= 1000:
            return {
                "status": 403,
                "message": "Votre solde doit être supérieur à 1000 pour cette opération.",
            }
        elif amount > solde:
            return {
                "status": 403,
                "message": "Le montant à retirer est supérieur au solde du compte.",
            }


@router.get("total_vente")
def totalVente(request):
    token = request.headers.get("Authorization").split(" ")[1]
    payload = verify_token(token)
    e = Entreprise.objects.get(id=payload.get("entreprise_id"))
    compte = CompteBancaire.objects.get(entreprise=e)

    today = datetime.now().date()
    start_of_month = today.replace(day=1)

    # Calcul du début du mois précédent
    start_of_last_month = (start_of_month - timedelta(days=1)).replace(day=1)
    end_of_last_month = start_of_month - timedelta(days=1)

    # Total de toutes les ventes réussies
    total_all_count = CHECKOUT.objects.filter(entreprise=e, status="Reussi").count()
    total_all_sum = CHECKOUT.objects.filter(entreprise=e, status="Reussi").aggregate(
        total=Sum("produit__prix_produit")
    )
    total_all = total_all_sum["total"] or 0

    # Total des ventes réussies pour aujourd'hui
    total_today_count = CHECKOUT.objects.filter(
        entreprise=e, status="Reussi", date__date=today
    ).count()
    total_today_sum = CHECKOUT.objects.filter(
        entreprise=e, status="Reussi", date__date=today
    ).aggregate(total=Sum("produit__prix_produit"))
    total_today = total_today_sum["total"] or 0

    # Total des ventes réussies pour ce mois-ci
    total_month_count = CHECKOUT.objects.filter(
        entreprise=e, status="Reussi", date__date__gte=start_of_month
    ).count()
    total_month_sum = CHECKOUT.objects.filter(
        entreprise=e, status="Reussi", date__date__gte=start_of_month
    ).aggregate(total=Sum("produit__prix_produit"))
    total_month = total_month_sum["total"] or 0

    # Total des ventes réussies pour le mois précédent
    total_last_month_count = CHECKOUT.objects.filter(
        entreprise=e,
        status="Reussi",
        date__date__gte=start_of_last_month,
        date__date__lte=end_of_last_month,
    ).count()
    total_last_month_sum = CHECKOUT.objects.filter(
        entreprise=e,
        status="Reussi",
        date__date__gte=start_of_last_month,
        date__date__lte=end_of_last_month,
    ).aggregate(total=Sum("produit__prix_produit"))
    total_last_month = total_last_month_sum["total"] or 0

    # Calcul de la croissance des ventes (en pourcentage) par rapport au mois précédent
    croissance_ventes = 0
    if total_last_month > 0:
        croissance_ventes = ((total_month - total_last_month) / total_last_month) * 100

    # Total des produits visibles et non visibles
    produitv = Produit.objects.filter(
        entreprise=e, is_visible=True, supprime=False
    ).count()
    produit = Produit.objects.filter(
        entreprise=e, is_visible=False, supprime=False
    ).count()

    # Formatage des sommes
    def format_number(value):
        return "{:,.0f}".format(value).replace(",", " ")

    data = {
        "totalVente": total_all_count,
        "totalVente_sum": format_number(total_all),
        "totalVente_jour": total_today_count,
        "totalVente_jour_sum": format_number(total_today),
        "totalVente_mois": total_month_count,
        "totalVente_mois_sum": format_number(total_month),
        "totalVente_mois_precedent": total_last_month_count,
        "totalVente_mois_precedent_sum": format_number(total_last_month),
        "croissance_ventes": f"{croissance_ventes:.2f}%",
        "produitv": produitv,
        "produitI": produit,
        "soldes": compte.solde,
    }
    print(data)
    return {"status": 200, "data": data}
