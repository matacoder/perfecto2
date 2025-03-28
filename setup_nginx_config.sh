#!/bin/bash
# Скрипт для корректной настройки директории и файлов конфигурации Nginx

# Создаем директорию для конфигурации, если она не существует
mkdir -p nginx/conf.d

# Копируем основной файл конфигурации в conf.d/default.conf
cp nginx/nginx.conf nginx/conf.d/default.conf

echo "✅ Конфигурация Nginx подготовлена:"
echo "- nginx/nginx.conf - основной файл конфигурации"
echo "- nginx/conf.d/default.conf - файл для монтирования в контейнер"

# Проверка на наличие директории для Docker Engine
if [ -S /var/run/docker.sock ]; then
    echo "🔍 Проверка конфигурации с помощью Docker..."
    docker run --rm -v $(pwd)/nginx/conf.d:/etc/nginx/conf.d:ro nginx:alpine nginx -t
    
    if [ $? -eq 0 ]; then
        echo "✅ Конфигурация корректна!"
    else
        echo "❌ В конфигурации есть ошибки!"
    fi
else
    echo "⚠️ Docker не доступен, пропускаем проверку конфигурации"
fi

echo "✅ Настройка завершена. Запустите деплой."
