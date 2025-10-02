import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sqlite3

HEURE_COURS = datetime.strptime("08:00", "%H:%M")

etudiants_par_filiere = {
    "CS27": [
        "BADO Yannick", "BADOLO Patricia", "BALIMA Hectore", "BAMOUNI Grace", "BASSINGA Jessica",
        "BATIONO Betranel", "BIRBA Wendabo Casimir", "BONKOUNGOU Jerome", "BOUNKOUGOU Wendyam Vanessa",
        "ZOUNGRANA Sébastien"
    ],
}

conn = sqlite3.connect('absences.db')
cursor = conn.cursor()

def colonne_existe(table, colonne):
    cursor.execute(f"PRAGMA table_info({table})")
    colonnes = [info[1] for info in cursor.fetchall()]
    return colonne in colonnes

def initialiser_bdd():
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
    # Ajouter la colonne jour si elle n'existe pas
    if not colonne_existe('absences', 'jour'):
        try:
            cursor.execute("ALTER TABLE absences ADD COLUMN jour TEXT")
            conn.commit()
        except Exception as e:
            print("Erreur ajout colonne 'jour':", e)

statut_vars = {}
boutons_retard = {}

def afficher_etudiants():
    for widget in frame_etudiants.winfo_children():
        widget.destroy()

    filiere = var_filiere.get()
    if filiere not in etudiants_par_filiere:
        return

    etudiants = etudiants_par_filiere[filiere]
    statut_vars.clear()

    for nom in etudiants:
        frame = tk.Frame(frame_etudiants, bg="#f0f8ff")
        frame.pack(fill="x", pady=2)

        label = tk.Label(frame, text=nom, width=30, anchor="w", bg="#f0f8ff")
        label.pack(side="left")

        var_abs = tk.IntVar()
        var_retard = tk.IntVar()
        statut_vars[nom] = (var_abs, var_retard)

        tk.Checkbutton(frame, text="Absent", variable=var_abs, bg="#f0f8ff").pack(side="left")
        tk.Checkbutton(frame, text="Retard", variable=var_retard, bg="#f0f8ff").pack(side="left")

def enregistrer():
    cours = entree_cours.get()
    filiere = var_filiere.get()
    jour = var_jour.get()
    if filiere == "" or cours == "" or jour == "":
        messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")
        return

    retardataires = [nom for nom, (absent, retard) in statut_vars.items() if retard.get()]
    if retardataires:
        fenetre_retards(retardataires)
    else:
        enregistrer_sans_retard()

def enregistrer_sans_retard():
    cours = entree_cours.get()
    filiere = var_filiere.get()
    jour = var_jour.get()
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    heure_str = now.strftime("%H:%M")

    lignes_enregistrees = []

    for nom, (absent, retard) in statut_vars.items():
        if not absent.get() and not retard.get():
            continue
        statut = "Absent" if absent.get() else "Retard"
        duree_retard = "?" if retard.get() else ""
        cursor.execute('''
            INSERT INTO absences (date, jour, heure, filiere, cours, etudiant, statut, duree_retard, justification)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (date_str, jour, heure_str, filiere, cours, nom, statut, duree_retard, ""))
        lignes_enregistrees.append([date_str, jour, heure_str, filiere, cours, nom, statut, duree_retard, ""])

    conn.commit()
    afficher_recapitulatif(lignes_enregistrees)

def fenetre_retards(retardataires):
    fen = tk.Toplevel(fenetre)
    fen.title("Minuteurs de Retard")
    fen.geometry("500x400")
    tk.Label(fen, text="Minuteurs des retardataires", font=("Arial", 14, "bold")).pack(pady=10)

    boutons_retard.clear()

    for nom in retardataires:
        frame = tk.Frame(fen)
        frame.pack(pady=5, fill="x")

        label = tk.Label(frame, text=f"{nom} : en cours...", font=("Arial", 10))
        label.pack(side="left", padx=10)

        btn = tk.Button(frame, text="Arrêter", command=lambda n=nom, l=label: arreter_minuteur(n, l))
        btn.pack(side="left")

    def enregistrer_retards():
        cours = entree_cours.get()
        filiere = var_filiere.get()
        jour = var_jour.get()
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        heure_str = now.strftime("%H:%M")

        lignes = []
        for nom, (absent, retard) in statut_vars.items():
            if not absent.get() and not retard.get():
                continue
            statut = "Absent" if absent.get() else "Retard"
            duree_retard = boutons_retard.get(nom, "Non arrêté") if statut == "Retard" else ""
            cursor.execute('''
                INSERT INTO absences (date, jour, heure, filiere, cours, etudiant, statut, duree_retard, justification)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (date_str, jour, heure_str, filiere, cours, nom, statut, duree_retard, ""))
            lignes.append([date_str, jour, heure_str, filiere, cours, nom, statut, duree_retard, ""])
        conn.commit()
        afficher_recapitulatif(lignes)
        fen.destroy()

    tk.Button(fen, text="Enregistrer tous les retards", bg="bisque", fg="white", command=enregistrer_retards).pack(pady=20)

