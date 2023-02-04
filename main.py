import telebot
from telebot import types
import requests #импорт
import json
import time
bot = telebot.TeleBot("") #токен бота

name = "" #Любое имя аккаунта
token_work = "" # Токен для выполнения заданий

@bot.message_handler(commands=["start"])
def test(message):
      keyboard = types.InlineKeyboardMarkup()
      work = types.InlineKeyboardButton(text='Проверка баланса', callback_data='balance')
      keyboard.add(work)
      version = types.InlineKeyboardButton(text='Версия', callback_data='version')
      keyboard.add(version)
      bot.send_message(message.from_user.id, text="Привет! Тыкай:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "balance":
        req = requests.get('https://app.ytmonster.ru/api/?balance=get&token=' + token_work)
        req = req.text
        req = req.replace('{"error":0,"response":{"status":"good","balance":', '')
        req = req.replace(',"money":0}}', '')
        bot.send_message(call.from_user.id, "Ваш баланс: " + req + " COIN")
        print('Сообщение отправлено!')
    elif call.data == "version":
        bot.send_message(call.message.chat.id, 'Версия бота: 0.1')

bot.infinity_polling(none_stop=True, interval=5)