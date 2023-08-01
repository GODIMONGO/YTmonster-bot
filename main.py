import time
import yt_monster_py
import requests
import bot
import telebot
import threading

version_bot = ('4.0.0 BETA')
print('Версия бота:' + version_bot)
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
time.sleep(5)
print('')