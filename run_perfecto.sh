#!/bin/bash

# Script to setup and run the Perfecto application
# Make sure this script is executable:
# chmod +x run_perfecto.sh

echo "🚀 Perfecto - запуск приложения"
echo "------------------------------"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Активация виртуального окружения..."
source venv/bin/activate

# Install dependencies
echo "📚 Установка зависимостей..."
pip install -r requirements.txt

# Run tests if --test flag is provided
if [[ "$1" == "--test" ]]; then
    echo "🧪 Запуск тестов..."
    python -m pytest --cov=accounts --cov=invitations --cov=companies --cov=teams --cov=reviews --cov=perfecto
    exit $?
fi

# Run migrations and setup data
echo "🗄️ Настройка базы данных..."
python setup.py

# Run the development server
echo "🌐 Запуск веб-сервера..."
echo "📱 Приложение доступно по адресу: http://127.0.0.1:8000/"
python manage.py runserver

# Deactivate virtual environment when server is stopped
deactivate
