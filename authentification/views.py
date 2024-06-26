from ninja import Router, UploadedFile, Form, File
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from ninja.errors import HttpError

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from banque.models import CompteBancaire
from .code import generer_code
from .models import Entreprise
from .schemas import EntrepriseSchema, LoginSchemas, RegisterSchemas
from .token import create_token, verify_token
import uuid
from datetime import datetime

router = Router()

# POST

# creation de compte


@router.post('register/', auth=None)
def register(request, data: RegisterSchemas):
    """
    **Endpoint pour l'enregistrement d'un nouvel utilisateur.**
    **Permet à un utilisateur de s'inscrire avec un nom d'utilisateur unique et un mot de passe.**
    ---
    paramètres:
    - nom:
        - type: string
        - description: Nom de l'utilisateur.
    - username:
        - type: string
        - description: Nom d'utilisateur unique.
    - motPasse:
        - type: string
        - description: Mot de passe de l'utilisateur.
    - CmotPasse:
        - type: string
        - description: Confirmation du mot de passe.

    """
    nom = data.nom
    username = data.username
    mdp = data.motPasse
    CmotPasse = data.CmotPasse
    u = User.objects.filter(username=username).exists()
    if u:
        raise HttpError(
            status_code=404, message=f"{username} existe déjà. Merci de changer")
    else:
        u = User.objects.create_user(
            username=username, password=mdp)
        u.first_name = nom
        u.save()
        token = create_token(u.id)
        return {"status": 201,'is_entreprise':False, "token": token, "message": "votre compte a été créé avec succès"}

# connexion


@router.post('login', auth=None)
def loginS(request, data: LoginSchemas):
    """
    **Endpoint pour la connexion d'un utilisateur.**
    **Permet à un utilisateur de se connecter avec son adresse email (username) et son mot de passe.**
    ---
    paramètres:
      - username:
          - type: string
          - description: Adresse email de l'utilisateur (username).
      - motPasse:
          - type: string
          - description: Mot de passe de l'utilisateur."""
    username = data.username  # username correspond a l'email
    mdp = data.motPasse
    print(username , mdp)
    users = authenticate(request, username=username, password=mdp)
    u = User.objects.filter(username=username).exists()
    if u:
        user = User.objects.get(username=username)
        t = user.check_password(mdp)
        print(t)
        print("identifiant de l'utilisateur",user.id)
        if t:
            token = create_token(user.id)
            is_entreprise = Entreprise.objects.filter(user=user).exists()
            if is_entreprise:
                return {"status": 200, 'is_entreprise': True, "token": token, "message": "Bienvenue " + user.first_name , 'name':user.first_name}
            else:
                return {"status": 200, 'is_entreprise': False, "token": token, "message": "Bienvenue " + user.first_name, 'name':user.first_name}

        else:
            raise HttpError(status_code=404,
                            message="Le mot de passe fourni est incorrect. Veuillez vérifier vos informations d'identification et réessayer.")
    else:
        raise HttpError(status_code=404,
                        message="L'adresse email fourni est incorrect. Veuillez vérifier et réessayer.")

# CREATION D'UNE ENTREPRISE


