# Django Booking API

Цей проєкт реалізує REST API для бронювання подій з авторизацією через JWT.

## Технології

- Python 3.12+
- Django
- Django REST Framework
- SimpleJWT
- PostgreSQL

## Встановлення

1. Клонуйте репозиторій та перейдіть у директорію:

```bash
git clone <repos-url>
cd Django_Technical_Task

# Створіть віртуальне оточення
python -m venv .venv

# Активуйте його
.venv\Scripts\activate  # для Windows
source .venv/bin/activate  # для Linux/macOS

# Встановіть залежності
pip install -r requirements.txt

# Виконайте міграції
python manage.py makemigrations
python manage.py migrate

# Запустіть сервер
python manage.py runserver
```

## Авторизація

Після реєстрації користувач повинен увійти в систему через `/api/login/`, щоб отримати JWT токени:

```http
POST /api/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

У відповідь:
```
{
  "refresh": "your-refresh-token",
  "access": "your-access-token"
}

Для доступу до захищених маршрутів використовуйте заголовок:

Authorization: Bearer <access_token>
```