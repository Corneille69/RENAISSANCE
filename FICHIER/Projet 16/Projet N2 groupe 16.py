import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime

FICHIER = "absences.csv"

def initialiser_fichier():
    try:
        with open(FICHIER, 'x', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Heure", "filiere", "Cours", "Étudiant", "Présence"])
    except FileExistsError:
        pass

def enregistrer_presence():
    nom = entree_nom.get()
    cours = entree_cours.get()
    filiere = var_filiere.get()
    presence = var_presence.get()

    if nom == "" or cours == "" or filiere == "":
        messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")
        return

    now = datetime.now()
    date_str = now.date()
    heure_str = now.strftime("%H:%M")

    with open(FICHIER, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date_str, heure_str, filiere, cours, nom, "Présent" if presence == 1 else "Absent"])
    
    messagebox.showinfo("Enregistré", f"Présence de {nom} enregistrée.")

def afficher_absents():
    fenetre_absents = tk.Toplevel(fenetre)
    fenetre_absents.title("Liste des absents")
    fenetre_absents.config(bg="#f9f9f9")

    with open(FICHIER, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        absents = [ligne for ligne in reader if ligne[5] == "Absent"]

    texte = tk.Text(fenetre_absents, width=90, height=20, bg="#fff8f0", fg="#333", font=("Arial", 10))
    texte.pack(padx=10, pady=10)
    texte.insert(tk.END, "Date\tHeure\tFiliere\tCours\tÉtudiant\n")
    texte.insert(tk.END, "-"*80 + "\n")
    for ligne in absents:
        texte.insert(tk.END, f"{ligne[0]}\t{ligne[1]}\t{ligne[2]}\t{ligne[3]}\t{ligne[4]}\n")

# Interface principale
fenetre = tk.Tk()
fenetre.title("Gestion des absences des étudiants")
fenetre.geometry("500x350")
fenetre.config(bg="#e6f2ff")  # bleu clair

# Titre
titre = tk.Label(fenetre, text="Suivi des Absences", font=("Helvetica", 16, "bold"), bg="#e6f2ff", fg="#003366")
titre.grid(row=0, column=0, columnspan=2, pady=10)

# Nom
tk.Label(fenetre, text="Nom de l'étudiant :", bg="#e6f2ff").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entree_nom = tk.Entry(fenetre)
entree_nom.grid(row=1, column=1, padx=5, pady=5)

# Cours
tk.Label(fenetre, text="Nom du cours :", bg="#e6f2ff").grid(row=2, column=0, sticky="e", padx=5, pady=5)
entree_cours = tk.Entry(fenetre)
entree_cours.grid(row=2, column=1, padx=5, pady=5)

# filiere
tk.Label(fenetre, text="filiere :", bg="#e6f2ff").grid(row=3, column=0, sticky="e", padx=5, pady=5)
filiere= ["CS27", ]
var_filiere= tk.StringVar()
menu_filiere = tk.OptionMenu(fenetre, var_filiere, *filiere)
menu_filiere.grid(row=3, column=1, padx=5, pady=5)
var_filiere.set(filiere[0])

# Présence/Absence
var_presence = tk.IntVar()
frame_presence = tk.Frame(fenetre, bg="#e6f2ff")
frame_presence.grid(row=4, column=0, columnspan=2, pady=5)
tk.Radiobutton(frame_presence, text="Présent", variable=var_presence, value=1, bg="#e6f2ff").pack(side="left", padx=10)
tk.Radiobutton(frame_presence, text="Absent", variable=var_presence, value=0, bg="#e6f2ff").pack(side="left", padx=10)

# Boutons
btn_style = {"font": ("Arial", 10), "bg": "#0066cc", "fg": "white", "padx": 10, "pady": 5}
tk.Button(fenetre, text="Enregistrer", command=enregistrer_presence, **btn_style).grid(row=5, column=0, pady=15)
tk.Button(fenetre, text="Voir les absents", command=afficher_absents, **btn_style).grid(row=5, column=1, pady=15)

initialiser_fichier()
fenetre.mainloop()