import work
import time
import auto_add_task
def auto_add():
    time.sleep(20)
    while work.read_file('config.txt', 4) == 'on':
        auto_add_task.auto_add_task()
        time_min = int(work.read_file('config.txt', 5))
        time.sleep(time_min * 60)

    return