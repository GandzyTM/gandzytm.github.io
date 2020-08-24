import json

import pandas as pd
import sys
import requests

auth_params = {
    'key': "cd6c3397613cbdf12ed90a0363e5d002",
    'token': "725dce3ead219a9a1a22d00735ffa06043cacb3661f4d28d96108eb9bdc03c91",
}

base_url = "https://api.trello.com/1/{}"
board_id = 'D0QtTj1P'

def read():
    column_data = requests.get(base_url.format('boards' + '/' + board_id + '/lists'), params=auth_params).json()
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print(column['name'] + ' ' + str(len(task_data)) + ' задачи')
        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            print('\t' + task['name'])


def create(name, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    for column in column_data:
        if column['name'] == column_name:
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break


def move(name, column_name):
    column_data = requests.get(base_url.format('boards' + '/' + board_id + '/lists'), params=auth_params).json()

    task_id = None
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                break
        if task_id:
            break

    for column in column_data:
        if column['name'] == column_name:
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
            break


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])

    json_string = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    print(json_string)
    for i in json_string:
        # a_json = json.loads(i)
        # print(a_json)
        dataFrame = pd.DataFrame.from_dict(i, columns=['name'], orient="index")
    print(dataFrame)

    # print(requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).text)