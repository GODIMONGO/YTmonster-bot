import yt_monster_py as yt_monster
import requests
import time
import telebot
from telebot import types
import os
import sys
from datetime import datetime
import statistics
import ping3
import speedtest
mes = None
values = {}
task_tg = None
tokens = ['', '', '']
Versoin = '3.4'
Change_log = '\n1. Добавлено закрытие клиентов' \
             '\n2. Переделаны кнопки' \
             '\n3. Исправлены некоторые синтаксические ошибки' \
             '\n4. Добавлена команда: /restart (перезагружает код соответственно все переменные очищяются)' \
             '\n5. Исправил пинг (теперь пингуются реальные сервера из списка в самом коде)' \
             '\n6. Изменена информация о пинге' \
             '\n7. Добавили смену токена телеграм бота во время работы (очень удобно если бот стоит на сервер)' \
             '\n8. Добавили ответ если вы написали что то боту а он не знает что это' \
             '\n9. Убрал спам (бот теперь просто редактирует сообщение)' \
             '\n10. Теперь можно открепить закрепленное сообщение с помощью команды /unpin'



print("Для получения токена Yt_monster используйте: https://ytmonster.ru/api/#key или https://clifl.com/api/#key "
      "\nДля получения токена Telegram бота используйте: https://t.me/BotFather\nTelegram канал разработчика: https://t.me/GODIMONGO"
      "\nВерсия:" + Versoin + '\n' + Change_log + '\n'*2)
time.sleep(2)
yt_monster.log('Старт бота')




try:
    with open('token.txt', 'r') as f:
        tokens = [line.strip() for line in f]
except FileNotFoundError:
    print('token.txt err: FileNotFoundError')
for i, token_name in enumerate(['telegram бота', 'Ytmonster (для выполнения заданий)', 'Ytmonster (для добавления заданий)']):
    if not tokens[i]:
        tokens[i] = input(f'Введите токен {token_name}: ')
with open('token.txt', 'w') as f:
    f.write('\n'.join(tokens))


print('Проверка токена для (для выполнения заданий)')
while True:
    req, err = yt_monster.ytmonster_req(tokens[1:], 'balance')
    if err == 'ok':
        break
    print(err)
    tokens[1] = input('Введите токен Ytmonster (для выполнения заданий): ')
    with open('token.txt', 'w') as f:
        f.write('\n'.join(tokens))


print('Проверка токена для (для добавления заданий)')
while True:
    req, err = yt_monster.ytmonster_req(tokens[1:], 'my_task', 'ytview')
    if err == 'ok':
        break
    tokens[2] = input('Введите токен Ytmonster (для добавления заданий): ')
    with open('token.txt', 'w') as f:
        f.write('\n'.join(tokens))


print('Проверка токена для Telegram бота')
print('ping: api.telegram.org ...')
time.sleep(1)
while True:
    req = requests.get(f'https://api.telegram.org/bot{tokens[0]}/getMe')
    if req.status_code == 200:
        break
    print("Вы неправильно ввели токен бота!\nВведите токен telegram бота:")
    tokens[0] = input('')
    with open('token.txt', 'w') as f:
        f.write('\n'.join(tokens))

yt_monster.log('Все токены проверены и верны')
token_ytmonster = [tokens[1], tokens[2]]


