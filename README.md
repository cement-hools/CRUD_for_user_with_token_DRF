# CRUD для юзеров с токен аутентификацией на Django REST framework

### Регистрация пользователя
- **POST**```/api/v1/registration/``` Регистрация, передать login и password

Тебования:
- login:
  - Максимум 150 символов.
  - Буквы, цифры и только @/./+/ -/_.
- password:
   - Не должен совпадать с вашим именем или другой персональной информацией или быть слишком похожим на неё.
   - Должен содержать как минимум 8 символов.
   - Не может быть одним из широко распространённых паролей.
   - Не может состоять только из цифр
  
      

### Получить токен
- **POST**```/api/api-token-auth/``` Получить токен, передать login и password
```
{
    "token": "ef416a5aa91f011a8c09e4e90c3a58362ed9c50c"
}
```

### JSON
```
[
    {
        "id": 1,
        "username": "admin",
        "first_name": "Leo",
        "last_name": "Martines",
        "email": "martines@cool.ru",
        "is_staff": true,
        "date_joined": "2021-05-08T02:12:45.654835Z"
    },
]
```

### ENDPOINT
- **GET**```/api/v1/users/```  Список всех пользователей
- **POST**```/api/v1/users/``` Админ может создать нового пользователя
- **GET**```/api/v1/users/1/``` Просмотр пользователя с id=1
- **PUT**```/api/v1/users/1/```  Пользователь может редактировать свои данные. Админ может редактировать всех пользователей и менять значение "is_staff"
- **DELETE**```/api/v1/users/1/``` Пользователь может удалить свои данные. Админ может удалить любого пользователя


## Установка и запуск
1. Клонировать репозиторий
    ```
    git clone https://github.com/cement-hools/CRUD_for_user_with_token_DRF
    ```
2. Перейдите в директорию CRUD_for_user_with_token_DRF
    ```
   cd CRUD_for_user_with_token_DRF
    ```
3. Создать виртуальное окружение и установить зависимости
    ``` 
   python -m venv venv
    ```
   Варианты активации окружения:
   - windows ``` venv/Scripts/activate ```
   - linux ``` venv/bin/activate ```
     <br><br>
   ```
   python -m pip install -U pip
   ```
   ```
   pip install -r requirements.txt
   ```
4. Выполните миграции
   ```
   python manage.py migrate
   ```
5. Создать суперюзера
   ```
   python manage.py createsuperuser
   ```
6. Запустить приложение на сервере разработчика
   ```
   python manage.py runserver
   ```
7. Проект доступен ```http://localhost:8000/```


## Тесты

   ```
   python manage.py test
   ```
