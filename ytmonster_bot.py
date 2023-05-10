import time
import yt_monster_py as yt_monster

def read_file(filename, line_number, task, new_value=None):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if len(lines) == 0:
                if task == 'read':
                    return '', 'The file is empty'
                elif task == 'delete':
                    return '', 'The file is empty'
                elif task == 'replace':
                    lines.append('\n')
            elif line_number < 1 or line_number > len(lines):
                if task == 'replace' and line_number == len(lines) + 1:
                    lines.append('\n' * (line_number - len(lines) - 1))
                else:
                    raise ValueError(f'Line number {line_number} is out of range')
            if task == 'read':
                return lines[line_number-1].strip(), ''
            elif task == 'delete':
                del lines[line_number-1]
                with open(filename, 'w') as file:
                    file.writelines(lines)
                return '', f'Deleted line {line_number}: {lines[line_number-1]}'
            elif task == 'replace':
                if new_value is None:
                    raise ValueError('New value is not specified')
                if line_number == len(lines) + 1:
                    lines.append('\n' * (line_number - len(lines) - 1))
                lines[line_number-1] = new_value + '\n'
                with open(filename, 'w') as file:
                    file.writelines(lines)
                return '', f'Replaced line {line_number}: {new_value}'

    except FileNotFoundError:
        with open(filename, 'w') as file:
            file.write('')
            return '', 'File not found, created empty file'
    except ValueError as e:
        return '', f'Error: {str(e)}'

print('Версия программы запуска: 1.1 Beta Версия используемой библиотеки: ' + str(yt_monster.Version()) + ' Чендж лог: ' +
      '\nДобавлена поддержка разных версий')
time.sleep(1)


