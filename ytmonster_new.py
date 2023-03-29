import telebot
from telebot import types
import requests
import json
import time
from datetime import datetime
import speedtest
import yt_monster_py as yt_monster


text = ""
bot1 = ""
token_work = "" #(для выполнения заданий)
token_task = ""
id = ''
Versoin = '2.6 '

print("Для получения токена Yt_monster используйте: https://ytmonster.ru/api/#key \nДля получения токена Telegram бота используйте: https://t.me/BotFather\nTelegram канал разработчика: https://t.me/GODIMONGO\nВерсия:" + Versoin)
time.sleep(5)
yt_monster.log('Старт бота')
#принт начального сообщения
try:
    with open('token.txt', 'r') as f:
        try:
            l = [line.strip() for line in f]
            bot1 = l[0]
            token_work = l[1]
            token_task = l[2]
            f.close()
        except IndexError:
            yt_monster.log('IndexError')
            print('Ошибка чтения файла!!!!')
            bot1 = input("Введите токен telegram бота: ")
            token_work = input("Введите токен Ytmonster (для выполнения заданий): ")
            token_task = input("Введите токен Ytmonster (для добавления заданий): ")
except FileNotFoundError:
    yt_monster.log('token.txt err: FileNotFoundError')
    bot1 = input("Введите токен telegram бота: ")
    token_work = input("Введите токен Ytmonster (для выполнения заданий): ")
    token_task = input("Введите токен Ytmonster (для добавления заданий): ")
    with open('token.txt', 'w') as f:
        f.write(bot1 + '\n')
        f.write(token_work + '\n')
        f.write(token_task + '\n')
        f.close()
token = [token_work, token_task] #создания списка из токенов



print('Проверка токена для (для выполнения заданий)')
yt_monster.log('Проверка токена для (для выполнения заданий)')
req, err = yt_monster.ytmonster_req(token, 'balance') #запрос проверки токена для проверки баланса
while err != 'ok':
    print(err)
    token[0] = input('Введите токен Ytmonster (для выполнения заданий):')
    req, err = yt_monster.ytmonster_req(token, 'balance')
with open('token.txt', 'w') as f:
    f.write(bot1 + '\n')
    f.write(token[0] + '\n')
    f.write(token[1] + '\n')



print('Проверка токена для (для добавления заданий)\nЭтот процес займет немного времени!')
yt_monster.log('Проверка токена для (для добавления заданий)')
req, err = yt_monster.ytmonster_req(token, 'my_task', 'ytview')
while err != 'ok':
    token[1] = input('Введите токен Ytmonster (для добавления заданий):')
    req, err = yt_monster.ytmonster_req(token, 'my_task', 'ytview')


print('ping: api.telegram.org ...')
time.sleep(1)
req = requests.get('https://api.telegram.org/bot' + bot1 + '/getMe')
while req.text == """{"ok":false,"error_code":404,"description":"Not Found"}""" or bot1 == "" or req.text == """{"ok":false,"error_code":401,"description":"Unauthorized"}""":
    print("Вы неправильно ввели токен бота!")
    bot1 = input("Введите токен telegram бота: ")
    req = requests.get('https://api.telegram.org/bot' + bot1 + '/getMe')
time.sleep(1)
with open('token.txt', 'w') as f:
    f.write(bot1 + '\n')
    f.write(token[0] + '\n')
    f.write(token[1] + '\n')

def button_start():
    keyboard = types.InlineKeyboardMarkup()
    work = types.InlineKeyboardButton(text='Проверка баланса', callback_data='balance')
    keyboard.add(work)
    version = types.InlineKeyboardButton(text='Версия', callback_data='version')
    keyboard.add(version)
    get_client = types.InlineKeyboardButton(text='Получить список рабочих клиентов', callback_data='get_client')
    keyboard.add(get_client)
    change = types.InlineKeyboardButton(text='Поменять токен от ytmonster(скоро)', callback_data='change')
    keyboard.add(change)
    clear_log = types.InlineKeyboardButton(text='Очистить фаел логов', callback_data='clear_log')
    keyboard.add(clear_log)
    close_client = types.InlineKeyboardButton(text='Закрыть клиент(скоро)', callback_data='close_client')
    keyboard.add(close_client)
    my_task = types.InlineKeyboardButton(text='Получить список заданий', callback_data='my_task')
    keyboard.add(my_task)
    send_log = types.InlineKeyboardButton(text='Отправить лог', callback_data='send_log')
    keyboard.add(send_log)
    speedtest = types.InlineKeyboardButton(text='Замерить скорость интернета(скоро)', callback_data='speedtest')
    keyboard.add(speedtest)
    return keyboard

bot = telebot.TeleBot(bot1)
print('\n'* 100)
print('Бот запущен!')
yt_monster.log('Бот запущен!')
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEINtRkGK9SK6pHQrYy1aKnW-6ZcmlEjQAC8zAAAiP1yEgwajIpJJRmtS8E')
    bot.send_message(message.from_user.id, text="Привет! Выбери кнопку:", reply_markup=button_start())


