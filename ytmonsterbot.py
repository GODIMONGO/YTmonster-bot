import telebot
from telebot import types
import requests
import json
import time
from datetime import datetime
import speedtest

text =  ""
bot1 = ""
token_work = ""
token_task = ""
id = ''
Versoin = '2.3.1 Beta'

with open('log.txt', 'a') as f:
    f.write('\nbot start: ' + str(datetime.now()))
    f.close()

def log(text):
    with open('log.txt', 'a') as f:
        f.write('\n' + str(datetime.now()) + '  ' + text )
        f.close()


print("Для получения токена Yt_monster используйте: https://ytmonster.ru/api/#key \nДля получения токена Telegram бота используйте: https://t.me/BotFather\nTelegram канал разработчика: https://t.me/GODIMONGO\nВерсия:" + Versoin)
# проверка токена ytmonster, принимает условия
time.sleep(5)
def ytmonster(task):
    global token_task, token_work, id
    print('ping: ytmonster.ru ...')
    try:
        if task == 'balance':
            req = requests.get('https://app.ytmonster.ru/api/?balance=get&token=' + token_work)
            json1 = json.loads(req.text)
            error = (json1["error"])
            print(error)
        elif task == 'get_client':
            req = requests.get('https://app.ytmonster.ru/api/?get-clients=get&token=' + token_work)
            json1 = json.loads(req.text)
            error = (json1["error"])
            print(error)
        elif task == 'close_client':
            req = requests.get('https://app.ytmonster.ru/api/?close-client=' + id + '&token=' + token_work)
            json1 = json.loads(req.text)
            error = (json1["error"])
            print(error)
        elif task == 'my_task':
            req = requests.get('https://app.ytmonster.ru/api/?my-tasks=ytview&offset=0&token=' + token_task)
            if req.text == """{"error":902,"error_response":"Неверный тип токена"}""": # почему то нормально не сделали и приходится обрабатывать так
                print("Неверный тип токена")
                err = ("err: 902 Неверный тип токена")
                log(err)
                return '', err
            else:
                json1 = json.loads(req.text)
                error = json1["error"]
                print(error)
        elif task == '':
            req = requests.get('https://app.ytmonster.ru/api/?get-task=[type]&id_account=[id_account]&token=' + token_task)

        else:
            err = 'Ошибка ping! Нет указания что делать'
            log(err)
            return '', err
        if error == 1002 or error == "" or error == 1001 or error == 1004:
            err = "ОШИБКА " + req.text + "Возможно вы ввели не верный токен!"
            time.sleep(1)
            log(err)
            return '', err
        elif error == 1003:
            err = "ОШИБКА 1003!! Включите токен на сайте: https://ytmonster.ru/api/#key"
            time.sleep(1)
            log(err)
            return '', err
        elif error == 902:
            err = "ОШИБКА 902!! Вы ввели не верный тип токена."
            time.sleep(1)
            log(err)
            return '', err
        else:
            print('ok')
            err = 'ok'
            time.sleep(1)
            print(req)
            print(req.text)
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
        err = "Вы неправильно ввели токен бота!"
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
            token_task = l[2]
            f.close()
        except IndexError:
            print('Ошибка чтения файла!!!!')
            bot1 = input("Введите токен telegram бота: ")
            token_work = input("Введите токен Ytmonster (для выполнения заданий): ")
            token_task = input("Введите токен Ytmonster (для добавления заданий): ")
except FileNotFoundError:
    log('text.txt err: FileNotFoundError')
    bot1 = input("Введите токен telegram бота: ")
    token_work = input("Введите токен Ytmonster (для выполнения заданий): ")
    token_task = input("Введите токен Ytmonster (для добавления заданий): ")
    with open('text.txt', 'w') as f:
        f.write(bot1 + '\n')
        f.write(token_work + '\n')
        f.write(token_task + '\n')
        f.close()

print('Проверка данных!')
log('Проверка данных!')
req, err = ytmonster('get_client')
while err != 'ok':
    if err == 'ok':
        print('Все хорошо!')
    else:
        print(err)
        token_work = input("Введите токен Ytmonster (для выполнения заданий): ")
        req, err = ytmonster('get_client')

req, err = ytmonster('my_task')
while err != 'ok':
    if err == 'ok':
        print('Все хорошо!')
    else:
        print(err)
        token_task = input("Введите токен Ytmonster (для добавления заданий): ")
        req, err = ytmonster('my_task')

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
    f.write(token_task + '\n')
    f.close()
