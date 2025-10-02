


Entreprise="ocran19"
encodex="TRIO127"

print("Bonjour chers membres veuillez entrer vos donnes svp!\n")

opportunity=input("veuillez saisir le nom de l'entreprise avec pricision si vous etes membres:")
passe_word=input("veuillez entrer le mot de passe svp!:")

while Entreprise != opportunity :
    print("vous avez fait une erreur!")
    print(" entrer a nouveau le nom de l'entreprise")
    opportunity=input("veuillez saisir le nom de l'entreprise avec pricision si vous etes membres:")
   

while encodex!=passe_word :
    print(" vous n'avez pas entrer le bonne ")
    print("veuillez ressayez a nouveau svp")
    passe_word=input("veuillez entrer le mot de passe svp!:")
    

if Entreprise==opportunity :
    print("Bienvenue ! vous etes sur la bonne platforme ")
if encodex==passe_word :
    print("felecitation pour le code trouver!")

if Entreprise != opportunity and encodex!=passe_word :
    print("pas d'acces")