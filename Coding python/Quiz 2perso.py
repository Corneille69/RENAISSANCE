

import tkinter as tk
import random

questions = [
    {
        "question": "Quelle est la capitale de l'Australie ?",
        "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"],
        "answer": "Canberra"
    },
    {
        "question": "Combien de joueurs y a-t-il dans une équipe de football ?",
        "options": ["9", "10", "11", "12"],
        "answer": "11"
    },
    {
        "question": "Qui a peint la Joconde ?",
        "options": ["Michel-Ange", "Léonard de Vinci", "Raphaël", "Van Gogh"],
        "answer": "Léonard de Vinci"
    },
    {
        "question": "Quelle est la formule chimique de l'eau ?",
        "options": ["CO2", "H2O", "NaCl", "O2"],
        "answer": "H2O"
    },
    {
        "question": "Quelle planète est la plus proche du Soleil ?",
        "options": ["Vénus", "Mars", "Mercure", "Terre"],
        "answer": "Mercure"
    }
]


random.shuffle(questions)

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz - Niveau Moyen")
        self.current_question = 0
        self.score = 0

        self.question_label = tk.Label(root, text="", font=("Arial", 16), wraplength=400, justify="center")
        self.question_label.pack(pady=20)

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.next_button = tk.Button(root, text="Question suivante", command=self.next_question)
        self.next_button.pack(pady=10)

        self.load_question()

    def load_question(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        if self.current_question < len(questions):
            q = questions[self.current_question]
            self.question_label.config(text=q["question"])
            for option in q["options"]:
                btn = tk.Button(self.buttons_frame, text=option, width=30,
                                command=lambda opt=option: self.check_answer(opt))
                btn.pack(pady=5)
        else:
            self.question_label.config(text=f"🎉 Fin du quiz ! Score : {self.score}/{len(questions)}")
            self.buttons_frame.destroy()
            self.next_button.destroy()
            self.result_label.destroy()

    def check_answer(self, selected_option):
        correct = questions[self.current_question]["answer"]
        if selected_option == correct:
            self.result_label.config(text="✅ Bonne réponse !")
            self.score += 1
        else:
            self.result_label.config(text=f"❌ Mauvaise réponse. Réponse : {correct}")

    def next_question(self):
        self.result_label.config(text="")
        self.current_question += 1
        self.load_question()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x400")
    app = QuizApp(root)
    root.mainloop()

app.mainloop()