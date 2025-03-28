#!/bin/bash
# Скрипт для проверки конфигурации nginx

# Проверка существования директории и файлов конфигурации
if [ ! -d "nginx/conf.d" ]; then
    echo "❌ Директория nginx/conf.d не существует"
    echo "Создаем структуру директорий..."
    ./mkdir_nginx_conf.sh
else
    echo "✅ Директория nginx/conf.d существует"
    
    # Проверка существования конфигурационного файла
    if [ -f "nginx/conf.d/default.conf" ]; then
        echo "✅ Файл конфигурации nginx/conf.d/default.conf существует"
    else
        echo "❌ Файл конфигурации nginx/conf.d/default.conf не существует"
        
        if [ -f "nginx/nginx.conf" ]; then
            echo "🔄 Копируем nginx.conf в conf.d/default.conf"
            cp nginx/nginx.conf nginx/conf.d/default.conf
            echo "✅ Конфигурация скопирована"
        else
            echo "❌ Файл nginx/nginx.conf также не существует"
            echo "Необходимо создать конфигурационный файл nginx"
            exit 1
        fi
    fi
    
    # Проверка синтаксиса конфигурации с помощью Docker
    echo "🔍 Проверка синтаксиса nginx конфигурации..."
    docker run --rm -v $(pwd)/nginx/conf.d:/etc/nginx/conf.d:ro nginx:alpine nginx -t
    
    if [ $? -eq 0 ]; then
        echo "✅ Конфигурация nginx корректна"
    else
        echo "❌ В конфигурации nginx есть ошибки"
        exit 1
    fi
fi

echo "📝 Список конфигурационных файлов:"
find nginx -type f | sort
