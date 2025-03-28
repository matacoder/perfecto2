#!/bin/bash
# Скрипт для проверки настроек CSRF

ENV_FILE=${1:-".env.prod"}

echo "🔍 Проверка настроек CSRF"
echo "========================="

# Проверяем файл .env.prod
if [ -f "${ENV_FILE}" ]; then
    echo "✅ Файл ${ENV_FILE} найден"
    
    # Ищем строку с CSRF_TRUSTED_ORIGINS
    if grep -q "^CSRF_TRUSTED_ORIGINS=" "${ENV_FILE}"; then
        CSRF_TRUSTED_ORIGINS=$(grep "^CSRF_TRUSTED_ORIGINS=" "${ENV_FILE}" | cut -d= -f2)
        echo "✅ Настройка CSRF_TRUSTED_ORIGINS найдена: ${CSRF_TRUSTED_ORIGINS}"
        
        # Проверяем наличие https:// префикса
        if [[ "${CSRF_TRUSTED_ORIGINS}" == *"https://"* ]]; then
            echo "✅ CSRF_TRUSTED_ORIGINS содержит https:// префикс"
        else
            echo "❌ CSRF_TRUSTED_ORIGINS не содержит https:// префикс!"
            echo "📝 Рекомендация: Добавьте полные URL с префиксами, например: https://perf.mtkv.ru,http://perf.mtkv.ru"
        fi
    else
        echo "❌ Настройка CSRF_TRUSTED_ORIGINS не найдена в файле ${ENV_FILE}"
        echo "📝 Рекомендация: Добавьте строку 'CSRF_TRUSTED_ORIGINS=https://perf.mtkv.ru,http://perf.mtkv.ru' в файл ${ENV_FILE}"
    fi
    
    # Проверяем настройки безопасности Cookie
    if grep -q "^CSRF_COOKIE_SECURE=" "${ENV_FILE}"; then
        echo "✅ Настройка CSRF_COOKIE_SECURE найдена"
    else
        echo "❌ Настройка CSRF_COOKIE_SECURE не найдена в файле ${ENV_FILE}"
        echo "📝 Рекомендация: Добавьте строку 'CSRF_COOKIE_SECURE=True' в файл ${ENV_FILE}"
    fi
else
    echo "❌ Файл ${ENV_FILE} не найден"
fi

# Проверяем конфигурацию Nginx
if [ -f "nginx/nginx.conf" ]; then
    echo "✅ Файл nginx/nginx.conf найден"
    
    # Проверяем наличие заголовков X-Forwarded-*
    if grep -q "X-Forwarded-Host" "nginx/nginx.conf" && grep -q "X-Forwarded-Proto" "nginx/nginx.conf"; then
        echo "✅ Nginx настроен для передачи необходимых заголовков X-Forwarded-*"
    else
        echo "❌ В nginx/nginx.conf отсутствуют некоторые необходимые заголовки X-Forwarded-*"
        echo "📝 Рекомендация: Добавьте 'proxy_set_header X-Forwarded-Host \$host;' и другие заголовки в файл nginx/nginx.conf"
    fi
else
    echo "❌ Файл nginx/nginx.conf не найден"
fi

echo "========================="
echo "📝 Рекомендации для исправления CSRF ошибки:"
echo "1. Убедитесь, что CSRF_TRUSTED_ORIGINS содержит полные URL с префиксами https:// и http://"
echo "2. Проверьте, что Nginx правильно передает X-Forwarded-* заголовки"
echo "3. После внесения изменений перезапустите контейнеры: docker compose restart"
