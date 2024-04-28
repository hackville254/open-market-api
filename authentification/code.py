import random
import string

def generer_code():
    code = []
    
    # Générer les trois premiers caractères
    for _ in range(3):
        code.append(random.choice(string.ascii_uppercase + string.digits))
    
    # Ajouter le premier tiret
    code.append("-")
    
    # Générer les quatre caractères suivants
    for _ in range(4):
        code.append(random.choice(string.ascii_uppercase + string.digits))
    
    # Ajouter le deuxième tiret
    code.append("-")
    
    # Générer les cinq caractères suivants
    for _ in range(5):
        code.append(random.choice(string.ascii_uppercase + string.digits))
    
    # Ajouter le troisième tiret
    code.append("-")
    
    # Générer le dernier caractère
    code.append(random.choice(string.ascii_uppercase + string.digits))
    
    # Retourner le code sous forme de chaîne de caractères
    return "".join(code)

# Exemple d'utilisation
code_generé = generer_code()
print(code_generé)
