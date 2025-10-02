import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from datetime import datetime, timedelta
import calendar


# Connexion à la base de données SQLite
conn = sqlite3.connect("absences.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS absences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    jour TEXT,
    heure TEXT,
    filiere TEXT,
    cours TEXT,
    etudiant TEXT,
    statut TEXT,
    duree_retard TEXT,
    justification TEXT
)
''')
conn.commit()

etudiants_par_filiere = {
    "CS27": [
        "BADO Yannick", "BADOLO Patricia", "BALIMA Hectore",
    ]
}

statut_vars = {}
duree_retards = {}
fenetre = tk.Tk()
fenetre.title("Gestion des absences")
fenetre.geometry("900x700")
fenetre.config(bg="lightblue")
var_filiere = tk.StringVar()
var_filiere.set("CS27")

def effacer_fenetre():
    for widget in fenetre.winfo_children():
        widget.destroy()

def afficher_accueil():
    effacer_fenetre()
    jour_actuel = calendar.day_name[datetime.now().weekday()]
    if jour_actuel != "Sunday":
        tk.Label(fenetre, text=f"Aujourd'hui : {jour_actuel}", font=("Arial", 12, "bold"), bg="lightblue").pack(pady=5)

    tk.Label(fenetre, text="Filière :", bg="lightblue").pack(pady=5)
    tk.OptionMenu(fenetre, var_filiere, *etudiants_par_filiere.keys()).pack()

    tk.Label(fenetre, text="Cours :", bg="lightblue").pack(pady=5)
    global champ_cours
    champ_cours = tk.Entry(fenetre)
    champ_cours.pack(pady=5)

    tk.Button(fenetre, text="Afficher les étudiants", command=afficher_liste_etudiants, bg="skyblue").pack(pady=5)
    tk.Button(fenetre, text="Enregistrer", command=enregistrer, bg="green", fg="white").pack(pady=5)
    tk.Button(fenetre, text="Justifier absences/retards", command=justification, bg="orange", fg="white").pack(pady=5)
    tk.Button(fenetre, text="Afficher absences et retards du jour", command=afficher_absences_retards_du_jour, bg="purple", fg="white").pack(pady=5)
    tk.Button(fenetre, text="Rapport individuel (Samedi)", command=rapport_individuel_semaine, bg="blue", fg="white").pack(pady=10)

def rapport_individuel_semaine():
    effacer_fenetre()
    today = datetime.now()
    last_saturday = today - timedelta(days=today.weekday() + 2) if today.weekday() < 5 else today - timedelta(days=today.weekday() - 5)
    this_monday = last_saturday - timedelta(days=6)
    debut_semaine = this_monday.strftime("%Y-%m-%d")
    fin_semaine = last_saturday.strftime("%Y-%m-%d")

    tk.Label(fenetre, text=f"Rapport de la semaine : {debut_semaine} au {fin_semaine}", font=("Arial", 14, "bold"), bg="lightblue").pack(pady=10)

    frame_liste = tk.Frame(fenetre)
    frame_liste.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_liste, bg="white")
    scrollbar = tk.Scrollbar(frame_liste, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="white")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    global rapports
    cursor.execute("SELECT etudiant, statut, duree_retard FROM absences WHERE date BETWEEN ? AND ?", (debut_semaine, fin_semaine))
    donnees = cursor.fetchall()

    rapports = {}
    for etudiant, statut, duree in donnees:
        if etudiant not in rapports:
            rapports[etudiant] = {"Absences": 0, "Retards": 0, "Minutes": 0}
        if statut == "Absent":
            rapports[etudiant]["Absences"] += 1
        elif statut == "Retard":
            rapports[etudiant]["Retards"] += 1
            if duree and duree.endswith("min"):
                try:
                    minutes = int(duree.replace(" min", ""))
                    rapports[etudiant]["Minutes"] += minutes
                except ValueError:
                    pass

    if not rapports:
        tk.Label(scroll_frame, text="Aucune donnée enregistrée cette semaine.", bg="lightblue").pack(pady=20)
    else:
        for nom, data in rapports.items():
            ligne = f"{nom} | Absences: {data['Absences']} | Retards: {data['Retards']} | Durée totale: {data['Minutes']} min"
            tk.Label(scroll_frame, text=ligne, anchor="w", bg="white").pack(fill="x", padx=10, pady=3)

    tk.Button(fenetre, text="Retour", command=afficher_accueil, bg="grey", fg="white").pack(pady=10)

  


 

def afficher_liste_etudiants():
    effacer_fenetre()
    tk.Label(fenetre, text="Liste des étudiants", font=("Arial", 14), bg="lightblue").pack(pady=10)
    frame = tk.Frame(fenetre, bg="white")
    frame.pack(fill="both", expand=True)

    for nom in etudiants_par_filiere[var_filiere.get()]:
        frame_etud = tk.Frame(frame, bg="white")
        frame_etud.pack(fill="x", pady=2, padx=10)
        tk.Label(frame_etud, text=nom, width=30, anchor="w", bg="white").pack(side="left")

        var = tk.StringVar()
        var.set("Présent")
        statut_vars[nom] = var
        tk.OptionMenu(frame_etud, var, "Présent", "Absent", "Retard").pack(side="left")

        entry_retard = tk.Entry(frame_etud, width=10)
        entry_retard.pack(side="left", padx=5)
        duree_retards[nom] = entry_retard

    tk.Button(fenetre, text="Retour", command=afficher_accueil, bg="grey", fg="white").pack(pady=10)

def enregistrer():
    date = datetime.now().strftime("%Y-%m-%d")
    jour = calendar.day_name[datetime.now().weekday()]
    heure = datetime.now().strftime("%H:%M")
    filiere = var_filiere.get()
    cours = champ_cours.get()

    for nom in etudiants_par_filiere[filiere]:
        statut = statut_vars[nom].get()
        duree = duree_retards[nom].get() if statut == "Retard" else ""

        cursor.execute('''INSERT INTO absences (date, jour, heure, filiere, cours, etudiant, statut, duree_retard, justification)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (date, jour, heure, filiere, cours, nom, statut, duree, ""))
    conn.commit()
    messagebox.showinfo("Succès", "Enregistrement effectué avec succès !")

