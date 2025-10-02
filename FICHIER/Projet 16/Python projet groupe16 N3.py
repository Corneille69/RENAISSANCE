import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from datetime import datetime
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
    "CS27": [f"Étudiant {i+1}" for i in range(400)]
}

statut_vars = {}
retard_debut = None
duree_retards = {}

fenetre = tk.Tk()
fenetre.title("Gestion des absences")
fenetre.geometry("800x700")
fenetre.config(bg="lightblue")

# Affichage du jour de la semaine
jour_actuel = calendar.day_name[datetime.now().weekday()]
if jour_actuel != "Sunday":
    label_jour = tk.Label(fenetre, text=f"Aujourd'hui : {jour_actuel}", font=("Arial", 12, "bold"), bg="lightblue")
    label_jour.pack(pady=5)

# Scrollbar pour étudiants
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

def initialiser_interface():
    for widget in frame_etudiants.winfo_children():
        widget.destroy()

    filiere = var_filiere.get()
    if filiere not in etudiants_par_filiere:
        return

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
    global retard_debut, duree_retards

    cours = champ_cours.get()
    filiere = var_filiere.get()
    if not cours or not filiere:
        messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")
        return

    maintenant = datetime.now()
    date = maintenant.strftime("%Y-%m-%d")
    jour = calendar.day_name[maintenant.weekday()]
    if jour == "Sunday":
        messagebox.showinfo("Jour non autorisé", "Les cours ne sont pas enregistrés le dimanche.")
        return

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
    mot_de_passe = simpledialog.askstring("Sécurité", "Entrez le mot de passe pour accéder à la justification :", show='*')
    if mot_de_passe != "admin123":
        messagebox.showerror("Accès refusé", "Mot de passe incorrect.")
        return

    fen = tk.Toplevel(fenetre)
    fen.title("Justification")
    fen.geometry("1000x600")

    tk.Label(fen, text="Justifier les absences et retards", font=("Arial", 14, "bold")).pack(pady=10)

    frame_liste = tk.Frame(fen)
    frame_liste.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_liste)
    scrollbar = tk.Scrollbar(frame_liste, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    cursor.execute("SELECT * FROM absences WHERE justification IS NULL OR justification = ''")
    lignes = cursor.fetchall()

    champs_justif = {}
    for ligne in lignes:
        desc = f"{ligne[1]} ({ligne[2]}) | {ligne[3]} | {ligne[4]} | {ligne[5]} | {ligne[6]} | {ligne[7]} | {ligne[8]}"
        frame = tk.Frame(scroll_frame)
        frame.pack(fill="x", padx=5, pady=2)
        tk.Label(frame, text=desc, anchor="w", width=100).pack(side="left")
        champ = tk.Entry(frame, width=40)
        champ.pack(side="right")
        champs_justif[ligne[0]] = champ

    def sauvegarder():
        for id_ligne, champ in champs_justif.items():
            justification = champ.get()
            cursor.execute("UPDATE absences SET justification = ? WHERE id = ?", (justification, id_ligne))
        conn.commit()
        messagebox.showinfo("Justification", "Justifications enregistrées.")
        fen.destroy()

    tk.Button(fen, text="Sauvegarder les justifications", command=sauvegarder, bg="green", fg="white").pack(pady=10)

# Interface principale
tk.Label(fenetre, text="Filière :", bg="lightblue").pack(pady=5)
var_filiere = tk.StringVar()
tk.OptionMenu(fenetre, var_filiere, *etudiants_par_filiere.keys()).pack()
var_filiere.set("CS27")

tk.Label(fenetre, text="Cours :", bg="lightblue").pack(pady=5)
champ_cours = tk.Entry(fenetre)
champ_cours.pack(pady=5)

tk.Button(fenetre, text="Afficher les étudiants", command=initialiser_interface, bg="skyblue").pack(pady=5)

tk.Button(fenetre, text="Enregistrer", command=enregistrer, bg="green", fg="white").pack(pady=10)
tk.Button(fenetre, text="Justifier Absences/Retards", command=justification, bg="orange", fg="white").pack(pady=5)

fenetre.mainloop()
conn.close()