log('ok')
bot = telebot.TeleBot(bot1)
print('\n\n\n\n\n\nБот запущен!')
@bot.message_handler(commands=["start"])
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
    my_task = types.InlineKeyboardButton(text='Получить список заданий', callback_data='my_task')
    keyboard.add(my_task)
    send_log = types.InlineKeyboardButton(text='Отправить лог', callback_data='send_log')
    keyboard.add(send_log)
    speedtest = types.InlineKeyboardButton(text='Замерить скорость интернета', callback_data='speedtest')
    keyboard.add(speedtest)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEINtRkGK9SK6pHQrYy1aKnW-6ZcmlEjQAC8zAAAiP1yEgwajIpJJRmtS8E')
    bot.send_message(message.from_user.id, text="Привет! Выбери кнопку:", reply_markup=keyboard)



def keyboard_start(call):
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
    my_task = types.InlineKeyboardButton(text='Получить список заданий', callback_data='my_task')
    keyboard.add(my_task)
    send_log = types.InlineKeyboardButton(text='Отправить лог', callback_data='send_log')
    keyboard.add(send_log)
    speedtest = types.InlineKeyboardButton(text='Замерить скорость интернета', callback_data='speedtest')
    keyboard.add(speedtest)
    bot.send_sticker(call.from_user.id, 'CAACAgIAAxkBAAEINtRkGK9SK6pHQrYy1aKnW-6ZcmlEjQAC8zAAAiP1yEgwajIpJJRmtS8E')
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
    global bot1, token_work, Versoin, token_task
    if call.data == "balance":
        req, err = ytmonster('balance')
        print(err, req.text)
        if err == 'ok':
            req = req.text
            req = req.replace('{"error":0,"response":{"status":"good","balance":', '')
            req = req.replace(',"money":0}}', '')
            mes = "Ваш баланс: " + req + " COIN\nTelegram канал разработчика: https://t.me/GODIMONGO" 
            back_def(call, mes)
            print('Сообщение отправлено!')
            time.sleep(5)
        else:
            bot.send_message(call.from_user.id, err)
            print('Сообщение отправлено!')

    elif call.data == "version":
        bot.send_message(call.message.chat.id, 'Версия бота: ' + str(Versoin) + '\nTelegram канал разработчика: https://t.me/GODIMONGO')
        print('Сообщение отправлено!')

    elif call.data == "get_client":
        bot.send_message(call.message.chat.id, 'Делаем запрос к yt_monster')
        req, err = ytmonster('get_client')
        bot.send_message(call.message.chat.id, 'Запрос выполнен! Ошибки: ' + str(err))
        if err != 'ok':
            back_def(call, err)
        if req.text == """{"error":0,"response":[]}""":
            print('Нет рабочих клиентов')
            back_def(call, 'Нет рабочих клиентов\nTelegram канал разработчика: https://t.me/GODIMONGO')
        else:
            json1 = json.loads(req.text)
            i = len(json1['response'])
            b = 0  # количество просмотренной информации
            client_info = ""
            while i > b:  # количество просмотренных видео
                time.sleep(1)
                count = (json1["response"][b]["data"]["count"])
                sec = (json1["response"][b]["info"]["sec"])
                error = (json1["response"][b]["info"]["error"])
                http = (json1["response"][b]["info"]["http"])
                id = (json1["response"][b]["id"])
                client_info = client_info + '\n---------------\nКлиент: ' + str(b + 1) + ' \nПросмотрел: ' + str(count) + ' видео' + '\nОшибок: ' + str(error) + '\nОсталось до конца просмотра: ' + str(sec) + ' секунд' +  '\nСылка: https://www.youtube.com/watch?v=' + http + '\nid: ' + id
                b += 1
                bot.send_message(call.message.chat.id, 'Обработано клиентов: ' + str(b))
            print(client_info)
            client_info += '\n\n\nДля закрытия клиента пропиши команду: /close_client айди клиента \n Пример: /close_client fea9f5'
            time.sleep(1)
            back_def(call, client_info + '\nTelegram канал разработчика: https://t.me/GODIMONGO')
    elif call.data == "back":
        keyboard_start(call)
    elif call.data == 'change':
        back_def(call, 'Для смены токена от ytmonster Есть 2 команды: /newtokenytmonster_work (токен для выполнения заданий без скобок)- меняет токен для выполнения заданий\n /newtokenytmonster_task (токен для добавления заданий без скобок )- меняет токен для выполнения заданий')
    elif call.data == 'clear_log':
        with open('log.txt', 'w') as f:
            f.write('\nclear log: ' + str(datetime.now()))
            f.close()
            back_def(call,'Лог очищен')
    elif call.data == 'close_client':
        back_def(call, 'Для закрытия клиента используйте команду: /close_client айди клиента \n Пример: /close_client fea9f8')
    elif call.data == 'my_task':
        req, err = ytmonster('my_task')
        json1 = json.loads(req.text)
        i = len(json1['response'])
        b = 0
        mess = ''
        a = ''
        while i > b:
                time.sleep(1)
                id = (json1["response"][b]["id"])
                soc = (json1["response"][b]["soc"])
                url = (json1["response"][b]["url"])
                mess =  mess + '\n' + soc + '\n' + url + '\n' + id + '\n-----------'
                if b == 1:
                    a = ' задание'
                elif b == 2 or b == 3 or b == 2:
                    a = 'задания'
                else:
                    a = ' заданий'
                if b > 0:
                    bot.delete_message(call.message.chat.id, last_msg.message_id)
                last_msg = bot.send_message(call.message.chat.id, 'Бот прочитал:' + str(b) + a)
                b = b + 1
        print(mess)
        back_def(call, mess)
    elif call.data == 'send_log':
        bot.send_message(call.message.chat.id, 'Отправка лога')
        log=open('log.txt','rb')
        bot.send_document(call.message.chat.id, log)
        log.close()
    elif call.data == 'speedtest':
        bot.send_message(call.message.chat.id, 'Производится замер скорости интеренета! Результат появится в течении 1-3 минут!')
        time.sleep(1)
        st = speedtest.Speedtest()
        upload = str(int(st.upload())) 
        download = str(int(st.download()))
        upload = upload[:2]
        download = download[:2]
        mes = '-----------\nСкорсоть на загрузку:' + str(download) + 'Mbit/s\n-----------\nСкорсоть на выгрузку:' + str(upload) + 'Mbit/s'
        print(mes)
        bot.send_message(call.message.chat.id, mes)



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





