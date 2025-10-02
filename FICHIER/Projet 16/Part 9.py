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
    "CS27": ["BADO Yannick", "BADOLO Patricia", "BALIMA Hectore"]  # Ajouter la liste complète ici
}

statut_vars = {}
duree_retards = {}
fenetre = tk.Tk()
fenetre.title("Gestion des absences")
fenetre.geometry("900x700")
fenetre.config(bg="lightblue")

var_filiere = tk.StringVar()
var_filiere.set("CS27")
fenetre_absents_retards = None


def afficher_accueil():
    for widget in fenetre.winfo_children():
        widget.destroy()

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
    if jour_actuel == "Saturday":
        tk.Button(fenetre, text="Générer rapport hebdomadaire", command=generer_rapport_hebdo, bg="darkblue", fg="white").pack(pady=5)


def afficher_liste_etudiants():
    for widget in fenetre.winfo_children():
        widget.destroy()

    afficher_accueil()

    filiere = var_filiere.get()
    frame_etudiants_container = tk.Frame(fenetre)
    frame_etudiants_container.pack(fill="both", expand=True, padx=10, pady=10)

    canvas_etudiants = tk.Canvas(frame_etudiants_container, bg="white")
    scrollbar_etudiants = tk.Scrollbar(frame_etudiants_container, orient="vertical", command=canvas_etudiants.yview)
    frame_etudiants = tk.Frame(canvas_etudiants, bg="white")

    frame_etudiants.bind("<Configure>", lambda e: canvas_etudiants.configure(scrollregion=canvas_etudiants.bbox("all")))
    canvas_etudiants.create_window((0, 0), window=frame_etudiants, anchor="nw")
    canvas_etudiants.configure(yscrollcommand=scrollbar_etudiants.set)

    canvas_etudiants.pack(side="left", fill="both", expand=True)
    scrollbar_etudiants.pack(side="right", fill="y")

    global statut_vars
    statut_vars = {}

    for nom in etudiants_par_filiere[filiere]:
        frame = tk.Frame(frame_etudiants, bg="white")
        frame.pack(fill="x", padx=5, pady=2)
        tk.Label(frame, text=nom, width=30, anchor="w", bg="white").pack(side="left")
        var_abs = tk.IntVar()
        var_retard = tk.IntVar()
        statut_vars[nom] = (var_abs, var_retard)
        tk.Checkbutton(frame, text="Absent", variable=var_abs, bg="white").pack(side="left")
        tk.Checkbutton(frame, text="Retard", variable=var_retard, bg="white").pack(side="left")


def enregistrer():
    duree_retards.clear()
    cours = champ_cours.get()
    filiere = var_filiere.get()
    maintenant = datetime.now()
    date = maintenant.strftime("%Y-%m-%d")
    jour = calendar.day_name[maintenant.weekday()]
    heure = maintenant.strftime("%H:%M")

    for nom, (var_abs, var_retard) in statut_vars.items():
        statut = "Présent"
        duree = ""
        if var_abs.get():
            statut = "Absent"
        elif var_retard.get():
            statut = "Retard"
            retard = datetime.now() - datetime.strptime("08:00", "%H:%M")
            minutes = retard.seconds // 60
            duree = f"{minutes} min"
            duree_retards[nom] = duree
        if statut != "Présent":
            cursor.execute('''INSERT INTO absences (date, jour, heure, filiere, cours, etudiant, statut, duree_retard, justification)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (date, jour, heure, filiere, cours, nom, statut, duree, ""))
    conn.commit()
    messagebox.showinfo("Succès", "Données enregistrées avec succès")


def justification():
    for widget in fenetre.winfo_children():
        widget.destroy()

    mot_de_passe = simpledialog.askstring("Sécurité", "Entrez le mot de passe :", show='*')
    if mot_de_passe != "admin123":
        messagebox.showerror("Erreur", "Mot de passe incorrect")
        afficher_accueil()
        return

    tk.Label(fenetre, text="Justification des absences/retards", bg="lightblue").pack(pady=5)
    frame = tk.Frame(fenetre)
    frame.pack(fill="both", expand=True)
    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    cursor.execute("SELECT * FROM absences WHERE justification IS NULL OR justification = ''")
    lignes = cursor.fetchall()
    champs = {}
    for ligne in lignes:
        text = f"{ligne[1]} {ligne[2]} | {ligne[6]} | {ligne[7]}"
        tk.Label(scroll_frame, text=text, bg="white").pack(fill="x")
        champ = tk.Entry(scroll_frame)
        champ.pack(fill="x")
        champs[ligne[0]] = champ

    def sauver():
        for id_, champ in champs.items():
            val = champ.get()
            cursor.execute("UPDATE absences SET justification = ? WHERE id = ?", (val, id_))
        conn.commit()
        messagebox.showinfo("Succès", "Justifications enregistrées")
        afficher_accueil()

    tk.Button(fenetre, text="Sauvegarder", command=sauver, bg="green", fg="white").pack(pady=5)
    tk.Button(fenetre, text="Retour", command=afficher_accueil).pack()


def afficher_absences_retards_du_jour():
    global fenetre_absents_retards
    if fenetre_absents_retards is not None and fenetre_absents_retards.winfo_exists():
        fenetre_absents_retards.destroy()
    fenetre_absents_retards = tk.Toplevel(fenetre)
    fenetre_absents_retards.title("Absences et retards du jour")
    frame = tk.Frame(fenetre_absents_retards)
    frame.pack(fill="both", expand=True)
    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    aujourd_hui = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT etudiant, statut, duree_retard FROM absences WHERE date = ?", (aujourd_hui,))
    lignes = cursor.fetchall()
    for nom, statut, duree in lignes:
        texte = f"{nom} - {statut}"
        if statut == "Retard":
            texte += f" ({duree})"
        tk.Label(scroll_frame, text=texte, anchor="w").pack(fill="x")


def generer_rapport_hebdo():
    debut = datetime.now() - timedelta(days=6)
    date_debut = debut.strftime("%Y-%m-%d")
    date_fin = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        SELECT etudiant, statut, duree_retard
        FROM absences
        WHERE date BETWEEN ? AND ?
    """, (date_debut, date_fin))
    lignes = cursor.fetchall()

    stats_etudiants = {}

    for etudiant, statut, duree in lignes:
        if etudiant not in stats_etudiants:
            stats_etudiants[etudiant] = {'absent': 0, 'retard': 0, 'duree_retard': 0}
        if statut == "Absent":
            stats_etudiants[etudiant]['absent'] += 1
        elif statut == "Retard":
            stats_etudiants[etudiant]['retard'] += 1
            if duree:
                try:
                    minutes = int(duree.split()[0])
                except:
                    minutes = 0
                stats_etudiants[etudiant]['duree_retard'] += minutes

    # Affichage du rapport dans la fenêtre principale (écrase l'ancien contenu)
    for widget in fenetre.winfo_children():
        widget.destroy()

    tk.Label(fenetre, text=f"Rapport hebdomadaire du {date_debut} au {date_fin}", font=("Arial", 14, "bold"), bg="lightblue").pack(pady=10)

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

    for etudiant, stats in sorted(stats_etudiants.items()):
        texte = (f"{etudiant} : Absences = {stats['absent']} | "
                 f"Retards = {stats['retard']} | "
                 f"Durée totale retard = {stats['duree_retard']} min")
        tk.Label(scroll_frame, text=texte, anchor="w", bg="white").pack(fill="x", pady=2)

    tk.Button(fenetre, text="Retour", command=afficher_accueil).pack(pady=10)


# Lancement de l'application
afficher_accueil()
fenetre.mainloop()
conn.close()