import telebot
from telebot import types
import requests
import json
import time
a = ""
b = ""
bot1 = ""
token_work = ""
i = '0'
print("Для получения токена Yt_monster используйте: https://ytmonster.ru/api/#key \nДля получения токена Telegram бота используйте: https://t.me/BotFather ")
try:
    f = open('text.txt', 'r')
    l = [line.strip() for line in f]
    bot1 = l[0]
    token_work = l[1]
    f.close()
except FileNotFoundError:

    bot1 = input("Введите токен telegram бота: ")
    token_work = input("Введите токен Ytmonster: ")
    f = open('text.txt', 'w')
    f.write(bot1 + '\n')
    f.write(token_work + '\n')
    f.close()
def rew():
    global bot1, token_work, a, b, i
    i = 0
    while i == 0:
        print('\nping: ytmonster.ru ...')
        req_test = requests.get('https://app.ytmonster.ru/api/?balance=get&token=' + token_work)
        if req_test.text == """{"error":1002}""" or token_work == "" or req_test.text == """{"error":1001}""" or req_test.text == """{"error":1004}""":
            token_work = input("\nОШИБКА " + req_test.text + "! Введите токен Ytmonster:")
            f = open('text.txt', 'w')
            f.write(bot1 + '\n')
            f.write(token_work + '\n')
            f.close()
            time.sleep(1)
        elif req_test.text == """{"error":1003}""":
            print("\nОШИБКА 1003!! Включите токен на сайте: https://ytmonster.ru/api/#key")
            token_work = input('Введите токен Ytmonster:')
            time.sleep(1)
        elif req_test.text == """{"error":902}""":
            print("ОШИБКА 902!! Вы ввели не верный токен! Нужен токен: Ключ доступа (для выполнения заданий)")
            token_work = '\nВведите токен Ytmonster:'
        else:
            print('Ok')
            time.sleep(1)
            i = 1

    print('ping: api.telegram.org ...')
    time.sleep(1)
    req_test = requests.get('https://api.telegram.org/bot' + bot1 + '/getMe')
    print(req_test.text)
    while req_test.text == """{"ok":false,"error_code":404,"description":"Not Found"}""" or bot1 == "" or req_test.text == """{"ok":false,"error_code":401,"description":"Unauthorized"}""":
        bot1 = input("Вы неправильно ввели токен бота! Введите токен telegram бота: ")
        f = open('text.txt', 'w')
        f.write(bot1 + '\n')
        f.write(token_work + '\n')
        f.close()
        print('ping: api.telegram.org ...')
        req_test = requests.get('https://api.telegram.org/bot' + bot1 + '/getMe')
        time.sleep(1)
    print('Ok')
rew()
bot = telebot.TeleBot(bot1)

@bot.message_handler(commands=["start"]) #начальные кнопочки
def test(message):
    keyboard = types.InlineKeyboardMarkup()
    work = types.InlineKeyboardButton(text='Проверка баланса', callback_data='balance')
    keyboard.add(work)
    version = types.InlineKeyboardButton(text='Версия', callback_data='version')
    keyboard.add(version)
    get_client = types.InlineKeyboardButton(text='Получить список рабочих клиентов', callback_data='get_client')
    keyboard.add(get_client)
    change = types.InlineKeyboardButton(text='Поменять данные от телеграм или ютмонстер', callback_data='change')
    keyboard.add(change)
    bot.send_message(message.from_user.id, text="Привет! Выбери кнопку:", reply_markup=keyboard)



def repa(call): #повторение кнопочек
    keyboard = types.InlineKeyboardMarkup()
    work = types.InlineKeyboardButton(text='Проверка баланса', callback_data='balance')
    keyboard.add(work)
    version = types.InlineKeyboardButton(text='Версия', callback_data='version')
    keyboard.add(version)
    get_client = types.InlineKeyboardButton(text='Получить список рабочих клиентов', callback_data='get_client')
    keyboard.add(get_client)
    change = types.InlineKeyboardButton(text='Поменять данные от телеграм или ютмонстер', callback_data='change')
    keyboard.add(change)
    bot.send_message(call.from_user.id, text="Привет! Выбери кнопку:", reply_markup=keyboard)

def back_def(call, mes):
    keyboard = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton(text='Назад', callback_data='back')
    keyboard.add(back)
    bot.send_message(call.from_user.id, mes, reply_markup=keyboard)
    print('Сообщение отправлено!')

