from uuid import UUID
from ninja import Schema


class FacebookPixelIn(Schema):
    pixel_id: str

# Schema pour l'affichage
class FacebookPixelOut(Schema):
    product_id:UUID
    produit: str
    pixel_id: str
