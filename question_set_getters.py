import re


def get_questions_answers_set(filename):
    with open(filename, 'r', encoding='KOI8-R') as quiz_file:
        text_parts = quiz_file.read().split('\n\n')

    questions_set, answers_set = [], []
    for text_part in text_parts:
        if re.findall(r'Вопрос \d', text_part):
            questions_set.append(text_part)
        if re.findall(r'Ответ:', text_part):
            answers_set.append(text_part)

    return dict(zip(questions_set, answers_set))