@bot.callback_query_handler(func=lambda call: True) #ответ на кнопки
def callback_worker(call):
    global bot1, token_work, a, b, i
    if call.data == "balance":
        req = requests.get('https://app.ytmonster.ru/api/?balance=get&token=' + token_work)
        req = req.text
        if req == """{"error":1002}""":
            bot.send_message(call.from_user.id, "Вы забыли указать Токен от yt_monster для выполнения задания")
            print('Ошибка 1002! Укажите данные в переменную: token_work')
        elif req == """{"error":1003}""":
            bot.send_message(call.from_user.id, "Включите токен на сайте: https://ytmonster.ru/api/#key")
        else:
            req = req.replace('{"error":0,"response":{"status":"good","balance":', '')
            req = req.replace(',"money":0}}', '')
            mes = "Ваш баланс: " + req + " COIN"
            back_def(call, mes) # отправка сообщения и кнопки домой
            print('Сообщение отправлено!')
            time.sleep(5)
    elif call.data == "version":
        bot.send_message(call.message.chat.id, 'Версия бота: 1')
        print('Сообщение отправлено!')
    elif call.data == "get_client":
        bot.send_message(call.message.chat.id, 'Выполняется проверка клиентов')
        try:
            req = requests.get('https://app.ytmonster.ru/api/?get-clients=get&token=' + token_work)
        except requests.exceptions.RequestException as e:
            time.sleep(10)
            bot.send_message(call.message.chat.id, 'Ошибка запроса к API проверьте работает ли сайт ?')
        if req.text == """{"error":1002}""":
            bot.send_message(call.from_user.id, "Вы забыли указать Токен от yt_monster для выполнения задания")
            print('Ошибка 1002! Укажите данные в переменную: token_work')
        elif req.text =="""{"error":1003}""":
            bot.send_message(call.from_user.id, "Включите токен на сайте: https://ytmonster.ru/api/#key")
            print("Включите токен на сайте: https://ytmonster.ru/api/#key")
        else:
            if req.text == """{"error":0,"response":[]}""":
                client_info = 'Нет рабочих клиентов'
                print(client_info)
                bot.send_message(call.message.chat.id, 'Нет рабочих клиентов')
            else:
                json1 = json.loads(req.text)
                i = len(json1['response'])
                b = 0  # количество просмотренной информации
                client_info = ""
                while i > b:  # количество просмотренных видео
                    time.sleep(1)
                    count = (json1["response"][b]["data"]["count"])  # получение количества просмотров клиента
                    sec = (json1["response"][b]["info"]["sec"])  # получение количества времени до конца просмотра ролика
                    error = (json1["response"][b]["info"]["error"])  # получение количества ошибок клиента
                    client_info = client_info + '\n---------------\nКлиент: ' + str(b) + ' \nПросмотрел: ' + str(count) + ' видео' + '\nОшибок: ' + str(error) + '\nОсталось до конца просмотра: ' + str(sec) + ' секунд'
                    b += 1
                    bot.send_message(call.message.chat.id, 'Обработано клиентов: ' + str(b))
                print(client_info)
                mes = client_info
                time.sleep(1)
                back_def(call, mes)  # отправка сообщения и кнопки домой
    elif call.data == "back":
        repa(call)
    elif call.data == 'change':
        mes = 'Для смены токена Telegram бота: \nВведите команду /newtokenbot и укажите вместе с ней токен Пример: \n/newtoken 6167739229:AAEObtnn7OfIt6Rkjx99X3 \n Для смены токена ют монстер введите: /newtokenytmonster и укажите токен \n Пример: \n /newtokenytmonster 0539765JngIyxaPEpOxdhzguT '
        back_def(call, mes)
    elif call.data == 'contin_bot':
        bot1 = a
        f = open('text.txt', 'w')
        f.write(bot1 + '\n')
        f.write(token_work + '\n')
        f.close()
        rew()
        bot.send_message(call.message.chat.id, 'Бот готов к работе!')



@bot.message_handler(commands=["newtokenbot"])
def newtokenbot(message):
    global bot1, a
    mess = message.text.replace('/newtokenbot', '')
    time.sleep(0.1)
    mess = mess.strip()
    time.sleep(0.1)
    req_test = requests.get('https://api.telegram.org/bot' + mess + '/getMe')
    if req_test.text == """{"ok":false,"error_code":404,"description":"Not Found"}""" or bot1 == "" or req_test.text == """{"ok":false,"error_code":401,"description":"Unauthorized"}""":
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(back)
        bot.send_message(message.from_user.id, text='Вы ввели не правильно токен! Повторите попытку.', reply_markup=keyboard)
        print('Сообщение отправлено!')
    else:
        print('Бот меняет свой токен на:' + mess)
        json1 = json.loads(req_test.text)
        username = (json1["result"]["username"])
        print(username)
        bot.send_message(message.from_user.id, text='Все верно! Старый токен отключается и подключается новый!Ваш новый токен привязан к боту: @' + username)
        keyboard = types.InlineKeyboardMarkup()
        contin_bot = types.InlineKeyboardButton(text='ПРОДОЛЖИТЬ', callback_data='contin_bot')
        keyboard.add(contin_bot)
        bot.send_message(message.from_user.id, text='Перейдите в нового бота и нажмите СТАРТ: @' + username + 'После этого нажмите кнопку ПРОДОЛЖИТЬ', reply_markup=keyboard)
        a = mess
@bot.message_handler(commands=["newtokenytmonster"])
def newtokenytmonster(message):
    global bot1, a
    mess = message.text.replace('newtokenytmonster', '')
    time.sleep(0.1)
    mess = mess.strip()
    time.sleep(0.1)
    print('\nping: ytmonster.ru ...')
    bot.send_message(message.from_user.id, text='ping: ytmonster.ru ...')
    req_test = requests.get('https://app.ytmonster.ru/api/?balance=get&token=' + mess)
    if req_test.text == """{"error":1002}""" or mess == "" or req_test.text == """{"error":1001}""" or req_test.text == """{"error":1004}""":
        bot.send_message(message.from_user.id, 'ОШИБКА! ' + req_test.text + 'Возможно вы не правильно указали токен!' )
    elif req_test.text == """{"error":1003}""":
        bot.send_message(message.from_user.id, "ОШИБКА 1003!! Включите токен на сайте: https://ytmonster.ru/api/#key")
    elif req_test.text == """{"error":902}""":
        bot.send_message(message.from_user.id, "ОШИБКА 902!! Вы ввели не верный токен! Нужен токен: Ключ доступа (для выполнения заданий)")
    else:
        print('Ok')
        time.sleep(1)
        bot.send_message(message.from_user.id, text='ok, секунду...')
        f = open('text.txt', 'w')
        f.write(bot1 + '\n')
        f.write(token_work + '\n')
        f.close()
        rew()
        bot.send_message(message.from_user.id, text='Все верно!Токен от yt_monster поменялся')


bot.infinity_polling(none_stop=True, interval=0)