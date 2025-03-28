#!/bin/bash
# Скрипт для проверки доступности и конфигурации PostgreSQL

echo "🔍 Проверка настроек и доступности базы данных PostgreSQL..."

# Загружаем переменные из .env.prod, если файл существует
ENV_FILE=".env.prod"
if [ -f "$ENV_FILE" ]; then
    echo "📄 Загрузка переменных из $ENV_FILE"
    source "$ENV_FILE"
else
    echo "⚠️ Файл $ENV_FILE не найден, используем значения по умолчанию"
fi

# Устанавливаем значения по умолчанию, если переменные не определены
DB_HOST=${POSTGRES_HOST:-"db"}
DB_PORT=${POSTGRES_PORT:-"5432"}
DB_NAME=${POSTGRES_DB:-"perfecto_db"}
DB_USER=${POSTGRES_USER:-"perfecto_user"}

echo "🔍 Проверка настроек базы данных:"
echo "- Хост: $DB_HOST"
echo "- Порт: $DB_PORT"
echo "- Имя БД: $DB_NAME"
echo "- Пользователь: $DB_USER"
echo "- Engine в Django: ${DB_ENGINE:-django.db.backends.postgresql}"

# Проверяем настройки в settings.py
if [ -f "perfecto/settings.py" ]; then
    echo "🔍 Проверка settings.py на наличие настроек PostgreSQL..."
    if grep -q "django.db.backends.postgresql" "perfecto/settings.py"; then
        echo "✅ В settings.py найдена конфигурация PostgreSQL"
    else
        echo "❌ В settings.py не найдена конфигурация PostgreSQL"
        echo "📝 Рекомендация: Обновите settings.py для использования переменных окружения и PostgreSQL"
    fi
else
    echo "❌ Файл perfecto/settings.py не найден"
fi

# Проверяем наличие psycopg2 в requirements.txt
if [ -f "requirements.txt" ]; then
    if grep -q "psycopg2" "requirements.txt"; then
        echo "✅ В requirements.txt найден psycopg2"
    else
        echo "❌ В requirements.txt не найден psycopg2"
        echo "📝 Рекомендация: Добавьте psycopg2-binary в requirements.txt"
    fi
else
    echo "❌ Файл requirements.txt не найден"
fi

# Если доступен Docker, пробуем проверить подключение к БД в контейнере
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    if docker ps | grep -q "perfecto.*db"; then
        echo "🔍 Проверка подключения к PostgreSQL в контейнере..."
        docker exec -it $(docker ps | grep "perfecto.*db" | awk '{print $1}') \
            psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT version();" || \
            echo "❌ Не удалось подключиться к PostgreSQL в контейнере"
    else
        echo "⚠️ Контейнер базы данных не запущен, пропускаем проверку подключения"
    fi
else
    echo "⚠️ Docker не доступен, пропускаем проверку подключения к контейнеру"
fi

echo "✅ Проверка завершена!"
