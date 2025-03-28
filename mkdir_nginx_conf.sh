#!/bin/bash
# Скрипт для создания правильной структуры nginx директорий

mkdir -p nginx/conf.d
cp nginx/nginx.conf nginx/conf.d/default.conf

echo "✅ Структура директорий nginx создана"
echo "📂 nginx/conf.d/default.conf"
