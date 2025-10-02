import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta

# Connexion à la base SQLite
conn = sqlite3.connect('absences.db')
cursor = conn.cursor()

# Création de la table si elle n'existe pas
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

# Paramètres
HEURE_COURS = datetime.strptime("08:00", "%H:%M")

# Interface principale
fenetre = tk.Tk()
fenetre.title("Gestion des Absences et Retards")
fenetre.geometry("800x600")

etudiants = [f"Etudiant {i+1}" for i in range(200)]
justifications = {}
retard_debut = None

canvas = tk.Canvas(fenetre)
scroll_y = tk.Scrollbar(fenetre, orient="vertical", command=canvas.yview)
scroll_frame = tk.Frame(canvas)

scroll_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)

canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

# Fonctions principales
def enregistrer_presence(nom, statut_var, retard_label):
    statut = statut_var.get()
    heure_actuelle = datetime.now().strftime("%H:%M")
    date_ = datetime.now().strftime("%Y-%m-%d")
    jour_ = datetime.now().strftime("%A")
    filiere = "CS27"
    cours = "Programmation"
    duree_retard = ""

    if statut == "Retard":
        heure_retard = datetime.strptime(heure_actuelle, "%H:%M")
        retard = heure_retard - HEURE_COURS
        duree_minutes = int(retard.total_seconds() / 60)
        duree_retard = f"{duree_minutes} minutes"
        retard_label.config(text=duree_retard, fg="red")

    cursor.execute('''
        INSERT INTO absences (date, jour, heure, filiere, cours, etudiant, statut, duree_retard, justification)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (date_, jour_, heure_actuelle, filiere, cours, nom, statut, duree_retard, "")
    )
    conn.commit()
    messagebox.showinfo("Succès", f"{nom} marqué comme {statut}")

def ouvrir_interface_justification():
    fen_justif = tk.Toplevel(fenetre)
    fen_justif.title("Justification des absences et retards")
    fen_justif.geometry("1200x600")

    tk.Label(fen_justif, text="Ajouter une justification :", font=("Arial", 14, "bold")).pack(pady=10)

    filtre_var = tk.StringVar(value="Tous")
    options_filtre = ["Tous", "Absents non justifiés", "Retards non justifiés", "Retards > 10 min"]
    tk.OptionMenu(fen_justif, filtre_var, *options_filtre).pack()

    justifications = {}
    cadres_affiches = []

    def afficher_justifications():
        for c in cadres_affiches:
            c.destroy()
        cadres_affiches.clear()

        filtre = filtre_var.get()
        cursor.execute('SELECT * FROM absences WHERE statut IN ("Absent", "Retard") ORDER BY date DESC')
        lignes = cursor.fetchall()

        for ligne in lignes:
            id_, date_, jour_, heure_, filiere_, cours_, etudiant_, statut_, duree_retard_, justification_ = ligne

            if filtre == "Absents non justifiés" and (statut_ != "Absent" or justification_):
                continue
            if filtre == "Retards non justifiés" and (statut_ != "Retard" or justification_):
                continue
            if filtre == "Retards > 10 min":
                try:
                    minutes = int(duree_retard_.split()[0])
                    if statut_ != "Retard" or minutes <= 10:
                        continue
                except:
                    continue

            frame = tk.Frame(fen_justif)
            frame.pack(padx=5, pady=2, fill="x")
            cadres_affiches.append(frame)

            desc = f'{date_} | {jour_} | {heure_} | {filiere_} | {cours_} | {etudiant_} | {statut_} | {duree_retard_}'
            tk.Label(frame, text=desc, anchor="w", width=100).pack(side="left")

            champ = tk.Entry(frame, width=40)
            champ.insert(0, justification_ if justification_ else "")
            champ.pack(side="left")
            justifications[id_] = champ

            label_info = tk.Label(frame, text="", width=12)
            label_info.pack(side="right")

            btn = tk.Button(frame, text="Justifier", bg="green", fg="white",
                            command=lambda i=id_, c=champ, l=label_info: justifier_individuellement(i, c, l))
            btn.pack(side="left", padx=5)

    def justifier_individuellement(id_, champ, label_info):
        nouvelle_justif = champ.get()
        cursor.execute('UPDATE absences SET justification = ? WHERE id = ?', (nouvelle_justif, id_))
        conn.commit()
        label_info.config(text="✅ Sauvegardé", fg="green")

    def sauvegarder_justifications():
        for id_, champ in justifications.items():
            nouvelle_justif = champ.get()
            cursor.execute('UPDATE absences SET justification = ? WHERE id = ?', (nouvelle_justif, id_))
        conn.commit()
        messagebox.showinfo("Succès", "Toutes les justifications ont été enregistrées.")

    filtre_var.trace("w", lambda *args: afficher_justifications())

    tk.Button(fen_justif, text="Sauvegarder toutes les justifications", command=sauvegarder_justifications,
              bg="darkblue", fg="white").pack(pady=10)

    afficher_justifications()

# Affichage des étudiants
tk.Label(scroll_frame, text="Liste des étudiants CS27", font=("Arial", 14, "bold"), bg="lightblue").pack(fill="x")

for nom in etudiants:
    cadre = tk.Frame(scroll_frame)
    cadre.pack(fill="x", padx=5, pady=2)

    label_nom = tk.Label(cadre, text=nom, width=30, anchor="w")
    label_nom.pack(side="left")

    statut_var = tk.StringVar()
    statut_menu = tk.OptionMenu(cadre, statut_var, "Présent", "Absent", "Retard")
    statut_menu.pack(side="left")

    label_retard = tk.Label(cadre, text="", width=15)
    label_retard.pack(side="left")

    btn_enregistrer = tk.Button(cadre, text="Enregistrer", bg="blue", fg="white",
                                command=lambda n=nom, sv=statut_var, lr=label_retard: enregistrer_presence(n, sv, lr))
    btn_enregistrer.pack(side="left", padx=5)

# Bouton pour ouvrir l'interface de justification
tk.Button(fenetre, text="Justifier Absences / Retards", bg="green", fg="white", command=ouvrir_interface_justification).pack(pady=10)

fenetre.mainloop()
