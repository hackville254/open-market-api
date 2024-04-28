from authentification.token import verify_token
from ninja import NinjaAPI
from ninja.security import HttpBearer
from produits.routers.produitNumeriqueRouter import router as produitRouter
from produits.routers.livreRouter import router as livreRouter
from produits.routers.LiensRouter import router as LiensRouter
from banque.banqueRouter import router as banqueRouter


from authentification.views import router as AuthRouter

class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        t = verify_token(token=token)
        return t


app = NinjaAPI(
    title='open market',
    version="1.0.0",
    auth=GlobalAuth(),
)
app.add_router("authentification/",AuthRouter,tags=["Authentification"])
app.add_router("/", produitRouter, tags=["PRODUIT NUMERIQUE"])
app.add_router("/", livreRouter, tags=["LIVRE,EBOOK"])
app.add_router("/", LiensRouter, tags=["LIEN ACCES"])
app.add_router("/banque", banqueRouter, tags=["OPERATION BANCAIRE"])



