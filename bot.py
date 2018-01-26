# -*- coding: utf-8 -*-
# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json
updater = Updater(token='505945240:AAEsDMDHWpQWnTq3sQ5e5MJ0ept5PqmjXCw')
dispatcher = updater.dispatcher
WORK = True
welcome_text = 'Привет! Задавай вопрос, а я постараюсь на него ответить'
# Обработка команд
def startCommand(bot, update):
    bot.sendMessage(update.message.chat_id, text=welcome_text)
    #psw = update.message.text
    #if psw == 123:
    #    GO = 1
    #else:
    #    bot.send_message(chat_id=update.message.chat_id, text='Введите команду /start и ответьте на вопрос для работы с чатом')
def on(bot, update):
    global WORK
    WORK = True
    bot.send_message(chat_id=update.message.chat_id, text= u'Можем начинать!')
def off(bot, update):
    global WORK
    WORK = False
    bot.send_message(chat_id=update.message.chat_id, text= u'Я ушел, но если введешь команду я вернусь!')
# Сообщения Dialogflow
def textMessage(bot, update):
    if WORK == True:
        request = apiai.ApiAI('a4d8ab30cf8f4f648a5c0bb165091513').text_request() # Токен API к Dialogflow
        request.lang = 'ru' # На каком языке будет послан запрос
        request.session_id = 'SBBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
        request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
        # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
        if response:
            bot.send_message(chat_id=update.message.chat_id, text=response)
        else:
            bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')
    else:
        bot.send_message(chat_id=update.message.chat_id, text= u'Привет, введи пароль чтобы начать!')
        #psw = update.message.text
        #if psw == 123:
        #    GO = 1
# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
dispatcher.add_handler(CommandHandler('on', on))
dispatcher.add_handler(CommandHandler('off', off))
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
