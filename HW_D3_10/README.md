Для реализации проекта: 
- установите виртуальное окружение.
- скачать проект.
- установить зависимости pip install -r requirements.txt
- запустить локальный сервер python manage.py runserver `не забываем изменить settings.py`
- издательства доступны по http://127.0.0.1:8000/publishers/

**PS**
-
- модель издательства в файле model.py
- bootsrap можно наблюдать в index.html, publishers.html
- стили так же добавлены list-group
- админка добавлена в admin.py, можно проверить по http://127.0.0.1:8000/admin/p_library/publishers/
- так же реализована связь между книгой и издательством