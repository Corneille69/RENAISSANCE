import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import csv
afficher_recapitulatif(donnees_enregistrees)
FICHIER = "absences.csv"

# Étudiants par filière (à modifier selon tes besoins)
etudiants_par_filiere = {
    "CS27": ["BADO Yannick", "BADOLO Patricia", "BALIMA Hectore","BAMOUNI Grace","BASSINGA Jessica","BATIONO Betranel","BIRBA Wendabo Casimir" ,
             "BONKOUNGOU Jerome","BOUNKOUGOU Wendyam Vanessa","BOUDA Mouniratou", "BOUGMA Sadiata","COMPAORE Adim Fahim Saidou","COMPAORE Kisito",
             "COMPAORE Salimata","CONGO Anifatou","COULIBALY Faez","DAH Cheoutierou","DAKUYO Prisca", "DAYAMBA Abigael","DEHOUMOU Christelle","DEMBELE Gaethan Khaleb",
             "DIALLO Maimata", "DORI Marie Madeleine", "DOUAMBASidonie","DRABO Farel","GADIERE Farida","GARANE Farida Kevine","ILBOUDO Balkissa","ILBOUDO John Michee","KABORE Albertine",
             "KABORE Karelle 2e jumelle", "KABORE Odiane Elia","KABORE Grace Oceanne","KABORE Awa","KABORE Bienvenu","KAFANDO Dan","KAGAMBEGA Saturne","KAGAMBEGA Claudine","KAMBOU Yeri Hermine",
             "KANTAGBA Efraim","KANTIONO Diane", "KERE Noeldinolippeu","KIEMTORE Simplice","KIENDREBEOGO Carine","KIENDREBEOGO Sephora","KIENDREBEOGO Moussa","KIENDREBEOGO Arnaud","KINI Jacob",
             "KOALGA Heliane", "KOANDA Checkib", "KOLOGO Robert","KONDOMBO Josue","KONOMBO Madeleine","KOUTIEBOU Ornella","KYEMTORE Gloria","MANDI Melki","MEDA Franck", "NACOULMA Betsaleel",
             "NANA Prisca","NANA Marc","NASSA Didier","NIKIEMA Flora Marie Ines","NIKIEMA Marieta","NITIEMA Eddy Martial","NKUNA Israel","NOMBRE Ange","N'ZOMBIE Rodrigue","OUATTARA Fawzia","OUEDRAOGO Corneille",
             "OUEDRAOGO Landry","OUEDRAOGO Akram","OUEDRAOGO Alimata","OUEDRAOGO Adele","OUEDRAOGO Jonathan","OUEDRAOGO Esther","OUEDRAOGO Abdoulaye","OUILY Nasser","PARE Joseph","PARE Boris Marcel ","PARE Assetou ", "ROUAMBA Mounira","ROUAMBA Sarifatou" "SANFO Madi","SANON Abdoul Ben Fatao",
             "SAWADOGO Grace", "SAWADOGO Elisabeth", "SAWADOGO Azael","SAWADOGO Asseta","SAWADOGO Risnata","SEMDE Aicha","SIMPORE Alima","SIMPORE Sidiki","SOULAMA Ulrich","TANKOANO Michel",
             "TAO Fazollah","TOE Kevin","TOUBRIWOUMYIAN Yan Ulrich","TOUGOUMA Trevis","TRAORE Ramatou","TRAORE Mathias*","TRAORE ESmelle",
             "WANGRE Esther","ZABRE Elvine","YABRE Amma","YAMEOGO Aymar","YAMEOGO Cedric", "YAMEOGO Athanasse","YAMEOGO Angeline","YAMEOGO Firmin","YAMEOGO Marie Joseph","YAMEOGO Claudine",
             "YANOGO Stephanie","YELEMOU Martial ","YOUGBARE Eunice","ZABRE Tania",
             "ZAMANE Elodie","ZARANI Abdoul Kader","ZINGUE Cynthia"," ZOMA Amelie ","ZONGO P.Juste","ZONGO Pascal","ZONGO Ange Anselme","ZONGO Alida Isidore","ZONGO Malkiram","ZONGO Safiatou",
             "ZONGO Abdel Sadek","ZOUGOURI Aurel Clauvis ","ZOUNGRANA Brenger","ZOUNGRANA Zalissa","ZOUNGRANA Eulalie","ZOUNGRANA Sébastien"],
    
}

