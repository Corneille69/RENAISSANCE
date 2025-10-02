# -*- coding: utf-8 -*- 
class Humain:
   
    """classe qui definit un humain"""



    def __init__(self , nom, age, ):
        self.nom = nom
        self.age = age 
        
    def parler (self, message,):
       print("{} a dit : {}".format(self.nom,message))
    
h1= Humain("Benock" , 24)
h1.parler("Bonjour a tous les membraes de la famille OUEDRAOGO 🥰 :)")
h1.parler("comment allez vous ?😎")
h1.parler("jaimerais solliciter une rencontre de la famille")
h2= Humain("jean" , 30)
h2.parler(" oui la famille se portent tres bien😻")
h2.parler(" OK! la rencontre se deroulera le 21/04/2025 a koudougou dans le grande famille ")
    

