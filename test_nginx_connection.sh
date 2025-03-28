#!/bin/bash
# Скрипт для проверки работы Nginx и соединения с Django приложением

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Проверка конфигурации Nginx и соединения с приложением Django${NC}"
echo "---------------------------------------------------------------"

# 1. Проверяем наличие конфигурационного файла
if [ -f "nginx/nginx.conf" ]; then
    echo -e "${GREEN}✓ Файл конфигурации nginx/nginx.conf найден${NC}"
    
    # Показываем основные директивы из конфигурации
    echo -e "${YELLOW}Основные директивы в конфигурации:${NC}"
    grep -E "listen|server_name|proxy_pass" nginx/nginx.conf
else
    echo -e "${RED}✗ Файл конфигурации nginx/nginx.conf не найден!${NC}"
    exit 1
fi

# 2. Проверяем наличие Docker Compose файла
if [ -f "docker-compose.prod.yml" ]; then
    echo -e "${GREEN}✓ Файл docker-compose.prod.yml найден${NC}"
    
    # Проверяем настройки volume для nginx
    echo -e "${YELLOW}Настройки volumes для nginx:${NC}"
    grep -A 5 "volumes:" docker-compose.prod.yml | grep -v "volumes:"
else
    echo -e "${RED}✗ Файл docker-compose.prod.yml не найден!${NC}"
    exit 1
fi

# 3. Локальная проверка конфигурации nginx
if command -v docker &> /dev/null; then
    echo -e "${YELLOW}Проверка синтаксиса nginx конфигурации с помощью Docker:${NC}"
    docker run --rm -v $(pwd)/nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro nginx:alpine nginx -t
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Синтаксис конфигурации nginx корректен${NC}"
    else
        echo -e "${RED}✗ Обнаружены ошибки в синтаксисе конфигурации!${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Docker не установлен, пропускаем проверку синтаксиса${NC}"
fi

echo -e "\n${YELLOW}РЕКОМЕНДАЦИИ:${NC}"
echo "1. Убедитесь, что в конфигурации nginx proxy_pass указывает на app:8000"
echo "2. Убедитесь, что app контейнер доступен для nginx через Docker network"
echo "3. Проверьте, что конфигурационный файл корректно монтируется в контейнер"
echo "4. Проверьте логи nginx после деплоя: docker compose logs nginx"

echo -e "\n${GREEN}Проверка завершена!${NC}"
