import tkinter
from quiz_manager import charger_questions

def lancer_quiz() :
    questions= charger_questions("easy")
    question_actuelle= questions[0]

    def verification_fichier(index) :  # Removed space before (index)
        if question_actuelle["options"][index]== question_actuelle["answer"] :
            resultat.config(text="Bonne reponse !",fg ="green")
        else :
            resultat.config(text="Mauvaise reponse !",fg ="red")


    verification_fichier(0)
    # Créer une nouvelle fenêtre pour afficher la question
    question_window = tkinter.Toplevel(app)
def Continuer() :
    main_frame.grid_forget()    
    second_interface_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
    second_interface_frame.geometry('740x400')

#initialisation de l'interface
app= tkinter.Tk()
app.title("Quiz")
app.geometry('740x400')


# Création du frame principal (Page de connexion)
main_frame = tkinter.Frame(app)
main_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

Welcom= tkinter.Label(main_frame, text='WELCOM ')
btn1= tkinter.Button(main_frame, text='Continuer',command=Continuer)





Welcom.config(font=("Arial", 25), bg='white', fg='black')
Welcom.grid(row=0, column=1, padx=10, pady=10)
btn1.config(font=("Arial", 16), bg='green', fg='black')
btn1.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(2, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(2, weight=1)

# Interface après connexion (Tableau de bord)
second_interface_frame = tkinter.Frame(app)
second=tkinter.Label(second_interface_frame, text="Veillez choisir un niveau",font=("Arial", 16))
question =tkinter.Label(second, text="Question[option]", font=("Arial", 12))
second.config(bg='white', fg='black')
second.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

question.grid()
from PIL import Image, ImageTk

# Chargement de l'image avec Pillow
img = Image.open('x.png')  # Remplacez 'x.jpg' par le chemin de votre image
photo = ImageTk.PhotoImage(img)
btn2=tkinter.Button(second_interface_frame, text='Facile',command=lancer_quiz)

btn3=tkinter.Button(second_interface_frame, text='Moyen')
btn4=tkinter.Button(second_interface_frame, text='Difficile')
# Redimensionner l'image avec Pillow
img = img.resize((200, 200))  # Ajustez les dimensions (200, 200) selon vos besoins

photo = ImageTk.PhotoImage(img)
mage_label = tkinter.Label(second_interface_frame, image=photo)
second.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
mage_label.grid(row=2, column=1, padx=2, pady=2)
btn2.grid(row=3,column=0)
btn3.grid(row=3,column=1)
btn4.grid(row=3,column=2)

resultat=tkinter.Label(second,text="option", font=("Arial", 12))
resultat.config(bg='white', fg='black')
resultat.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")


# Initialisation des couleurs de l'interface
app.configure(bg='#f9f9f9')
app.mainloop()