import random

questions = [
    {
        "question": "Столица Франции?",
        "options": ["Париж", "Лондон", "Рим", "Берлин"],
        "answer": "Париж"
    },
    {
        "question": "Сколько планет в Солнечной системе?",
        "options": ["7", "8", "9", "10"],
        "answer": "8"
    },
    {
        "question": "Кто написал 'Войну и мир'?",
        "options": ["Толстой", "Достоевский", "Пушкин", "Чехов"],
        "answer": "Толстой"
    },
]

def get_question():
    return random.choice(questions)
