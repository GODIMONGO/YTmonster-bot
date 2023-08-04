import telebot
from telebot import types
import work
import random
import time

import yt_monster_py

state = ''
id_tg = ''
def start(tokens):
    global state
    state = ''

    text_tg_bot = str(random.randint(1000, 9999))
    try:
        id_tg = work.read_file('config.txt', 1)
        id_tg = id_tg.replace(' ', '')
        if id_tg == '' or id_tg == 'NO':
            print('\n\n\nКажется, мы не знаем ваш ID в Telegram! '
                  '\nВам требуется ввести 4-значный код (без пробелов и других символов) '
                  f'\nдля телеграм-бота после его запуска: {text_tg_bot}. ')
            state = 'tg_id'
        else:
            id_tg = int(id_tg)
    except (FileNotFoundError, ValueError, IndexError):
        id_tg = ''
        print('\n\n\nКажется, мы не знаем ваш ID в Telegram! '
              '\nВам требуется ввести 4-значный код (без пробелов и других символов) '
              f'\nдля телеграм-бота после его запуска: {text_tg_bot}. ')
        state = 'tg_id'



    bot = telebot.TeleBot(tokens[0])
    if id_tg != '' and id_tg != 'NO':
        bot.send_message(id_tg, 'Бот запущен! Вы можете ввести команду для получения главного меню: /start')
    print('Бот запущен!')

    @bot.message_handler(commands=["start"])
    def start(message):
        global state, id_tg
        if state == 'tg_id':
            bot.send_message(message.from_user.id, text="Пришлите пожалуйста код который был вам отправлен в консоль! ("
                                                        "Код продублирован в консоль еще раз)")
            print(text_tg_bot)
        else:
            chat_id = message.chat.id
            message_text = ('Внимание! Данная врсия бота находится в стадии BETA теста')
            pinned_message = bot.get_chat(chat_id).pinned_message
            if pinned_message is None or pinned_message.text != message_text:
                sent_message = bot.send_message(chat_id, message_text)
                bot.pin_chat_message(chat_id, sent_message.message_id)
            time.sleep(0.0001)
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEINtRkGK9SK6pHQrYy1aKnW-6ZcmlEjQAC8zAAAiP1yEgwajIpJJRmtS8E')
            keyboard_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("/restart (для перезагрузки бота)")
            button2 = types.KeyboardButton("/unpin (для открепления сообщения)")
            button3 = types.KeyboardButton("/start (для получения главного меню)")
            keyboard_reply.add(button1, button2)
            keyboard_reply.add(button3)
            bot.send_message(message.chat.id, "Сообщение для обновления клавиатуры", reply_markup=keyboard_reply)
            bot.send_message(message.from_user.id, text="Привет! Выбери кнопку:", reply_markup=work.button_start())

    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call):
        global state, id_tg
        keyboard_back = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard_back.add(back)
        if call.data == "back":
            bot.send_message(call.from_user.id,
                             text="Telegram канал разработчика: https://t.me/GODIMONGO\nПривет! Выбери кнопку:",
                             reply_markup=work.button_start())
            bot.answer_callback_query(call.id)
        elif call.data == "balance":
            req, err = yt_monster_py.balance_coin(tokens[1])
            if err !='NO':
                bot.send_message(call.from_user.id,
                                 text="Возникла ошибка:  " + str(err))
            else:
                mes = 'Баланс:\nCOIN: ' + str(req)
                req, err = yt_monster_py.balance_many(tokens[1])
                if err != 'NO':
                    bot.send_message(call.from_user.id,
                                     text="Возникла ошибка:  " + str(err))
                else:
                    mes = mes + '\nДенег: ' + str(req)
                    bot.send_message(call.from_user.id,
                                     text=str(mes), reply_markup=keyboard_back)
        elif call.data == "version":
            bot.send_message(call.from_user.id,
                             text='Версия библиотеки: ' + str(yt_monster_py.version()), reply_markup=keyboard_back)
        elif call.data == "get_client":
            clients = yt_monster_py.ytclients_get(tokens[1])
            print(clients)
            mess = '=========\n'
            a = 0
            while len(clients) > a:
                client = clients[a]
                mess += f'ID: ' + str(client['id'])
                mess += '\nСекунд до завершения просмотра: ' + str(client['sec'])
                mess += '\nСылка: ' + client['http']
                mess += '\nОшибок при просмотре: ' + str(client['error'])
                mess += '\nIP клиента: ' + client['ip']
                if str(client['youtube_account']) == '':
                    mess += '\nЮтуб аккаунт: вы вошли в аккаунт: Auth'
                else:
                    mess += '\nЮтуб аккаунт: вы вошли в аккаунт:' + str(client['youtube_account'])
                mess += '\nЗаработано коинов за просмотр видео: ' + str(client['coin'])
                mess += '\nПросмотрено видео: ' + str(client['count'])
                mess += '\nВыполнено заданий: ' + str(client['count_task'])
                mess += '\nЗаработано коинов за выполнение заданий: ' + str(client['coin_task'])
                mess += '\n=========\n'
                a += 1
            bot.send_message(call.from_user.id,
                             text=mess, reply_markup=keyboard_back)

        else:
            bot.send_message(call.from_user.id,
                             text='Похоже кнопка еще не доступна! ', reply_markup=keyboard_back)





    @bot.message_handler(func=lambda message: True)
    def handle_text(message):
        global state, id_tg
        if state == 'tg_id':
            if str(message.text) == str(text_tg_bot):
                bot.send_message(message.chat.id, 'ID успешно подтвержден! Нажмите еще раз /start')
                work.file_action("Дополнить", "config.txt", line_number=1,
                                 content_to_append=str(message.chat.id))
                id_tg = str(message.chat.id)
                state = ''
            else:
                bot.send_message(message.chat.id, 'Неверный код подтверждения! Код продублирован в консоль')
                print(text_tg_bot)
        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить на это!')
            print(text_tg_bot)

    bot.infinity_polling(none_stop=True, interval=0)