def initialiser_fichier():
    try:
        with open(FICHIER, 'x', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Heure", "Filière", "Cours","Enseignant" "Étudiant", "Statut"])
    except FileExistsError:
        pass

def afficher_etudiants():
    # Supprimer anciens widgets
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

        label = tk.Label(frame, text=nom, width=25, anchor="w", bg="#f0f8ff")
        label.pack(side="left")

        var_abs = tk.IntVar()
        var_retard = tk.IntVar()
        statut_vars[nom] = (var_abs, var_retard)

        tk.Checkbutton(frame, text="Absent", variable=var_abs, bg="#f0f8ff").pack(side="left")
        tk.Checkbutton(frame, text="Retard", variable=var_retard, bg="#f0f8ff").pack(side="left")

def enregistrer():
    cours = entree_cours.get()
    filiere = var_filiere.get()
    now = datetime.now()
    date_str = now.date()
    heure_str = now.strftime("%H:%M")

    if filiere == "" or cours == "":
        messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")
        return

    donnees_enregistrees = []

    with open(FICHIER, 'a', newline='') as f:
        writer = csv.writer(f)
        for nom, (absent, retard) in statut_vars.items():
            if absent.get():
                statut = "Absent"
            elif retard.get():
                statut = "Retard"
            else:
                statut = "Présent"

            ligne = [date_str, heure_str, filiere, cours, nom, statut]
            writer.writerow(ligne)
            donnees_enregistrees.append(ligne)

    afficher_recapitulatif(donnees_enregistrees)

    def afficher_recapitulatif(donnees):
    fenetre_recap = tk.Toplevel(fenetre)
    fenetre_recap.title("Récapitulatif de la présence")
    fenetre_recap.geometry("650x400")
    fenetre_recap.config(bg="#f9f9f9")

    titre = tk.Label(fenetre_recap, text="Liste de la classe - Récapitulatif", font=("Arial", 14, "bold"), bg="#f9f9f9")
    titre.pack(pady=10)

    texte = tk.Text(fenetre_recap, width=80, height=20, bg="#fff8f0", fg="#000", font=("Arial", 10))
    texte.pack(padx=10, pady=10)

    texte.insert(tk.END, f"{'Date':<12}{'Heure':<8}{'Filière':<15}{'Cours':<15}{'Étudiant':<25}{'Statut'}\n")
    texte.insert(tk.END, "-" * 80 + "\n")

    for ligne in donnees:
        date, heure, filiere, cours, nom, statut = ligne
        texte.insert(tk.END, f"{date:<12}{heure:<8}{filiere:<15}{cours:<15}{nom:<25}{statut}\n")

    texte.config(state="disabled")

# Interface
fenetre = tk.Tk()
fenetre.title("Suivi des absences")
fenetre.geometry("600x600")
fenetre.config(bg="#e6f2ff")

# Titre
tk.Label(fenetre, text="Gestion des Absences par Filière", font=("Arial", 16, "bold"), bg="#e6f2ff", fg="#003366").pack(pady=10)

# Sélection filière
tk.Label(fenetre, text="Filière :", bg="#e6f2ff").pack()
var_filiere = tk.StringVar()
menu_filiere = tk.OptionMenu(fenetre, var_filiere, *etudiants_par_filiere.keys())
menu_filiere.pack()
var_filiere.set("CS27")
tk.Button(fenetre, text="Afficher la liste", command=afficher_etudiants, bg="#0066cc", fg="white", padx=10, pady=5).pack(pady=5)

# Cours
tk.Label(fenetre, text="Cours :", bg="#e6f2ff").pack()
entree_cours = tk.Entry(fenetre)
entree_cours.pack(pady=5)


# Liste des étudiants
frame_etudiants = tk.Frame(fenetre, bg="#f0f8ff", bd=2, relief="groove")
frame_etudiants.pack(fill="both", expand=True, padx=10, pady=30)

# Bouton d'enregistrement
tk.Button(fenetre, text="Enregistrer", command=enregistrer, bg="#28a745", fg="white", padx=20, pady=10).pack(pady=10)

statut_vars = {}
initialiser_fichier()
afficher_etudiants()  # affichage initial
fenetre.mainloop()