print('Внимание! Поддержка версий кроме Standart пока не осуществляется!')
while True:

    value, error = read_file('config.txt', 2, 'read')
    if error:
        print(error)
        print(f'Возникла ошибка в config.txt')
        new_value = input('Введите цифру какую версию бота вы хотите запустить? Версии: 1. Standart 2. Lite 3. Pro\nВведите именно цифру без доп значений: ')
        try:
            _, message = read_file('config.txt', 2, 'replace', new_value=new_value)
            print(message)
        except ValueError as e:
            print(str(e))
            print(f'Возникла ошибка в config.txt')
            new_value = input('Введите цифру какую версию бота вы хотите запустить? Версии: 1. Standart 2. Lite 3. Pro\n Введите именно цифру без доп значений: ')
            _, message = read_file('config.txt', 2, 'replace', new_value=new_value)
            print(message)
    elif value == '1':

        import random
        import requests
        import telebot
        from telebot import types
        import os
        import sys
        from datetime import datetime
        import statistics
        import ping3
        import speedtest
        import threading
        import json


        print('\n\n\nЗапуск бота версии Standart\n\n\n')
        time.sleep(1)

        state = None
        mes = None
        values = {}
        task_tg = None
        tokens = ['', '', '']
        Versoin = '3.9'
        Change_log = '\n1. Исправлены ошибки.' \
                     '\n2. Обновление 3.9 добавлена поддержка программы запуска 1.1'
        id_tg = ''
        text_tg_bot = None

        print("Для получения токена Yt_monster используйте: https://ytmonster.ru/api/#key или https://clifl.com/api/#key "
              "\nДля получения токена Telegram бота используйте: https://t.me/BotFather\nTelegram канал разработчика: https://t.me/GODIMONGO"
              "\nВерсия:" + Versoin + '\n' + Change_log + '\n' * 2)
        time.sleep(2)
        yt_monster.log('Старт бота')


        def balase_task(token):
            token_work = token[0]
            token_task = token[1]
            while True:
                try:
                    # Отправляем запрос на получение баланса
                    req = requests.get('https://app.ytmonster.ru/api/?balance=get&token=' + token_work)
                    json1 = json.loads(req.text)

                    # Обработка ошибок и запись баланса в файл
                    a, err = yt_monster.ytmonster_error(json1["error"])
                    if err == 'ok':
                        with open('balance.txt', 'a') as f:
                            f.write(f'{json1["response"]["balance"]}\n')
                    else:
                        time.sleep(10)
                        yt_monster.log('Возникла ошибка в цикле! Получения баланса')

                    # Ждем 24 часа
                    time.sleep(24 * 60 * 60)
                except requests.exceptions.RequestException:
                    time.sleep(10)
                    yt_monster.log('Возникла ошибка в цикле! Получения баланса')


        def client_task(token):
            token_work = token[0]
            status = True
            while True:
                try:
                    req = requests.get('https://app.ytmonster.ru/api/?get-clients=get&token=' + token_work)
                    json1 = json.loads(req.text)
                    a, err = yt_monster.ytmonster_error(json1["error"])
                    if err != 'ok':
                        yt_monster.log('Возникла ошибка в цикле! Получения клиента')
                    elif req.text == """{"error":0,"response":[]}""":
                        if status == True:
                            status = False
                            bot.send_message(id_tg, 'Похоже что все рабочие клиенты закрыты!')
                    else:
                        status = True
                    time.sleep(10)
                except requests.exceptions.RequestException:
                    yt_monster.log('Возникла ошибка в цикле! Получения клиента')


        TOKEN_NAMES = ['telegram бота', 'Ytmonster (для выполнения заданий)', 'Ytmonster (для добавления заданий)']


        def read_tokens():
            try:
                with open('token.txt', 'r') as f:
                    tokens = [line.strip() for line in f]
            except FileNotFoundError:
                print('token.txt err: FileNotFoundError')
                tokens = []
            return tokens


        def write_tokens(tokens):
            with open('token.txt', 'w') as f:
                f.write('\n'.join(tokens))


        def get_token(tokens, index, name):
            try:
                if not tokens[index]:
                    tokens[index] = input(f'Введите токен {name}: ')
            except IndexError:
                tokens.append(input(f'Введите токен {name}: '))


        def check_ytmonster_token(tokens, index):
            while True:
                req, err = yt_monster.ytmonster_req(tokens[1:], 'balance' if index == 1 else 'my_task',
                                                    'ytview' if index == 2 else '')
                if err == 'ok':
                    break
                tokens[index] = input(
                    f'Введите токен Ytmonster ({"для выполнения заданий" if index == 1 else "для добавления заданий"}): ')
                write_tokens(tokens)


        def check_telegram_bot_token(tokens):
            print('Проверка токена для Telegram бота')
            print('ping: api.telegram.org ...')
            time.sleep(1)
            while True:
                req = requests.get(f'https://api.telegram.org/bot{tokens[0]}/getMe')
                if req.status_code == 200:
                    break
                print("Вы неправильно ввели токен бота!\nВведите токен telegram бота:")
                tokens[0] = input('')
                write_tokens(tokens)


        tokens = read_tokens()

        for i, token_name in enumerate(TOKEN_NAMES):
            get_token(tokens, i, token_name)

        write_tokens(tokens)

        check_ytmonster_token(tokens, 1)
        check_ytmonster_token(tokens, 2)

        check_telegram_bot_token(tokens)

        yt_monster.log('Все токены проверены и верны')


        token_ytmonster = [tokens[1], tokens[2]]
        balase_task_thread = threading.Thread(target=balase_task, args=(token_ytmonster,))
        balase_task_thread.start()

        client_task_thread = threading.Thread(target=client_task, args=(token_ytmonster,))
        client_task_thread.start()


        def button_start():
            keyboard = types.InlineKeyboardMarkup()

            # Первая строка кнопок
            balance = types.InlineKeyboardButton(text='💰 Баланс', callback_data='balance')
            version = types.InlineKeyboardButton(text='🌟 Версия', callback_data='version')
            keyboard.row(balance, version)

            # Вторая строка кнопок
            get_client = types.InlineKeyboardButton(text='📋 Список клиентов', callback_data='get_client')
            keyboard.row(get_client)

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
            add_id = types.InlineKeyboardButton(text='Ввести код подтверждения.', callback_data='ID_Telegram')
            keyboard.row(clear_log, add_id)
            change = types.InlineKeyboardButton(text='🔄 Изменить токен ytmonster', callback_data='change_token_ytmonster')
            keyboard.row(change)
            return keyboard


        try:
            id_tg, error = read_file('config.txt', 1, 'read')
            if error:
                raise FileNotFoundError(f'config.txt is missing or empty')
            id_tg = id_tg.replace(' ', '')
            if id_tg == '':
                text_tg_bot = str(random.randint(1000, 9999))
                print('\n\n\nКажется, мы не знаем ваш ID в Telegram! '
                      '\nВам требуется ввести 4-значный код (без пробелов и других символов) '
                      f'\nдля телеграм-бота после его запуска: {text_tg_bot}. '
                      '\nВведите любое значение и нажмите Enter для продолжения!')
                input('')
            else:
                id_tg = int(id_tg)
        except (FileNotFoundError, ValueError):
            text_tg_bot = str(random.randint(1000, 9999))
            print('\n\n\nКажется, мы не знаем ваш ID в Telegram! '
                  '\nВам требуется ввести 4-значный код (без пробелов и других символов) '
                  f'\nдля телеграм-бота после его запуска: {text_tg_bot}. '
                  '\nВведите любое значение и нажмите Enter для продолжения!')
            input('')


        bot = telebot.TeleBot(str(tokens[0]))
        print('\n' * 4)
        if id_tg != '':
            bot.send_message(id_tg, 'Бот запущен! Вы можете ввести команду для получения главного меню: /start')
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


        @bot.callback_query_handler(func=lambda call: True)  # ответ на кнопки
        def callback_worker(call):
            global token_ytmonster, task_tg, mes, values
            keyboard_back = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton(text='Назад', callback_data='back')
            keyboard_back.add(back)

            if call.data == "back":
                bot.send_message(call.from_user.id,
                                 text="Telegram канал разработчика: https://t.me/GODIMONGO\nПривет! Выбери кнопку:",
                                 reply_markup=button_start())
                bot.answer_callback_query(call.id)
                mes = None
                values = {}
                task_tg = None
                print('Сообщение отправлено!')

            elif call.data == "balance":
                with open('balance.txt', 'r') as f:
                    balance = f.readlines()
                if len(balance) == 0:
                    bot.send_message(call.from_user.id, text='Статистика баланса не готова.', reply_markup=keyboard_back)
                    yt_monster.log('Статистика баланса не готова.')
                else:
                    last_ten_days = balance[-10:]
                    stats = ''
                    for i in range(len(last_ten_days)):
                        stats += f'{i + 1} день: {last_ten_days[i]}'

                    start_balance = float(last_ten_days[0].strip())
                    end_balance = float(last_ten_days[-1].strip())
                    balance_change = end_balance - start_balance
                    balance_percent = (balance_change / start_balance) * 100

                    req, err = yt_monster.ytmonster_req(token_ytmonster, 'balance')
                    if err != 'ok':
                        bot.send_message(call.from_user.id, text='Произошла ошибка:' + err, reply_markup=keyboard_back)
                        yt_monster.log('Произошла ошибка:' + err)
                        print('Сообщение отправлено!')
                    else:
                        bot.send_message(call.from_user.id, text=f'💰 Баланс на данный момент: {req} COIN\n\n'
                                                                 f'📊 Статистика баланса за последние {len(last_ten_days)} дней:\n\n'
                                                                 f'{stats}\n\n'
                                                                 f'📈 Изменение баланса за последние {len(last_ten_days)} дней: {balance_change:.2f} COIN ({balance_percent:.2f}%)\n',
                                         reply_markup=keyboard_back)
                        bot.answer_callback_query(call.id)
                        print('Сообщение отправлено!')



            elif call.data == "version":
                bot.send_message(call.from_user.id, text=str('Версия бота: ' + str(
                    Versoin) + '\nTelegram канал разработчика: https://t.me/GODIMONGO' + '\n' + Change_log),
                                 reply_markup=keyboard_back)
                bot.answer_callback_query(call.id)
                print('Сообщение отправлено!')

            elif call.data == "get_client":
                bot.send_message(call.from_user.id,
                                 'Эта задача займет некоторое время \nTelegram канал разработчика: https://t.me/GODIMONGO')
                req, err, ID_CLIENT = yt_monster.ytmonster_req(token_ytmonster, 'get_client')
                if req == 'not_work':
                    bot.send_message(call.from_user.id, text='Нет рабочих клиентов.', reply_markup=keyboard_back)
                elif err != 'ok':
                    bot.send_message(call.from_user.id, text='Произашла ошибка:' + str(err), reply_markup=keyboard_back)
                else:
                    keyboard_client = types.InlineKeyboardMarkup(row_width=1)
                    for client_id in ID_CLIENT:
                        button = types.InlineKeyboardButton(text='Закрыть клиент:' + str(client_id),
                                                            callback_data='client_id_close' + str(client_id))
                        keyboard_client.add(button)
                    keyboard_client.add(back)
                    bot.send_message(call.from_user.id,
                                     text=str(req) + '\n----\n Вы можете закрыть клиент с помощью кнопки ниже:',
                                     reply_markup=keyboard_client)
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
                bot.send_message(call.from_user.id, text='Идет обработка запроса! Пожалуйста ожидайте..')
                bot.answer_callback_query(call.id)
                req, err = yt_monster.ytmonster_req(token_ytmonster, 'my_task', call.data)
                bot.send_message(call.from_user.id, text=req, reply_markup=keyboard_back)
                print('Сообщение отправлено!')

            elif call.data == 'send_log':
                bot.send_message(call.message.chat.id, 'Отправка лога')
                log = open('log.txt', 'rb')
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
                    bot.send_message(call.from_user.id,
                                     text=f"Скорость загрузки {i + 1}: {download_speed:.2f} Мбит/с" + '\n' + f"Скорость отправки {i + 1}: {upload_speed:.2f} Мбит/с")
                avg_download_speed = sum(download_speeds) / len(download_speeds)
                avg_upload_speed = sum(upload_speeds) / len(upload_speeds)
                bot.send_message(call.from_user.id,
                                 text=f"Средняя скорость загрузки: {avg_download_speed:.2f} Мбит/с" + '\n' + f"Средняя скорость отправки: {avg_upload_speed:.2f} Мбит/с",
                                 reply_markup=keyboard)


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
                if id_tg == call.data:
                    task_tg = 'add_task'
                    bot.send_message(call.from_user.id, text="Ошибка: вы не являетесь владельцем этого бота!"
                                                             "\n Если вы хотите сбросить айди владельца просто удалите фаел config.txt")
                    bot.send_message(call.from_user.id, text='Введите тип задания!(Учитывая регистр) '
                                                             'Доступные типы:'
                                                             '\nСоздание заданий на реакции в телеграм:'
                                                             '\nlike_tg'
                                                             '\nПросмотры в телеграм:'
                                                             '\nview_tg', reply_markup=keyboard_back)
                    bot.answer_callback_query(call.id)
                else:
                    bot.send_message(call.from_user.id, text='')

            elif call.data == 'change_token_ytmonster':
                task_tg = 'change_token_ytmonster'
                bot.send_message(call.from_user.id, text='Введите новый токен(выполнения заданий):',
                                 reply_markup=keyboard_back)
                bot.answer_callback_query(call.id)

            elif call.data == 'change_token_telegram':
                global old_tokens
                task_tg = 'change_token_telegram'
                with open('token.txt') as f:
                    old_tokens = f.read().splitlines()
                # Сообщаем пользователю, что нужно ввести новый токен
                bot.send_message(call.from_user.id, text='Введите новый токен:', reply_markup=keyboard_back)
                bot.answer_callback_query(call.id)

            elif call.data == 'ID_Telegram':
                bot.send_message(call.from_user.id, text='Введите код:')
                task_tg = 'id'

            elif call.data == 'work_task':
                keyboard = types.InlineKeyboardMarkup()
                add_accaunt = types.InlineKeyboardButton(text='Добавить аккаунт', callback_data='add_accaunt')
                del_accaunt = types.InlineKeyboardButton(text='Удалить аккаунт', callback_data='del_accaunt')
                keyboard.row(add_accaunt, del_accaunt)
                bot.send_message(call.from_user.id, text='Выберите что вы хотите сделать:', reply_markup=keyboard)

            elif call.data == 'create_task':
                chat_id = call.from_user.id
                err = ''
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
                    bot.send_message(call.from_user.id,
                                     text='Код ответа от сайта:   ' + err + '\nПоявилась ошибка:  ' + req,
                                     reply_markup=keyboard_back)
                else:
                    bot.send_message(call.from_user.id, text='Ответ от сайта: ' + req + '  Задание успешно добавлено!',
                                     reply_markup=keyboard_back)


        @bot.message_handler(func=lambda message: True, content_types=['text'])
        def handle_message(message):
            global tokens, values, mes, task_tg, text_tg_bot, id_tg, token_ytmonster, state
            keyboard_back = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton(text='Назад', callback_data='back')
            keyboard_back.add(back)
            # Проверяем, верный ли токен

            if task_tg == 'change_token_telegram':
                if int(id_tg) != int(message.from_user.id):
                    bot.send_message(message.from_user.id, text="Ошибка: вы не являетесь владельцем этого бота!"
                                                                "\n Если вы хотите сбросить айди владельца просто удалите фаел config.txt",
                                     reply_markup=keyboard_back)
                    return

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
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEINtRkGK9SK6pHQrYy1aKnW-6ZcmlEjQAC8zAAAiP1yEgwajIpJJRmtS8E')
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
                            bot.send_message(chat_id,
                                             'Введите ссылку на пост (Пример: https://t.me/channel_name/post_id): ')
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
                        req, err = yt_monster.ytmonster_req(token_ytmonster, 'balance')
                        if err != 'ok':
                            result = '\nТип: ' + values[chat_id][0] + '\nСсылка: ' + values[chat_id][
                                1] + '\nРеакции: ' + str(
                                values[chat_id][2]) + '\nКоличество выполнений на задание: ' + values[chat_id][3] + \
                                     '\nКоличество выполнений в час: ' + values[chat_id][4] + \
                                     '\nЦена за 1 выполнение задания: ' + values[chat_id][5] + \
                                     '\nВсе верно?'
                        else:
                            result = '\nТип: ' + values[chat_id][0] + '\nСсылка: ' + values[chat_id][
                                1] + '\nРеакции: ' + str(
                                values[chat_id][2]) + '\nКоличество выполнений на задание: ' + values[chat_id][3] + \
                                     '\nКоличество выполнений в час: ' + values[chat_id][4] + \
                                     '\nЦена за 1 выполнение задания: ' + values[chat_id][5] + \
                                     '\nВаш баланс:' + str(req) + \
                                     '\nБудет затрачено: ' + str(int(values[chat_id][5]) * int(values[chat_id][3])) + \
                                     '\nВсе верно?'
                        task_tg = ''
                        del req
                        bot.send_message(chat_id, result, reply_markup=keyboard)

                elif mes == 'view_tg':
                    chat_id = message.chat.id
                    if chat_id not in values:
                        values[chat_id] = []
                    count = len(values[chat_id])
                    if count < 3:
                        values[chat_id].append(message.text)
                        if count == 0:
                            bot.send_message(chat_id,
                                             'Введите ссылку на пост (Пример: https://t.me/channel_name/post_id): ')
                        elif count == 1:
                            bot.send_message(chat_id, 'Введите количество выполнений на задание.')
                        elif count == 2:
                            bot.send_message(chat_id, 'Введите количество выполнений в час.')
                    elif count == 3:
                        values[chat_id].append(message.text)
                        task = types.InlineKeyboardButton(text='Да', callback_data='create_task')
                        keyboard.add(task)
                        req, err = yt_monster.ytmonster_req(token_ytmonster, 'balance')
                        if err != 'ok':
                            result = '\nТип: ' + values[chat_id][0] + '\nСсылка: ' + values[chat_id][
                                1] + '\nКоличество выполнений на задание: ' + values[chat_id][
                                         2] + '\nКоличетсво выполнений в час: ' + values[chat_id][
                                         3] + '\nЦена за 1 выполнение задание: 100 COIN (фиксированно)' + '\nВсе верно?'
                        else:
                            result = '\nТип: ' + values[chat_id][0] + '\nСсылка: ' + values[chat_id][
                                1] + '\nКоличество выполнений на задание: ' + values[chat_id][
                                         2] + '\nКоличетсво выполнений в час: ' + values[chat_id][
                                         3] + '\nЦена за 1 выполнение задание: 100 COIN (фиксированно)' + \
                                     '\nВаш баланс:' + str(req) + 'Будет затрачено: ' + str(int(values[chat_id][2]) * 100) \
                                     + '\nВсе верно?'
                        task_tg = 'view_tg'
                        del req
                        bot.send_message(chat_id, result, reply_markup=keyboard)

                else:
                    bot.send_message(chat_id,
                                     'Такого типа на данный момент не существует!\nВведите тип задания! Доступные типы:  like',
                                     reply_markup=keyboard)
                    mes = None

            elif task_tg == 'id':
                if text_tg_bot == message.text:
                    try:
                        _, file = read_file('config.txt', 1, 'replace', new_value=str(message.from_user.id))
                        print(file)
                        bot.send_message(message.from_user.id,
                                         'Ваш айди: ' + str(message.from_user.id) + ' Был успешно сохранен!',
                                         reply_markup=keyboard_back)
                    except:
                        bot.send_message(message.from_user.id,
                                         'Возникла ошибка',
                                         reply_markup=keyboard_back)

                else:
                    bot.send_message(message.from_user.id, 'Похоже вы ошиблись в коде! Поробуйте заново.')
                    task_tg = ''

            elif task_tg == 'change_token_ytmonster':
                print(message.text)

                if state == None:
                    a = [str(message.text), '']
                    bot.send_message(message.chat.id, 'ping: ytmonster.ru ...')
                    req, err = yt_monster.ytmonster_req(a, 'balance')
                    if err != 'ok':
                        bot.send_message(message.chat.id, 'Ошибка в токене: ' + str(err))
                        task_tg = ''
                    else:
                        bot.send_message(message.chat.id, 'Токен верен!')
                        state = ''
                        token_ytmonster = [str(message.text), token_ytmonster[1]]
                        bot.send_message(message.chat.id, 'Введите токен (для добавления заданий):')
                else:
                    a = ['', str(message.text)]
                    bot.send_message(message.chat.id, 'ping: ytmonster.ru ...')
                    req, err = yt_monster.ytmonster_req(a, 'my_task', 'ytview')
                    if err != 'ok':
                        bot.send_message(message.chat.id, 'Ошибка в токене: ' + str(err))
                        task_tg = ''
                    else:
                        token_ytmonster = [token_ytmonster[0], str(message.text)]
                        tokens = [tokens[0], token_ytmonster[0], token_ytmonster[1]]
                        bot.send_message(message.chat.id, 'Токен верен!')
                        with open('token.txt', 'w') as f:
                            f.write('\n'.join(map(str, tokens)))
                        state = None
                        bot.send_message(message.chat.id, 'Токены сохранены!', reply_markup=keyboard_back)
                        task_tg = ''

            else:
                keyboard = types.InlineKeyboardMarkup()
                back = types.InlineKeyboardButton(text='Гл. меню', callback_data='back')
                keyboard.add(back)
                bot.send_message(message.from_user.id, text='Я вас не понял. Вы всегда можете вернуться в главное меню!',
                                 reply_markup=keyboard)


        bot.infinity_polling(none_stop=True, interval=0)

    elif value == '2':
        print('Text for condition 2')
    elif value == '3':
        print('Text for condition 3')
    else:
        print(f'Возникла ошибка в config.txt')
        new_value = input('Введите цифру какую версию бота вы хотите запустить? Версии: 1. Standart 2. Lite 3. Pro\n Введите именно цифру без доп значений: ')
        try:
            _, message = read_file('config.txt', 2, 'replace', new_value=new_value)
            print(message)
        except ValueError as e:
            print(str(e))
            print(f'Возникла ошибка в config.txt')
            new_value = input('Введите цифру какую версию бота вы хотите запустить? Версии: 1. Standart 2. Lite 3. Pro\n Введите именно цифру без доп значений: ')
            _, message = read_file('config.txt', 2, 'replace', new_value=new_value)
            print(message)
