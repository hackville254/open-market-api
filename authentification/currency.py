from unidecode import unidecode

monnaies = {
    "cameroun": "XAF",
    "centrafrique": "XAF",
    "tchad": "XAF",
    "congo-brazzaville": "XAF",
    "congo-kinshasa": "XAF",
    "gabon": "XAF",
    "gambie": "XOF",
    "mali": "XOF",
    "niger": "XOF",
    "senegal": "XOF",
    "togo": "XOF",
    "benin": "XOF",
    "burkina faso": "XOF",
    "cote d'ivoire": "XOF",
    "guinee-bissau": "XOF",
    "sierra leone": "XOF",
}

def obtenir_monnaie(pays):
    pays_normalise = unidecode(pays.lower())
    return monnaies.get(pays_normalise, "Monnaie inconnue")

# Exemple d'utilisation
""" print(obtenir_monnaie("Cameroun"))         # Affiche "XAF"
print(obtenir_monnaie("Mali"))             # Affiche "XOF"
print(obtenir_monnaie("france"))           # Affiche "Monnaie inconnue"
print(obtenir_monnaie("Côte d'Ivoire"))   # Affiche "XOF"
 """