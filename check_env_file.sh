#!/bin/bash
# Скрипт для проверки корректности файла с переменными окружения

ENV_FILE=${1:-".env.prod"}

if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Ошибка: файл $ENV_FILE не найден!"
    exit 1
fi

echo "✅ Проверка файла $ENV_FILE:"
echo "Размер файла: $(wc -c < $ENV_FILE) байт"
echo "Количество строк: $(wc -l < $ENV_FILE)"
echo "Количество переменных: $(grep -c '=' $ENV_FILE)"

# Проверка основных необходимых переменных
REQUIRED_VARS=("POSTGRES_DB" "POSTGRES_USER" "POSTGRES_PASSWORD" "SECRET_KEY" "ALLOWED_HOSTS")

for var in "${REQUIRED_VARS[@]}"; do
    if grep -q "^$var=" "$ENV_FILE"; then
        echo "✓ $var задан"
    else
        echo "❌ $var не задан или некорректно отформатирован"
    fi
done

# Проверка на правильный формат переменных (без пробелов вокруг =)
BAD_FORMAT=$(grep -E ' *= *' "$ENV_FILE" || echo "")
if [ -n "$BAD_FORMAT" ]; then
    echo "⚠️ Обнаружены переменные с некорректным форматом (пробелы вокруг =):"
    echo "$BAD_FORMAT"
    echo "Рекомендуется: VARIABLE=value (без пробелов вокруг =)"
fi

# Проверка на пустые переменные
EMPTY_VARS=$(grep -E '=$' "$ENV_FILE" || echo "")
if [ -n "$EMPTY_VARS" ]; then
    echo "⚠️ Обнаружены пустые переменные:"
    echo "$EMPTY_VARS"
fi

echo "✅ Проверка завершена!"
