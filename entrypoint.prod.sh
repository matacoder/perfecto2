#!/bin/bash

# Скрипт для запуска Django приложения в production режиме
# Ждем доступности БД перед запуском приложения
echo "🔍 Проверка доступности базы данных..."
python -c 'import time, sys, psycopg2;
while True:
    try:
        conn = psycopg2.connect(
            dbname=sys.argv[1],
            user=sys.argv[2],
            password=sys.argv[3],
            host=sys.argv[4]
        );
        conn.close();
        break;
    except psycopg2.OperationalError:
        print("Ждем доступности БД...");
        time.sleep(1);
' "${POSTGRES_DB}" "${POSTGRES_USER}" "${POSTGRES_PASSWORD}" "${POSTGRES_HOST:-db}"

# Применяем миграции
echo "🔄 Применение миграций..."
python manage.py migrate --noinput

# Собираем статические файлы
echo "📦 Сбор статических файлов..."
python manage.py collectstatic --noinput

# Запускаем Gunicorn с настройками из переменных окружения
echo "🚀 Запуск Gunicorn сервера..."
gunicorn perfecto.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS:-3} \
    --timeout ${GUNICORN_TIMEOUT:-120} \
    --access-logfile - \
    --error-logfile - \
    --log-level info
