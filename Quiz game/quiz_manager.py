import json

import json

def charger_questions(niveau):
    with open(f'data/questions/{niveau}.json', 'r', encoding='utf-8') as fichier:
        questions = json.load(fichier)
    return questions
