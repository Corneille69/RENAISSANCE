
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

def jouer_quiz():
    score = 0
    random.shuffle(questions)
    
    for q in questions:
        print("\n" + q["question"])
        for i, option in enumerate(q["options"], 1):
            print(f"{i}. {option}")
        
        try:
            choix = int(input("Votre réponse (1-4) : "))
            if q["options"][choix - 1] == q["answer"]:
                print("✅ Bonne réponse !")
                score += 1
            else:
                print(f"❌ Mauvaise réponse. La bonne réponse était : {q['answer']}")
        except (ValueError, IndexError):
            print("Entrée invalide. Essayez encore.")

    print(f"\n🎯 Votre score final est : {score}/{len(questions)}")

jouer_quiz()