@bot.callback_query_handler(func=lambda call: True) #ответ на кнопки
def callback_worker(call):
    global bot1, token_work, Versoin, token_task
    if call.data == "balance":
        req, err = yt_monster.ytmonster_req(token, 'balance')
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(back)
        if err != 'ok':
            bot.send_message(call.from_user.id, text='Произошла ошибка:' + err, reply_markup=keyboard)
            yt_monster.log('Произошла ошибка:' + err)
            print('Сообщение отправлено!')
        bot.send_message(call.from_user.id, text='Баланс: ' + str(req) + ' COIN', reply_markup=keyboard)
        print('Сообщение отправлено!')

    elif call.data == "version":
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(back)
        bot.send_message(call.from_user.id, text=str('Версия бота: ' + str(Versoin) + '\nTelegram канал разработчика: https://t.me/GODIMONGO'), reply_markup=keyboard)
        print('Сообщение отправлено!')

    elif call.data == "get_client":
        bot.send_message(call.from_user.id, 'Эта задача займет некоторое время')
        req, err = yt_monster.ytmonster_req(token, 'get_client')
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(back)
        bot.send_message(call.from_user.id, text=str(req), reply_markup= keyboard)
        print('Сообщение отправлено!')

    elif call.data == "back":
        bot.send_message(call.from_user.id, text="Привет! Выбери кнопку:", reply_markup=button_start())
        print('Сообщение отправлено!')

    elif call.data == "my_task":
        keyboard = types.InlineKeyboardMarkup()
        vk = types.InlineKeyboardButton(text='Вконтакте', callback_data='vk')
        keyboard.add(vk)
        inst = types.InlineKeyboardButton(text='Instagram', callback_data='inst')
        keyboard.add(inst)
        tiktok = types.InlineKeyboardButton(text='TikTok', callback_data='tiktok')
        keyboard.add(tiktok)
        paid = types.InlineKeyboardButton(text='Платные задания', callback_data='paid')
        keyboard.add(paid)
        ytview = types.InlineKeyboardButton(text='Youtube просмотры', callback_data='ytview')
        keyboard.add(ytview)
        ytlike = types.InlineKeyboardButton(text='Youtube лайки', callback_data='ytlike')
        keyboard.add(ytlike)
        ytsubs = types.InlineKeyboardButton(text='Youtube подписчики', callback_data='ytsubs')
        keyboard.add(ytsubs)
        ytcomm = types.InlineKeyboardButton(text='Youtube комментарии', callback_data='ytcomm')
        keyboard.add(ytcomm)
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(back)
        bot.send_message(call.from_user.id, text="Выберите соц. сеть по которой хотели бы получить информацию", reply_markup=keyboard)
    elif call.data == "vk":
        req, err = yt_monster.ytmonster_req(token, 'my_task', "vk")
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(back)
        bot.send_message(call.from_user.id, text=req, reply_markup=keyboard)
    elif call.data == "inst":
        req, err = yt_monster.ytmonster_req(token, 'my_task', "inst")
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(back)
        bot.send_message(call.from_user.id, text=req, reply_markup=keyboard)
    elif call.data == "tiktok":
        req, err = yt_monster.ytmonster_req(token, 'my_task', "tiktok")
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(back)
        bot.send_message(call.from_user.id, text=req, reply_markup=keyboard)
    elif call.data == 'paid':
        req, err = yt_monster.ytmonster_req(token, 'my_task', "paid")
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(back)
        bot.send_message(call.from_user.id, text=req, reply_markup=keyboard)
    elif call.data == 'ytview':
        req, err = yt_monster.ytmonster_req(token, 'my_task', "ytview")
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(back)
        bot.send_message(call.from_user.id, text=req, reply_markup=keyboard)
    elif call.data == 'ytlike':
        req, err = yt_monster.ytmonster_req(token, 'my_task', "ytlike")
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(back)
        bot.send_message(call.from_user.id, text=req, reply_markup=keyboard)
    elif call.data == 'ytsubs':
        req, err = yt_monster.ytmonster_req(token, 'my_task', "ytsubs")
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(back)
        bot.send_message(call.from_user.id, text=req, reply_markup=keyboard)
    elif call.data == 'ytcomm':
        req, err = yt_monster.ytmonster_req(token, 'my_task', "ytcomm")
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(back)
        bot.send_message(call.from_user.id, text=req, reply_markup=keyboard)
    elif call.data == 'send_log':
        bot.send_message(call.message.chat.id, 'Отправка лога')
        log=open('log.txt', 'rb')
        bot.send_document(call.message.chat.id, log)
        log.close()
    elif call.data == 'clear_log':
        with open('log.txt', 'w') as f:
            f.write('\nclear log: ' + str(datetime.now()))
            f.close()
            keyboard = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton(text='Назад', callback_data='back')
            keyboard.add(back)
            bot.send_message(call.from_user.id, text='Лог очищен.', reply_markup=keyboard)




bot.infinity_polling(none_stop=True, interval=0)