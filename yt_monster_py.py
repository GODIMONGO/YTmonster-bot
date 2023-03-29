import requests
import json
import time
from datetime import datetime
import base64
token_task = ''
token_work = ''
id_task = ''
def log(text): #Логирование в фаел лога
    with open('log.txt', 'a') as f:
        f.write('\n' + str(datetime.now()) + '  ' + text)
        f.close()

def ytmonster_error(error):#обработка ошибок
    error = int(error)
    if error == 900:
        err = 'Лимит, возникает при большом числе запросов.'
        return '', err
    elif error == 901:
        err = 'Лимит, возникает при большом числе ошибок связанных с токеном (1001-1004)'
        return '', err
    elif error == 902:
        err = 'Неверный тип токена. Например: вы используете Ключ доступа (для выполнения заданий) при добавлении задания'
        return '', err
    elif error == 1001:
        err = 'Отсутвует токен'
        return '', err
    elif error == 1002:
        err =  'Не найден токен'
        return '', err
    elif error == 1003:
        err = "Токен отключен Включите токен на сайте: https://ytmonster.ru/api/#key"
        return '', err
    elif error == 1004:
        err = 'Ошибка токена'
        return '', err
    elif error == 1101:
        err = 'Неправильный тип задания add-account'
        return '', err
    elif error == 1102 or error == 1103:
        err = 'Ошибка в ссылке аккаунта'
        return '', err
    elif error == 1301:
        err = 'Неправильный параметр get-accounts'
        return '', err
    elif error == 1401:
        err = 'Не найден аккаунт untie'
        return '', err
    elif error == 1501:
        err = 'Не найден аккаунт id_account'
        return '', err
    elif error == 1502:
        err = 'Не найден тип задания по get-task'
        return '', err
    elif error == 1503:
        err = 'Нет заданий данного типа'
        return '', err
    elif error == 1504:
        err = 'timeout - перерыв необходимый для получения нового задания выбранного типа'
        return '', err
    elif error == 1601:
        err = 'Не найден аккаунт id_account'
        return '', err
    elif error == 1602:
        err = 'Задание не выполнено'
        return err
    elif error == 1603:
        err = 'Задание было выполнено ранее'
        return '', err
    elif error == 1701:
        err = 'Не найден аккаунт id_account'
        return '', err
    elif error == 1109 or error == 1509 or error == 1609 or error == 1809 or error == 1909 or error == 2009 or error == 3009:
        err = 'Ошибка, проверьте поле error_response'
        return '', err
    else:
        print('ok')
        err = 'ok'
        return '', err

def ytmonster_req(token, task, id=''): #запрос к ytmonster и обработка некоторых ошибок
    token_work = token[0]
    token_task = token[1]
    print('ping: ytmonster.ru ...')
    try:
        if task == 'balance':
            req = requests.get('https://app.ytmonster.ru/api/?balance=get&token=' + token_work)
            json1 = json.loads(req.text)
            a, err = ytmonster_error(json1["error"])
            if err != 'ok':
                return '', err
            else:
                return json1["response"]["balance"], 'ok'
        elif task == 'close_client':
            print('ok')
        elif task == 'get_client':
            req = requests.get('https://app.ytmonster.ru/api/?get-clients=get&token=' + token_work)
            print(req.text)
            json1 = json.loads(req.text)
            a, err = ytmonster_error(json1["error"])
            if err != 'ok':
                return a, err
            if req.text == """{"error":0,"response":[]}""":
                return '', 'Нет рабочих клиентов'
            b = 0
            mess = '--------------\n'
            while len(json1['response']) > b:
                mess = mess + '\nНомер клиента: ' + str(b) + '\nID клиента: ' + str(json1["response"][b]["id"]) + \
                       '\nТип браузера: ' + str(json1["response"][b]["type_browse"]["name"]) + '\nОсталось просмотреть: ' + str(json1["response"][b]["info"]["sec"]) + ' сек.' + \
                       '\nСылка на просмотриваемое видео: https://www.youtube.com/watch?v=' + json1["response"][b]["info"]["http"] + \
                       '\nКоличество ошибок при просмотре: ' + str(json1["response"][b]["info"]["error"]) + \
                       '\nIP клиента: ' + str(json1["response"][b]["info"]["ip"]) + \
                       '\nСтатус аккаунта ютуб:' + str(json1["response"][b]["accounts"]["youtube"]) + \
                       '\nПросмотрел видео: ' + str(json1["response"][b]["data"]["count"]) + \
                       '\nЗаработал за просмотр видео: ' + str(json1["response"][b]["data"]["coin"]) + ' COIN' + \
                       '\nВыполнил заданий: ' + str(json1["response"][b]["data"]["count_task"]) + \
                       '\nЗаработал за выполнения заданий: ' + str(json1["response"][b]["data"]["coin_task"]) + '\n--------------'
                b = b + 1
            return mess, err

        elif task == 'my_task':
            req = requests.get('https://app.ytmonster.ru/api/?my-tasks=' + id +'&offset=0&token=' + token_task)
            json1 = json.loads(req.text)
            a, err = ytmonster_error(json1["error"])
            if '''{"error":0,"response":[]}''' == req.text:
                return 'Нет заданий такого типа!', err
            if err != 'ok':
                return '', err
            i = len(json1['response'])
            b = 0
            mess = ''
            while i > b:
                time.sleep(1)
                mess = mess + '\n'+ 'Нужно выполнить: ' + json1["response"][b]["need"] + '/Выполнено: '+ json1["response"][b]["now"] +'\nКоличество выполнения в час: '+ json1["response"][b]["valh"] +'\nID: ' + json1["response"][b]["id"] + '\n' + 'Сылка: ' + json1["response"][b]["url"] + '\n' + 'Тип: ' + json1["response"][b]["soc"] + '\n-----------'
                b = b + 1
            return mess, err
        elif task == 'test':
            req = requests.get('https://app.ytmonster.ru/api/?get-task=[type]&id_account=[id_account]&token=' + token_task)
        else:
            log('Ошибка выполнения функции ytmonster! Нет указания что делать')
            return '', 'Ошибка выполнения функции ytmonster! Нет указания что делать'  
    except requests.exceptions.RequestException:
        time.sleep(10)
        print('ping err')
        err = 'Ошибка запроса к API ytmonster! Работает ли сайт?'
        return '', err
    return req, 'ok'
        
# Beta функция на данный момент не доработана
def yt_monster_create_task(token, soc_name, type, href, count, coin, valh = '0', sec = '', comments = '', sec_max= '', params=''):
    if soc_name == 'tg':
        href = base64.b64encode(href)
        print(href)
    if comments != '':
        comments = base64.b64encode(comments)
        print(comments)
    
    req = requests.get('https://app.ytmonster.ru/api/?add-task='+ soc_name +'&href='+ href +'&count='+ count +'&type='+ type +'&valh='+ valh +'&coin='+ coin +'&token='+ token)
    json1 = json.loads(req.text)
    a, err = ytmonster_error(json1["error"])

