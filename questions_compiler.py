import re


def get_questions_units(filename):
    with open(filename, 'r', encoding='KOI8-R') as quiz_file:
        text_parts = quiz_file.read().split('\n\n')

    questions, answers = [], []
    for text_part in text_parts:
        if re.findall(r'Вопрос \d', text_part):
            questions.append(text_part)
        if re.findall(r'Ответ:', text_part):
            answers.append(text_part)

    return dict(zip(questions, answers))
