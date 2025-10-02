
cote_a=int (input("entrer la vleur du cote a :"))
cote_b=int (input("entrer la vleur du cote b :"))
cote_c=int (input("entrer la vleur du cote c :"))

print("La nature du triangle demande est un ")

if cote_a*cote_a + cote_b*cote_b == cote_c*cote_c :
    print("Triangle rectangle")

elif cote_a==cote_b and cote_a==cote_c :
    print(" Triangle equilaterale")

elif cote_a==cote_b or cote_a==cote_c :
    print(" Triangle isocele")

else:
    print("la nature demande ne refere pas a un triangle")