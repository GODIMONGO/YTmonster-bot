import telebot
from telebot import types
import requests
import json
import time
from datetime import datetime

text =  ""
bot1 = ""
token_work = ""
id = ''

with open('log.txt', 'a') as f:
    f.write('\nbot start: ' + str(datetime.now()))
    f.close()

def log(text):
    with open('log.txt', 'a') as f:
        f.write('\n' + str(datetime.now()) + '  ' + text )
        f.close()


print("Для получения токена Yt_monster используйте: https://ytmonster.ru/api/#key \nДля получения токена Telegram бота используйте: https://t.me/BotFather ")
# проверка токена ytmonster, принимает условия
def ytmonster(task):
    global token_work, id
    print('ping: ytmonster.ru ...')
    try:
        if task == 'balance':
            req = requests.get('https://app.ytmonster.ru/api/?balance=get&token=' + token_work)
        elif task == 'get_client':
            req = requests.get('https://app.ytmonster.ru/api/?get-clients=get&token=' + token_work)
        elif task == 'close_client':
            req = requests.get('https://app.ytmonster.ru/api/?close-client=' + id + '&token=' + token_work)
        else:
            err = 'Ошибка ping! Нет указания что делать'
            log(err)
            return '', err
        if req.text == """{"error":1002}""" or token_work == "" or req.text == """{"error":1001}""" or req.text == """{"error":1004}""":
            err = "ОШИБКА " + req.text + "Возможно вы ввели не верный токен!"
            time.sleep(1)
            log(err)
            return '', err
        elif req.text == """{"error":1003}""":
            err = "ОШИБКА 1003!! Включите токен на сайте: https://ytmonster.ru/api/#key"
            time.sleep(1)
            log(err)
            return '', err
        elif req.text == """{"error":902}""":
            err = "ОШИБКА 902!! Вы ввели не верный токен! Нужен токен: Ключ доступа (для выполнения заданий)"
            time.sleep(1)
            log(err)
            return '', err
        else:
            print('ok')
            err = 'ok'
            time.sleep(1)
            return req, err
    except requests.exceptions.RequestException as e:
        time.sleep(10)
        print('ping err')
        err = 'Ошибка запроса к API ytmonster! Работает ли сайт?'
        return '', err

# проверка токена бота, не принимает условий
def telegram():
    print('ping: api.telegram.org ...')
    time.sleep(1)
    req = requests.get('https://api.telegram.org/bot' + bot1 + '/getMe')
    print(req.text)
    if req.text == """{"ok":false,"error_code":404,"description":"Not Found"}""" or bot1 == "" or req.text == """{"ok":false,"error_code":401,"description":"Unauthorized"}""":
        err = "Вы неправильно ввели токен бота! Введите токен telegram бота: "
        log(err)
        return '', err
    else:
        print('ok')
        time.sleep(1)
        err = 'ok'
        return req, err


try:
    with open('text.txt', 'r') as f:
        try:
            l = [line.strip() for line in f]
            bot1 = l[0]
            token_work = l[1]
            f.close()
        except IndexError:
            print('Ошибка чтения файла!!!!')
            bot1 = input("Введите токен telegram бота: ")
            token_work = input("Введите токен Ytmonster: ")
except FileNotFoundError:
    log('text.txt err: FileNotFoundError')
    bot1 = input("Введите токен telegram бота: ")
    token_work = input("Введите токен Ytmonster: ")
    with open('text.txt', 'w') as f:
        f.write(bot1 + '\n')
        f.write(token_work + '\n')
        f.close()

print('Проверка данных!')
log('Проверка данных!')
req, err = ytmonster('balance')
while err != 'ok':
    if err == 'ok':
        print('Все хорошо!')
    else:
        print(err)
        token_work = input('Введите токен Yt monster:')
        req, err = ytmonster('balance')


req, err = telegram()
while err != 'ok':
    if err == 'ok':
        print('Все хорошо!')
    else:
        print(err)
        bot1 = input('Введите токен Telegram бота:')
        req, err = telegram()


with open('text.txt', 'w') as f:
    f.write(bot1 + '\n')
    f.write(token_work + '\n')
    f.close()
log('ok')
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
    change = types.InlineKeyboardButton(text='Поменять токен от ytmonster', callback_data='change')
    keyboard.add(change)
    clear_log = types.InlineKeyboardButton(text='Очистить фаел логов', callback_data='clear_log')
    keyboard.add(clear_log)
    close_client = types.InlineKeyboardButton(text='Закрыть клиент', callback_data='close_client')
    keyboard.add(close_client)
    bot.send_message(message.from_user.id, text="Привет! Выбери кнопку:", reply_markup=keyboard)



def keyboard_start(call): #повторение кнопочек
    keyboard = types.InlineKeyboardMarkup()
    work = types.InlineKeyboardButton(text='Проверка баланса', callback_data='balance')
    keyboard.add(work)
    version = types.InlineKeyboardButton(text='Версия', callback_data='version')
    keyboard.add(version)
    get_client = types.InlineKeyboardButton(text='Получить список рабочих клиентов', callback_data='get_client')
    keyboard.add(get_client)
    change = types.InlineKeyboardButton(text='Поменять токен от ytmonster', callback_data='change')
    keyboard.add(change)
    clear_log = types.InlineKeyboardButton(text='Очистить фаел логов', callback_data='clear_log')
    keyboard.add(clear_log)
    close_client = types.InlineKeyboardButton(text='Закрыть клиент', callback_data='close_client')
    keyboard.add(close_client)
    bot.send_message(call.from_user.id, text="Привет! Выбери кнопку:", reply_markup=keyboard)
    print('Сообщение отправлено!')

