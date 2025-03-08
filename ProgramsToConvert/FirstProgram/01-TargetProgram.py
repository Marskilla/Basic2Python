import os

# Équivalent de CLS
os.system('cls' if os.name == 'nt' else 'clear')

# Définition et affichage du message de bienvenue
a = "Welcome to this first program"
print(a)
print("to convert in Python")
print("")
print("What is your name")

# Saisie du nom
name = input()

# Saisie de l'âge avec conversion en entier
age = int(input("What is your age : "))

# Effacement de l'écran et affichage du résultat
os.system('cls' if os.name == 'nt' else 'clear')
print(f"Next year, {name} you will be {age+1}.") 