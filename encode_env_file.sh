#!/bin/bash
# Скрипт для кодирования файла .env.prod в BASE64 формат
# для дальнейшего использования в GitHub Secrets

ENV_FILE=${1:-".env.prod"}

if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Ошибка: файл $ENV_FILE не найден!"
    echo "Сначала создайте файл $ENV_FILE на основе .env.prod.example"
    exit 1
fi

# Проверка и исправление формата файла
echo "🔧 Проверка и подготовка файла перед кодированием..."
# Создаем временную копию для безопасности
cp "$ENV_FILE" "${ENV_FILE}.orig"

# Исправление типичных проблем с форматом
echo "🔧 Исправление типичных проблем с форматом..."
sed -i 's/ *= */=/g' "$ENV_FILE"  # Убираем пробелы вокруг =
sed -i 's/`/"/g' "$ENV_FILE"      # Заменяем обратные кавычки на двойные
sed -i "s/'/\"/g" "$ENV_FILE"     # Заменяем одинарные кавычки на двойные

# Удаляем комментарии и пустые строки для экономии места
echo "🔧 Очистка файла от комментариев и пустых строк..."
CLEANED_FILE="${ENV_FILE}.cleaned"
grep -v '^#' "$ENV_FILE" | grep -v '^$' > "$CLEANED_FILE"

echo "🔍 Информация о файлах:"
echo "- Размер исходного файла: $(wc -c < ${ENV_FILE}.orig) байт"
echo "- Размер исправленного файла: $(wc -c < $ENV_FILE) байт"
echo "- Размер очищенного файла: $(wc -c < $CLEANED_FILE) байт"

# Проверка итогового файла на ошибки
echo "🔍 Финальная проверка файла..."
ERROR_FOUND=0
while IFS= read -r line || [[ -n "$line" ]]; do
    if ! [[ "$line" =~ ^[A-Za-z0-9_]+=.* ]]; then
        echo "⚠️ Возможная проблема в строке: $line"
        ERROR_FOUND=1
    fi
done < "$CLEANED_FILE"

if [ $ERROR_FOUND -eq 1 ]; then
    echo "⚠️ Найдены возможные проблемы в файле. Проверьте его перед использованием."
else
    echo "✅ Файл проверен, ошибок не найдено."
fi

# Кодируем очищенный файл в BASE64
encoded=$(base64 -i "$CLEANED_FILE")

# Удаляем временные файлы
rm "$CLEANED_FILE"

echo "🔐 Файл $ENV_FILE закодирован в формате BASE64:"
echo
echo "$encoded"
echo
echo "✅ Добавьте эту строку в GitHub Secrets с именем ENV_FILE_BASE64"
