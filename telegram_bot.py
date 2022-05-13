import os
import random
import re
import logging
from enum import Enum
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from questions_compiler import get_questions_units
from functools import partial
import redis

logger = logging.getLogger(__name__)


class States(Enum):
    HANDLE_NEW_QUESTION_REQUEST = 0
    HANDLE_SOLUTION_ATTEMPT = 1


def start(bot, update):
    custom_keyboard = [['Новый вопрос', 'Сдаться']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(
        text='Привет я бот для викторин! Для начала игры жми "Новый вопрос" ',
        reply_markup=reply_markup
    )

    return States.HANDLE_NEW_QUESTION_REQUEST


def handle_new_question_request(bot, update, redis_db, questions):
    question, answer = random.choice(list(questions.items()))
    chat_id = update.message.chat_id
    redis_db.set(chat_id, answer)
    update.message.reply_text(text=question)

    return States.HANDLE_SOLUTION_ATTEMPT


def handle_solution_attempt(bot, update, redis_db):
    true_answer = re.split(r'\.|\(', redis_db.get(update.message.chat_id))[0].replace('Ответ:\n', '')
    if update.message.text == true_answer:
        logger.info(redis_db.get(update.message.chat_id))
        update.message.reply_text(
            text='Поздравляю,правильный ответ!',
        )
    else:
        update.message.reply_text(text='К сожалению, ответ неверный')


def give_up(bot, update, redis_db):
    update.message.reply_text(
        text=redis_db.get(update.message.chat_id)
    )
    handle_new_question_request(redis_db, bot, update)


def cancel(bot, update):
    user = update.message.from_user
    logger.info(f'User {user.first_name} canceled the conversation.')
    update.message.reply_text('До встречи! Спасибо за игру!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():

    logging.basicConfig(format='TG-bot: %(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    while True:
        try:
            logging.info('Бот в Телеграм успешно запущен')

            redis_connection_pool = redis.ConnectionPool(host=os.getenv('REDIS_HOST'),
                                                         port=os.getenv('REDIS_PORT'),
                                                         db=os.getenv('REDIS_DB'),
                                                         password=os.getenv('REDIS_PASSWORD'),
                                                         decode_responses=True,
                                                         encoding='KOI8-R'
                                                         )
            redis_db = redis.Redis(connection_pool=redis_connection_pool)
            questions = get_questions_units(os.getenv('QUIZ_FILE'))
            updater = Updater(token=os.getenv('TG_BOT_TOKEN'))
            dp = updater.dispatcher
            conv_handler = ConversationHandler(
                entry_points=[CommandHandler('start', start)],
                states={
                    States.HANDLE_NEW_QUESTION_REQUEST: [MessageHandler(Filters.regex(r'Новый вопрос'),
                                                                        partial(handle_new_question_request,
                                                                                redis_db=redis_db,
                                                                                questions=questions
                                                                                )
                                                                        )
                                                         ],

                    States.HANDLE_SOLUTION_ATTEMPT: [MessageHandler(Filters.regex(r'Сдаться'),
                                                                    partial(give_up,
                                                                            redis_db=redis_db)
                                                                    ),

                                                     MessageHandler(Filters.regex(r'Новый вопрос'),
                                                                    partial(handle_new_question_request,
                                                                            redis_db=redis_db,
                                                                            questions=questions
                                                                            )
                                                                    ),

                                                     MessageHandler(Filters.text,
                                                                    partial(handle_solution_attempt,
                                                                            redis_db=redis_db
                                                                            )
                                                                    )
                                                     ],
                },

                fallbacks=[CommandHandler('cancel', cancel)])

            dp.add_handler(conv_handler)
            updater.start_polling()
            updater.idle()

        except Exception as err:
            logging.error('Телеграм бот упал с ошибкой:')
            logging.exception(err)


if __name__ == '__main__':
    main()
