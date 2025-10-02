import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Connexion à la base SQLite
conn = sqlite3.connect('absences.db')
cursor = conn.cursor()

# Création de la table si non existante
cursor.execute('''
CREATE TABLE IF NOT EXISTS absences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    heure TEXT,
    filiere TEXT,
    cours TEXT,
    etudiant TEXT,
    statut TEXT,
    duree TEXT,
    justification TEXT
)
''')
conn.commit()

HEURE_COURS = datetime.strptime("08:00", "%H:%M")

# Étudiants par filière
etudiants_par_filiere = {
    "CS27": [
        "BADO Yannick", "BADOLO Patricia", "BALIMA Hectore", "BAMOUNI Grace", "BASSINGA Jessica",
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
        "ZOUNGRANA Brenger", "ZOUNGRANA Zalissa", "ZOUNGRANA Eulalie", "ZOUNGRANA Sébastien"
    ],
}

statut_vars = {}
minuteurs_retard = {}
minuteurs_absent = {}

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

        cb_abs = tk.Checkbutton(frame, text="Absent", variable=var_abs, bg="#f0f8ff",
                                command=lambda n=nom: toggle_minuteur_absent(n))
        cb_abs.pack(side="left")

        cb_retard = tk.Checkbutton(frame, text="Retard", variable=var_retard, bg="#f0f8ff",
                                   command=lambda n=nom: toggle_minuteur_retard(n))
        cb_retard.pack(side="left")

        label_timer = tk.Label(frame, text="", width=20, bg="#f0f8ff")
        label_timer.pack(side="left", padx=5)

        btn_stop = tk.Button(frame, text="Arrêter", state="disabled", bg="lightgray")
        btn_stop.pack(side="left")

        # Fonction pour lancer le minuteur de retard
        def lancer_minuteur_retard(nom=nom, label=label_timer, bouton=btn_stop):
            def update():
                if bouton["state"] == "normal":
                    maintenant = datetime.now()
                    delta = maintenant - HEURE_COURS
                    minutes = delta.seconds // 60
                    secondes = delta.seconds % 60
                    label.config(text=f"{minutes} min {secondes} s")
                    label.after(1000, update)

            bouton.config(state="normal", command=lambda: arreter_minuteur_retard(nom, label, bouton))
            update()

        # Fonction d'arrêt du minuteur de retard
        def arreter_minuteur_retard(nom, label, bouton):
            maintenant = datetime.now()
            delta = maintenant - HEURE_COURS
            minutes = delta.seconds // 60
            secondes = delta.seconds % 60
            texte = f"{minutes} min {secondes} s"
            label.config(text=texte)
            bouton.config(state="disabled")
            minuteurs_retard[nom] = texte

        # Démarrage ou arrêt automatique minuteur retard quand on coche/décoche la case
        def checkbox_retard_changed(*args, nom=nom):
            if statut_vars[nom][1].get():
                lancer_minuteur_retard()
            else:
                btn_stop.config(state="disabled")
                label_timer.config(text="")
                if nom in minuteurs_retard:
                    del minuteurs_retard[nom]

        var_retard.trace_add("write", checkbox_retard_changed)

        # Fonction pour lancer minuteur absent (fenêtre popup)
        def ouvrir_minuteur_absent(nom):
            fen_minuteur = tk.Toplevel(root)
            fen_minuteur.title(f"Minuteur Absence - {nom}")
            fen_minuteur.geometry("300x100")

            label = tk.Label(fen_minuteur, text="00:00", font=("Helvetica", 24))
            label.pack(pady=10)

            def arreter_minuteur():
                maintenant = datetime.now()
                retard = maintenant - HEURE_COURS
                minutes = retard.seconds // 60
                secondes = retard.seconds % 60
                texte = f"{minutes} min {secondes} s"
                label.config(text=texte)
                btn_arreter.config(state="disabled")
                minuteurs_absent[nom] = texte

            btn_arreter = tk.Button(fen_minuteur, text="Arrêter", command=arreter_minuteur)
            btn_arreter.pack()

            def update():
                if btn_arreter["state"] == "normal":
                    maintenant = datetime.now()
                    retard = maintenant - HEURE_COURS
                    minutes = retard.seconds // 60
                    secondes = retard.seconds % 60
                    label.config(text=f"{minutes} min {secondes} s")
                    label.after(1000, update)

            update()

        # Lancement ou arrêt minuteur absent quand on coche/décoche la case
        def toggle_minuteur_absent(nom):
            if statut_vars[nom][0].get() == 1:
                ouvrir_minuteur_absent(nom)
            else:
                if nom in minuteurs_absent:
                    del minuteurs_absent[nom]

        # Lancement ou arrêt minuteur retard quand on coche/décoche la case
        def toggle_minuteur_retard(nom):
            if statut_vars[nom][1].get() == 1:
                lancer_minuteur_retard()
            else:
                btn_stop.config(state="disabled")
                label_timer.config(text="")
                if nom in minuteurs_retard:
                    del minuteurs_retard[nom]

