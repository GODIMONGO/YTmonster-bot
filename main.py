import telebot
from telebot import types
import requests
import json
import time
bot = telebot.TeleBot("") #токен бота

token_work = "" # токен ют монстер для выполнения заданий

@bot.message_handler(commands=["start"]) #начальные кнопочки
def test(message):
      keyboard = types.InlineKeyboardMarkup()
      work = types.InlineKeyboardButton(text='Проверка баланса', callback_data='balance')
      keyboard.add(work)
      version = types.InlineKeyboardButton(text='Версия', callback_data='version')
      keyboard.add(version)
      get_client = types.InlineKeyboardButton(text='Получить список рабочих клиентов', callback_data='get_client')
      keyboard.add(get_client)
      bot.send_message(message.from_user.id, text="Привет! Выбери кнопку:", reply_markup=keyboard)



def repa(call): #повторение кнопочек
    keyboard = types.InlineKeyboardMarkup()
    work = types.InlineKeyboardButton(text='Проверка баланса', callback_data='balance')
    keyboard.add(work)
    version = types.InlineKeyboardButton(text='Версия', callback_data='version')
    keyboard.add(version)
    get_client = types.InlineKeyboardButton(text='Получить список рабочих клиентов', callback_data='get_client')
    keyboard.add(get_client)
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
        print(req.text)
        if req.text == """{"error":1002}""":
            bot.send_message(call.from_user.id, "Вы забыли указать Токен от yt_monster для выполнения задания")
            print('Ошибка 1002! Укажите данные в переменную: token_work')
        elif req.text =="""{"error":1003}""":
            bot.send_message(call.from_user.id, "Включите токен на сайте: https://ytmonster.ru/api/#key")
            print("Включите токен на сайте: https://ytmonster.ru/api/#key")
        else:
            if req.text == """{"error":0,"response":[]}""":
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



bot.infinity_polling(none_stop=True, interval=0)