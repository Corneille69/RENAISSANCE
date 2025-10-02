


def calcul(n):

    suite = []
    A,B=0,1
    for i in range(n) :
        suite.append(A)
        A,B=B,A+B
    return suite
li= int(input("veuillez entrer un nombre :"))
resultat =calcul(li)


print("suite de calcul",resultat)