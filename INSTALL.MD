# Инструкция по установке и запуску Perfecto

## 1. Предварительные требования

Для работы с системой Perfecto необходимо установить:

- Python 3.8 или выше
- pip (устанавливается вместе с Python)
- git (для клонирования репозитория)

## 2. Подготовка окружения

### 2.1. Клонирование репозитория

```bash
git clone <repository_url>
cd perfecto2
```

### 2.2. Создание и активация виртуального окружения

#### Для Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Для Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 2.3. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 3. Настройка базы данных и первый запуск

### 3.1. Автоматическая настройка (рекомендуется)

Выполните скрипт настройки, который создаст миграции, применит их и добавит тестовые данные:

#### Для Linux/macOS:
```bash
chmod +x run_perfecto.sh
./run_perfecto.sh
```

#### Для Windows:
```bash
python setup.py
python manage.py runserver
```

### 3.2. Настройка вручную

Если вы предпочитаете пошаговую настройку:

1. Создание миграций:
```bash
python manage.py makemigrations accounts companies teams reviews
```

2. Применение миграций:
```bash
python manage.py migrate
```

3. Создание суперпользователя:
```bash
python manage.py createsuperuser
```

4. Запуск сервера разработки:
```bash
python manage.py runserver
```

## 4. Доступ к системе

После запуска приложение будет доступно по адресу:
- http://127.0.0.1:8000/

### 4.1. Тестовые учетные записи

Если вы использовали автоматическую настройку через `setup.py`, в системе уже созданы следующие учетные записи:

#### Администратор:
- Email: admin@example.com
- Пароль: adminpassword

#### Пользователь:
- Email: user@example.com
- Пароль: userpassword

### 4.2. Панель администратора

Доступ к панели администратора Django:
- http://127.0.0.1:8000/admin/

## 5. Возможные проблемы и их решения

### 5.1. Проблемы с зависимостями

Если возникают ошибки при установке зависимостей:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5.2. Проблемы с миграциями

Если возникают ошибки при миграции, можно удалить файл базы данных и миграции, затем создать их заново:
```bash
# Удалите файл базы данных
rm db.sqlite3

# Удалите файлы миграций (кроме __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Создайте миграции заново
python manage.py makemigrations accounts companies teams reviews
python manage.py migrate
```

### 5.3. Статические файлы не отображаются

Соберите статические файлы с помощью команды:
```bash
python manage.py collectstatic
```

## 6. Настройка для продакшена

Для настройки в продакшен-окружении:

1. Измените `DEBUG = False` в файле settings.py
2. Настройте безопасный `SECRET_KEY` (через переменные окружения)
3. Настройте PostgreSQL вместо SQLite
4. Настройте HTTPS
5. Используйте Gunicorn или uWSGI вместо встроенного сервера Django
6. Настройте Nginx для обработки статических файлов и проксирования запросов

## 7. Структура проекта

```
perfecto2/
├── accounts/           # Приложение для пользователей и аутентификации
├── companies/          # Приложение для управления компаниями
├── teams/              # Приложение для управления командами
├── reviews/            # Приложение для перформанс-ревью
├── templates/          # HTML-шаблоны
│   ├── accounts/       # Шаблоны для аутентификации
│   ├── companies/      # Шаблоны для компаний
│   ├── teams/          # Шаблоны для команд
│   └── reviews/        # Шаблоны для перформанс-ревью
├── static/             # Статические файлы (CSS, JS)
├── perfecto/           # Основной модуль проекта
│   ├── settings.py     # Настройки проекта
│   ├── urls.py         # Маршрутизация URL
│   └── wsgi.py         # WSGI-конфигурация
├── requirements.txt    # Зависимости проекта
├── setup.py            # Скрипт настройки
└── manage.py           # Утилита управления Django
```
