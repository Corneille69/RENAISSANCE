import random

def jeu_hasard():
    print("🎲 Bienvenue au jeu de hasard : Devine le nombre !")
    print("Je pense à un nombre entre 1 et 100...")
    
    nombre_secret = random.randint(1, 100)
    tentatives = 0

    while True:
        try:
             = int(input("Ta proposition : "))
            tentatives += 1

            if guess < nombre_secret:
                print("🔽 Trop petit ! Essaie encore.")
            elif guess > nombre_secret:
                print("🔼 Trop grand ! Essaie encore.")
            else:
                print(f"🎉 Bravo ! Tu as trouvé le nombre {nombre_secret} en {tentatives} tentative(s) !")
                break
        except ValueError:
            print("⚠️ Saisis un nombre valide, s’il te plaît.")