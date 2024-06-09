# Utilisation d'une image de base Alpine Linux optimisée pour Python
FROM python:3.10-alpine

# Définir des variables d'environnement pour éviter les avertissements Python lors de l'exécution en mode non interactif
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Créer et définir le répertoire de travail dans le conteneur
WORKDIR /OPENMARKET

# Copier le fichier requirements.txt dans le conteneur
COPY ./requirements.txt /OPENMARKET/

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application Django dans le conteneur
COPY . /OPENMARKET/


# Exposer le port sur lequel l'application Django écoute
EXPOSE 8059

# Commande pour démarrer l'application Django
CMD ["gunicorn", "--bind", "0.0.0.0:8059", "open_Market.wsgi:application"]
