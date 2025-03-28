#!/bin/bash

# Скрипт для запуска Django приложения в production режиме

# Проверка установленных пакетов
echo "🔍 Проверка установленных Python пакетов..."
pip list

# Вывод информации об окружении (без чувствительных данных)
echo "🔍 Информация о переменных окружения:"
echo "POSTGRES_HOST: ${POSTGRES_HOST:-db}"
echo "POSTGRES_DB: ${POSTGRES_DB:-<not set>}"
echo "POSTGRES_USER: ${POSTGRES_USER:+<set>}"  # Показываем только факт наличия переменной
echo "POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:+<set>}"  # Показываем только факт наличия переменной
echo "GUNICORN_WORKERS: ${GUNICORN_WORKERS:-3}"
echo "GUNICORN_TIMEOUT: ${GUNICORN_TIMEOUT:-120}"

# Попытка импорта необходимых модулей
echo "🔍 Проверка импорта psycopg2..."
python -c "import psycopg2; print('✅ psycopg2 импортирован успешно')" || echo "❌ Ошибка импорта psycopg2"

# Ждем доступности БД перед запуском приложения
echo "🔍 Проверка доступности базы данных..."
python -c '
import time, sys, os
try:
    import psycopg2
    while True:
        try:
            print("Пытаемся подключиться к БД...")
            conn = psycopg2.connect(
                dbname=os.environ.get("POSTGRES_DB", "postgres"),
                user=os.environ.get("POSTGRES_USER", "postgres"),
                password=os.environ.get("POSTGRES_PASSWORD", ""),
                host=os.environ.get("POSTGRES_HOST", "db"),
                port=os.environ.get("POSTGRES_PORT", "5432")
            )
            print("Подключение успешно!")
            conn.close()
            break
        except psycopg2.OperationalError as e:
            print(f"Не удалось подключиться к БД: {e}")
            print("Ждем доступности БД...")
            time.sleep(1)
except ImportError:
    print("Ошибка: модуль psycopg2 не найден")
    sys.exit(1)
'

# Проверка наличия gunicorn
if ! command -v gunicorn &> /dev/null; then
    echo "❌ Ошибка: gunicorn не установлен!"
    echo "Попытка установки gunicorn..."
    pip install gunicorn
fi

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
