import tkinter as tk
from  quiz_manager import charger_questions
import json

index_question= 0

def lancer_quiz() :
    questions= charger_questions("easy")
    question_actuelle= questions[0]

    question_label.config(text=question_actuelle["question"])
    reponse1_button.config(text=question_actuelle["reponses"][0])       
    reponse2_button.config(text=question_actuelle["reponses"][1])
    reponse3_button.config(text=question_actuelle["reponses"][2])
    reponse4_button.config(text=question_actuelle["reponses"][3])
    reponse1_button.config(command=lambda: verifier_reponse(0, question_actuelle["reponse_correcte"]))
    reponse2_button.config(command=lambda: verifier_reponse(1, question_actuelle["reponse_correcte"]))
    reponse3_button.config(command=lambda: verifier_reponse(2, question_actuelle["reponse_correcte"]))
    reponse4_button.config(command=lambda: verifier_reponse(3, question_actuelle["reponse_correcte"]))
    question_label.pack()
    reponse1_button.pack()
    reponse2_button.pack()
    reponse3_button.pack()
    reponse4_button.pack()
    reponse_label.pack()
    reponse_label.config(text="")
    reponse_label.pack_forget()
    question_label.pack_forget()
        







