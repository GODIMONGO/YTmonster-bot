import requests
import json
import base64

url_clifl = "https://api.clifl.com/"


def version():
    return 3.0


def balance_coin(token):
    global url_clifl

    params = {
        "action": "user-balance",
        "token": str(token)
    }

    response = requests.post(url_clifl, data=params).json()

    if response['status'] != 'success' and response['error'] != '':
        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response['error']
    return response['response']['coin'], 'NO'

def balance_many(token):
    global url_clifl

    params = {
        "action": "user-balance",
        "token": str(token)
    }

    response = requests.post(url_clifl, data=params).json()

    if response['status'] != 'success' and response['error'] != '':
        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response['error']
    return int(response['response']['money']), 'NO'

def add_account(token, platform, url):
    global url_clifl

    params = {
        "action": "accounts-add",
        "platform": str(platform),
        "url": str(url),
        "token": str(token)
    }

    response = requests.post(url_clifl, data=params).json()

    if response['status'] != 'success' and response['error'] != '':

        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response['error']
    response = {'account': str(response['response']['account']), 'task': str(response['response']['task']),
                'url': str(response['response']['url']), 'type': str(response['response']['type'])}
    return response, 'NO'

def check_account(token, account, task):
    global url_clifl

    params = {
        "action": "accounts-check",
        "account": str(account),
        "task": str(task),
        "token": str(token)
    }

    response = requests.post(url_clifl, data=params).json()

    if response['status'] != 'success' and response['error'] != '':
        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response['error']
    return str(response['status']), 'NO'


import requests

def get_task_list(token, platform, offset=0, limit=100):
    global url_clifl
    data = {
        "action": "mytasks-get",
        "platform": str(platform),
        "offset": str(offset),
        "limit": str(limit),
        "token": str(token)
    }

    response = requests.post(url_clifl, data=data).json()

    if response['status'] != 'success':
        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response.get('error')
    elif not response['response']:
        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', 'Нет заданий данного типа'
    else:
        task_list = response['response']
        processed_tasks = []

        for task in task_list:
            processed_task = {}
            processed_task['id'] = int(task['id'])
            processed_task['platform'] = str(task['platform'])
            if task['type'] == 'viewg':
                processed_task['type'] = 'view'
            else:
                processed_task['type'] = str(task['type'])
            processed_task['short_url'] = str(task['short_url'])
            processed_task['url'] = str(task['url'])
            if task['valh'] == '&infin;':
                processed_task['valh'] = 0
            else:
                processed_task['valh'] = int(task['valh'])
            processed_task['need'] = int(task['need'])
            processed_task['now'] = int(task['now'])
            processed_tasks.append(processed_task)

        return processed_tasks, 'NO'


def add_task(token, platform, href, count, coin, valh=0, sec=None, comments=None, sec_max=None, params=None, type=None):
    global url_clifl
    from urllib.parse import parse_qs, urlparse
    task = {"action": "mytasks-add", "token": str(token), "platform": str(platform), "count": str(count), "valh": str(valh)}
    if platform == 'tg' and type == 'view':
        task["coin"] = str(100)
    else:
        task["coin"] = str(coin)


    if type != None:
        task["type"] = str(type)
    if platform == "ytview" or platform == "ytlike" or platform == "ytcomm":
        if "/shorts/" in href:
            parsed_url = urlparse(href)
            path = parsed_url.path
            parts = path.split('/')
            href = parts[-1]
        else:
            parsed_url = urlparse(href)
            video_id = parsed_url.path.lstrip("/")
            href = f"https://www.youtube.com/watch?v={video_id}"

    if platform == "inst":
        from urllib.parse import urlparse, urlunparse
        parsed_url = urlparse(href.encode('utf-8'))
        netloc_parts = parsed_url.netloc.split(b'.')
        if len(netloc_parts) == 2 and netloc_parts[0] == b'instagram':
            netloc_parts.insert(0, b'www')
            new_netloc = b'.'.join(netloc_parts)
            new_parsed_url = parsed_url._replace(netloc=new_netloc)
            href = urlunparse(new_parsed_url).decode('utf-8')


    href = base64.b64encode(href.encode('utf-8'))
    href = href.decode('utf-8')
    task["href"] = str(href)
    if platform == "ytview":
        task["sec"] = str(sec)
    if platform == "ytcomm":
        comments = base64.b64encode(comments.encode('utf-8'))
        comments = comments.decode('utf-8')
        task["comments"] = str(comments)
    if platform == 'ytview' and sec_max != None:
        task["sec_max"] = sec_max
    if platform == 'tg' and type == 'like':
        reaction_dict = {}
        reactions_list = params.split(',')

        for reaction in reactions_list:
            reaction_name, reaction_percentage = reaction.split(':')
            reaction_dict[reaction_name] = int(reaction_percentage)

        encoded_data = base64.b64encode(json.dumps({"reactions": reaction_dict}).encode('utf-8'))
        params = encoded_data.decode('utf-8')
    if platform == 'tg' and type == 'poll':
        answers_dict = {}
        answers_list = params.split(',')

        for answer in answers_list:
            answer_index, answer_percentage = answer.split(':')
            answers_dict[int(answer_index)] = int(answer_percentage)

        encoded_data = base64.b64encode(json.dumps({"poll": answers_dict}).encode('utf-8'))
        params = encoded_data.decode('utf-8')
    if params != None:
        task["params"] = str(params)
    print(task)

    response = requests.post(url_clifl, data=task).json()

    if response['status'] != 'success' and response['error'] != '':
        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response['error']
    return response['id'], 'NO'

def task_remove(token, platform,  id):
    global url_clifl

    params = {
        "action": "mytasks-remove",
        "platform": str(platform),
        "id": str(id),
        "token": str(token)
    }

    response = requests.post(url_clifl, data=params).json()

    if response['status'] != 'success' and response['error'] != '':
        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response['error']
    return str(response['status']), 'NO'


def task_addition(token, platform, id, count):
    global url_clifl
    data = {
        "action": "mytasks-addition",
        "id": str(id),
        "platform": str(platform),
        "count": str(count),
        "token": str(token)
    }

    response = requests.post(url_clifl, data=data).json()

    if response['status'] != 'success':
        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response.get('error')
    else:
        return str(response['status']), 'NO'

def ytclients_get(token):
    global url_clifl
    data = {
        "action": "ytclients-get",
        "token": str(token)
    }

    response = requests.post(url_clifl, data=data).json()
    if response['status'] != 'success':
        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response.get('error')
    else:
        task_list = response['response']
        all_processed_tasks = []

        for client in task_list:
            processed_task = {
                'id': str(client['id']),
                'sec': int(client['info']['sec']),
                'http': client['info']['http'],
                'error': int(client['info']['error']),
                'ip': client['info']['ip'],
                'youtube_account': client['accounts']['youtube'],
                'coin': int(client['data']['coin']),
                'coin_task': int(client['data']['coin_task']),
                'count': int(client['data']['count']),
                'count_task': int(client['data']['count_task'])
            }
            all_processed_tasks.append(processed_task)

        return all_processed_tasks
