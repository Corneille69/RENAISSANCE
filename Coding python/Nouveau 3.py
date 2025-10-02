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
    "CS27": ["BADO Yannick", "BADOLO Patricia", "BALIMA Hectore", "BAMOUNI Grace", "BASSINGA Jessica",
        "BATIONO Betranel", "BIRBA Wendabo Casimir", "BONKOUNGOU Jerome", "BOUNKOUGOU Wendyam Vanessa",
        "BOUDA Mouniratou", "BOUGMA Sadiata", "COMPAORE Adim Fahim Saidou", "COMPAORE Kisito",
        "COMPAORE Salimata", "CONGO Anifatou", "COULIBALY Faez", "DAH Cheoutierou", "DAKUYO Prisca",
        "DAYAMBA Abigael", "DEHOUMOU Christelle", "DEMBELE Gaethan Khaleb", "DIALLO Maimata",
        "DORI Marie Madeleine", "DOUAMBASidonie", "DRABO Farel", "GADIERE Farida",
        "GARANE Farida Kevine", "ILBOUDO Balkissa", "ILBOUDO John Michee", "KABORE Albertine",
        "KABORE Karelle 2e jumelle", "KABORE Odiane Elia", "KABORE Grace Oceanne", "KABORE Awa",
        "KABORE Bienvenu", "KAFANDO Dan", "KAGAMBEGA Saturne", "KAGAMBEGA Claudine", "KAMBOU Yeri Hermine",
        "KANTAGBA Efraim", "KANTIONO Diane", "KERE Noeldinolippeu", "KIEMTORE Simplice",
        "KIENDREBEOGO Carine", "KIENDREBEOGO Sephora", "KIENDREBEOGO Moussa", "KIENDREBEOGO Arnaud",
        "KINI Jacob", "KOALGA Heliane", "KOANDA Checkib", "KOLOGO Robert", "KONDOMBO Josue",
        "KONOMBO Madeleine", "KOUTIEBOU Ornella", "KYEMTORE Gloria", "MANDI Melki", "MEDA Franck",
        "NACOULMA Betsaleel", "NANA Prisca", "NANA Marc", "NASSA Didier", "NIKIEMA Flora Marie Ines",
        "NIKIEMA Marieta", "NITIEMA Eddy Martial", "NKUNA Israel", "NOMBRE Ange", "N'ZOMBIE Rodrigue",
        "OUATTARA Fawzia", "OUEDRAOGO Corneille", "OUEDRAOGO Landry", "OUEDRAOGO Akram",
        "OUEDRAOGO Alimata", "OUEDRAOGO Adele", "OUEDRAOGO Jonathan", "OUEDRAOGO Esther",
        "OUEDRAOGO Abdoulaye", "OUILY Nasser", "PARE Joseph", "PARE Boris Marcel", "PARE Assetou",
        "ROUAMBA Mounira", "ROUAMBA Sarifatou", "SANFO Madi", "SANON Abdoul Ben Fatao",
        "SAWADOGO Grace", "SAWADOGO Elisabeth", "SAWADOGO Azael", "SAWADOGO Asseta", "SAWADOGO Risnata",
        "SEMDE Aicha", "SIMPORE Alima", "SIMPORE Sidiki", "SOULAMA Ulrich", "TANKOANO Michel",
        "TAO Fazollah", "TOE Kevin", "TOUBRIWOUMYIAN Yan Ulrich", "TOUGOUMA Trevis", "TRAORE Ramatou",
        "TRAORE Mathias", "TRAORE ESmelle", "WANGRE Esther", "ZABRE Elvine", "YABRE Amma",
        "YAMEOGO Aymar", "YAMEOGO Cedric", "YAMEOGO Athanasse", "YAMEOGO Angeline", "YAMEOGO Firmin",
        "YAMEOGO Marie Joseph", "YAMEOGO Claudine", "YANOGO Stephanie", "YELEMOU Martial",
        "YOUGBARE Eunice", "ZABRE Tania", "ZAMANE Elodie", "ZARANI Abdoul Kader", "ZINGUE Cynthia",
        "ZOMA Amelie", "ZONGO P.Juste", "ZONGO Pascal", "ZONGO Ange Anselme", "ZONGO Alida Isidore",
        "ZONGO Malkiram", "ZONGO Safiatou", "ZONGO Abdel Sadek", "ZOUGOURI Aurel Clauvis",
        "ZOUNGRANA Brenger", "ZOUNGRANA Zalissa", "ZOUNGRANA Eulalie", "ZOUNGRANA Sébastien"]  # Ajouter la liste complète ici
}

statut_vars = {}
duree_retards = {}
fenetre = tk.Tk()
fenetre.title("LATE GESTION")
fenetre.geometry("900x700")
fenetre.config(bg="lightyellow")

var_filiere = tk.StringVar()
var_filiere.set("CS27")
fenetre_absents_retards = None
def creer_bandeau(bandeau, message='Absence Management'):
    bandeau = tk.Frame(fenetre, bg="#000480", height=40)  # Couleur bleu foncé, hauteur fixe
    bandeau.pack(side="top", fill="x")

    label = tk.Label(bandeau, text="Absence Management", fg="white", bg="#002480",
                     font=("Arial", 16, "bold"))
    label.pack(pady=5)
    return bandeau

