# Quiz-bot

Запускаем бота-викторину для Вконтакте и Telegram на стеке Python/Redis

### Как установить

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Перед запуском 

##### Переменные окружения и их настройка
В проекте будут использованы следующие переменные окружения:  
`TG_BOT_TOKEN`
`REDIS_HOST`
`REDIS_PORT`
`REDIS_DB`
`REDIS_PASSWORD`
`QUIZ_FILE`
`VK_GROUP_ACCESS_KEY`
 
Данные переменные должны быть прописаны в файле с именем `.env`, лежащим в корневом каталоге проекта.
Подробнее о том, какие значения присвоить каждой из них в инструкции далее.

##### 1. Создаем базу данных Redis. 
Переходим по ссылке: https://redislabs.com/

Адрес Вашей БД до двоеточия укажите в переменную:
`REDIS_HOST`
Порт пишется прямо в адресе, через двоеточие. Впишите его в переменную окружения:
`REDIS_PORT`
Переменную окружения `REDIS_DB` по умолчанию укажите равной "0".
Пароль от базы данных укажите в переменную окружения:
`REDIS_PASSWORD`

##### 2. Группа Вконтакте, в которой будет использоваться Ваш Вконтакте-бот.

Разрешаем боту отправку сообщений:
<img src="https://dvmn.org/media/screenshot_from_2019-04-29_20-15-54.png">

##### 3 .Получаем ключ от группы в меню “Работа с API” - создать ключ доступа:
<img src="https://dvmn.org/filer/canonical/1556554255/101/">

Данный ключ помещаем в переменную `VK_GROUP_ACCESS_KEY` файла `.env` проекта:
```
VK_GROUP_ACCESS_KEY='YOUR_VK_GROUP_ACCESS_KEY'
```


##### 4. Создаем телеграмм чат-бота. 

Инструкция по регистрации бота и получению токена здесь: https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/ или здесь: https://habr.com/ru/post/262247/.
Кратко: просто напишите в телеграмм боту @BotFather и следуйте его инструкциям. 
Полученный токен сохраните в переменную `TG_BOT_TOKEN` файла `.env` проекта:

```
TG_BOT_TOKEN='YOUR_TELEGRAM_BOT_TOKEN'
```

##### 5. Сохраняем файл с вопросами
Сохраняем путь до файла с вопросами в переменную окружения `QUIZ_FILE`.
Тестовый набор файлов можно скачать по ссылке: https://dvmn.org/media/modules_dist/quiz-questions.zip

### Начало работы
Теперь, когда мы заполнили все требуемые переменные окружения можно приступать к запуску наших ботов в теством режиме.
Для того, чтобы создать тестовые интенты для агента Dialogflow, используйте следующую команду в терминале:
```  
$python dialogflow_learner.py
```  

В тестовом режиме (без деплоя) скрипты ботов запускаются простым выполнением команд из терминала:
для Телеграмм-бота:
```  
$python telegram_bot.py
```  
и для бота Вконтакте, соответственно:
```  
$python vk_bot.py
```  

### Примеры работы ботов
Пример работы бота в Телеграм:

<img src="https://i.ibb.co/WHWNkwj/Tg-bot.gif">

Пример работы бота Вконтакте:

<img src="https://i.ibb.co/58ZfVHF/Vk-bot.gif">

#### Ссылки на задеплоенные тестовые боты:

Вконтакте: 
https://vk.com/im?sel=-212933177

Телеграм: 
https://t.me/dvmn_quiz_telebot

### Деплоим проект с помощью Heroku
Необязательный шаг. Бот может работать и непосредственно на Вашем сервере (при наличии такового). 
Чтобы развернуть наш бот на сервере бесплатно можно использовать сервис Heroku https://heroku.com. Инструкция по деплою здесь: https://ru.stackoverflow.com/questions/896229/%D0%94%D0%B5%D0%BF%D0%BB%D0%BE%D0%B9-%D0%B1%D0%BE%D1%82%D0%B0-%D0%BD%D0%B0-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B5-heroku или здесь (инструкция для ВК-приложений на Python, но все работает аналогично): https://blog.disonds.com/2017/03/20/python-bot-dlya-vk-na-heroku/ 
Важно отметить, что создать приложение на Heroku можно и без использования Heroku CLI, но оно будет крайне полезно для сбора наших логов.

Кратко:

создаем и или используем существующий аккаунт GitHub https://github.com/;
"клонируем" данный репозиторий к себе в аккаунт;
регистрируемся в Heroku и создаем приложение по инструкции выше;
"привязываем" учетную запись GitHub к учетной записи Heroku;
в качестве репозитория в Deployment Method на странице Deploy Вашего приложения в Heroku указываем GitHub и добавляем ссылку на данный репозиторий;
запускаем бота на сервере, нажав кнопку connect.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.
