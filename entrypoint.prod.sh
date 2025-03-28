#!/bin/bash

# Скрипт для запуска Django приложения в production режиме

# Вывод информации об окружении (без чувствительных данных)
echo "🔍 Информация о переменных окружения:"
echo "POSTGRES_HOST: ${POSTGRES_HOST:-db}"
echo "POSTGRES_DB: ${POSTGRES_DB:-<not set>}"
echo "POSTGRES_USER: ${POSTGRES_USER:+<set>}"  # Показываем только факт наличия переменной
echo "POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:+<set>}"  # Показываем только факт наличия переменной
echo "GUNICORN_WORKERS: ${GUNICORN_WORKERS:-3}"
echo "GUNICORN_TIMEOUT: ${GUNICORN_TIMEOUT:-120}"

# Ждем доступности БД перед запуском приложения
echo "🔍 Проверка доступности базы данных..."
python -c 'import time, sys, psycopg2;
while True:
    try:
        print("Пытаемся подключиться к БД...");
        conn = psycopg2.connect(
            dbname=sys.argv[1],
            user=sys.argv[2],
            password=sys.argv[3],
            host=sys.argv[4],
            port=sys.argv[5]
        );
        print("Подключение успешно!");
        conn.close();
        break;
    except psycopg2.OperationalError as e:
        print(f"Не удалось подключиться к БД: {e}");
        print("Ждем доступности БД...");
        time.sleep(1);
' "${POSTGRES_DB}" "${POSTGRES_USER}" "${POSTGRES_PASSWORD}" "${POSTGRES_HOST:-db}" "${POSTGRES_PORT:-5432}"

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