@router.post('cree_entreprise')
def cree_entreprise(request, data: Form[EntrepriseSchema], logo: UploadedFile = None):
    """
    **Endpoint pour la création d'une entreprise.**
    **Permet à un utilisateur de créer une entreprise avec les informations fournies.**
    ---
    paramètres:
      - nom_entreprise:
          - type: string
          - description: Nom de l'entreprise à créer.
      - description:
          - type: string
          - description: Description de l'entreprise.
      - logo:
          - type: fichier
          - description: Logo de l'entreprise.
      - pays:
          - type: string
          - description: Pays où est située l'entreprise.
      - ville:
          - type: string
          - description: Ville où est située l'entreprise.
      - numero:
          - type: string
          - description: Numéro de téléphone de l'entreprise.
      - email:
          - type: string
          - description: Adresse email de contact de l'entreprise.
      - secteur_activiter:
          - type: string
          - description: Secteur d'activité de l'entreprise.
    """
    token = request.headers.get("Authorization").split(" ")[1]
    payload = verify_token(token)
    user_id = payload.get('user_id')
    u = User.objects.filter(id=user_id).first()
    print(data)
    if u:
        # Check if the company already exists
        entreprise = Entreprise.objects.filter(
            nom_entreprise=data.nom_entreprise).first()
        if entreprise:  # notification a l'entreprise pour lui dire de securiser son nom
            if entreprise.is_private:  # notification a l'entreprise pour lui dire qu'un compte a voulue etre cree en son nom
                raise HttpError(
                    status_code=400, message="Vous ne pouvez pas utiliser ce nom car il a été privatisé")
            raise HttpError(status_code=400,
                            message="Cette entreprise existe déjà")
        else:
            new_company = Entreprise.objects.create(
                **data.dict(), user=u, logo=logo)
            new_company = Entreprise.objects.get(slug = new_company.slug)
            print('entreprise = ',new_company)
            c = CompteBancaire.objects.create(entreprise=new_company)
            print(c)
            return {"status": 200,"message": "Entreprise créée avec succès", "entreprise": EntrepriseSchema.from_orm(new_company)}


# GET
# RECUPERER LES INFORMATIONS DE L'UTILISATEUR
@router.get('getuser/')
def getUser(request):
    """
    **Endpoint pour récupérer les informations de l'utilisateur connecté.**
    **Permet à un utilisateur authentifié de récupérer ses propres informations.**
    ---
    paramètres:
      - Authorization:
          - in: header
          - type: string
          - required: true
          - description: Jeton d'authentification de l'utilisateur."""
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        payload = verify_token(token)
        user_id = payload.get('user_id')
        u = list(User.objects.filter(id=user_id).values(
            "id", "username", "is_active", "first_name"))
        return u

    except:
        raise HttpError(status_code=404, message="veillez vous connectez svp")

# RECUPERER LES INFORMATIONS DE L'ENTREPRISE


@router.get('getEntreprise/')
def getEntreprise(request):
    """
    **Endpoint pour récupérer les informations de l'entreprise de l'utilisateur connecté.**
    **Permet à un utilisateur authentifié de récupérer les informations de son entreprise associée.**
    ---
    paramètres:
      - Authorization:
          - in: header
          - type: string
          - required: true
          - description: Jeton d'authentification de l'utilisateur."""
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        payload = verify_token(token)
        user_id = payload.get('user_id')
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise HttpError(404, "Utilisateur non trouvé.")
        userInfos= list(User.objects.filter(id=user_id).values(
            "username", "first_name"))
        entreprise = list(Entreprise.objects.filter(user=user).values("nom_entreprise","description","pays","numero","email","logo","ville","slug"))
        if not entreprise:
            raise HttpError(404, "Aucune entreprise associée à cet utilisateur.")
        result = []
        result = {
            'userInfos': userInfos,
            'entrepriseInfos': entreprise
        }
        return result
    except HttpError as e:
        raise e
    except Exception as e:
        raise HttpError(500, "Une erreur s'est produite lors de la récupération des données de l'entreprise.")


# RECUPERER LES INFORMATIONS DE L'UTILISATEUR
@router.get('token')
def getToken(request):
    try:
        print(request.headers)
        print('------------------------------------------')
        token = request.headers.get("Authorization").split(" ")[1]
        payload = verify_token(token)
        return 200
    except:
        raise HttpError(status_code=404, message="veillez vous connectez svp")


@router.get('send_email', auth = None)
def send_emailB(request):
    subject = 'Confirmation de votre achat sur Open Market'
    username = 'Franklin Delbo' 
    nom_produit = "produit de massage"
    recipient = 'fdelbo47@gmail.com'
    html_content = render_to_string('email_template.html', {'username': username , 'nom_produit' : nom_produit})
    text_content = strip_tags(html_content)
    # Créer l'email multi alternatives
    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [recipient])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return {"success": True, "message": "Email sent successfully"}