def button_start():
    keyboard = types.InlineKeyboardMarkup()

    # Первая строка кнопок
    balance = types.InlineKeyboardButton(text='💰 Баланс', callback_data='balance')
    version = types.InlineKeyboardButton(text='🌟 Версия', callback_data='version')
    keyboard.row(balance, version)

    # Вторая строка кнопок
    get_client = types.InlineKeyboardButton(text='📋 Список клиентов', callback_data='get_client')
    change = types.InlineKeyboardButton(text='🔄 Токен (скоро)', callback_data='change')
    keyboard.row(get_client, change)

    # Четвертая строка кнопок
    my_task = types.InlineKeyboardButton(text='📝 Задания', callback_data='my_task')
    send_log = types.InlineKeyboardButton(text='📤 Отправить лог', callback_data='send_log')
    keyboard.row(my_task, send_log)

    # Пятая строка кнопок
    speedtest = types.InlineKeyboardButton(text='🌐 Скорость', callback_data='speedtest')
    ping = types.InlineKeyboardButton(text='🏓 Пинг', callback_data='ping')
    keyboard.row(speedtest, ping)

    change_token = types.InlineKeyboardButton(text='🔑 Изменить токен бота', callback_data='change_token_telegram')
    add_task = types.InlineKeyboardButton(text='➕ Добавить задание', callback_data='add_task')
    keyboard.row(add_task, change_token)

    clear_log = types.InlineKeyboardButton(text='🗑 Очистить лог', callback_data='clear_log')
    keyboard.row(clear_log)

    return keyboard


bot = telebot.TeleBot(str(tokens[0]))
print('\n'* 100)
print('Бот запущен!')
yt_monster.log('Бот запущен!')



@bot.message_handler(commands=["help"])
def help_command(message):
    text = "Доступные команды:\n/start (старт)\n/unpin (открепить закрепленное сообщение)\nНемного о боте: Бот создан для упрощения работы с сайтом ytmonster.ru (clifl.com) А так же для работы с библиотекой!"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    message_text = 'Пока тут пусто'
    # проверяем, есть ли уже закрепленное сообщение с таким текстом
    pinned_message = bot.get_chat(chat_id).pinned_message
    if pinned_message is None or pinned_message.text != message_text:
        # если нет, то отправляем и закрепляем сообщение
        sent_message = bot.send_message(chat_id, message_text)
        bot.pin_chat_message(chat_id, sent_message.message_id)
    time.sleep(0.1)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEINtRkGK9SK6pHQrYy1aKnW-6ZcmlEjQAC8zAAAiP1yEgwajIpJJRmtS8E')
    keyboard_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("/restart (для перезагрузки бота)")
    button2 = types.KeyboardButton("/unpin (для открепления сообщения)")
    button3 = types.KeyboardButton("/start (для получения главного меню)")
    keyboard_reply.add(button1, button2)
    keyboard_reply.add(button3)
    bot.send_message(message.chat.id, "Сообщение для обновления клавиатуры", reply_markup=keyboard_reply)
    bot.send_message(message.from_user.id, text="Привет! Выбери кнопку:", reply_markup=button_start())


@bot.message_handler(commands=['restart'])
def restart_command(message):
    bot.send_message(message.chat.id, "Перезагрузка...")
    # добавьте здесь код, который выполняется при перезагрузке
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.message_handler(commands=["unpin"])
def unpin_command(message):
    bot.unpin_chat_message(message.chat.id)
    bot.send_message(message.chat.id, 'сообщение откреплено')



