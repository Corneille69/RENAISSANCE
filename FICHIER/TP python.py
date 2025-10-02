

nom1= input(" entrer votre nom de famille :")
nom2= input(" entrer votre nom de famille secondaire :")


prenom1 =input("entrer votre  prenom:")



print("1-Membre  de la famille")
print("2-visiteur")
print("3-voisin")
print("4-Grand pere")

choix=input("quelle genre de choix faites vous :")

if choix=="1":
    Membredelafamille = nom1+ prenom1
    print("la reponse est",Membredelafamille)
elif choix=="2":
        visiteur=nom1- prenom1
        print("la reponse est",visiteur)

elif choix =="3" :
        voisin =nom1!=prenom1
        print("la reponse est",voisin)
elif choix=="4" :
        Grandpere =nom1+nom2
        print("la reponse est",Grandpere)
else :
        print("vous etes un intrus dans les choix")





