import pickle
import os
def read_file(filename, line_number):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if line_number <= 0 or line_number > len(lines):
                raise IndexError("Неверный номер строки")
            line = lines[line_number - 1].strip()
            return line
    except FileNotFoundError:
        with open(filename, 'w') as file:
            lines = file.readlines()
            if line_number <= 0 or line_number > len(lines):
                raise IndexError("Неверный номер строки")
            line = lines[line_number - 1].strip()
            return line
    except IndexError as e:
        raise IndexError("Ошибка при чтении строки из файла") from e


def append_to_file(filename, line_number, content_to_append):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        if not content_to_append.strip():
            raise ValueError("Строка для добавления пустая")

        if line_number <= 0:
            raise IndexError("Неверный номер строки")

        # Если номер строки больше, чем количество строк, то добавим пустые строки до нужной позиции
        while line_number > len(lines):
            lines.append("\n")

        lines[line_number - 1] = content_to_append + "\n"

        with open(filename, 'w') as file:
            file.writelines(lines)

    except FileNotFoundError:
        raise FileNotFoundError("Файл не найден")
    except ValueError as e:
        raise ValueError("Строка для добавления пустая") from e
    except IndexError as e:
        raise IndexError("Ошибка при обновлении строки в файле") from e
    except Exception as e:
        raise Exception("Произошла непредвиденная ошибка при обновлении файла") from e




def file_action(action_type, filename, line_number=None, content_to_append=None):
    if action_type == "Прочитать":
        if line_number is None:
            raise ValueError("Необходимо указать номер строки для чтения")
        return read_file(filename, line_number)
    elif action_type == "Дополнить":
        if line_number is None or content_to_append is None:
            raise ValueError("Необходимо указать номер строки и содержимое для дополнения")
        append_to_file(filename, line_number, content_to_append)
    else:
        raise ValueError("Неверный тип действия. Допустимые значения: 'Прочитать' и 'Дополнить'")


def button_start():
    from telebot import types
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


def save_list_to_file(file_path, data_list):
    try:
        with open(file_path, 'ab') as file:
            pickle.dump(data_list, file)
        print("Список успешно сохранен в файл.")
    except Exception as e:
        print("Ошибка при сохранении списка:", str(e))

def read_lists_from_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            all_lists = []
            while True:
                try:
                    data_list = pickle.load(file)
                    all_lists.append(data_list)
                except EOFError:
                    break
        return all_lists
    except Exception as e:
        print("Ошибка при чтении списка из файла:", str(e))
        return []

def delete_list_from_file(file_path, index):
    try:
        all_lists = read_lists_from_file(file_path)
        if index < len(all_lists):
            removed_list = all_lists.pop(index)
            with open(file_path, 'wb') as file:
                for data_list in all_lists:
                    pickle.dump(data_list, file)
            print("Список успешно удален из файла.")
            return removed_list
        else:
            print("Индекс списка недопустим.")
            return None
    except Exception as e:
        print("Ошибка при удалении списка:", str(e))
        return None

def update_list_in_file(file_path, index, updated_list):
    try:
        all_lists = read_lists_from_file(file_path)
        if index < len(all_lists):
            all_lists[index] = updated_list
            with open(file_path, 'wb') as file:
                for data_list in all_lists:
                    pickle.dump(data_list, file)
            print("Список успешно обновлен в файле.")
        else:
            print("Индекс списка недопустим.")
    except Exception as e:
        print("Ошибка при обновлении списка:", str(e))