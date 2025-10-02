import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from datetime import datetime, timedelta
import calendar

# --- Configuration Base de Données ---
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

# --- Données des étudiants ---
etudiants_par_filiere = {
    "CS27": [
        "BADO Yannick", "BADOLO Patricia", "BALIMA Hectore", "BAMOUNI Grace",
        "BASSINGA Jessica", "BATIONO Betranel", "BIRBA Wendabo Casimir", # ...
        "ZOUNGRANA Eulalie", "ZOUNGRANA Sébastien"
    ]
}

# --- Variables globales ---
statut_vars = {}
duree_retards = {}
var_filiere = tk.StringVar(value="CS27")

# --- Fenêtre principale ---
fenetre = tk.Tk()
fenetre.title("Absence & Retard Manager")
fenetre.geometry("900x700")
fenetre.config(bg="lightyellow")

# --- Fonctions utilitaires ---
def creer_bandeau():
    bandeau = tk.Frame(fenetre, bg="#002480", height=40)
    bandeau.pack(side="top", fill="x")
    tk.Label(bandeau, text="Absence Management", fg="white", bg="#002480",
             font=("Arial", 16, "bold")).pack(pady=5)

def nettoyer_fenetre():
    for widget in fenetre.winfo_children():
        widget.destroy()

# --- Affichage Accueil ---
def afficher_accueil():
    nettoyer_fenetre()
    creer_bandeau()
    jour = calendar.day_name[datetime.now().weekday()]
    if jour != "Sunday":
        tk.Label(fenetre, text=f"TODAY: {jour}", font=("Arial", 12, "bold"), bg="green").pack(pady=5)

    tk.Label(fenetre, text="Filière :", bg="lightblue").pack(pady=5)
    tk.OptionMenu(fenetre, var_filiere, *etudiants_par_filiere.keys()).pack()

    tk.Label(fenetre, text="Cours :", bg="lightblue").pack(pady=5)
    global champ_cours
    champ_cours = tk.Entry(fenetre)
    champ_cours.pack(pady=5)

    tk.Button(fenetre, text="Afficher les étudiants", command=afficher_liste_etudiants, bg="skyblue").pack(pady=3)
    tk.Button(fenetre, text="Enregistrer", command=enregistrer, bg="green", fg="white").pack(pady=5)
    tk.Button(fenetre, text="Justifications", command=justification, bg="orange", fg="white").pack(pady=5)
    tk.Button(fenetre, text="Rapport Hebdomadaire", command=generer_rapport_hebdo, bg="darkblue", fg="white").pack(pady=5)

# --- Affichage Liste Etudiants ---
def afficher_liste_etudiants():
    nettoyer_fenetre()
    creer_bandeau()
    afficher_accueil()
    filiere = var_filiere.get()

    container = tk.Frame(fenetre)
    container.pack(fill="both", expand=True, padx=10, pady=10)
    canvas = tk.Canvas(container)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    global statut_vars
    statut_vars = {}
    for nom in etudiants_par_filiere[filiere]:
        ligne = tk.Frame(scrollable_frame, bg="white")
        ligne.pack(fill="x", padx=5, pady=2)
        tk.Label(ligne, text=nom, width=30, anchor="w", bg="white").pack(side="left")
        var_abs, var_retard = tk.IntVar(), tk.IntVar()
        statut_vars[nom] = (var_abs, var_retard)
        tk.Checkbutton(ligne, text="Absent", variable=var_abs, bg="white").pack(side="left")
        tk.Checkbutton(ligne, text="Retard", variable=var_retard, bg="white").pack(side="left")

