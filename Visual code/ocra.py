# -*- coding: utf-8 -*-
"""

"""
class Humain:
    """
    Classe des etres vivants
    """
    lieu_habitation = "terre"
    def __init__(self,nom,age,):
        print("Lancement du programme...")
    
        self.prenom = nom
        self.age = age
def parler(self, message): 
    print("{} a dit : {}".format(self.nom, message)) 

def changer_planete(cls, nouvelle_planete):
    Humain.lieu_habitation = nouvelle_planete
    print("planete actuelle : {}".format(Humain.lieu_habitation))
    Humain.changer_planete("MARS")
    print("planete actuelle:~{}".format(Humain.lieu_habitation))
    