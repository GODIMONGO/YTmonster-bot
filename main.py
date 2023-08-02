import time
import yt_monster_py
import requests
import bot
import threading
from art import tprint
from colorama import init
init()
from colorama import Fore, Back, Style
import time
import tqdm
import work




try:
    menu = work.read_file('config.txt', 2)
    if menu == '':
        if input('Хотели бы вы использовать меню в консоли?\n 1. Да \n 2. Нет\n') == '1':
            menu = '1'
            work.file_action("Дополнить", "config.txt", line_number=2, content_to_append=str(1))
        else:
            menu = '2'
            print('Ок меню отключено (вы всегда можете поменять эти настройки в боте!')
            work.file_action("Дополнить", "config.txt", line_number=2, content_to_append=str(2))
except (FileNotFoundError, ValueError, IndexError):

    if input('Хотели бы вы использовать меню в консоли?\n 1. Да \n 2. Нет') == '1':
        menu = '1'
        work.file_action("Дополнить", "config.txt", line_number=2, content_to_append=str(1))
    else:
        menu = '2'
        print('Ок меню отключено (вы всегда можете поменять эти настройки в боте!')
        work.file_action("Дополнить", "config.txt", line_number=2, content_to_append=str(2))


version_bot = ('4.0.3 BETA')
print('Версия бота: ' + version_bot)
print('🔰Данный бот поддерживает версию API 2.0 Пожалуйста учитывайте это поскольку токены между собой не совместимы!\n'
      'Бот протестирован для версии библиотеки yt_monster_py: 2.9🔰\n------')
time.sleep(5)


if yt_monster_py.version() == 2.9:
    print(f'Версия библиотеки: ' + str(yt_monster_py.version()) + ' поддерживается!')
else:
    print(f'⚠️ Версия библиотеки: ' + str(yt_monster_py.version()) + ' НЕ ПРОТЕСТИРОВАННА! ВОЗМОЖНЫ ОШИБКИ ⚠️')
    time.sleep(4)

TOKEN_NAMES = ['telegram бота', 'Ytmonster (для выполнения заданий)', 'Ytmonster (для добавления заданий)']

# Открыть файл и считывать список из 3 токенов
try:
    with open("token.txt") as f:
        tokens = f.read().splitlines()
except FileNotFoundError:
    # Проверить каждый токен
    for token_name in TOKEN_NAMES:
        print(f"Введите токен {token_name}:")
        token = input()
        tokens.append(token)



while True:
    print("Проверка токена " + TOKEN_NAMES[2])
    req, err = yt_monster_py.get_task_list(str(tokens[2]), 'tg')
    if err != 'NO':
        print("❗️❗️❗️ Токен " + TOKEN_NAMES[2] + ' введен с ошибкой ❗️❗️❗️')
        tokens[2] = input('Введите правильный токен ' + TOKEN_NAMES[2] + ':')
    else:
        print(f"Токен " + TOKEN_NAMES[2] + 'верен!\n------')
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
    print("Проверка токена " + TOKEN_NAMES[0])
    req = requests.get(f'https://api.telegram.org/bot{tokens[0]}/getMe')
    if req.status_code != 200:
        print("❗️❗️❗️ Токен " + TOKEN_NAMES[0] + ' введен с ошибкой ❗️❗️❗️')
        tokens[0] = input('Введите правильный токен ' + TOKEN_NAMES[0] + ':')
    else:
        print(f"Токен " + TOKEN_NAMES[0] + 'верен!\n------')
        break

with open('token.txt', 'w') as f:
    f.write('\n'.join(tokens))


print('Все токены успешно проверены!')



bot = threading.Thread(target=bot.start, args=(tokens[0],))
bot.start()
if menu == '1':
    time.sleep(5)
    print('Это меню находится в BETA тестировании! Но тут уже есть пару фишек')
    print(Fore.GREEN + 'Запуск меню...')
    for _ in tqdm.tqdm(range(100)):
        time.sleep(0.1)
    import yt_monster_py
    print('\n'*100)
    print(Fore.WHITE)
    tprint("YTMONSTER-CLIENT")
    print(Style.BRIGHT + '---------------------------------------------МЕНЮ-------------------------------------'
                         '--------\n' + Style.RESET_ALL)

    while True:
        print('1. Версия')
        print('2. Баланс')
        print('3. Информация')
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
            print('Просто меню если вы хотите использовать одновременно бота и меню!')
            time.sleep(3)
        else:
            print('Я не понял число!')
