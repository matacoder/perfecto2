#!/bin/bash
# Скрипт для кодирования файла .env.prod в BASE64 формат
# для дальнейшего использования в GitHub Secrets

ENV_FILE=${1:-".env.prod"}

if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Ошибка: файл $ENV_FILE не найден!"
    echo "Сначала создайте файл $ENV_FILE на основе .env.prod.example"
    exit 1
fi

# Проверяем содержимое файла перед кодированием
echo "🔍 Проверка файла $ENV_FILE перед кодированием:"
./check_env_file.sh "$ENV_FILE"

# Удаляем комментарии и пустые строки для экономии места
CLEANED_FILE="${ENV_FILE}.cleaned"
grep -E -v "^#|^$" "$ENV_FILE" > "$CLEANED_FILE"

echo "🔍 Информация о очищенном файле:"
echo "Размер исходного файла: $(wc -c < $ENV_FILE) байт"
echo "Размер очищенного файла: $(wc -c < $CLEANED_FILE) байт"

# Кодируем очищенный файл в BASE64
encoded=$(base64 -i "$CLEANED_FILE")

# Удаляем временный файл
rm "$CLEANED_FILE"

echo "🔐 Файл $ENV_FILE закодирован в формате BASE64:"
echo
echo "$encoded"
echo
echo "✅ Добавьте эту строку в GitHub Secrets с именем ENV_FILE_BASE64"