def arreter_minuteur(nom, label):
    maintenant = datetime.now()
    retard = maintenant - HEURE_COURS
    minutes = retard.seconds // 60
    secondes = retard.seconds % 60
    label.config(text=f"{nom} : Retard de {minutes} min {secondes} s")
    boutons_retard[nom] = f"{minutes} min {secondes} s"

def afficher_recapitulatif(lignes):
    recap = tk.Toplevel(fenetre)
    recap.title("Récapitulatif des absences")
    text = tk.Text(recap, width=100, height=25)
    text.pack(padx=10, pady=10)
    text.insert(tk.END, "Date | Jour | Heure | Filière | Cours | Étudiant | Statut | Durée Retard | Justification\n")
    text.insert(tk.END, "-"*120 + "\n")
    for ligne in lignes:
        text.insert(tk.END, " | ".join(str(item) for item in ligne) + "\n")
    text.config(state=tk.DISABLED)

def verifier_acces_justification():
    def verifier():
        if champ_mdp.get() == "admin123":
            fen_mdp.destroy()
            ouvrir_interface_justification()
        else:
            messagebox.showerror("Erreur", "Mot de passe incorrect")

    fen_mdp = tk.Toplevel(fenetre)
    fen_mdp.title("Accès sécurisé")
    tk.Label(fen_mdp, text="Entrez le mot de passe :").pack(pady=5)
    champ_mdp = tk.Entry(fen_mdp, show="*")
    champ_mdp.pack(pady=5)
    tk.Button(fen_mdp, text="Valider", command=verifier).pack(pady=5)

def ouvrir_interface_justification():
    fen_justif = tk.Toplevel(fenetre)
    fen_justif.title("Justification des absences et retards")
    fen_justif.geometry("900x500")

    tk.Label(fen_justif, text="Ajouter une justification :", font=("Arial", 14, "bold")).pack(pady=10)

    justifications = {}

    cursor.execute('SELECT * FROM absences WHERE statut IN ("Absent", "Retard")')
    lignes = cursor.fetchall()

    for ligne in lignes:
        id_, date_, jour_, heure_, filiere_, cours_, etudiant_, statut_, duree_retard_, justification_ = ligne
        frame = tk.Frame(fen_justif)
        frame.pack(padx=5, pady=2, fill="x")
        desc = f'{date_} | {jour_} | {heure_} | {filiere_} | {cours_} | {etudiant_} | {statut_} | {duree_retard_}'
        tk.Label(frame, text=desc, anchor="w", width=100).pack(side="left")
        champ = tk.Entry(frame, width=40)
        champ.pack(side="right")
        champ.insert(0, justification_ if justification_ else "")
        justifications[id_] = champ

    def sauvegarder_justifications():
        for id_, champ in justifications.items():
            nouvelle_justif = champ.get()
            cursor.execute('UPDATE absences SET justification = ? WHERE id = ?', (nouvelle_justif, id_))
        conn.commit()
        messagebox.showinfo("Succès", "Justifications enregistrées.")

    tk.Button(fen_justif, text="Sauvegarder les justifications", command=sauvegarder_justifications, bg="green", fg="white").pack(pady=10)

# --- Interface principale ---

fenetre = tk.Tk()
fenetre.title("Suivi des absences")
fenetre.geometry("700x750")
fenetre.config(bg="cyan")

tk.Label(fenetre, text="Gestion des Absences", font=("Arial", 16, "bold"), bg="yellowgreen", fg="#003366").pack(pady=10)

# Filtre filière
tk.Label(fenetre, text="Filière :", bg="bisque").pack()
var_filiere = tk.StringVar()
menu_filiere = tk.OptionMenu(fenetre, var_filiere, *etudiants_par_filiere.keys())
menu_filiere.pack()
var_filiere.set("CS27")

# Choix du jour (sans dimanche)
tk.Label(fenetre, text="Jour :", bg="bisque").pack()
jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
var_jour = tk.StringVar()
menu_jour = tk.OptionMenu(fenetre, var_jour, *jours_semaine)
menu_jour.pack()
var_jour.set(jours_semaine[0])

# Cours
tk.Label(fenetre, text="Cours :", bg="yellowgreen").pack()
entree_cours = tk.Entry(fenetre)
entree_cours.pack(pady=5)

# Liste étudiants avec scrollbar
container = tk.Frame(fenetre, bg="black", bd=2, relief="groove")
container.pack(fill="both", expand=True, padx=10, pady=30)

canvas = tk.Canvas(container, bg="olive")
canvas.pack(side="right", fill="both", expand=True)

scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

frame_etudiants = tk.Frame(canvas, bg="green")
canvas.create_window((0, 0), window=frame_etudiants, anchor="nw")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame_etudiants.bind("<Configure>", on_frame_configure)

# Boutons
tk.Button(fenetre, text="Afficher la liste", command=afficher_etudiants, bg="orange", fg="white", padx=10, pady=5).pack(pady=5)
tk.Button(fenetre, text="Enregistrer", command=enregistrer, bg="olive", fg="white", padx=20, pady=10).pack(pady=10)
tk.Button(fenetre, text="Justifier Absences/Retards", bg="red", fg="white", command=verifier_acces_justification).pack(pady=5)

initialiser_bdd()
afficher_etudiants()

fenetre.mainloop()
conn.close()