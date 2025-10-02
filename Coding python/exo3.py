
Lieux="EXhotel "
salle="cote est"
mot_de_passe="0274"
print("Bienvenue a notre test d'entrer veuillez suivre les instructions SVP!")
print("Veuillez deverouiller pour etre acces a la conference du president")

localisation =input("Entre le nom de l'hotel :")
room=input("Entrer le nom de la salle:")
encodex=input("Entrer le mot_de_passe secret si vous ete un invite d'honneur :")

while  localisation != Lieux :
    print("vous n'etes pas sur le bon endroit du deroulement de la conference\n veuillez ressaisir le nom svp!")
    localisation =input("Entre le nom de l'hotel :")
    print("passer a une autre etape")

while room!=salle :
    print("ERROR vous n'avez pas retrouver la bonne salle\n svp! veuillez entrer a nouveau le nom de la salle si vous ete un membre")
    room=input("Entrer le nom de la salle:")
    print("continuer le processus svp!")

while encodex != mot_de_passe :
    print("code non valide !\n veuillez retrouver le bon 🚨")
    encodex=input("Entrer le mot_de_passe secret si vous ete un invite d'honneur:")


if localisation==Lieux :
    print("Bienvenue a  Excellence hotel de koudougou")

if room==salle :
    print(" Felecitation d'avoir trouver la salle!👍")

if encodex== mot_de_passe :
    print(" vous avez pu remplir les bonnnes donnes\t Veuillez entrer dans la salle svp!🧨")

    