# Fonction pour enregistrer les absences/retards dans la base
def enregistrer_donnees():
    date = datetime.now().strftime("%Y-%m-%d")
    heure = datetime.now().strftime("%H:%M:%S")
    filiere = var_filiere.get()
    cours = var_cours.get()

    for nom, (var_abs, var_retard) in statut_vars.items():
        if var_abs.get() == 1 or var_retard.get() == 1:
            statut = ""
            if var_abs.get() == 1:
                statut = "Absent"
            elif var_retard.get() == 1:
                statut = "Retard"
            duree = minuteurs_absent.get(nom) if statut == "Absent" else minuteurs_retard.get(nom, "")
            cursor.execute('''
                INSERT INTO absences (date, heure, filiere, cours, etudiant, statut, duree, justification)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (date, heure, filiere, cours, nom, statut, duree, ""))
    conn.commit()
    messagebox.showinfo("Succès", "Données enregistrées avec succès.")

# Interface justification protégée par mot de passe (fonction complète)
def ouvrir_interface_justification():
    def verifier_mot_de_passe():
        mdp = entree_mdp.get()
        if mdp == "admin":  # Mot de passe dur, à modifier selon besoin
            fen_justif.destroy()
            ouvrir_fenetre_justification()
        else:
            messagebox.showerror("Erreur", "Mot de passe incorrect")

    fen_justif = tk.Toplevel(root)
    fen_justif.title("Connexion Justification")
    fen_justif.geometry("300x100")
    tk.Label(fen_justif, text="Mot de passe:").pack(pady=5)
    entree_mdp = tk.Entry(fen_justif, show="*")
    entree_mdp.pack(pady=5)
    tk.Button(fen_justif, text="Valider", command=verifier_mot_de_passe).pack(pady=5)

def ouvrir_fenetre_justification():
    fen_justif = tk.Toplevel(root)
    fen_justif.title("Justification Absences/Retards")
    fen_justif.geometry("600x400")

    canvas = tk.Canvas(fen_justif)
    scrollbar = tk.Scrollbar(fen_justif, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    cursor.execute('SELECT id, etudiant, statut, justification FROM absences')
    rows = cursor.fetchall()

    champs_justif = {}

    for idx, (id_, etu, statut, justif) in enumerate(rows):
        tk.Label(scrollable_frame, text=f"{etu} ({statut})", anchor="w", width=40).grid(row=idx, column=0, sticky="w", pady=2, padx=2)
        txt = tk.Text(scrollable_frame, height=2, width=40)
        txt.grid(row=idx, column=1, pady=2, padx=2)
        if justif:
            txt.insert("1.0", justif)
        champs_justif[id_] = txt

    def sauvegarder_justifications():
        for id_, txt in champs_justif.items():
            contenu = txt.get("1.0", "end").strip()
            cursor.execute('UPDATE absences SET justification=? WHERE id=?', (contenu, id_))
        conn.commit()
        messagebox.showinfo("Succès", "Justifications sauvegardées.")

    btn_save = tk.Button(fen_justif, text="Sauvegarder", command=sauvegarder_justifications)
    btn_save.pack(pady=10)

# Création fenêtre principale
root = tk.Tk()
root.title("Gestion des absences et retards")
root.geometry("800x600")

frame_haut = tk.Frame(root)
frame_haut.pack(fill="x", padx=10, pady=10)

tk.Label(frame_haut, text="Filière:").pack(side="left")
var_filiere = tk.StringVar(value="CS27")
filieres = list(etudiants_par_filiere.keys())
menu_filiere = tk.OptionMenu(frame_haut, var_filiere, *filieres, command=lambda _: afficher_etudiants())
menu_filiere.pack(side="left", padx=5)

tk.Label(frame_haut, text="Cours:").pack(side="left", padx=10)
var_cours = tk.StringVar(value="")
entree_cours = tk.Entry(frame_haut, textvariable=var_cours)
entree_cours.pack(side="left", padx=5)

btn_justification = tk.Button(frame_haut, text="Justification", command=ouvrir_interface_justification)
btn_justification.pack(side="right")

frame_etudiants = tk.Frame(root)
frame_etudiants.pack(fill="both", expand=True, padx=10, pady=10)

# Ajout scrollbar verticale
canvas = tk.Canvas(frame_etudiants)
scrollbar = tk.Scrollbar(frame_etudiants, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

frame_etudiants = scrollable_frame  # redéfinir le frame pour afficher dedans

# Bouton enregistrer
btn_enregistrer = tk.Button(root, text="Enregistrer", command=enregistrer_donnees)
btn_enregistrer.pack(pady=10)

afficher_etudiants()

root.mainloop()