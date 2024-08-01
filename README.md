echo "# open-market-frontend" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/hackville254/open-market-frontend.git
git push -u origin main



git remote add origin https://github.com/hackville254/open-market-api.git
git branch -M main
git push -u origin main

# Assurez-vous que vous êtes sur la branche principale
git checkout main

# Mettez à jour la branche principale avec les dernières modifications du dépôt distant
git pull origin main

# Créez une nouvelle branche et basculez dessus
git checkout -b nom-de-la-nouvelle-branche

# Ajouter les modifications à l'index
git add .

# Valider les modifications
git commit -m "Fin de la premiere version fonctionnel"


git push origin v1
