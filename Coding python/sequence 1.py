

nom1=str(input("votre nom1 est:"))
nom2=str(input("votre nom2 est:"))




if nom1!=nom2:
    print("c'est bien votre compte\n")
    print("veuillez continuer le remplissage")
else:
    print("ce ne pas votre compte\n")
    print("veuiller Bien remplir vos donnes :")





prenom1=str(input("votre prenom est:"))
surnom=str(input("votre surnom est :"))

if prenom1==surnom:
    print("Bienvenue!\n")
    print("veuillez continuer")
else:
    print("voleur!\n")
    print("vous vous etes tromper")

mot_de_passe=int(input("votre mot_de_passe est:"))
N_piece=int(input("votre N_piece est :"))

if mot_de_passe !=N_piece :
    print("c'est normal\n continuer le processus ")

elif mot_de_passe < N_piece:
    print("vous etes sur le platforme")
    
else:
    print("le site ne vous appartient pas ") 


