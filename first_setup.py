import time
import work
import  subprocess
import sys
def setup():
    def print_typing_effect(text):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(0.15)
        print()

    print_typing_effect('Привет! Давай приступим к настройке бота!')
    menu = ''
    try:
        menu = work.read_file('config.txt', 2)
        if menu != 1 or menu != 2:
            while menu != 'ok':
                menu = input('Хотели бы вы использовать меню в консоли?\n 1. Да \n 2. Нет\n')
                if menu == '1':
                    menu = '1'
                    work.file_action("Дополнить", "config.txt", line_number=2, content_to_append=menu)
                    menu = 'ok'
                elif menu == '2':
                    print('Ок меню отключено (вы всегда можете поменять эти настройки в боте!')
                    work.file_action("Дополнить", "config.txt", line_number=2, content_to_append=menu)
                    menu = 'ok'
                else:
                    print('Я вас не понял')
    except (FileNotFoundError, ValueError, IndexError):
        while menu != 'ok':
            menu = input('Хотели бы вы использовать меню в консоли?\n 1. Да \n 2. Нет\n')
            if menu == '1':
                menu = '1'
                work.file_action("Дополнить", "config.txt", line_number=2, content_to_append=menu)
                menu = 'ok'
            elif menu == '2':
                print('Ок меню отключено (вы всегда можете поменять эти настройки в боте!')
                work.file_action("Дополнить", "config.txt", line_number=2, content_to_append=menu)
                menu = 'ok'
            else:
                print('Я вас не понял')
    def not_programm():
        try:
            print_typing_effect('Проверяю установку библиотек')
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
            import os
            print('Все библиотеки установлены!')
        except ModuleNotFoundError:
            print('Кажется какая-то библиотека не установлена! \nДавайте я вам помогу с установкой!')
            bibl = ''
            while bibl != 'ok':
                bibl = input('Как бы вы хотели установить библиотеки? 1. Автоматически (BETA) 2. Самостоятельно')
                if bibl == '1':
                    print('Выбрана автоматическая установка библиотек... Это займет некоторое время пожалуйста не '
                          'используйте компьютер во время установки!')
                    subprocess.check_call(["pip", "install", "-r", 'requirements.txt'])
                    bibl = 'ok'
                if bibl == '2':
                    print('OK установите все библиотеки из requriments.txt и запустите программу')
                    sys.exit()
                else:
                    print('Я вас не понял')
    not_programm()