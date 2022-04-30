import os
import random
import re
import logging
from enum import Enum
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from question_set_getters import get_questions_answers_set
from redis_db_handler import redis_db

logger = logging.getLogger(__name__)


class States(Enum):
    HANDLE_NEW_QUESTION_REQUEST = 0
    HANDLE_SOLUTION_ATTEMPT = 1


questions_answers_set = get_questions_answers_set(os.getenv('QUIZ_FILE'))


def start(bot, update):
    custom_keyboard = [['Новый вопрос', 'Сдаться']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(
        text='Привет я бот для викторин! Для начала игры жми "Новый вопрос" ',
        reply_markup=reply_markup
    )

    return States.HANDLE_NEW_QUESTION_REQUEST


def handle_new_question_request(bot, update):
    question_text = random.choice(list(questions_answers_set.keys()))
    chat_id = update.message.chat_id
    redis_db.set(chat_id, questions_answers_set[question_text])
    update.message.reply_text(text=question_text)

    return States.HANDLE_SOLUTION_ATTEMPT


def handle_solution_attempt(bot, update):
    true_answer = re.split(r'\.|\(', redis_db.get(update.message.chat_id))[0].replace('Ответ:\n', '')
    if update.message.text == true_answer:
        logger.info(redis_db.get(update.message.chat_id))
        update.message.reply_text(
            text='Поздравляю,правильный ответ!',
        )
    else:
        update.message.reply_text(text='К сожалению, ответ неверный')


def give_up(bot, update):
    update.message.reply_text(
        text=redis_db.get(update.message.chat_id)
    )
    handle_new_question_request(bot, update)


def cancel(bot, update):
    user = update.message.from_user
    logger.info('User %s canceled the conversation.', user.first_name)
    update.message.reply_text('До встречи! Спасибо за игру!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():

    logging.basicConfig(format='TG-bot: %(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    while True:
        try:
            logging.info('Бот в Телеграм успешно запущен')
            updater = Updater(token=os.getenv('TG_BOT_TOKEN'))
            dp = updater.dispatcher
            conv_handler = ConversationHandler(
                entry_points=[CommandHandler('start', start)],

                states={

                    States.HANDLE_NEW_QUESTION_REQUEST: [MessageHandler(Filters.regex(r'Новый вопрос'),
                                                                        handle_new_question_request)],

                    States.HANDLE_SOLUTION_ATTEMPT: [MessageHandler(Filters.regex(r'Сдаться'),
                                                                    give_up),
                                                     MessageHandler(Filters.regex(r'Новый вопрос'),
                                                                    handle_new_question_request),
                                                     MessageHandler(Filters.text,
                                                                    handle_solution_attempt)],
                },

                fallbacks=[CommandHandler('cancel', cancel)]
            )

            dp.add_handler(conv_handler)
            updater.start_polling()
            updater.idle()

        except Exception as err:
            logging.error('Телеграм бот упал с ошибкой:')
            logging.exception(err)


if __name__ == '__main__':
    main()