@bot.message_handler(commands=["newtokenytmonster_work"])
def newtokenytmonster_work(message):
    global token_task, bot1, token_work
    mess = message.text.replace('/newtokenytmonster_work', '')
    time.sleep(0.1)
    mess = mess.strip()
    time.sleep(0.1)
    a = token_work
    time.sleep(0.1)
    token_work = mess
    time.sleep(0.1)
    log('Попытка смены токена yt monster (для выполнения заданий)')
    bot.send_message(message.from_user.id, text='ping Ytmonster')
    req, err = ytmonster('get_client')
    if err != 'ok':
        bot.send_message(message.from_user.id, text= err)
        token_work = a
        log('Проблема со сменой токена ytmonster (для выполнения заданий): ' + err)
    else:
        print('Ok')
        time.sleep(1)
        bot.send_message(message.from_user.id, text='ok, секунду...')
        with open('text.txt', 'w') as f:
            f.write(bot1 + '\n')
            f.write(token_work + '\n')
            f.write(token_task + '\n')
            f.close()
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(back)
        bot.send_message(message.from_user.id, text='Все верно!Токен от yt_monster (для выполнения заданий) поменялся', reply_markup=keyboard)
        log('Смена токена yt monster (для выполнения заданий) ')
        print('Сообщение отправлено!')



@bot.message_handler(commands=["newtokenytmonster_task"])
def newtokenytmonster_work(message):
    global token_task, bot1, token_work
    mess = message.text.replace('/newtokenytmonster_task', '')
    time.sleep(0.1)
    mess = mess.strip()
    time.sleep(0.1)
    a = token_task
    time.sleep(0.1)
    token_task = mess
    time.sleep(0.1)
    print(mess)
    time.sleep(0.1)
    log('Попытка смены токена yt monster (для добавления заданий)')
    bot.send_message(message.from_user.id, text='ping Ytmonster')
    req, err = ytmonster('my_task')
    if err != 'ok':
        bot.send_message(message.from_user.id, text= err)
        token_task = a
        log('Проблема со сменой токена ytmonster (для добавления заданий): ' + err)
    else:
        print('Ok')
        time.sleep(1)
        bot.send_message(message.from_user.id, text='ok, секунду...')
        with open('text.txt', 'w') as f:
            f.write(bot1 + '\n')
            f.write(token_work + '\n')
            f.write(token_task + '\n')
            f.close()
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(back)
        bot.send_message(message.from_user.id, text='Все верно!Токен от yt_monster (для добавления заданий) поменялся', reply_markup=keyboard)
        log('Смена токена yt monster (для добавления заданий) ')
        print('Сообщение отправлено!')




bot.infinity_polling(none_stop=True, interval=0)