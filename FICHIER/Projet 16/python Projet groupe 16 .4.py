import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import csv

FICHIER = "absences.csv"

HEURE_COURS = datetime.strptime("08:00", "%H:%M")

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
boutons_retard = {}

def initialiser_fichier():
    try:
        with open(FICHIER, 'x', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Heure", "Filière", "Cours", "Étudiant", "Statut", "Durée Retard"])
    except FileExistsError:
        pass

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
    if filiere == "" or cours == "":
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
    now = datetime.now()
    date_str = now.date()
    heure_str = now.strftime("%H:%M")

    donnees_enregistrees = []

    with open(FICHIER, 'a', newline='') as f:
        writer = csv.writer(f)
        for nom, (absent, retard) in statut_vars.items():
            statut = "Présent"
            duree_retard = ""
            if absent.get():
                statut = "Absent"
            elif retard.get():
                statut = "Retard"
                duree_retard = "?"  # Non mesuré
            ligne = [date_str, heure_str, filiere, cours, nom, statut, duree_retard]
            donnees_enregistrees.append(ligne)
            writer.writerow(ligne)

    afficher_recapitulatif(donnees_enregistrees)

def fenetre_retards(retardataires):
    fen = tk.Toplevel(fenetre)
    fen.title("Minuteurs de Retard")
    fen.geometry("500x400")
    tk.Label(fen, text="Minuteurs des retardataires", font=("Arial", 14, "bold")).pack(pady=10)

    # Réinitialiser les boutons-retards pour cette session
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
        now = datetime.now()
        date_str = now.date()
        heure_str = now.strftime("%H:%M")

        lignes = []
        with open(FICHIER, 'a', newline='') as f:
            writer = csv.writer(f)
            for nom, (absent, retard) in statut_vars.items():
                statut = "Présent"
                duree_retard = ""
                if absent.get():
                    statut = "Absent"
                elif retard.get():
                    statut = "Retard"
                    duree_retard = boutons_retard.get(nom, "Non arrêté")
                ligne = [date_str, heure_str, filiere, cours, nom, statut, duree_retard]
                lignes.append(ligne)
                writer.writerow(ligne)

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
    text = tk.Text(recap, width=80, height=25)
    text.pack(padx=10, pady=10)
    text.insert(tk.END, "Date | Heure | Filière | Cours | Étudiant| Statut | Durée Retard\n")
    text.insert(tk.END, "-"*80 + "\n")
    for ligne in lignes:
        text.insert(tk.END, " | ".join(str(item) for item in ligne) + "\n")
    text.config(state=tk.DISABLED)

fenetre = tk.Tk()
fenetre.title("Suivi des absences")
fenetre.geometry("700x700")
fenetre.config(bg="cyan")

tk.Label(fenetre, text="Gestion des Absences", font=("Arial", 16, "bold"), bg="yellowgreen", fg="#003366").pack(pady=10)

tk.Label(fenetre, text="Filière :", bg="bisque").pack()
var_filiere = tk.StringVar()
menu_filiere = tk.OptionMenu(fenetre, var_filiere, *etudiants_par_filiere.keys())
menu_filiere.pack()
var_filiere.set("CS27")

tk.Button(fenetre, text="Afficher la liste", command=afficher_etudiants, bg="orange", fg="white", padx=10, pady=5).pack(pady=5)


tk.Label(fenetre, text="Doctor Name :", bg="yellowgreen").pack()
entree_cours = tk.Entry(fenetre)
entree_cours.pack(pady=5)

tk.Label(fenetre, text="Course :", bg="yellow").pack()
entree_cours = tk.Entry(fenetre)
entree_cours.pack(pady=5)

tk.Label(fenetre, text="Days:", bg="yellowgreen").pack()
entree_cours = tk.Entry(fenetre)
entree_cours.pack(pady=5)

container = tk.Frame(fenetre, bg="black", bd=2, relief="groove")
container.pack(fill="both", expand=True, padx=10, pady=30)

canvas = tk.Canvas(container, bg="olive")

canvas.pack(side="right", fill="both", expand=True)

scrollbar = tk.Scrollbar(container, orient="horizontal", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

frame_etudiants = tk.Frame(canvas, bg="green")
canvas.create_window((0, 0), window=frame_etudiants, anchor="nw")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame_etudiants.bind("<Configure>", on_frame_configure)

tk.Button(fenetre, text="Enregistrer", command=enregistrer, bg="olive", fg="white", padx=20, pady=10).pack(pady=10)

initialiser_fichier()
afficher_etudiants()

fenetre.mainloop()