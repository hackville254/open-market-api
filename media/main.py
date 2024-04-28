import os
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from routers.produits import router as produitsRouters
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



folder_path = "media"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

app.mount(f"/{folder_path}", StaticFiles(directory="media"), name="media")
app.include_router(produitsRouters, prefix="/produits")






origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={"models": ["models.produits"]},
    generate_schemas=True,
    add_exception_handlers=True,
)