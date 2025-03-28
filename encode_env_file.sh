#!/bin/bash
# Скрипт для кодирования файла .env.prod в BASE64 формат
# для дальнейшего использования в GitHub Secrets

if [ ! -f ".env.prod" ]; then
    echo "❌ Ошибка: файл .env.prod не найден!"
    echo "Сначала создайте файл .env.prod на основе .env.prod.example"
    exit 1
fi

# Кодируем файл в BASE64
encoded=$(base64 -i .env.prod)

echo "🔐 Файл .env.prod закодирован в формате BASE64:"
echo
echo "$encoded"
echo
echo "✅ Добавьте эту строку в GitHub Secrets с именем ENV_FILE_BASE64"