def back_def(call, mes):
    keyboard = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton(text='Назад', callback_data='back')
    keyboard.add(back)
    bot.send_message(call.from_user.id, mes, reply_markup=keyboard)
    print('Сообщение отправлено!')

@bot.callback_query_handler(func=lambda call: True) #ответ на кнопки
def callback_worker(call):
    global bot1, token_work
    if call.data == "balance":
        req, err = ytmonster('balance')
        print(err, req.text)
        if err == 'ok':
            req = req.text
            req = req.replace('{"error":0,"response":{"status":"good","balance":', '')
            req = req.replace(',"money":0}}', '')
            mes = "Ваш баланс: " + req + " COIN"
            back_def(call, mes) # отправка сообщения и кнопки домой
            print('Сообщение отправлено!')
            time.sleep(5)
        else:
            bot.send_message(call.from_user.id, err)
            print('Сообщение отправлено!')

    elif call.data == "version":
        bot.send_message(call.message.chat.id, 'Версия бота: ' + str(2.1))
        print('Сообщение отправлено!')

    elif call.data == "get_client":
        bot.send_message(call.message.chat.id, 'Делаем запрос к yt_monster')
        req, err = ytmonster('get_client')
        bot.send_message(call.message.chat.id, 'Запрос выполнен! Ошибки: ' + err)
        if err != 'ok':
            back_def(call, err)
        if req.text == """{"error":0,"response":[]}""":
            print('Нет рабочих клиентов')
            back_def(call, 'Нет рабочих клиентов')
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
                http = (json1["response"][b]["info"]["http"])  # получение количества ошибок клиента
                id = (json1["response"][b]["id"])
                client_info = client_info + '\n---------------\nКлиент: ' + str(b + 1) + ' \nПросмотрел: ' + str(count) + ' видео' + '\nОшибок: ' + str(error) + '\nОсталось до конца просмотра: ' + str(sec) + ' секунд' +  '\nСылка: https://www.youtube.com/watch?v=' + http + '\nid: ' + id
                b += 1
                bot.send_message(call.message.chat.id, 'Обработано клиентов: ' + str(b))
            print(client_info)
            client_info += '\n\n\nДля закрытия клиента пропиши команду: /close_client айди клиента \n Пример: /close_client fea9f5'
            time.sleep(1)
            back_def(call, client_info)
    elif call.data == "back":
        keyboard_start(call)
    elif call.data == 'change':
        back_def(call, 'Для смены токена от ytmonster пропишите команду: /newtokenytmonster и токен \n Пример: 0000539765mUVlCZpDDNBLGHKtJnrIDa ')
    elif call.data == 'clear_log':
        with open('log.txt', 'w') as f:
            f.write('\nclear log: ' + str(datetime.now()))
            f.close()
            back_def(call,'Лог очищен')
    elif call.data == 'close_client':
        back_def(call, 'Для закрытия клиента используйте команду: /close_client айди клиента \n Пример: /close_client fea9f8')


@bot.message_handler(commands=["close_client"])
def newtokenytmonster(message):
    global id
    mess = message.text.replace('close_client', '')
    time.sleep(0.1)
    id = mess.strip()
    time.sleep(0.1)
    bot.send_message(message.from_user.id, 'Делаем запрос к yt_monster')
    req, err = ytmonster('close_client')
    json1 = json.loads(req.text)
    json1 = (json1["error"])
    if err != 'ok':
        bot.send_message(message.from_user.id, err)
        log(err)
    elif json1 != 0:
        bot.send_message(message.from_user.id, 'ОШИБКА: ' + str(json1) + ' Возможно вы указали не верный id клиента?')
        log('ОШИБКА: ' + str(json1) + ' Возможно вы указали не верный id клиента?')
    else:
        bot.send_message(message.from_user.id, 'Окно закроется в течении 1-5 минут')





@bot.message_handler(commands=["newtokenytmonster"])
def newtokenytmonster(message):
    global token_work
    mess = message.text.replace('newtokenytmonster', '')
    time.sleep(0.1)
    mess = mess.strip()
    time.sleep(0.1)
    a = token_work
    time.sleep(0.1)
    token_work = mess
    time.sleep(0.1)
    log('Попытка смены токена yt monster')
    bot.send_message(message.from_user.id, text='ping Ytmonster')
    req, err = ytmonster('balance')
    if err != 'ok':
        bot.send_message(message.from_user.id, text= err)
        token_work = a
        log('Проблема со сменой токена ytmonster: ' + err)
    else:
        print('Ok')
        time.sleep(1)
        bot.send_message(message.from_user.id, text='ok, секунду...')
        with open('text.txt', 'w') as f:
            f.write(bot1 + '\n')
            f.write(token_work + '\n')
            f.close()
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(back)
        bot.send_message(message.from_user.id, text='Все верно!Токен от yt_monster поменялся', reply_markup=keyboard)
        log('Смена токена yt monster ')
        print('Сообщение отправлено!')
bot.infinity_polling(none_stop=True, interval=0)