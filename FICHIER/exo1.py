
nom = "OUEDRAOGO"
code = "126"
print("BONJOUR Bienvenue  sur notre plateforme")

name = input("votre nom est:")
mot_de_passe = (input("votre mot_de_passe est:"))

while mot_de_passe != code :
    print("vous n'etes pas sur votre page")
    mot_de_passe = (input("votre mot_de_passe est:"))
while name != nom :
    print("error")  
    print("veuillez ressayer svp!")
    name = input("votre nom est:")

if mot_de_passe == code :
    print("vous etes sur votre page")
if name==nom :
    print("Bienvenue!")



    