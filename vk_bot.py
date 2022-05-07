import os
import random
import re
import logging
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from questions_compiler import get_questions_units
from redis_db_handler import redis_db

logger = logging.getLogger(__name__)

questions_answers_set = get_questions_units(os.getenv('QUIZ_FILE'))

def send_keyboard(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message='Привет, я бот для викторин. Для начала нажми "Новый вопрос"',
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard(),
    )


def send_question_text(event, vk_api):
    question_text = random.choice(list(questions_answers_set.keys()))
    chat_id = event.user_id
    redis_db.set(chat_id, questions_answers_set[question_text])
    vk_api.messages.send(
        user_id=event.user_id,
        message=question_text,
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard(),
    )


def handle_solution_attempt(event, vk_api):
    true_answer = re.split(r'\.|\(',
                           redis_db.get(event.user_id))[0].replace(
                           'Ответ:\n', ''
    )
    if event.text == true_answer:
        logger.info(redis_db.get(event.user_id))
        vk_api.messages.send(
            user_id=event.user_id,
            message='Поздравляю,правильный ответ!',
            random_id=random.randint(1, 1000),
            keyboard=keyboard.get_keyboard(),
        )

    else:
        vk_api.messages.send(
            user_id=event.user_id,
            message='К сожалению, ответ неверный',
            random_id=random.randint(1, 1000),
            keyboard=keyboard.get_keyboard(),
        )


def give_up(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=redis_db.get(event.user_id),
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard(),
    )

    send_question_text(event, vk_api)


if __name__ == '__main__':

    logging.basicConfig(format='VK-bot: %(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    while True:
        try:
            logging.info('Бот Вконтакте успешно запущен')
            vk_session = vk_api.VkApi(token=os.getenv('VK_GROUP_ACCESS_KEY'))
            vk_api = vk_session.get_api()

            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)

            longpoll = VkLongPoll(vk_session)


            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    if event.text == 'Привет':
                        send_keyboard(event, vk_api)
                    elif event.text == 'Новый вопрос':
                        send_question_text(event, vk_api)
                    elif event.text == 'Сдаться':
                        give_up(event, vk_api)
                    else:
                        handle_solution_attempt(event, vk_api)

        except Exception as err:
            logging.error('Вконтакте бот упал с ошибкой:')
            logging.exception(err)