from ninja import Router
from django.contrib.auth.models import User
from pydantic import ValidationError
from .schemas import CompteBancaireShema, TransactionSchema
from .models import CompteBancaire, Transaction
from django.db import transaction
router = Router()

# Endpoint pour récupérer un compte par son ID


@router.get("/comptes/{compte_id}")
def get_compte(request, compte_id: str):
    """
    **Endpoint pour récupérer un compte par son ID.**
    **Permet de récupérer les détails d'un compte bancaire en fonction de son identifiant.**
    ---
    paramètres:
    - compte_id:
        - type : str
        - description: L'identifiant unique du compte bancaire.
    """
    compte = CompteBancaire.objects.get(
        id=compte_id, supprime=False, bloque=False)
    return {"compte": compte}


# Endpoint pour mettre à jour un compte existant
@router.post("/comptes/{compte_id}")
def update_compte(request, compte_id: str, compte: CompteBancaireShema):
    """
    **Endpoint pour mettre à jour un compte existant.**
    **Permet de mettre à jour les détails d'un compte bancaire existant en fonction de son identifiant.**
    ---
    paramètres:
    - compte_id:
        - type : str
        - description: L'identifiant unique du compte bancaire à mettre à jour.
    - compte:
        - type: CompteBancaire
        - description: Les nouveaux détails du compte bancaire.
    """
    compte.numero_operateur = compte.numero_operateur
    compte.save()
    return {"status": 200}

# Endpoint pour supprimer un compte


@router.delete("/comptes/{compte_id}")
def delete_compte(request, compte_id: str):
    """
    **Endpoint pour supprimer un compte.**
    **Permet de supprimer un compte bancaire en fonction de son identifiant.**
    ---
    paramètres:
    - compte_id:
        - type : str
        - description: L'identifiant unique du compte bancaire à supprimer.
    """
    compte = CompteBancaire.objects.get(
        id=compte_id, supprime=False, bloque=False)
    compte.supprime = True
    compte.save()
    return {"message": "Compte deleted successfully"}

# Endpoint pour récupérer les transactions d'un compte


@router.get("/comptes/{compte_id}/transactions")
def get_transactions(request, compte_id: str):
    """
    **Endpoint pour récupérer les transactions d'un compte.**
    **Permet de récupérer les transactions associées à un compte bancaire en fonction de son identifiant.**
    ---
    paramètres:
    - compte_id:
        - type : str
        - description: L'identifiant unique du compte bancaire.
    """
    compte = CompteBancaire.objects.get(
        id=compte_id, supprime=False, bloque=False)
    transactions = Transaction.objects.filter(compte_source=compte)
    return {"transactions": transactions}

# Endpoint pour créer une nouvelle transaction pour un compte


@router.post("/comptes/{compte_id}/transactions")
@transaction.atomic
def create_transaction(request, compte_id: str, transaction: TransactionSchema):
    """
    **Endpoint pour créer une nouvelle transaction pour un compte.**
    **Permet de créer une nouvelle transaction associée à un compte bancaire en fonction de son identifiant.**
    ---
    paramètres:
    - compte_id:
        - type : str
        - description: L'identifiant unique du compte bancaire.
    - transaction:
        - type: Transaction
        - description: Les détails de la nouvelle transaction à créer.
    """

    # Vérifier que les deux comptes existent réellement
    compte_source = CompteBancaire.objects.filter(
        numero_compte=transaction.numero_compte_source).first()
    compte_destination = CompteBancaire.objects.filter(
        numero_compte=transaction.numero_compte_destination).first()
    if not compte_source or not compte_destination:
        raise ValidationError(
            "Les deux comptes doivent exister pour effectuer la transaction")

    # Vérifier que le compte source est différent du compte destinataire
    if transaction.numero_compte_source == transaction.numero_compte_destination:
        raise ValidationError(
            "Le compte source ne peut pas être le même que le compte destinataire")

    # Enregistrer la transaction dans la base de données
    nouvelle_transaction = Transaction(
        montant=transaction.montant,
        compte_source_id=compte_source.id,
        compte_destination_id=compte_destination.id,
        user=compte_destination.entreprise.user
    )
    nouvelle_transaction.save()

    return {"message": "Transaction créée avec succès"}
