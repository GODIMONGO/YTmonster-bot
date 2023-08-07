import work
import yt_monster_py
def version():
    return 0.5

def auto_add_task():

    print('\nЗапуск авто таскера... Версия: ' + str(version()))
    a = 0
    task_lists = work.read_lists_from_file('task.dat')
    print('Считывание данных из файла')
    while len(task_lists) >= a:
        print('Задание: ' + str(a))
        try:
            task = task_lists[a]
            print(task)
            task[2] = yt_monster_py.href_format(task[2], task[1])
            print(task)
            if task[1] == 'ytview' or task[1] == 'ytlike' or task[1] == 'ytsubs' or task[1] == 'ytcomm':
                req, err = yt_monster_py.add_task(str(task[0]), str(task[1]), str(task[2]), str(task[3]), str(task[4]))
            else:
                req, err = yt_monster_py.add_task(str(task[0]), str(task[1]), str(task[2]), str(task[3]), str(task[4]),
                                                  type=str(task[5]))
            a += 1
        except IndexError:
            break

        if (err == ('Данное задание еще выполняется. Запрещено добавлять задание которое еще не выполнено. '
                   'Вы можете добавить выполнений во вкладке "Мои задания".') or
                err == 'Данное задание еще выполняется, вы можете добавить выполнения во вкладке "Мои задания"'):
            list = task
            print('Запуск апдейта заказа')

            platforms = ['vk', 'inst', 'tg', 'tiktok', 'paid', 'ytview', 'ytlike', 'ytsubs', 'ytcomm']
            task_list = []

            for platform in platforms:
                offset = 0
                old_task_ids = set()

                while True:
                    tasks, err = yt_monster_py.get_task_list(list[0], platform, offset=str(offset))

                    if err != 'NO':
                        print(f"Error occurred for platform '{platform}': {err}")
                        break

                    if isinstance(tasks, str):
                        print(f"Error occurred for platform '{platform}': {tasks}")
                        break

                    new_task_ids = [task['id'] for task in tasks]
                    common_task_ids = set(new_task_ids) & old_task_ids

                    if common_task_ids:
                        break

                    task_list.extend(tasks)
                    old_task_ids.update(new_task_ids)
                    offset += 100

                    if len(tasks) < 100:
                        break
            if list[1] == 'ytlike':
                list[1] = 'yt'
                list[5] = 'like'
            if list[1] == 'ytview':
                list[1] = 'yt'
                list[5] = 'view'
            if list[1] == 'ytsubs':
                list[1] = 'yt'
                list[5] = 'subs'
            if list[1] == 'ytcomm':
                list[1] = 'yt'
                list[5] = 'comm'

            for entry in task_list:
                task_id = entry['id']
                task_soc = entry['platform']
                task_url = entry['url']
                task_type = entry['type']
                if task_soc == list[1] and task_url == list[2] and task_type == list[5]:
                    if list[1] == 'yt' and list[5] == 'comm':
                        task_soc = 'ytcomm'
                    if list[1] == 'yt' and list[5] == 'like':
                        task_soc = 'ytlike'
                    if list[1] == 'yt' and list[5] == 'subs':
                        task_soc = 'ytsubs'
                    if list[1] == 'yt' and list[5] == 'view':
                        task_soc = 'ytview'
                    req, err = yt_monster_py.task_addition(list[0], task_soc, task_id, task[3])
                    if err == 'NO':
                        print('Успешно!')
                    else:
                        print(err)
        elif err != 'NO':
            print(err)
        print(task[7])
        if int(task[6]) >= int(task[7]):
            print(task[7])
            task[7] = int(task[7]) + 1
            work.update_list_in_file('task.dat', a - 1, task)
        else:
            work.delete_list_from_file('task.dat', a - 1)


    print('Все задания отправлены:' + str(a))