# --- Enregistrement des présences ---
def enregistrer():
    duree_retards.clear()
    cours = champ_cours.get()
    filiere = var_filiere.get()
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    jour = calendar.day_name[now.weekday()]
    heure = now.strftime("%H:%M")

    for nom, (var_abs, var_retard) in statut_vars.items():
        statut, duree = "Présent", ""
        if var_abs.get():
            statut = "Absent"
        elif var_retard.get():
            statut = "Retard"
            minutes = (now - datetime.strptime("08:00", "%H:%M")).seconds // 60
            duree = f"{minutes} min"
            duree_retards[nom] = duree

        if statut != "Présent":
            cursor.execute('''INSERT INTO absences
                (date, jour, heure, filiere, cours, etudiant, statut, duree_retard, justification)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (date, jour, heure, filiere, cours, nom, statut, duree, ""))

    conn.commit()
    messagebox.showinfo("Succès", "Données enregistrées")

# --- Interface de justification ---
def justification():
    nettoyer_fenetre()
    creer_bandeau()
    mdp = simpledialog.askstring("Sécurité", "Mot de passe :", show='*')
    if mdp != "M.SAMA6940":
        messagebox.showerror("Erreur", "Mot de passe incorrect")
        afficher_accueil()
        return

    tk.Label(fenetre, text="Justification des absences et retards", bg="blue", fg="white").pack(pady=5)

    frame = tk.Frame(fenetre)
    frame.pack(fill="both", expand=True)
    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable = tk.Frame(canvas)

    scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    champs = {}
    cursor.execute("SELECT * FROM absences WHERE justification IS NULL OR justification = ''")
    lignes = cursor.fetchall()
    for ligne in lignes:
        info = f"{ligne[1]} {ligne[2]} | {ligne[6]} | {ligne[7]}"
        tk.Label(scrollable, text=info, bg="white").pack(fill="x")
        champ = tk.Entry(scrollable)
        champ.pack(fill="x")
        champs[ligne[0]] = champ

    def sauver():
        for id_, champ in champs.items():
            texte = champ.get()
            cursor.execute("UPDATE absences SET justification = ? WHERE id = ?", (texte, id_))
        conn.commit()
        messagebox.showinfo("Succès", "Justifications enregistrées")
        afficher_accueil()

    tk.Button(fenetre, text="Sauvegarder", command=sauver, bg="green", fg="white").pack(pady=5)
    tk.Button(fenetre, text="Retour", command=afficher_accueil).pack()

# --- Rapport Hebdomadaire ---
def generer_rapport_hebdo():
    nettoyer_fenetre()
    creer_bandeau()

    debut = datetime.now() - timedelta(days=6)
    cursor.execute("""
        SELECT date, jour, etudiant, statut, duree_retard
        FROM absences
        WHERE date BETWEEN ? AND ?
        ORDER BY etudiant, date
    """, (debut.strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d")))
    lignes = cursor.fetchall()

    rapports = {}
    for date_str, jour, etudiant, statut, duree in lignes:
        if jour == "Sunday":
            continue
        if etudiant not in rapports:
            rapports[etudiant] = {"absents": 0, "retards": 0, "minutes": 0, "details": []}
        if statut == "Absent":
            rapports[etudiant]["absents"] += 1
        elif statut == "Retard":
            rapports[etudiant]["retards"] += 1
            if duree:
                rapports[etudiant]["minutes"] += int(duree.split()[0])
        detail = f"{date_str} ({jour}): {statut}"
        if duree:
            detail += f" - {duree}"
        rapports[etudiant]["details"].append(detail)

    frame = tk.Frame(fenetre)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tk.Label(scroll_frame, text="Rapport hebdomadaire", font=("Arial", 12, "bold")).pack(pady=5)

    for etudiant, data in rapports.items():
        tk.Label(scroll_frame, text=etudiant, font=("Arial", 11, "bold"), anchor="w").pack(fill="x", pady=(10, 2))
        for detail in data["details"]:
            tk.Label(scroll_frame, text="  " + detail, anchor="w").pack(fill="x")
        resume = (f"Total: {data['absents']} absences, {data['retards']} retards, {data['minutes']} min de retard")
        tk.Label(scroll_frame, text=resume, font=("Arial", 10, "italic"), anchor="w").pack(fill="x", pady=(0, 5))

    tk.Button(fenetre, text="Retour", command=afficher_accueil, bg="gray", fg="white").pack(pady=10)

# --- Lancement ---
afficher_accueil()
fenetre.mainloop()
conn.close()
