# Perfecto - Система для перформанс-ревью в IT-компаниях

Perfecto - это удобная система для проведения перформанс-ревью для команд в IT-компаниях. Приложение позволяет структурировать процесс оценки достижений сотрудников, собирать объективную обратную связь от коллег и руководителей.

## Содержание

- [Особенности](#особенности)
- [Технический стек](#технический-стек)
- [Установка и запуск](#установка-и-запуск)
- [Архитектура приложения](#архитектура-приложения)
- [Структура проекта](#структура-проекта)
- [Модель данных](#модель-данных)
- [Основные страницы](#основные-страницы)
- [Разработка и вклад в проект](#разработка-и-вклад-в-проект)

## Особенности

- **Управление компаниями и командами**: создавайте компании, управляйте командами внутри них
- **Гибкая система ролей**: владельцы, менеджеры и обычные сотрудники
- **Перформанс-ревью**: создавайте индивидуальные или групповые ревью
- **Достижения**: документируйте и оценивайте достижения сотрудников
- **Коллективная оценка**: получайте оценки и комментарии от разных ревьюеров
- **Авторизация через Telegram**: возможность входа через ссылки в Telegram (в разработке)

## Технический стек

### Backend
- Django 4.2.7
- Django REST Framework
- PyJWT для авторизации
- SQLite (для разработки) / PostgreSQL (для продакшена)

### Frontend
- Django Template Language
- HTMX для интерактивности
- Bulma CSS Framework
- FontAwesome для иконок

## Установка и запуск

### Предварительные требования
- Python 3.8 или выше
- pip
- git

### Быстрый старт
Для быстрой установки и запуска используйте скрипт:

```bash
# Для Linux/macOS
chmod +x run_perfecto.sh
./run_perfecto.sh

# Для Windows
python setup.py
python manage.py runserver
```

### Ручная установка

1. Создание виртуального окружения:
```bash
# Для Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Для Windows
python -m venv venv
venv\Scripts\activate
```

2. Установка зависимостей:
```bash
pip install -r requirements.txt
```

3. Настройка базы данных:
```bash
python manage.py makemigrations accounts companies teams reviews
python manage.py migrate
```

4. Создание суперпользователя:
```bash
python manage.py createsuperuser
```

5. Запуск сервера разработки:
```bash
python manage.py runserver
```

После запуска приложение будет доступно по адресу http://127.0.0.1:8000/

### Тестовые учетные записи

При использовании `setup.py` автоматически создаются следующие тестовые учетные записи:

- **Администратор**:
  - Email: admin@example.com
  - Пароль: adminpassword

- **Пользователь**:
  - Email: user@example.com
  - Пароль: userpassword

## Архитектура приложения

Приложение построено на принципах чистой архитектуры с разделением ответственности:

### Принципы разработки
1. **Разделение ответственности**
   - Каждый класс/функция решает строго одну задачу
   - Следование принципам SOLID (SRP, OCP, DIP и др.)

2. **Низкая связанность (Low Coupling)**
   - Минимальные прямые зависимости между модулями
   - Взаимодействие через контракты (интерфейсы)
   - Использование Dependency Injection

3. **Высокая связность (High Cohesion)**
   - Логически связанный код находится в одном модуле
   - Отсутствуют "божественные объекты" (God Objects)

4. **Согласованность (Consistency)**
   - Следование стилю именования PEP 8
   - Использование типизации (type hints)
   - Применение шаблонов проектирования

5. **Тестируемость**
   - Код покрывается юнит-тестами
   - Отсутствуют сложные цепочки вызовов

### Приложения Django
- **accounts**: управление пользователями и аутентификацией
- **companies**: управление компаниями
- **teams**: управление командами внутри компаний
- **reviews**: управление перформанс-ревью и достижениями

## Структура проекта

```
perfecto2/
├── accounts/           # Приложение для пользователей и аутентификации
├── companies/          # Приложение для управления компаниями
├── teams/              # Приложение для управления командами
├── reviews/            # Приложение для перформанс-ревью
├── templates/          # HTML-шаблоны
│   ├── accounts/       
│   ├── companies/      
│   ├── teams/          
│   └── reviews/        
├── static/             # Статические файлы (CSS, JS)
├── perfecto/           # Основной модуль проекта
│   ├── settings.py     
│   ├── urls.py         
│   └── wsgi.py         
├── requirements.txt    # Зависимости проекта
├── setup.py            # Скрипт настройки
└── manage.py           # Утилита управления Django
```

## Модель данных

### User (Пользователь)
- id, email, user_name, user_job
- telegram_username, telegram_id
- Права и роли в системе

### Company (Компания)
- id, company_name, company_description
- created, edited
- Владельцы и менеджеры компании

### CompanyUsers (Пользователи компании)
- user_id, company_id
- is_manager, is_owner
- Разграничение прав в компании

### Team (Команда)
- id, team_name, team_description
- company_id, created, edited
- Команды внутри компании

### TeamUsers (Участники команды)
- user_id, team_id
- is_manager, is_owner
- Роли пользователей в команде

### PerfReview (Перформанс-ревью)
- id, user_id, team_id
- created, edited
- Индивидуальные ревью пользователей

### Achievement (Достижение)
- id, perfreview_id, title
- self_score (1-5)
- reviewers - массив ревьюеров
- created, edited

### AchievementScore (Оценка достижения)
- id, achievement_id, user_id
- score (1-5), comment
- created, edited

## Основные страницы

### Главная
- Промо-страница с описанием системы
- Кнопки для входа и регистрации

### Авторизация
- **Вход**: логин, пароль, вход через Telegram
- **Регистрация**: email, имя, пароль

### Дашборд
- Виджет управления компаниями и командами
- Виджет перформанс-ревью (активные, на проверку, завершенные)
- Быстрый доступ к основным функциям

### Компании и команды
- Создание и управление компаниями
- Управление командами внутри компаний
- Добавление участников и настройка ролей

### Перформанс-ревью
- Список ревью (мои, назначенные мне, командные)
- Создание индивидуальных и групповых ревью
- Управление статусами ревью

### Страница перформанс-ревью
- Информация о сотруднике и команде
- Список достижений с оценками
- Добавление новых достижений
- Оценка достижений ревьюерами

## Разработка и вклад в проект

### Рекомендации по разработке
- Следуйте архитектурным принципам проекта
- Соблюдайте стиль кода и правила именования
- Пишите тесты для новых функций
- Документируйте публичные API и важные алгоритмы

### Разворачивание в продакшен
- Настройте PostgreSQL вместо SQLite
- Настройте безопасное хранение переменных окружения
- Настройте HTTPS через Nginx/Apache
- Используйте Gunicorn/uWSGI вместо встроенного сервера Django
