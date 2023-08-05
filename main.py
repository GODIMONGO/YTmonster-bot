import first_setup
import work
import time

version_bot = ('4.3.2 BETA')
yt_monster_ver = 3.1


try:
    first_start = work.read_file('config.txt', 3)
    if first_start != 'NO':
        Q = input(
            'Хотели бы вы воспользоваться программой для предварительной установки YTMONSTER-BOT? \n1. Хочу \n2. Не хочу\n')
        while Q != 'ok':
            if Q == '1':
                first_setup.setup()
                print('Спасибо за использование программы предварительной установки YTMONSTER-BOT!')
                time.sleep(5)
                Q = 'ok'
            elif Q == '2':
                print('OK')
                work.file_action("Дополнить", "config.txt", line_number=3, content_to_append='NO')
                Q = 'ok'
            else:
                print('Я вас не понял!')
except (FileNotFoundError, ValueError, IndexError):
    Q = input(
        'Хотели бы вы воспользоваться программой для предварительной установки YTMONSTER-BOT? \n1. Хочу \n2. Не хочу\n')
    while Q != 'ok':
        if Q == '1':
            first_setup.setup()
            print('Спасибо за использование программы предварительной установки YTMONSTER-BOT!')
            time.sleep(5)
            Q = 'ok'
        elif Q == '2':
            print('OK')
            work.file_action("Дополнить", "config.txt", line_number=3, content_to_append='NO')
            Q = 'ok'
        else:
            print('Я вас не понял!')




import yt_monster_py
import requests
import bot
import threading
from art import tprint
from colorama import init
init()
from colorama import Fore, Back, Style
import tqdm
import os
import sys






tprint("YTMONSTER-BOT")

print('Версия бота: ' + version_bot)
print('🔰Данный бот поддерживает версию API 2.0 Пожалуйста учитывайте это поскольку токены между собой не совместимы!\n'
      'Бот протестирован для версии библиотеки yt_monster_py:' + str(yt_monster_ver) + '🔰\n------')
time.sleep(5)


if yt_monster_py.version() == yt_monster_ver:
    print(f'Версия библиотеки: ' + str(yt_monster_py.version()) + ' поддерживается!')
elif yt_monster_py.version() <= yt_monster_ver:
    print(f'⚠️ Версия библиотеки: ' + str(yt_monster_py.version()) + ' НЕ ПОДДЕРЖИВАЕТСЯ! ⚠️')
    time.sleep(4)
else:
    print(f'⚠️ Версия библиотеки: ' + str(yt_monster_py.version()) + ' НЕ ПРОТЕСТИРОВАННА! ВОЗМОЖНЫ ОШИБКИ ⚠️')
    time.sleep(4)

TOKEN_NAMES = ['telegram бота', 'Ytmonster (для выполнения заданий)', 'Ytmonster (для добавления заданий)']

# Открыть файл и считывать список из 3 токенов
try:
    with open("token.txt") as f:
        tokens = f.read().splitlines()
        try:
            if tokens[1] != None and tokens[0] != None and tokens[2] != None:
                print('OK')
        except IndexError:
            tokens = ['1', '1', '1']

except FileNotFoundError:
    with open("token.txt", 'w') as file:
        tokens = []
    # Проверить каждый токен
    for token_name in TOKEN_NAMES:
        print(f"Введите токен {token_name}:")
        token = input()
        tokens.append(token)



while True:
    print("Проверка токена " + TOKEN_NAMES[0])
    req = requests.get(f'https://api.telegram.org/bot{tokens[0]}/getMe')
    if req.status_code != 200:
        print("❗️❗️❗️ Токен " + TOKEN_NAMES[0] + ' введен с ошибкой ❗️❗️❗️')
        tokens[0] = input('Введите правильный токен ' + TOKEN_NAMES[0] + ':')
    else:
        print(f"Токен " + TOKEN_NAMES[0] + 'верен!\n------')
        break


while True:
    print("Проверка токена " + TOKEN_NAMES[1])
    req, err = yt_monster_py.balance_coin(tokens[1])
    if err != 'NO':
        print("❗️❗️❗️ Токен " + TOKEN_NAMES[1] + ' введен с ошибкой ❗️❗️❗️')
        tokens[1] = input('Введите правильный токен ' + TOKEN_NAMES[1] + ':')
    else:
        print(f"Токен " + TOKEN_NAMES[1] + 'верен!\n------')
        break



while True:
    print("Проверка токена " + TOKEN_NAMES[2])
    req, err = yt_monster_py.get_task_list(str(tokens[2]), 'tg')
    if err != 'NO':
        print("❗️❗️❗️ Токен " + TOKEN_NAMES[2] + ' введен с ошибкой ❗️❗️❗️')
        tokens[2] = input('Введите правильный токен ' + TOKEN_NAMES[2] + ':')
    else:
        print(f"Токен " + TOKEN_NAMES[2] + 'верен!\n------')
        break


with open('token.txt', 'w') as f:
    f.write('\n'.join(tokens))


print('Все токены успешно проверены!')



bot = threading.Thread(target=bot.start, args=(tokens,))
bot.start()
menu = work.read_file('config.txt', 2)
if menu == '1':
    time.sleep(5)
    print('Это меню находится в BETA тестировании! Но тут уже есть пару фишек')
    print(Fore.GREEN + 'Запуск меню...')
    for _ in tqdm.tqdm(range(100)):
        time.sleep(0.01)
    import yt_monster_py
    print('\n'*100)
    print(Fore.CYAN)
    tprint("YTMONSTER-CLIENT")
    print('' + Style.RESET_ALL)

    while True:
        print('=====МЕНЮ=====')
        print('1. Версия')
        print('2. Баланс')
        print('3. Настройки')
        print('==============')
        print('Введите номер пункта меню:')
        a = input('')
        if a == '1':
            print('Версия бота:' + version_bot + ' Версия меню: 1.0 BETA')
            time.sleep(3)
        elif a == '2':
            req, err = yt_monster_py.balance_coin(tokens[1])
            print('Ваш баланс:' + str(req))
            time.sleep(3)
        elif a == '3':
            while True:
                print('=====НАСТРОЙКИ=====')
                print('1. Отключить меню')
                print('2. Повторить подтверждение по ID в телеграм')
                print('3. Выход')
                print('===================')
                print('Введите номер пункта меню:')
                a = input('')
                if a == '1':
                    work.file_action("Дополнить", "config.txt", line_number=2, content_to_append=str(2))
                    print('Перезагрузка....')
                    time.sleep(1)
                    os.execl(sys.executable, sys.executable, *sys.argv)
                elif a == '2':
                    work.file_action("Дополнить", "config.txt", line_number=1,
                                     content_to_append='NO')
                    print('Перезагрузка....')
                    time.sleep(1)
                    os.execl(sys.executable, sys.executable, *sys.argv)
                elif a == '3':
                    break
                else:
                    print('Я не понял число!')

        else:
            print('Я не понял число!')
