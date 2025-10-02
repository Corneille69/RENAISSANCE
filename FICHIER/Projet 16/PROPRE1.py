import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Image de fond du cahier d'absence
FOND_IMAGE = "cahier_absence.jpg"  # Remplace par le nom réel de ton image

class ApplicationAbsence:
    def __init__(self, root):
        self.root = root
        self.root.title("Cahier d'Absence")
        self.root.geometry("1024x768")

        # Chargement de l'image de fond
        self.image_fond = Image.open(FOND_IMAGE)
        self.photo_fond = ImageTk.PhotoImage(self.image_fond)

        self.label_fond = tk.Label(self.root, image=self.photo_fond)
        self.label_fond.place(x=0, y=0, relwidth=1, relheight=1)

        # Cadre transparent pour le tableau
        self.cadre = tk.Frame(self.root, bg='white', bd=2)
        self.cadre.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.6)

        self.creer_tableau()

    def creer_tableau(self):
        colonnes = ("Nom", "Date", "Statut", "Justification")

        self.tableau = ttk.Treeview(self.cadre, columns=colonnes, show="headings")
        for col in colonnes:
            self.tableau.heading(col, text=col)
            self.tableau.column(col, width=150)

        self.tableau.pack(fill="both", expand=True)

        # Exemples de données
        self.tableau.insert("", "end", values=("Jean Dupont", "2025-06-16", "Retard", "Embouteillage"))
        self.tableau.insert("", "end", values=("Marie Claire", "2025-06-16", "Absent", "Malade"))

# Exécution de l'application
if __name__ == "__main__":
    racine = tk.Tk()
    app = ApplicationAbsence(racine)
    racine.mainloop()