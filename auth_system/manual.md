# Инструкция по запуску
### 1. Установка зависимостей

```
bash

pip install -r requirements.txt
```

### 2. Настройка базы данных
Для PostgreSQL:

```sql
CREATE DATABASE auth_system;

CREATE USER auth_user WITH PASSWORD 'auth_password';

GRANT ALL PRIVILEGES ON DATABASE auth_system TO auth_user;
```

### 3. Настройка переменных окружения

Создайте файл .env в папке backend/:
```
env

SECRET_KEY=your-super-secret-key-here
DEBUG=True
DB_NAME=auth_system
DB_USER=auth_user
DB_PASSWORD=auth_password
DB_HOST=localhost
DB_PORT=5432
JWT_SECRET_KEY=your-jwt-secret-key
```
### 4. Миграции и начальные данные
```
bash
# Создание миграций
python manage.py makemigrations auth_app

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Загрузка тестовых данных (роли, разрешения)
python manage.py seed_data
```

### 5. Запуск сервера
```
bash

python manage.py runserver
```