@bot.callback_query_handler(func=lambda call: True) #ответ на кнопки
def callback_worker(call):
    global token_ytmonster, task_tg, mes, values
    keyboard_back = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton(text='Назад', callback_data='back')
    keyboard_back.add(back)


    if call.data == "back":
        bot.send_message(call.from_user.id, text="Telegram канал разработчика: https://t.me/GODIMONGO\nПривет! Выбери кнопку:", reply_markup=button_start())
        bot.answer_callback_query(call.id)
        mes = None
        values = {}
        task_tg = None
        print('Сообщение отправлено!')

    elif call.data == "balance":
        req, err = yt_monster.ytmonster_req(token_ytmonster, 'balance')
        if err != 'ok':
            bot.send_message(call.from_user.id, text='Произошла ошибка:' + err, reply_markup=keyboard_back)
            yt_monster.log('Произошла ошибка:' + err)
            print('Сообщение отправлено!')
        bot.send_message(call.from_user.id, text='Баланс: ' + str(req) + ' COIN', reply_markup=keyboard_back)
        bot.answer_callback_query(call.id)
        print('Сообщение отправлено!')

    elif call.data == "version":
        bot.send_message(call.from_user.id, text=str('Версия бота: ' + str(Versoin) + '\nTelegram канал разработчика: https://t.me/GODIMONGO' + '\n' + Change_log), reply_markup=keyboard_back)
        bot.answer_callback_query(call.id)
        print('Сообщение отправлено!')

    elif call.data == "get_client":
        bot.send_message(call.from_user.id,
                         'Эта задача займет некоторое время \nTelegram канал разработчика: https://t.me/GODIMONGO')
        req, err, ID_CLIENT = yt_monster.ytmonster_req(token_ytmonster, 'get_client')
        if err != 'ok':
            bot.send_message(call.from_user.id, text='Произашла ошибка:' + str(err), reply_markup=keyboard_back)
        else:
            keyboard_client = types.InlineKeyboardMarkup(row_width=1)
            for client_id in ID_CLIENT:
                button = types.InlineKeyboardButton(text='Закрыть клиент:' + str(client_id), callback_data='client_id_close' + str(client_id))
                keyboard_client.add(button)
            keyboard_client.add(back)
            bot.send_message(call.from_user.id, text=str(req) + '\n----\n Вы можете закрыть клиент с помощью кнопки ниже:', reply_markup=keyboard_client)
        bot.answer_callback_query(call.id)
        print('Сообщение отправлено!')

    elif "client_id_close" in call.data:
        client_id = call.data.replace("client_id_close", "")
        req, err = yt_monster.ytmonster_req(token_ytmonster, 'close_client', id=client_id)
        if err != 'ok':
            bot.send_message(call.from_user.id, text='Произашла ошибка:' + str(err), reply_markup=keyboard_back)
        else:
            bot.send_message(call.from_user.id, text=str(req), reply_markup=keyboard_back)
        bot.answer_callback_query(call.id)
        print('Сообщение отправлено!')

    elif call.data == "my_task":
        keyboard = types.InlineKeyboardMarkup()
        social_networks = [
            {'text': 'Вконтакте', 'callback_data': 'vk'},
            {'text': 'Instagram', 'callback_data': 'inst'},
            {'text': 'TikTok', 'callback_data': 'tiktok'},
            {'text': 'Платные задания', 'callback_data': 'paid'},
            {'text': 'Youtube просмотры', 'callback_data': 'ytview'},
            {'text': 'Youtube лайки', 'callback_data': 'ytlike'},
            {'text': 'Youtube подписчики', 'callback_data': 'ytsubs'},
            {'text': 'Youtube комментарии', 'callback_data': 'ytcomm'},
            {'text': 'Telegram', 'callback_data': 'tg'},
            {'text': 'Назад', 'callback_data': 'back'}
        ]
        for social_network in social_networks:
            keyboard.add(types.InlineKeyboardButton(**social_network))
        bot.send_message(call.from_user.id, text="Выберите соц. сеть по которой хотели бы получить информацию",
                         reply_markup=keyboard)
        bot.answer_callback_query(call.id)
        print('Сообщение отправлено!')

    elif call.data in ['vk', 'inst', 'tiktok', 'tg', 'paid', 'ytview', 'ytlike', 'ytsubs', 'ytcomm']:
        req, err = yt_monster.ytmonster_req(token_ytmonster, 'my_task', call.data)
        bot.send_message(call.from_user.id, text=req, reply_markup=keyboard_back)
        bot.answer_callback_query(call.id)
        print('Сообщение отправлено!')

    elif call.data == 'send_log':
        bot.send_message(call.message.chat.id, 'Отправка лога')
        log=open('log.txt', 'rb')
        bot.send_document(call.message.chat.id, log)
        log.close()
        bot.answer_callback_query(call.id)


    elif call.data == 'clear_log':
        with open('log.txt', 'w') as f:
            f.write('\nclear log: ' + str(datetime.now()))
            f.close()
            bot.send_message(call.from_user.id, text='Лог очищен.', reply_markup=keyboard_back)
            bot.answer_callback_query(call.id)

    elif call.data == 'speedtest':
        bot.send_message(call.from_user.id, text='Замер скорости интернета займет время...')
        bot.answer_callback_query(call.id)
        st = speedtest.Speedtest()
        download_speeds = []
        upload_speeds = []
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(back)

        for i in range(5):
            download_speed = st.download() / 1000000  # скорость загрузки в Мбит/с
            upload_speed = st.upload() / 1000000  # скорость отгрузки в Мбит/с
            download_speeds.append(download_speed)
            upload_speeds.append(upload_speed)
            bot.send_message(call.from_user.id, text=f"Скорость загрузки {i + 1}: {download_speed:.2f} Мбит/с" + '\n' +f"Скорость отправки {i + 1}: {upload_speed:.2f} Мбит/с")
        avg_download_speed = sum(download_speeds) / len(download_speeds)
        avg_upload_speed = sum(upload_speeds) / len(upload_speeds)
        bot.send_message(call.from_user.id, text=f"Средняя скорость загрузки: {avg_download_speed:.2f} Мбит/с" + '\n' +f"Средняя скорость отправки: {avg_upload_speed:.2f} Мбит/с" , reply_markup=keyboard)


    elif call.data == 'ping':
        servers = [
            '8.8.8.8',
            '208.67.222.222',
            '168.95.1.1',
            '114.114.114.114',
            '203.0.178.191',
            '91.239.100.100',
            '176.103.130.130',
            '89.233.43.71',
            '77.88.8.8',
            '1.1.1.1',
            '9.9.9.9',
            '8.26.56.26',
            '185.228.168.168',
            '109.69.8.51',
            '80.80.80.80',
            '77.88.8.1',
            '1.0.0.1',
            '80.80.81.81',
            '156.154.70.1',
            '208.67.220.220',
            '8.8.4.4',
            '156.154.71.1',
            '9.9.9.10',
            '84.200.69.80',
            '84.200.70.40',
            '195.46.39.39',
            '195.46.39.40',
            '208.67.222.220',
            '77.88.8.88',
            '8.8.8.4'
        ]
        PING_EMOJI = "🏓"
        CHECKING_EMOJI = "🔎"
        UP_ARROW_EMOJI = "🔺"
        DOWN_ARROW_EMOJI = "🔻"
        MEDIAN_EMOJI = "🔘"
        response_times = []
        chat_id = call.message.chat.id
        bot.answer_callback_query(call.id)
        # send a new message to indicate that the bot is checking the servers
        a = bot.send_message(chat_id, f"{CHECKING_EMOJI} Проверка серверов...")
        message_id = a.message_id
        for server in servers:
            response_time = ping3.ping(server)
            if response_time is not None:
                response_time = round(response_time, 3)
                response_times.append(response_time)
                # edit the original message to show the ping time for each server
                bot.edit_message_text(f"{PING_EMOJI} Ping сервера: {server} занял: {response_time} сек", chat_id,
                                      message_id)
            else:
                # edit the original message to show that the server did not respond
                yt_monster.log(f"Сервер: {server} не дал ответа")
                bot.edit_message_text(f"{PING_EMOJI} Сервер: {server} не дал ответа", chat_id, message_id)

        if response_times:
            avg_response_time = statistics.mean(response_times)
            median_response_time = statistics.median(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
            # calculate the percentage change from the first to last server ping
            pct_change = round((response_times[-1] - response_times[0]) / response_times[0] * 100, 2)
            # determine whether the overall trend is up or down
            if response_times[0] < response_times[-1]:
                trend_emoji = UP_ARROW_EMOJI
            elif response_times[0] > response_times[-1]:
                trend_emoji = DOWN_ARROW_EMOJI
            else:
                trend_emoji = MEDIAN_EMOJI
            # edit the original message to show the ping statistics
            bot.edit_message_text(f"{PING_EMOJI} Среднее время ответа: {round(avg_response_time, 3)} сек\n"
                                  f"{PING_EMOJI} Медианное время ответа: {median_response_time} сек\n"
                                  f"{PING_EMOJI} Максимальное время ответа: {max_response_time} сек\n"
                                  f"{PING_EMOJI} Минимальное время ответа: {min_response_time} сек\n"
                                  f"{PING_EMOJI} Процентное изменение от первого к последнему серверу: {pct_change}% {trend_emoji}",
                                  chat_id, message_id, reply_markup=keyboard_back)
        else:
            # edit the original message to show that no server responded
            bot.edit_message_text("Не один сервер не дал ответа!", chat_id, message_id, reply_markup=keyboard_back)

    elif call.data == 'add_task':
        task_tg = 'add_task'
        bot.send_message(call.from_user.id, text='Введите тип задания!(Учитывая регистр) '
                                                 'Доступные типы:'
                                                 '\nСоздание заданий на реакции в телеграм:'
                                                 '\nlike_tg'
                                                 '\nПросмотры в телеграм:'
                                                 '\nview_tg', reply_markup=keyboard_back)
        bot.answer_callback_query(call.id)

    elif call.data == 'change_token_telegram':
        global old_tokens
        task_tg = 'change_token_telegram'
        with open('token.txt') as f:
            old_tokens = f.read().splitlines()
        # Сообщаем пользователю, что нужно ввести новый токен
        bot.send_message(call.from_user.id, text='Введите новый токен:', reply_markup=keyboard_back)
        bot.answer_callback_query(call.id)

    elif call.data == 'create_task':
        chat_id = call.from_user.id
        if task_tg == 'like_tg':
            req, err = yt_monster.yt_monster_create_task_tg(values[chat_id][0], values[chat_id][1],
                                                     token_ytmonster,
                                                     values[chat_id][2],
                                                     values[chat_id][3],
                                                     values[chat_id][4],
                                                     task_coin=values[chat_id][5])
        elif task_tg == 'view_tg':
            req, err = yt_monster.yt_monster_create_task_tg(values[chat_id][0], values[chat_id][1],
                                                     token_ytmonster,
                                                     task_count=values[chat_id][2],
                                                     task_valh=values[chat_id][3],
                                                     task_coin=100)
        values[chat_id] = []
        if err != 'ok':
            bot.send_message(call.from_user.id, text='Код ответа от сайта:   ' + err + '\nПоявилась ошибка:  ' + req, reply_markup=keyboard_back)
        else:
            bot.send_message(call.from_user.id, text='Ответ от сайта: ' + req + '  Задание успешно добавлено!', reply_markup=keyboard_back)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    global tokens,  values, mes, task_tg
    keyboard_back = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton(text='Назад', callback_data='back')
    keyboard_back.add(back)
    # Проверяем, верный ли токен

    if task_tg == 'change_token_telegram':
        try:
            bot_new = telebot.TeleBot(message.text)
            bot_new.get_me()
        except Exception as e:
            bot.send_message(message.from_user.id, text="Ошибка: " + str(e), reply_markup=keyboard_back)
            task_tg = ''
            return
        # Токен верный, меняем его и сохраняем в файле
        bot.token = message.text
        with open('token.txt', 'w') as f:
            f.write('\n'.join([message.text] + old_tokens[1:]))
        bot.send_message(message.from_user.id, text="Токен успешно изменен")
        task_tg = ''
        time.sleep(2)
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEINtRkGK9SK6pHQrYy1aKnW-6ZcmlEjQAC8zAAAiP1yEgwajIpJJRmtS8E')
        bot.send_message(message.from_user.id, text="Привет! Выбери кнопку:", reply_markup=button_start())

    elif task_tg == 'add_task':
        chat_id = message.chat.id
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(back)
        if mes == None:
            mes = message.text
        if mes == 'like_tg':
            if chat_id not in values:
                values[chat_id] = []
            count = len(values[chat_id])
            if count < 5:
                values[chat_id].append(message.text)
                if count == 0:
                    bot.send_message(chat_id, 'Введите ссылку на пост (Пример: https://t.me/channel_name/post_id): ')
                elif count == 1:
                    bot.send_message(chat_id,
                                     'Введите реакции и их проценты через enter в таком формате:\nрекция: процент на реакцию\n👏: 25\n😁: 25\n🤯: 25\n(Всего должно быть 100%)')
                elif count == 2:
                    bot.send_message(chat_id, 'Введите количество выполнений на задание.')
                elif count == 3:
                    bot.send_message(chat_id, 'Введите количество выполнений в час.')
                elif count == 4:
                    bot.send_message(chat_id, 'Введите цену в COIN за 1 выполнение.')
            elif count == 5:
                values[chat_id].append(message.text)
                reactions = {}
                try:
                    for line in values[chat_id][2].split('\n'):
                        reaction, percentage = line.split(':')
                        reactions[reaction.strip()] = int(percentage.strip())
                    values[chat_id][2] = reactions
                except ValueError:
                    bot.send_message(chat_id,
                                     'Произошла ошибка: ValueError. Проверьте формат ввода реакций и их процентов и повторите попытку.')
                    values[chat_id] = []
                    task_tg = 'add_task'
                    return
                task = types.InlineKeyboardButton(text='Да', callback_data='create_task', reply_markup=keyboard)
                keyboard.add(task)
                result = '\nТип: ' + values[chat_id][0] + '\nСсылка: ' + values[chat_id][1] + '\nРеакции: ' + str(
                    values[chat_id][2]) + '\nКоличество выполнений на задание: ' + values[chat_id][
                             3] + '\nКоличество выполнений в час: ' + values[chat_id][
                             4] + '\nЦена за 1 выполнение задания: ' + values[chat_id][5] + '\nВсе верно?'
                task_tg = ''
                bot.send_message(chat_id, result, reply_markup=keyboard)

        elif mes == 'view_tg':
            chat_id = message.chat.id
            if chat_id not in values:
                values[chat_id] = []
            count = len(values[chat_id])
            if count < 3:
                values[chat_id].append(message.text)
                if count == 0:
                    bot.send_message(chat_id, 'Введите ссылку на пост (Пример: https://t.me/channel_name/post_id): ')
                elif count == 1:
                    bot.send_message(chat_id, 'Введите количество выполнений на задание.')
                elif count == 2:
                    bot.send_message(chat_id, 'Введите количество выполнений в час.')
            elif count == 3:
                values[chat_id].append(message.text)
                task = types.InlineKeyboardButton(text='Да', callback_data='create_task')
                keyboard.add(task)
                result = '\nТип: ' + values[chat_id][0] + '\nСсылка: ' + values[chat_id][
                    1] + '\nКоличество выполнений на задание: ' + values[chat_id][
                             2] + '\nКоличетсво выполнений в час: ' + values[chat_id][
                             3] + '\nЦена за 1 выполнение задание: 100 COIN (фиксированно)' + '\nВсе верно?'
                task_tg = 'view_tg'
                bot.send_message(chat_id, result, reply_markup=keyboard)

        else:
            bot.send_message(chat_id,'Такого типа на данный момент не существует!\nВведите тип задания! Доступные типы:  like', reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Гл. меню', callback_data='back')
        keyboard.add(back)
        bot.send_message(message.from_user.id, text='Я вас не понял. Вы всегда можете вернуться в главное меню!', reply_markup=keyboard)


bot.infinity_polling(none_stop=True, interval=0)
