from ninja import Router
from authentification.models import Entreprise
from banque.models import PaiementEchoue,CompteBancaire
from ..models import Acce, Fichier, Livre, ProduitNumerique, Produit, CHECKOUT
from ..schemas import CHECKOUTSchema , MySoleaPay
from decouple import config
import requests
import json
from authentification.token import verify_token
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta
router = Router()

#BASE_URL = "https://soleaspay.com/api/agent/sandbox/"
BASE_URL = "https://soleaspay.com/api/"


@router.get('paiement')
def getPayement(request):
    token = request.headers.get("Authorization").split(" ")[1]
    payload = verify_token(token)
    e = Entreprise.objects.get(id = payload.get('entreprise_id'))
    c = list(CHECKOUT.objects.filter(entreprise = e).values("produit__nom_produit","nom_client","status","email","type","pays_client","date"))
    return {"status":200 , "data":c}



@router.post("checkout/user/{entreprise_slug}/{slug}", auth=None)
def checkout_produit(request, entreprise_slug: str, slug: str, data: CHECKOUTSchema):
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
    )
    url = f"{BASE_URL}agent/bills"
    order_id = checkout.slug
    
    headers = {
        "x-api-key": config("X-API-KEY"),
        "operation": "2",
        "service": str(data.id_operateur),
        "Content-Type": "application/json",
        "otp":data.codeOtp,
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
    print(response_data)
    if response_data.get("success") == False:
        checkout.status = "Echec"
        checkout.save()
        PaiementEchoue.objects.create(
            token=response_data.get("payToken"), checkout=checkout
        )
        return {
            "status": 400,
            "message": "Votre paiement a échoué. Merci de réessayer.",
        }
    if response_data.get("success") == True:
        checkout.status = "Reussi"
        checkout.save()
        return {
            "status": 200,
            "payId": response_data["data"]["payId"],
            "amount": response_data["data"]["amount"],
            "orderId": response_data["order_id"],
        }
    if data.devise_client == "USD":
        payUrl = response_data["data"]["payLink"]
        return {"status": 200, "url": payUrl}
    return {"status":400}

verify_url = "https://soleaspay.com/api/agent/verif-pay"


@router.get("donwload", auth=None)
def donwloadFile(request, id_operateur: str, amount: float, orderId: str, payId: str):
    params = {"amount": amount, "orderId": orderId, "payId": payId}
    headers = {
        "x-api-key": config("X-API-KEY"),
        "operation": "2",
        "service": str(id_operateur),
        "Content-Type": "application/json",
    }
    response = requests.get(verify_url, headers=headers, params=params)
    result = response.json()
    if result.get("success") == True:
        data =  []
        checkhout = CHECKOUT.objects.get(slug = orderId)
        checkhout.reference = payId
        checkhout.save()
        produit = checkhout.produit
        entreprise = Entreprise.objects.get(id = checkhout.entreprise.id)
        compte = CompteBancaire.objects.get(entreprise = entreprise)
        if produit.gratuit:
            compte.solde += 0
        elif produit.promotion:
            compte.solde += float(produit.prix_produit_promotion)
            compte.save()
        else:
            compte.solde = float(produit.prix_produit)
            compte.save()
        if produit.categorie_produit != 'lien':
            files = Fichier.objects.filter(produit = produit.id)
            for file in files:
                data.append({
                    'fichier':file.fichier.url
                })
            print('url du produit',data)
            return {"type":'produit_digital','data':data}
        else:
            liens = Acce.objects.filter(slug = produit.slug).first()
            print(liens)
            return {"type":'lien','data':liens.lien}
            
        print("false payment")
        print(result)
    if result.get("success") == False:
        return {'status':404 , 'message':'Aucun payment trouver'}
    return 200 


@router.post('payOut')
def payOut(request, data: MySoleaPay):
    token = request.headers.get("Authorization").split(" ")[1]
    payload = verify_token(token)
    e = Entreprise.objects.get(id=payload.get("entreprise_id"))
    compte = CompteBancaire.objects.get(entreprise = e)
    amount = data.amount
    print(data)
    print('amount' , amount)
    if compte.solde >= 100:
        if data.operator in [1, 2]:
            devise = "XAF"
        else:
            devise = "XOF"
        print(devise)
            
        url = f"{BASE_URL}action/auth"
        payload = {
            "public_apikey": config('X-API-KEY'),
            "private_secretkey": config('PRIVATE_SECRET_KEY'),
        }
        response = requests.request("POST", url, json=payload)

        response_data = json.loads(response.text)
        accestoken = response_data.get("access_token")
        print(accestoken)
        if 'access_token' in response_data:
            url = "https://soleaspay.com/api/action/account/withdraw"

            headers = {
                "operation": "4",
                "service": str(data.operator),
                "Authorization": "Bearer " + response_data['access_token'],
                "Content-Type": "application/json"
            }
            data = {
                "amount": float(data.amount),
                "wallet": data.customer_number,
                "currency":str(devise)
            }

            response = requests.post(url, headers=headers, data=json.dumps(data))
            result = response.json()
            print(result)
            if result.get('code') == 200:
                compte.solde -= float(amount)
                compte.save()
                return {"status":result.get('code') , "message": str(amount) +' ' + devise + " ont été retirés de votre compte. Merci de faire confiance à Open Market."}
    return {"status":403 , "message":"Votre solde doit être supérieur ou égal à 100 pour cette opération."}










@router.get('total_vente')
def totalVente(request):
    token = request.headers.get("Authorization").split(" ")[1]
    payload = verify_token(token)
    e = Entreprise.objects.get(id=payload.get("entreprise_id"))
    compte = CompteBancaire.objects.get(entreprise = e)
    
    # Total de toutes les ventes réussies
    total_all = CHECKOUT.objects.filter(entreprise=e, status="Reussi").count()

    # Total des ventes réussies pour aujourd'hui
    today = now().date()
    total_today = CHECKOUT.objects.filter(entreprise=e, status="Reussi", date__date=today).count()

    # Total des ventes réussies pour ce mois-ci
    start_of_month = today.replace(day=1)
    total_month = CHECKOUT.objects.filter(entreprise=e, status="Reussi", date__date__gte=start_of_month).count()
    #Total des produit
    produitv = Produit.objects.filter(entreprise = e, is_visible = True , supprime = False).count()
    produit = Produit.objects.filter(entreprise = e , is_visible = False , supprime = False).count()
    data = {
        'totalVente': total_all,
        'totalVente_jour': total_today,
        'totalVente_mois': total_month,
        'produitv':produitv,
        'produitI':produit,
        'soldes':compte.solde
    }
    return {'status':200 , 'data':data}