def justification():
    effacer_fenetre()
    tk.Label(fenetre, text="Justification des absences et retards", font=("Arial", 14), bg="lightblue").pack(pady=10)

    cursor.execute("SELECT id, etudiant, statut, justification FROM absences WHERE justification IS NULL OR justification = ''")
    lignes = cursor.fetchall()

    for ligne in lignes:
        id_, nom, statut, _ = ligne
        frame = tk.Frame(fenetre, bg="white")
        frame.pack(padx=10, pady=5, fill="x")
        tk.Label(frame, text=f"{nom} - {statut}", width=40, anchor="w", bg="white").pack(side="left")
        champ_justif = tk.Entry(frame, width=40)
        champ_justif.pack(side="left")

        def sauvegarder(just_entry=champ_justif, ligne_id=id_):
            texte = just_entry.get()
            cursor.execute("UPDATE absences SET justification = ? WHERE id = ?", (texte, ligne_id))
            conn.commit()
            messagebox.showinfo("Succès", f"Justification enregistrée pour {nom}")

        tk.Button(frame, text="Sauvegarder", command=sauvegarder).pack(side="left", padx=5)

    tk.Button(fenetre, text="Retour", command=afficher_accueil, bg="grey", fg="white").pack(pady=10)

def afficher_absences_retards_du_jour():
    effacer_fenetre()
    date_du_jour = datetime.now().strftime("%Y-%m-%d")

    tk.Label(fenetre, text=f"Absences et retards du {date_du_jour}", font=("Arial", 14), bg="lightblue").pack(pady=10)
    cursor.execute("SELECT etudiant, statut, duree_retard FROM absences WHERE date = ?", (date_du_jour,))
    resultats = cursor.fetchall()

    if not resultats:
        tk.Label(fenetre, text="Aucune absence ou retard pour aujourd'hui.", bg="lightblue").pack(pady=10)
    else:
        for etu, stat, duree in resultats:
            ligne = f"{etu} - {stat}"
            if stat == "Retard":
                ligne += f" ({duree})"
            tk.Label(fenetre, text=ligne, anchor="w", bg="white").pack(fill="x", padx=20, pady=2)

    tk.Button(fenetre, text="Retour", command=afficher_accueil, bg="grey", fg="white").pack(pady=10)

# Lancement de l'application
afficher_accueil()
fenetre.mainloop()
conn.close()