def afficher_accueil():
    for widget in fenetre.winfo_children():
        widget.destroy()

    creer_bandeau("Absence Management")

    jour_actuel = calendar.day_name[datetime.now().weekday()]
    if jour_actuel != "Sunday":
        tk.Label(fenetre, text=f"TODAYS : {jour_actuel}", font=("Arial", 12, "bold"), bg="green").pack(pady=5)

    tk.Label(fenetre, text="Filière :", bg="lightblue").pack(pady=5)
    tk.OptionMenu(fenetre, var_filiere, *etudiants_par_filiere.keys()).pack()

    tk.Label(fenetre, text="Course :", bg="lightblue").pack(pady=5)
    global champ_cours
    champ_cours = tk.Entry(fenetre)
    champ_cours.pack(pady=5)

    tk.Button(fenetre, text="Afficher les étudiants", command=afficher_liste_etudiants, bg="skyblue").pack(pady=3)
    tk.Button(fenetre, text="save", command=enregistrer, bg="green", fg="white").pack(pady=5)
    tk.Button(fenetre, text="Absence \ Tardiness Justification", command=justification, bg="orange", fg="white").pack(pady=5)
    
    tk.Button(fenetre, text="Générer rapport hebdomadaire", command=generer_rapport_hebdo, bg="darkblue", fg="white").pack(pady=5)


def afficher_liste_etudiants():
    for widget in fenetre.winfo_children():
        widget.destroy()
    creer_bandeau("Absence Management")
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
    creer_bandeau("Absence Management")
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
    creer_bandeau("Absence Management")
    mot_de_passe = simpledialog.askstring("Sécurité", "Entrez le mot de passe :", show='*')
    if mot_de_passe != "M.SAMA6940":
        messagebox.showerror("Erreur", "Mot de passe incorrect")
        afficher_accueil()
        return

    tk.Label(fenetre, text="Absence \ Tardiness Justification", bg="blue").pack(pady=5)
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
        creer_bandeau("Absence Management")
        for id_, champ in champs.items():
            val = champ.get()
            cursor.execute("UPDATE absences SET justification = ? WHERE id = ?", (val, id_))
        conn.commit()
        messagebox.showinfo("Succès", "Justifications enregistrées")
        afficher_accueil()

    tk.Button(fenetre, text="Sauvegarder", command=sauver, bg="green", fg="white").pack(pady=5)
    tk.Button(fenetre, text="Back", command=afficher_accueil).pack()





def generer_rapport_hebdo():
    for widget in fenetre.winfo_children():
        widget.destroy()
    creer_bandeau("Absence Management")
    debut = datetime.now() - timedelta(days=6)
    date_debut = debut.strftime("%Y-%m-%d")
    date_fin = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        SELECT date, jour, etudiant, statut, duree_retard
        FROM absences 
        WHERE date BETWEEN ? AND ?
        ORDER BY etudiant, date
    """, (date_debut, date_fin))
    lignes = cursor.fetchall()

    # Organiser les données par étudiant
    rapports = {}
    for date_str, jour, etudiant, statut, duree in lignes:
        if jour == "Sunday":
            continue  # Ignorer le dimanche
        if etudiant not in rapports:
            rapports[etudiant] = {"absents": 0, "retards": 0, "minutes_retard": 0, "details": []}
        if statut == "Absent":
            rapports[etudiant]["absents"] += 1
        elif statut == "Retard":
            rapports[etudiant]["retards"] += 1
            if duree:
                rapports[etudiant]["minutes_retard"] += int(duree.split()[0])
        # Ajouter détail journalier
        detail = f"{date_str} ({jour}): {statut}"
        if statut == "Retard" and duree:
            detail += f" - {duree}"
        rapports[etudiant]["details"].append(detail)

    # Création de la fenêtre avec scrollbar
    
  

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

    tk.Label(scroll_frame, text=f"Rapport du {date_debut} au {date_fin} (Lundi-Samedi)", font=("Arial", 12, "bold")).pack(pady=5)

    for etudiant, data in rapports.items():
        # Titre étudiant
        tk.Label(scroll_frame, text=etudiant, font=("Arial", 11, "bold"), anchor="w").pack(fill="x", pady=(10, 2))

        # Détail par jour
        for detail in data["details"]:
            tk.Label(scroll_frame, text="  " + detail, anchor="w", justify="left").pack(fill="x")

        # Résumé hebdo
        resume = (f"Total : {data['absents']} absences, {data['retards']} retards, "
                  f"{data['minutes_retard']} minutes de retard")
        tk.Label(scroll_frame, text=resume, font=("Arial", 10, "italic"), anchor="w").pack(fill="x", pady=(0, 5))
    tk.Button(fenetre, text="Retour", command=afficher_accueil, bg="gray", fg="white").pack(pady=10)

# Lancement de l'application
afficher_accueil()
fenetre.mainloop()
conn.close()