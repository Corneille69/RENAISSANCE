import datetime
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# --- Constantes ---
DATA_FILE = "presences_par_filiere.json"

# --- Palette de couleurs ---
COLORS = {
    'primary': '#2C3E50',
    'secondary': '#3498DB',
    'success': '#2ECC71',
    'danger': '#E74C3C',
    'warning': '#F39C12',
    'background': '#ECF0F1',
    'card': '#FFFFFF',
    'text': '#2C3E50',
    'accent': '#34495E'
}

# --- Fonctions utilitaires ---
def charger_donnees():
    """Charge les données depuis un fichier JSON."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            messagebox.showwarning("Erreur", "Fichier corrompu. Création d'un nouveau.")
            return {}
    return {}

def sauvegarder_donnees(data):
    """Sauvegarde les données dans un fichier JSON."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        messagebox.showerror("Erreur", f"Impossible de sauvegarder : {e}")

def generer_liste_presence(etudiants, jours_cours, semaine_debut, semaine_fin):
    """Génère une liste de présence par défaut ('A') pour une période donnée."""
    liste_presences = {etudiant['nom']: {} for etudiant in etudiants}
    try:
        start_date = datetime.datetime.strptime(semaine_debut, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(semaine_fin, '%Y-%m-%d').date()
    except ValueError:
        messagebox.showerror("Erreur", "Format date incorrect. Utilisez AAAA-MM-JJ.")
        return {}
    if start_date > end_date:
        messagebox.showwarning("Dates invalides", "La date de début est après la fin.")
        return {}

    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() in jours_cours:
            date_str = current_date.strftime('%Y-%m-%d')
            for etudiant in liste_presences:
                liste_presences[etudiant][date_str] = 'A'
        current_date += datetime.timedelta(days=1)
    return liste_presences

# --- Application Tkinter stylée ---
class GestionPresenceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Présences Étudiantes")
        self.root.geometry("1400x900")
        self.root.configure(bg=COLORS['background'])

        self.setup_styles()
        self.all_data = charger_donnees()
        if not self.all_data:
            self.all_data = {
                "Filière par défaut": {
                    "etudiants": [],
                    "jours_cours": [0, 1, 2, 3, 4],
                    "presences": {}
                }
            }
            sauvegarder_donnees(self.all_data)

        # Variables
        self.current_filiere = tk.StringVar(root)
        if list(self.all_data.keys()):
            self.current_filiere.set(list(self.all_data.keys())[0])
        else:
            self.current_filiere.set("Aucune filière")
        self.checkbox_vars = {}
        self.all_dates_in_display = []

        # Créer l'interface
        self.create_widgets()
        self.load_filiere_data()

    def setup_styles(self):
        """Configure les styles personnalisés pour les widgets."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=COLORS['background'])
        style.configure("TLabel", foreground=COLORS['text'], background=COLORS['background'])
        style.configure("TButton", padding=6, relief="flat", background=COLORS['secondary'], font=('Helvetica', 9))
        style.map("TButton", background=[('active', COLORS['accent'])])
        style.configure("Custom.TLabelframe", borderwidth=2, relief='groove',
                      font=('Helvetica', 10, 'bold'), foreground=COLORS['primary'], background=COLORS['background'])
        style.configure("Custom.TLabelframe.Label", foreground=COLORS['primary'], background=COLORS['background'])
        style.configure("Custom.Treeview", background=COLORS['card'], foreground=COLORS['text'],
                      rowheight=25, fieldbackground=COLORS['background'])
        style.map("Custom.Treeview.Heading",
                  foreground=[('active', COLORS['primary'])],
                  background=[('active', COLORS['secondary'])])
        style.configure("Custom.Treeview.Heading", font=('Helvetica', 10, 'bold'))

    def create_widgets(self):
        """Crée tous les widgets de l'interface."""
        main_container = ttk.Frame(self.root, style="TFrame")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Panneau gauche - Filières et Étudiants
        left_panel = ttk.Frame(main_container, style="TFrame", width=350)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        filiere_frame = ttk.LabelFrame(left_panel, text="Filières", style="Custom.TLabelframe")
        filiere_frame.pack(pady=10, fill="x")
        ttk.Label(filiere_frame, text="Sélectionner filière:", style="TLabel").pack(padx=5, pady=2, anchor="w")
        self.filiere_selector = ttk.Combobox(filiere_frame, textvariable=self.current_filiere,
                                            values=list(self.all_data.keys()), state="readonly")
        self.filiere_selector.pack(padx=5, pady=2, fill="x")
        self.filiere_selector.bind("<<ComboboxSelected>>", self.on_filiere_selected)
        ttk.Button(filiere_frame, text="➕ Ajouter filière", command=self.add_filiere).pack(pady=5, padx=5, fill="x")

        etudiant_frame = ttk.LabelFrame(left_panel, text="Étudiants", style="Custom.TLabelframe")
        etudiant_frame.pack(pady=10, fill="both", expand=True)
        self.etudiant_tree = ttk.Treeview(etudiant_frame, columns=("Nom"), show="headings", height=20)
        self.etudiant_tree.heading("Nom", text="Nom de l'étudiant")
        self.etudiant_tree.column("Nom", width=280, anchor="w")
        self.etudiant_tree.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        etudiant_scrollbar = ttk.Scrollbar(etudiant_frame, orient="vertical", command=self.etudiant_tree.yview)
        etudiant_scrollbar.pack(side="right", fill="y")
        self.etudiant_tree.configure(yscrollcommand=etudiant_scrollbar.set)

        btn_frame = ttk.Frame(etudiant_frame, style="TFrame")
        btn_frame.pack(pady=5, fill="x")
        ttk.Button(btn_frame, text="➕ Ajouter", command=self.add_student).pack(side="left", expand=True, padx=2)
        ttk.Button(btn_frame, text="✏️ Modifier", command=self.edit_student).pack(side="left", expand=True, padx=2)
        ttk.Button(btn_frame, text="🗑️ Supprimer", command=self.delete_student).pack(side="left", expand=True, padx=2)

        # Panneau droit - Paramètres et Présences
        right_panel = ttk.Frame(main_container, style="TFrame")
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))

        settings_frame = ttk.LabelFrame(right_panel, text="Paramètres", style="Custom.TLabelframe")
        settings_frame.pack(pady=10, fill="x")

        jours_frame = ttk.Frame(settings_frame, style="TFrame")
        jours_frame.pack(pady=5, fill="x")
        ttk.Label(jours_frame, text="Jours de cours (L=0 ... D=6):").pack(side="left", padx=5)
        self.jours_vars = []
        jours_labels = ["L", "M", "Me", "J", "V", "S", "D"]
        for i, jour_label in enumerate(jours_labels):
            var = tk.IntVar()
            cb = ttk.Checkbutton(jours_frame, text=jour_label, variable=var)
            cb.pack(side="left", padx=2)
            self.jours_vars.append(var)
        ttk.Button(jours_frame, text="✅ Appliquer", command=self.appliquer_jours_cours).pack(side="left", padx=5)

        date_frame = ttk.Frame(settings_frame, style="TFrame")
        date_frame.pack(pady=5, fill="x")
        ttk.Label(date_frame, text="Date début (AAAA-MM-JJ):").pack(side="left", padx=5)
        self.start_date_entry = ttk.Entry(date_frame, width=12)
        self.start_date_entry.pack(side="left", padx=5)
        self.start_date_entry.insert(0, datetime.date.today().strftime('%Y-%m-%d'))
        ttk.Label(date_frame, text="Date fin:").pack(side="left", padx=5)
        self.end_date_entry = ttk.Entry(date_frame, width=12)
        self.end_date_entry.pack(side="left", padx=5)
        self.end_date_entry.insert(0, (datetime.date.today() + datetime.timedelta(days=13)).strftime('%Y-%m-%d'))
        ttk.Label(date_frame, text="Date manuelle:").pack(side="left", padx=5)
        self.manual_date_entry = ttk.Entry(date_frame, width=12)
        self.manual_date_entry.pack(side="left", padx=5)
        self.manual_date_entry.insert(0, (datetime.date.today() + datetime.timedelta(days=14)).strftime('%Y-%m-%d'))
        ttk.Button(date_frame, text="🔄 Générer/Réinitialiser", command=self.generer_et_afficher_liste).pack(side="left", padx=10)

        presence_frame = ttk.LabelFrame(right_panel, text="Liste des Présences", style="Custom.TLabelframe")
        presence_frame.pack(pady=10, fill="both", expand=True)

        btn_actions = ttk.Frame(presence_frame, style="TFrame")
        btn_actions.pack(pady=5, fill="x")
        ttk.Button(btn_actions, text="✅ Tout Présent", command=lambda: self.mark_all_status('P')).pack(
            side="left", expand=True, padx=2)
        ttk.Button(btn_actions, text="❌ Tout Absent", command=lambda: self.mark_all_status('A')).pack(
            side="left", expand=True, padx=2)
        ttk.Button(btn_actions, text="🔁 Réinitialiser", command=self.reset_all_to_absent).pack(
            side="left", expand=True, padx=2)
        ttk.Button(btn_actions, text="➕ Présent (date)", command=lambda: self.add_status_for_manual_date('P')).pack(
            side="left", expand=True, padx=2)
        ttk.Button(btn_actions, text="➖ Absent (date)", command=lambda: self.add_status_for_manual_date('A')).pack(
            side="left", expand=True, padx=2)

        self.presence_tree = ttk.Treeview(presence_frame, show="headings", style="Custom.Treeview")
        self.presence_tree.pack(side="left", fill="both", expand=True)
        yscroll = ttk.Scrollbar(presence_frame, orient="vertical", command=self.presence_tree.yview)
        yscroll.pack(side="right", fill="y")
        xscroll = ttk.Scrollbar(presence_frame, orient="horizontal", command=self.presence_tree.xview)
        xscroll.pack(side="bottom", fill="x")
        self.presence_tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        self.presence_tree.tag_configure('present', background='#D4F5D0')
        self.presence_tree.tag_configure('absent', background='#F5D0D0')

        ttk.Button(self.root, text="💾 Sauvegarder", command=self.save_all_data).pack(pady=10)

    def on_filiere_selected(self, event=None):
        self.load_filiere_data()

    def load_filiere_data(self):
        filiere_name = self.current_filiere.get()
        if filiere_name not in self.all_data:
            self.all_data[filiere_name] = {"etudiants": [], "jours_cours": [], "presences": {}}
        jours_cours_filiere = self.all_data[filiere_name].get("jours_cours", [])
        for i, var in enumerate(self.jours_vars):
            var.set(1 if i in jours_cours_filiere else 0)
        self.display_students()
        self.generer_et_afficher_liste()

    def display_students(self):
        for item in self.etudiant_tree.get_children():
            self.etudiant_tree.delete(item)
        filiere_name = self.current_filiere.get()
        etudiants = self.all_data[filiere_name].get("etudiants", [])
        for etudiant in etudiants:
            self.etudiant_tree.insert("", "end", values=(etudiant['nom'],))

    def add_filiere(self):
        new_filiere = simpledialog.askstring("Nouvelle Filière", "Nom de la filière:", parent=self.root)
        if new_filiere:
            new_filiere = new_filiere.strip()
            if new_filiere in self.all_data:
                messagebox.showwarning("Existe", f"Filière '{new_filiere}' existe déjà.")
                return
            self.all_data[new_filiere] = {"etudiants": [], "jours_cours": [0, 1, 2, 3, 4], "presences": {}}
            self.filiere_selector["values"] = list(self.all_data.keys())
            self.current_filiere.set(new_filiere)
            self.load_filiere_data()
            sauvegarder_donnees(self.all_data)

    def add_student(self):
        filiere_name = self.current_filiere.get()
        if filiere_name == "Aucune filière":
            messagebox.showwarning("Action impossible", "Créez une filière d'abord.")
            return
        name = simpledialog.askstring("Nouvel Étudiant", f"Nom pour {filiere_name}:", parent=self.root)
        if name:
            name = name.strip()
            students = self.all_data[filiere_name]["etudiants"]
            if any(s['nom'] == name for s in students):
                messagebox.showwarning("Existant", f"{name} existe déjà dans cette filière.")
                return
            students.append({'nom': name})
            self.display_students()
            self.generer_et_afficher_liste()

    def edit_student(self):
        selected = self.etudiant_tree.selection()
        if not selected:
            messagebox.showwarning("Aucun sélectionné", "Sélectionnez un étudiant.")
            return
        old_name = self.etudiant_tree.item(selected, 'values')[0]
        new_name = simpledialog.askstring("Modifier", f"Nouveau nom pour {old_name}:", initialvalue=old_name, parent=self.root)
        if new_name and new_name.strip() != old_name:
            new_name = new_name.strip()
            filiere_name = self.current_filiere.get()
            students = self.all_data[filiere_name]["etudiants"]
            presences = self.all_data[filiere_name]["presences"]
            for s in students:
                if s['nom'] == old_name:
                    s['nom'] = new_name
                    break
            if old_name in presences:
                presences[new_name] = presences.pop(old_name)
            self.display_students()
            self.generer_et_afficher_liste()
            messagebox.showinfo("Modifié", f"{old_name} → {new_name}")

    def delete_student(self):
        selected = self.etudiant_tree.selection()
        if not selected:
            messagebox.showwarning("Aucun sélectionné", "Sélectionnez un étudiant.")
            return
        student_name = self.etudiant_tree.item(selected, 'values')[0]
        if messagebox.askyesno("Confirmer", f"Supprimer {student_name} ?", parent=self.root):
            filiere_name = self.current_filiere.get()
            self.all_data[filiere_name]["etudiants"] = [
                s for s in self.all_data[filiere_name]["etudiants"] if s['nom'] != student_name
            ]
            presences = self.all_data[filiere_name]["presences"]
            if student_name in presences:
                del presences[student_name]
            self.display_students()
            self.generer_et_afficher_liste()
            messagebox.showinfo("Supprimé", f"{student_name} supprimé.")

    def appliquer_jours_cours(self):
        filiere_name = self.current_filiere.get()
        selected_jours = [i for i, var in enumerate(self.jours_vars) if var.get()]
        self.all_data[filiere_name]["jours_cours"] = selected_jours
        self.generer_et_afficher_liste()

    def generer_et_afficher_liste(self):
        filiere_name = self.current_filiere.get()
        filiere_data = self.all_data[filiere_name]
        etudiants = filiere_data.get("etudiants", [])
        jours_cours = filiere_data.get("jours_cours", [])
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        
        if not start_date:
            self.start_date_entry.delete(0, tk.END)
            self.start_date_entry.insert(0, datetime.date.today().strftime('%Y-%m-%d'))
            start_date = self.start_date_entry.get()
        if not end_date:
            self.end_date_entry.delete(0, tk.END)
            self.end_date_entry.insert(0, (datetime.date.today() + datetime.timedelta(days=13)).strftime('%Y-%m-%d'))
            end_date = self.end_date_entry.get()

        if not etudiants or not jours_cours:
            self.clear_presence_treeview()
            return

        nouvelles_presences = generer_liste_presence(etudiants, jours_cours, start_date, end_date)
        presences_actuelles = filiere_data.get("presences", {})
        merged = {}
        for etudiant in etudiants:
            nom = etudiant['nom']
            merged[nom] = {}
            for date_str, statut in nouvelles_presences.get(nom, {}).items():
                merged[nom][date_str] = presences_actuelles.get(nom, {}).get(date_str, statut)
        filiere_data["presences"] = merged
        self.display_presences()

    def display_presences(self):
        filiere_name = self.current_filiere.get()
        presences = self.all_data[filiere_name].get("presences", {})
        etudiants_noms = [s['nom'] for s in self.all_data[filiere_name].get("etudiants", [])]

        for item in self.presence_tree.get_children():
            self.presence_tree.delete(item)

        if not presences or not etudiants_noms:
            self.presence_tree.heading("#0", text="Pas de données. Générez la liste.")
            return

        all_dates = sorted(set(date for p in presences.values() for date in p.keys()))
        self.all_dates_in_display = all_dates
        self.presence_tree["columns"] = ["Étudiant"] + all_dates
        self.presence_tree.heading("Étudiant", text="Étudiant")
        for date in all_dates:
            self.presence_tree.heading(date, text=date)
            self.presence_tree.column(date, width=60, anchor="center")

        self.checkbox_vars = {}
        for etudiant in etudiants_noms:
            values = [etudiant]
            for date_str in all_dates:
                statut = presences[etudiant].get(date_str, 'A')
                values.append(statut)
            item_id = self.presence_tree.insert("", "end", values=values)
            self.checkbox_vars[etudiant] = {}
            for i, date in enumerate(all_dates):
                statut = presences[etudiant].get(date, 'A')
                var = tk.StringVar(value=statut)
                self.checkbox_vars[etudiant][date] = var
                cb = ttk.Checkbutton(
                    self.presence_tree, text="", variable=var,
                    onvalue="P", offvalue="A",
                    command=lambda e=etudiant, d=date, v=var: self.update_presence(e, d, v)
                )
                self.presence_tree.set(item_id, column=i+1, value="")
                self.presence_tree.window_create(item_id, column=i+1, row=item_id, window=cb)

    def clear_presence_treeview(self):
        for item in self.presence_tree.get_children():
            self.presence_tree.delete(item)

    def update_presence(self, nom, date, var):
        filiere_name = self.current_filiere.get()
        presences = self.all_data[filiere_name]["presences"]
        if nom not in presences:
            presences[nom] = {}
        presences[nom][date] = var.get()

    def mark_all_status(self, status):
        filiere_name = self.current_filiere.get()
        presences = self.all_data[filiere_name]["presences"]
        etudiants_noms = [s['nom'] for s in self.all_data[filiere_name].get("etudiants", [])]
        all_dates = self.all_dates_in_display
        for etudiant in etudiants_noms:
            if etudiant not in presences:
                presences[etudiant] = {}
            for date in all_dates:
                presences[etudiant][date] = status
        self.display_presences()

    def reset_all_to_absent(self):
        filiere_name = self.current_filiere.get()
        presences = self.all_data[filiere_name]["presences"]
        etudiants_noms = [s['nom'] for s in self.all_data[filiere_name].get("etudiants", [])]
        all_dates = self.all_dates_in_display

        if not all_dates:
            messagebox.showinfo("Pas de dates", "Aucune date affichée. Générez d'abord la liste.")
            return

        if messagebox.askyesno("Réinitialiser", "Voulez-vous vraiment réinitialiser toutes les présences à 'Absent' ?"):
            for etudiant in etudiants_noms:
                if etudiant not in presences:
                    presences[etudiant] = {}
                for date in all_dates:
                    presences[etudiant][date] = 'A'
            self.display_presences()
            messagebox.showinfo("Réinitialisé", "Toutes les présences ont été remises à 'Absent'.")

    def add_status_for_manual_date(self, status):
        filiere_name = self.current_filiere.get()
        presences = self.all_data[filiere_name]["presences"]
        etudiants_noms = [s['nom'] for s in self.all_data[filiere_name].get("etudiants", [])]
        manual_date_str = self.manual_date_entry.get()

        try:
            manual_date = datetime.datetime.strptime(manual_date_str, "%Y-%m-%d").date()
            manual_date_str = manual_date.strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide. Utilisez AAAA-MM-JJ.")
            return

        for etudiant in etudiants_noms:
            if etudiant not in presences:
                presences[etudiant] = {}
            presences[etudiant][manual_date_str] = status

        self.display_presences()
        messagebox.showinfo("Statut mis à jour", f"Tous les étudiants marqués comme {'Présent' if status == 'P' else 'Absent'} pour le {manual_date_str}.")

    def save_all_data(self):
        sauvegarder_donnees(self.all_data)
        messagebox.showinfo("Sauvegardé", "Données sauvegardées.")

# --- Lancement de l'application ---
if __name__ == "__main__":
    root = tk.Tk()
    root.tk_setPalette(background=COLORS['background'])
    app = GestionPresenceApp(root)
    root.mainloop()