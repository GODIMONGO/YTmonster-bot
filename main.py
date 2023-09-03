import first_setup
import work
import time

version_bot = ('4.4.0 BETA')
yt_monster_ver = 3.2


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
from colorama import Fore, Style
import tqdm
import os
import sys
import tasker


try:
    auto_add_task = work.read_file('config.txt', 4)
    if auto_add_task == 'on':
        auto = threading.Thread(target=tasker.auto_add,)
        auto.start()
except IndexError:
    print('')



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
        print(f"Токен " + TOKEN_NAMES[0] + ' верен!\n------')
        break


while True:
    print("Проверка токена " + TOKEN_NAMES[1])
    req, err = yt_monster_py.balance_coin(tokens[1])
    if err != 'NO':
        print("❗️❗️❗️ Токен " + TOKEN_NAMES[1] + ' введен с ошибкой ❗️❗️❗️')
        tokens[1] = input('Введите правильный токен ' + TOKEN_NAMES[1] + ':')
    else:
        print(f"Токен " + TOKEN_NAMES[1] + ' верен!\n------')
        break



while True:
    print("Проверка токена " + TOKEN_NAMES[2])
    req, err = yt_monster_py.get_task_list(str(tokens[2]), 'tg')
    if err != 'NO':
        print("❗️❗️❗️ Токен " + TOKEN_NAMES[2] + ' введен с ошибкой ❗️❗️❗️')
        tokens[2] = input('Введите правильный токен ' + TOKEN_NAMES[2] + ':')
    else:
        print(f"Токен " + TOKEN_NAMES[2] + ' верен!\n------')
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
        print('4. Авто добавление заданий')
        print('==============')
        print('Введите номер пункта меню:')
        a = input('')
        if a == '1':
            print('Версия бота:' + version_bot + ' Версия меню: 1.2 BETA')
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
                print('4. Настройки авто добавления заданий')
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
                elif a == '4':
                    try:
                        cfg = work.read_file('config.txt', 4)
                    except IndexError:
                        cfg = 'off'
                    task = ''
                    while task != 'stop':
                        if cfg == 'off':
                            if input('Авто добавление заданий выключено! 1. Включить 2. Выйти\n') == '1':

                                work.file_action("Дополнить", "config.txt", line_number=4, content_to_append='on')
                                work.file_action("Дополнить", "config.txt", line_number=5,
                                                 content_to_append=
                                                 str(input('Раз во сколько минут нужно будет добавлять задания?'
                                                           '\nВведите  число:')))
                                print('Готово')
                                cfg = 'on'
                            else:
                                task = 'stop'
                        elif cfg == 'on':
                            print('=====НАСТРОЙКИ=====')
                            print('1. Отключить авто добавление заданий')
                            print('2. Изменить время через которое будет автоматически добавлятся задание')
                            print('3. Очистить все задания')
                            print('4. Выход')
                            print('===================')
                            q = input('Введите номер пункта меню:')
                            if q == '1':
                                print('Это не очищяет список заданий на авто добавление')
                                time.sleep(5)
                                work.file_action("Дополнить", "config.txt", line_number=4, content_to_append='off')
                                print('Перезагрузка....')
                                time.sleep(1)
                                os.execl(sys.executable, sys.executable, *sys.argv)
                            elif q == '2':
                                work.file_action("Дополнить", "config.txt", line_number=4,
                                                 content_to_append=
                                                 str(input('Раз во сколько минут нужно будет добавлять задания?'
                                                           '\nВведите в число:')))
                            elif q == '3':
                                os.remove('task.dat')
                            elif q == '4':
                                task = 'stop'
                            else:
                                print('Я не понял цифру!')




                else:
                    print('Я не понял цифру!')
        elif a == '4':
            print('Авто добавление заданий находится в стадии BETA тестирования и пока не поддерживает\n'
                  'некоторый функционал.')
            new_task = []
            task = ''
            while task != 'stop':
                new_task.append(tokens[2])
                new_task.append(input('\nvk - Вконтакте'
                                      '\ninst - Instagram'
                                      '\ntg - Telegram'
                                      '\ntiktok - Tiktok'
                                      '\nytview - Youtube просмотры'
                                      '\nytlike - Youtube лайки'
                                      '\nytsubs - Youtube подписчики'
                                      '\nytcomm - Youtube комментарии\nВыберите соц сеть:').lower())
                new_task.append(input('Введите сылку:').lower())
                new_task.append(input('Введите количество выполнений:').lower())
                new_task.append(input('Введите цену за 1 выполнение:').lower())
                new_task.append(input('\nYoutube: -'
                                      '\nВконтакте: like, repost, friend, group, view'
                                      '\nInstagram: like, friend'
                                      '\nTiktok: like, friend, view,'
                                      '\nTelegram: view, like, group, poll\nНужно ввести то что после двоеточия '
                                      '\nВыберите тип соцсети:').lower())
                new_task.append(input('Какое количество раз нужно добавлять заказ? Введите число:'))
                new_task.append(0) #сколько заданий уже выполнено
                print('\n\n\n\n\n\n================Итог=========')
                print('Токен используемый для авто добавления заказов: ***' +
                      '\nСоц. сеть:' + str(new_task[1]) + '\nСлыка:' + str(new_task[2]) +
                      '\nКоличество выполнений:' + str(new_task[3]) +
                      '\nЦена за одно выполнение:' + str(new_task[4]) +
                      '\nТип соц сети:' + str(new_task[5]) +
                      '\nКоличество раз задание автоматически добавится:' + str(new_task[6]))
                print('=============================')
                if input('Все верно? 1. Да 2. Нет') == '2':
                    print('Повторим')
                else:
                    work.save_list_to_file('task.dat', new_task)
                    new_task = []
                    if input('Это все? 1. Да 2. Нет\n') == '1':
                        print('Ок')
                        task = 'stop'
                    else:
                        print('\n\n\n\n\n\n\n')

        else:
            print('Я не понял цифру!')
