import sys
import requests

auth_params = {
    'key': "cd6c3397613cbdf12ed90a0363e5d002",
    'token': "725dce3ead219a9a1a22d00735ffa06043cacb3661f4d28d96108eb9bdc03c91",
}

base_url = "https://api.trello.com/1/{}"
board_id = 'D0QtTj1P'

def read():
    # Получим данные всех колонок на доске:
    path = base_url.format('boards') + '/' + board_id + '/lists'
    column_data = requests.get(path, params=auth_params).json()
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        print(column['name']+': '+calc_tasks(column['id']))
        # Получим данные всех задач в колонке и перечислим все названия
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        i=0
        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            i=i+1
            print('\t'+str(i)+' - ' + task['name'])

# функция подсчета заданий в колонке
def calc_tasks(column_id):
    task_data = requests.get(base_url.format('lists') + '/' + column_id + '/cards', params=auth_params).json()
    i=0
    for task in task_data:
        i=i+1
    return(str(i))


def create(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    if (len(find_name(name))==0):
       # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
         for column in column_data:
            if column['name'] == column_name:
            # Создадим задачу с именем _name_ в найденной колонке
                requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
                break

def create_column(column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        create_new = False
        if column['name'] == column_name:
            print('Такая колонка уже существует  '+column_name)
            break
        else:
            create_new = True
    if (create_new== True):
        print('Создадим новую колонку!')
        requests.post(base_url.format('boards')+ '/' + board_id + '/lists', data={'name': column_name, **auth_params})

def move(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # Среди всех колонок нужно найти задачу по имени и получить её id
    task_id = None
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                break
        if task_id:
            break
            # Теперь, когда у нас есть id задачи, которую мы хотим переместить
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
    for column in column_data:
        if column['name'] == column_name:
            # И выполним запрос к API для перемещения задачи в нужную колонку
            requests.put(base_url.format('cards') + '/' + task_id + '/idList',
                         data={'value': column['id'], **auth_params})
            break

# Поиск задачи по всем колонкам по имени
def find_name(name_task):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # Среди всех колонок нужно найти задачу по имени и получить её id
    tasks_id = []
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        id=0
        for task in column_tasks:
            if task['name'] == name_task:
                id=id+1
                tasks_id.append(task['id'])
                print('Задача:  '+str(id)+' '+name_task+' уже существует в колонке: '+column['name'])
    return tasks_id

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_column':
        create_column(sys.argv[2])


# python trello.py create 'Сделать из мухи слона' 'Моя колонка'
# python trello.py move 'Изучить Python' 'Нужно сделать'
# python trello.py read
# python trello.py create_column 'Мой архив'