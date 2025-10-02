

Base=int(input("la valeur de la base :"))
cote=int(input("le cote est:"))
Hypothenuse=int(input("l'hypothenuse :"))

print("calculer les valeur du triangle")

if Base==cote+Hypothenuse:
    print("le triangle est complet")
elif cote>Base+Hypothenuse:
    print("Triangle rectangle")
elif Hypothenuse<Base+cote:
    print("triangle isocele")
else:
    print("vous ne conntruiser pas un triangle en ce moment")