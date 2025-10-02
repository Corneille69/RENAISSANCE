from tkinter import *
import json

# Fonction pour charger les questions (actuellement définies en dur dans le code)
def charger_questions():
    return [
        {"question": "Quelle est la capitale de la France?", "options": ["Paris", "Londres", "Berlin", "Madrid"], "answer": "Paris"},
        {"question": "Combien font 2 + 2?", "options": ["3", "4", "5", "6"], "answer": "4"},
        {"question": "Quelle est la couleur du ciel?", "options": ["Bleu", "Vert", "Rouge", "Jaune"], "answer": "Bleu"}
    ]

# Fonction pour afficher le menu principal
def show_main_menu():
    # Réafficher les widgets de la première interface
    label.place(x=130, y=10)
    label1.place(x=100, y=80)
    btn1.place(x=145, y=120)
    btn2.place(x=140, y=170)
    btn3.place(x=137, y=220)

# Interface pour le niveau facile
def easy_interface():
    # Masquer les widgets de la première interface
    for widget in fenetre.winfo_children():
        widget.place_forget()
    
    # Afficher la deuxième interface
    second_interface.place(relx=0.5, rely=0.5, anchor="center")
    
    # Afficher la question
    question_label = Label(second_interface, text="Question:", font=("Arial", 14, "bold"), bg='#87CEEB')
    question_label.place(x=20, y=50)
    
    # Charger les questions du niveau facile
    questions = charger_questions()

    # Variable pour stocker la réponse sélectionnée
    reponse = StringVar()

    # Fonction pour vérifier la réponse
    def verifier_reponse():
        selected_option = reponse.get()
        if selected_option == questions[0]['answer']:
            result_label.config(text="Correct!", fg="green")
        else:
            result_label.config(text="Incorrect!", fg="red")

    # Afficher les options de réponse
    y_position = 150
    for option in questions[0]['options']:
        element = Button(second_interface, text=option, command=lambda opt=option: [reponse.set(opt), verifier_reponse()], bg='#87CEEB', font=("Arial", 12))
        element.place(x=100, y=y_position)
        y_position += 30

    # Label pour afficher le résultat
    result_label = Label(second_interface, text="", font=("Arial", 12, "bold"), bg='#87CEEB')
    result_label.place(x=20, y=y_position + 40)

    # Exemple d'affichage de la première question
    if questions:
        first_question = questions[0]['question']
        question_text = Label(second_interface, text=first_question, font=("Arial", 12), bg='#87CEEB')
        question_text.place(x=20, y=100)

# Interface pour le niveau moyen
def medium_interface():
    # Masquer les widgets de la première interface
    for widget in fenetre.winfo_children():
        widget.place_forget()
    
    # Afficher la deuxième interface pour le niveau moyen
    second1_interface.place(relx=0.5, rely=0.5, anchor="center")

# Interface pour le niveau difficile
def difficult_interface():
    # Masquer les widgets de la première interface
    for widget in fenetre.winfo_children():
        widget.place_forget()
    
    # Afficher la deuxième interface pour le niveau difficile
    second2_interface.place(relx=0.5, rely=0.5, anchor="center")

# Configuration de la fenêtre principale
fenetre = Tk()
fenetre.geometry('400x400')
fenetre.title('Black Star')
fenetre['bg'] = '#87CEEB'
fenetre.resizable(height=False, width=False)

# Image de fond pour la fenêtre principale
photo0 = PhotoImage(file='2.png')
label_image0 = Label(fenetre, image=photo0)
label_image0.place(relx=0.5, rely=0.7, anchor="center")

# Interface pour le niveau facile
second_interface = Frame(fenetre, bg='#87CEEB', width=400, height=400)
photo = PhotoImage(file='2.png')
label_image = Label(second_interface, image=photo)
label_image.place(relx=0.5, rely=0.5, anchor="center")
retour_button = Button(second_interface, text="Retour", command=lambda: [second_interface.place_forget(), show_main_menu()], bg="blue", fg="white", font=("Arial", 12, "bold"))
retour_button.place(x=20, y=350)

# Interface pour le niveau moyen
second1_interface = Frame(fenetre, bg='#87CEEB', width=400, height=400)
photo1 = PhotoImage(file='3.png')
label_image1 = Label(second1_interface, image=photo1)
label_image1.place(relx=0.5, rely=0.5, anchor="center")
retour_button = Button(second1_interface, text="Retour", command=lambda: [second1_interface.place_forget(), show_main_menu()], bg="blue", fg="white", font=("Arial", 12, "bold"))
retour_button.place(x=20, y=350)

# Interface pour le niveau difficile
second2_interface = Frame(fenetre, bg='#87CEEB', width=400, height=400)
photo2 = PhotoImage(file='2.png')
label_image2 = Label(second2_interface, image=photo2)
label_image2.place(relx=0.5, rely=0.4, anchor="center")
retour_button = Button(second2_interface, text="Retour", command=lambda: [second2_interface.place_forget(), show_main_menu()], bg="blue", fg="white", font=("Arial", 12, "bold"))
retour_button.place(x=20, y=350)

# Widgets de la première interface
label = Label(fenetre, text='Bienvenue', font=("Arial", 16, "italic bold"), fg='black', bg='#87CEEB')
label.place(x=130, y=10)
label1 = Label(fenetre, text='Choisir un niveau', font=("Arial", 16, "italic bold"), fg='white', bg='blue')
label1.place(x=100, y=80)

# Boutons pour choisir le niveau
btn1 = Button(fenetre, text='Facile', bg="blue", font=('arial', 14, 'italic bold'), fg='white', command=easy_interface)
btn1.place(x=145, y=120)
btn2 = Button(fenetre, text='Moyen', bg="blue", font=('arial', 14, 'italic bold'), fg='white', command=medium_interface)
btn2.place(x=140, y=170)
btn3 = Button(fenetre, text='Difficile', bg="blue", font=('arial', 14, 'italic bold'), fg='white', command=difficult_interface)
btn3.place(x=137, y=220)

# Lancement de la boucle principale de l'application
fenetre.mainloop()
