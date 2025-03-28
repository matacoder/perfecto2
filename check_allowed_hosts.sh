#!/bin/bash
# Скрипт для проверки настроек ALLOWED_HOSTS

DOMAIN=${1:-"perf.mtkv.ru"}
ENV_FILE=${2:-".env.prod"}

echo "🔍 Проверка настроек ALLOWED_HOSTS для домена ${DOMAIN}"
echo "======================================================="

# Проверяем файл .env.prod
if [ -f "${ENV_FILE}" ]; then
    echo "✅ Файл ${ENV_FILE} найден"
    
    # Ищем строку с ALLOWED_HOSTS
    if grep -q "^ALLOWED_HOSTS=" "${ENV_FILE}"; then
        ALLOWED_HOSTS=$(grep "^ALLOWED_HOSTS=" "${ENV_FILE}" | cut -d= -f2)
        echo "✅ Настройка ALLOWED_HOSTS найдена: ${ALLOWED_HOSTS}"
        
        # Проверяем наличие домена в ALLOWED_HOSTS
        if [[ "${ALLOWED_HOSTS}" == *"${DOMAIN}"* ]]; then
            echo "✅ Домен ${DOMAIN} найден в ALLOWED_HOSTS"
        else
            echo "❌ Домен ${DOMAIN} НЕ найден в ALLOWED_HOSTS!"
            echo "📝 Рекомендация: Добавьте ${DOMAIN} в ALLOWED_HOSTS в файле ${ENV_FILE}"
        fi
    else
        echo "❌ Настройка ALLOWED_HOSTS не найдена в файле ${ENV_FILE}"
        echo "📝 Рекомендация: Добавьте строку 'ALLOWED_HOSTS=${DOMAIN},localhost,127.0.0.1' в файл ${ENV_FILE}"
    fi
else
    echo "❌ Файл ${ENV_FILE} не найден"
fi

# Проверяем переменную окружения
if [ -n "${ALLOWED_HOSTS}" ]; then
    echo "✅ Переменная окружения ALLOWED_HOSTS установлена: ${ALLOWED_HOSTS}"
    
    # Проверяем наличие домена в переменной окружения
    if [[ "${ALLOWED_HOSTS}" == *"${DOMAIN}"* ]]; then
        echo "✅ Домен ${DOMAIN} найден в переменной окружения ALLOWED_HOSTS"
    else
        echo "❌ Домен ${DOMAIN} НЕ найден в переменной окружения ALLOWED_HOSTS!"
    fi
else
    echo "❌ Переменная окружения ALLOWED_HOSTS не установлена"
fi

echo "======================================================="
echo "📝 Итоговые рекомендации:"
echo "1. Убедитесь, что в файле ${ENV_FILE} есть строка 'ALLOWED_HOSTS=${DOMAIN},localhost,127.0.0.1'"
echo "2. Проверьте, что при запуске через Docker Compose переменная окружения передается в контейнер"
echo "3. Если вы используете GitHub Actions, убедитесь, что закодированный файл .env.prod содержит правильный ALLOWED_HOSTS"
echo "4. Перезапустите контейнеры после внесения изменений: docker compose restart"
