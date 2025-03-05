# To-Do List API

## Описание
Проект представляет собой API для управления задачами (To-Do List). Позволяет пользователям регистрироваться, аутентифицироваться и управлять своими задачами. Используется Django REST Framework, JWT-аутентификация и Celery.

## Стек технологий
- Python 3
- Django 5
- Django REST Framework
- PostgreSQL
- Celery + Redis
- Docker

## Установка и запуск

### 1. Клонирование репозитория
```sh
 git clone <ссылка на репозиторий>
 cd todo_project
```

### 2. Создание виртуального окружения
```sh
python -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate  # для Windows
```

### 3. Установка зависимостей
```sh
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
Создайте файл `.env` в корне проекта и укажите:
```
DEBUG=True
DB_NAME=labsite
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

### 5. Применение миграций
```sh
python manage.py migrate
```

### 6. Создание суперпользователя (необязательно)
```sh
python manage.py createsuperuser
```

### 7. Запуск сервера
```sh
python manage.py runserver
```

## Запуск Celery и Redis
Redis должен быть запущен на порту 6379. Запуск Celery:
```sh
celery -A config worker --loglevel=info
```

## Основные эндпоинты API

### Аутентификация
- `POST /api/token/` — получение JWT-токена
- `POST /api/token/refresh/` — обновление токена

### Задачи
- `GET /tasks/` — получить список задач
- `POST /tasks/` — создать новую задачу
- `GET /tasks/{id}/` — получить информацию о задаче
- `PUT /tasks/{id}/` — обновить задачу
- `DELETE /tasks/{id}/` — удалить задачу

### Пользователи
- `POST /users/register/` — регистрация
- `GET /users/me/` — получить информацию о текущем пользователе
