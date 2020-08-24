import sys
import requests

auth_params = {
    'key': "***",
    'token': "***",
}

base_url = "https://api.trello.com/1/{}"
board_id = '***'


# name текущее название колонки
def update_label(column_id, name):
    task_data = requests.get(base_url.format('lists') + '/' + column_id + '/cards', params=auth_params).json()
    print(task_data)
    arr_name = name.split(' ')
    print(arr_name)
    new_label = str(len(task_data)) + name[len(arr_name[0]):] if arr_name[0].isdigit() else str(
        len(task_data)) + ' ' + name
    print(new_label)
    requests.put(base_url.format('lists') + '/' + column_id, params={'name': new_label, **auth_params})


# название колонки без цифры
def get_column_name(name):
    arr_name = name.split(' ')
    name = ' '.join(arr_name[1:])
    return name


def read():
    # Получим данные всех колонок на доске:
    path = base_url.format('boards') + '/' + board_id + '/lists'
    column_data = requests.get(path, params=auth_params).json()
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        print(column['name'] + ': ' + calc_tasks(column['id']))
        # Получим данные всех задач в колонке и перечислим все названия
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        i = 0
        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            i = i + 1
            print('\t' + str(i) + ' - ' + task['name'])


# функция подсчета заданий в колонке
def calc_tasks(column_id):
    task_data = requests.get(base_url.format('lists') + '/' + column_id + '/cards', params=auth_params).json()
    i = 0
    for _ in task_data:
        i = i + 1
    return str(i)


def create(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    if len(find_name(name)) == 0:
        # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
        for column in column_data:
            if column['name'] == column_name:
                # Создадим задачу с именем _name_ в найденной колонке
                requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
                break


def create_column(name):
    response = requests.post(base_url.format('boards') + '/' + board_id + '/lists',
                             params={'name': name, **auth_params}).json()
    update_label(response['id'], name)
    print('create new columns "{}"'.format(name))


def move(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Среди всех колонок нужно найти задачу по имени и получить её id
    arr_tasks = []  # Сформировать список из словарей с данными по задачи с введенным названием
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                arr_tasks.append(
                    {'id': task['id'], 'idShort': task['idShort'], 'idList': task['idList'], 'column': column['name']})

    for i in range(len(arr_tasks)):
        print('Порядковый номер {}) Задача с идентификатором "{}" из колонки с названием "{}"'.format(i, arr_tasks[i][
            'id'], arr_tasks[i]['column']))

    arr_tasks_index = int(input('Введите порядковый номер задачи для дальнейшей обработки \n'))
    task_id = arr_tasks[arr_tasks_index]['id']
    column_id = arr_tasks[arr_tasks_index]['idList']  # из этой колонки будем удалять карточку
    column_old = arr_tasks[arr_tasks_index]['column']

    # Теперь, когда у нас есть id задачи, которую мы хотим переместить
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
    for column in column_data:
        if get_column_name(column['name']) == column_name:
            # И выполним запрос к API для перемещения задачи в нужную колонку
            requests.put(base_url.format('cards') + '/' + task_id + '/idList',
                         data={'value': column['id'], **auth_params})
            update_label(column['id'], column['name'])  # Обновляем к-во задач в названии колонки, куда добавили задачу
            update_label(column_id, column_old)  # Обновляем к-во задач в названии колонки, откуда удалили задачу
            print('Задача "{}" успешно перемещена из колонки "{}" в колонку "{}"'.format(name,
                                                                                         get_column_name(column_old),
                                                                                         column_name))
            break


# Поиск задачи по всем колонкам по имени
def find_name(name_task):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # Среди всех колонок нужно найти задачу по имени и получить её id
    tasks_id = []
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        id = 0
        for task in column_tasks:
            if task['name'] == name_task:
                id = id + 1
                tasks_id.append(task['id'])
                print('Задача:  ' + str(id) + ' ' + name_task + ' уже существует в колонке: ' + column['name'])
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
